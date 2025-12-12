"""
Módulo principal de Web Scraping
"""
import time
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from loguru import logger
from tqdm import tqdm

from config import (
    BASE_URL, DELAY_BETWEEN_REQUESTS, SELECTORS, 
    USE_SELENIUM, SELENIUM_HEADLESS, SELENIUM_WAIT_TIME
)
from src.utils import (
    safe_request, build_absolute_url, clean_text, 
    extract_price, sanitize_category, get_random_user_agent
)


class WebScraper:
    """Classe principal para fazer scraping de produtos"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or BASE_URL
        self.session = None
        self.products = []
        
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Obtém e faz parse de uma página HTML
        
        Args:
            url: URL da página
            
        Returns:
            BeautifulSoup object ou None
        """
        url = build_absolute_url(self.base_url, url)
        
        response = safe_request(url)
        if not response:
            return None
        
        try:
            soup = BeautifulSoup(response.content, 'lxml')
            return soup
        except Exception as e:
            logger.error(f"Erro ao fazer parse da página {url}: {e}")
            return None
    
    def extract_product_info(self, product_element, base_url: str = "") -> Dict:
        """
        Extrai informações de um produto de um elemento HTML
        
        Args:
            product_element: Elemento BeautifulSoup do produto
            base_url: URL base para construir URLs absolutas
            
        Returns:
            Dicionário com informações do produto
        """
        base_url = base_url or self.base_url
        
        # Extrai informações usando seletores
        selectors = SELECTORS
        
        try:
            # Nome do produto
            name_elem = product_element.select_one(selectors.get('product_name', '')) if selectors.get('product_name') else None
            name = clean_text(name_elem.get_text()) if name_elem else ""
            
            # Preço
            price_elem = product_element.select_one(selectors.get('product_price', '')) if selectors.get('product_price') else None
            price_text = clean_text(price_elem.get_text()) if price_elem else ""
            price = extract_price(price_text)
            
            # Imagem
            image_elem = product_element.select_one(selectors.get('product_image', '')) if selectors.get('product_image') else None
            image_url = ""
            if image_elem:
                image_url = image_elem.get('src') or image_elem.get('data-src') or image_elem.get('data-lazy-src') or ""
            image_url = build_absolute_url(base_url, image_url)
            
            # Link do produto
            link_elem = product_element.select_one(selectors.get('product_link', '')) if selectors.get('product_link') else None
            link = ""
            if link_elem:
                link = link_elem.get('href') or ""
            link = build_absolute_url(base_url, link)
            
            # Categoria
            category_elem = product_element.select_one(selectors.get('product_category', '')) if selectors.get('product_category') else None
            category = clean_text(category_elem.get_text()) if category_elem else "Sem_Categoria"
            category = sanitize_category(category)
            
            # Gera ID único (pode ser melhorado)
            product_id = f"{category}_{name}" if name else f"produto_{time.time()}"
            product_id = product_id.replace(' ', '_')[:100]
            
            product_info = {
                'id': product_id,
                'nome': name,
                'categoria': category,
                'preco': price,
                'preco_original': price_text,  # Mantém formato original
                'imagem_url': image_url,
                'link': link,
                'data_coleta': time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return product_info
            
        except Exception as e:
            logger.error(f"Erro ao extrair informações do produto: {e}")
            return {}
    
    def scrape_category_page(self, category_url: str) -> List[Dict]:
        """
        Faz scraping de uma página de categoria
        
        Args:
            category_url: URL da página de categoria
            
        Returns:
            Lista de produtos encontrados
        """
        logger.info(f"Scraping página: {category_url}")
        
        soup = self.get_page(category_url)
        if not soup:
            return []
        
        products = []
        
        # Encontra containers de produtos
        container_selector = SELECTORS.get('product_container', '')
        if not container_selector:
            logger.warning("Seletor de container de produtos não configurado!")
            return []
        
        product_containers = soup.select(container_selector)
        logger.info(f"Encontrados {len(product_containers)} produtos")
        
        for container in tqdm(product_containers, desc="Extraindo produtos"):
            try:
                product_info = self.extract_product_info(container, self.base_url)
                if product_info and product_info.get('nome'):  # Só adiciona se tiver nome
                    products.append(product_info)
            except Exception as e:
                logger.error(f"Erro ao processar produto: {e}")
                continue
        
        # Delay entre requisições
        if DELAY_BETWEEN_REQUESTS > 0:
            time.sleep(DELAY_BETWEEN_REQUESTS)
        
        return products
    
    def scrape_multiple_pages(self, category_url: str, max_pages: int = 1) -> List[Dict]:
        """
        Faz scraping de múltiplas páginas de uma categoria
        
        Args:
            category_url: URL da primeira página
            max_pages: Número máximo de páginas para processar
            
        Returns:
            Lista de todos os produtos encontrados
        """
        all_products = []
        current_url = category_url
        page = 1
        
        while page <= max_pages:
            logger.info(f"Processando página {page}/{max_pages}")
            
            products = self.scrape_category_page(current_url)
            all_products.extend(products)
            
            # Tenta encontrar link para próxima página
            if page < max_pages:
                soup = self.get_page(current_url)
                if soup:
                    next_selector = SELECTORS.get('next_page', '')
                    if next_selector:
                        next_link = soup.select_one(next_selector)
                        if next_link:
                            next_href = next_link.get('href')
                            if next_href:
                                current_url = build_absolute_url(self.base_url, next_href)
                                page += 1
                                continue
            
            # Se não encontrou próxima página, para
            break
        
        logger.info(f"Total de produtos coletados: {len(all_products)}")
        return all_products
    
    def scrape_categories(self, category_urls: List[str], max_pages_per_category: int = 1) -> List[Dict]:
        """
        Faz scraping de múltiplas categorias
        
        Args:
            category_urls: Lista de URLs de categorias
            max_pages_per_category: Número máximo de páginas por categoria
            
        Returns:
            Lista de todos os produtos encontrados
        """
        all_products = []
        
        for category_url in category_urls:
            logger.info(f"Processando categoria: {category_url}")
            products = self.scrape_multiple_pages(category_url, max_pages_per_category)
            all_products.extend(products)
            
            # Delay entre categorias
            if DELAY_BETWEEN_REQUESTS > 0:
                time.sleep(DELAY_BETWEEN_REQUESTS * 2)
        
        # Remove duplicatas baseado no ID
        unique_products = []
        seen_ids = set()
        for product in all_products:
            product_id = product.get('id')
            if product_id and product_id not in seen_ids:
                seen_ids.add(product_id)
                unique_products.append(product)
        
        logger.info(f"Total de produtos únicos coletados: {len(unique_products)}")
        return unique_products

