"""
Script auxiliar para inspecionar o site e identificar seletores CSS
Execute este script para ver a estrutura HTML da página e ajudar a identificar os seletores corretos
"""
import sys
from pathlib import Path
from bs4 import BeautifulSoup
from loguru import logger
from colorama import init, Fore, Style

sys.path.insert(0, str(Path(__file__).parent))

from config import BASE_URL, USE_SELENIUM
from src.scraper import WebScraper

init(autoreset=True)  # Inicializa colorama


def print_section(title: str):
    """Imprime título de seção formatado"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{title}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")


def inspect_page(url: str, scraper: WebScraper = None):
    """Inspeciona uma página e mostra a estrutura HTML"""
    print_section(f"Inspecionando: {url}")
    
    if scraper:
        soup = scraper.get_page(url)
    else:
        from src.utils import safe_request
        response = safe_request(url)
        if not response:
            logger.error(f"Erro ao acessar {url}")
            return
        soup = BeautifulSoup(response.content, 'lxml')
    
    if not soup:
        logger.error(f"Erro ao fazer parse da página {url}")
        return
    
    # Procura por possíveis containers de produtos
    print_section("Possíveis Containers de Produtos")
    
    # Seletores comuns para listas de produtos
    common_selectors = [
        '.product',
        '.produto',
        '.item',
        '.product-item',
        '.product-card',
        '[class*="product"]',
        '[class*="produto"]',
        '[class*="item"]',
        '.woocommerce ul.products li',
        '.products-list li',
    ]
    
    found_containers = []
    for selector in common_selectors:
        elements = soup.select(selector)
        if elements:
            found_containers.append({
                'selector': selector,
                'count': len(elements),
                'sample': elements[0] if elements else None
            })
    
    if found_containers:
        for item in found_containers:
            print(f"{Fore.GREEN}✓{Style.RESET_ALL} Seletor: {Fore.YELLOW}{item['selector']}{Style.RESET_ALL}")
            print(f"  Encontrados: {Fore.CYAN}{item['count']}{Style.RESET_ALL} elementos")
            if item['sample']:
                # Mostra classes do primeiro elemento
                classes = item['sample'].get('class', [])
                if classes:
                    print(f"  Classes: {Fore.MAGENTA}{' '.join(classes)}{Style.RESET_ALL}")
                # Mostra estrutura básica
                name_elem = item['sample'].find(['h1', 'h2', 'h3', 'h4', 'a', 'span'], class_=lambda x: x and any(
                    word in ' '.join(x).lower() for word in ['title', 'name', 'nome', 'titulo']
                ))
                if name_elem:
                    print(f"  Exemplo de nome: {Fore.WHITE}{name_elem.get_text(strip=True)[:50]}...{Style.RESET_ALL}")
            print()
    else:
        print(f"{Fore.RED}✗{Style.RESET_ALL} Nenhum container de produto comum encontrado")
        print(f"{Fore.YELLOW}Dica:{Style.RESET_ALL} Use F12 no navegador para inspecionar manualmente\n")
    
    # Procura por imagens
    print_section("Imagens Encontradas")
    images = soup.find_all('img')
    product_images = [img for img in images if img.get('src') or img.get('data-src')]
    print(f"Total de imagens: {Fore.CYAN}{len(product_images)}{Style.RESET_ALL}")
    
    if product_images:
        print(f"\n{Fore.YELLOW}Primeiras 5 imagens:{Style.RESET_ALL}")
        for i, img in enumerate(product_images[:5], 1):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src') or 'N/A'
            parent_class = ' '.join(img.parent.get('class', [])) if img.parent else 'N/A'
            print(f"  {i}. {Fore.CYAN}{src[:80]}...{Style.RESET_ALL}")
            if parent_class != 'N/A':
                print(f"     Container: {Fore.MAGENTA}.{parent_class.replace(' ', '.')}{Style.RESET_ALL}")
    
    # Procura por preços
    print_section("Preços Encontrados")
    price_patterns = soup.find_all(string=lambda text: text and any(
        char in text for char in ['R$', '$', '€', '£']
    ))
    
    if price_patterns:
        print(f"Total de textos com símbolos de moeda: {Fore.CYAN}{len(price_patterns)}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Primeiros 5 preços encontrados:{Style.RESET_ALL}")
        for i, price_text in enumerate(price_patterns[:5], 1):
            parent = price_text.parent
            parent_class = ' '.join(parent.get('class', [])) if parent and parent.get('class') else 'N/A'
            print(f"  {i}. {Fore.WHITE}{price_text.strip()[:50]}{Style.RESET_ALL}")
            if parent_class != 'N/A':
                print(f"     Seletor sugerido: {Fore.MAGENTA}.{parent_class.split()[0]}{Style.RESET_ALL}")
    
    # Salva HTML para inspeção manual
    html_file = Path("page_inspection.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print(f"\n{Fore.GREEN}HTML da página salvo em: {html_file}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Abra este arquivo no navegador para inspecionar manualmente{Style.RESET_ALL}\n")


def main():
    """Função principal"""
    print(f"{Fore.GREEN}{'='*60}")
    print(f"{Fore.GREEN}Inspetor de Seletores CSS - Utimix")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
    
    # Inicializa scraper se Selenium estiver habilitado
    scraper = None
    if USE_SELENIUM:
        logger.info("Usando Selenium para acessar o site...")
        scraper = WebScraper(BASE_URL)
    
    # URLs para inspecionar
    urls_to_inspect = [
        BASE_URL,
        f"{BASE_URL}/produtos",  # Possível página de produtos
    ]
    
    for url in urls_to_inspect:
        try:
            inspect_page(url, scraper)
        except Exception as e:
            logger.error(f"Erro ao inspecionar {url}: {e}")
    
    # Fecha driver se foi usado
    if scraper and scraper.driver:
        try:
            scraper.driver.quit()
        except:
            pass
    
    print_section("Próximos Passos")
    print(f"1. {Fore.YELLOW}Abra o arquivo page_inspection.html no navegador{Style.RESET_ALL}")
    print(f"2. {Fore.YELLOW}Pressione F12 para abrir o DevTools{Style.RESET_ALL}")
    print(f"3. {Fore.YELLOW}Use a ferramenta de inspeção (Ctrl+Shift+C) para selecionar elementos{Style.RESET_ALL}")
    print(f"4. {Fore.YELLOW}No DevTools, clique com botão direito no elemento > Copy > Copy selector{Style.RESET_ALL}")
    print(f"5. {Fore.YELLOW}Cole os seletores encontrados no arquivo config.py{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()

