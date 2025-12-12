"""
Funções utilitárias para o projeto de Web Scraping
"""
import re
import time
import validators
from pathlib import Path
from urllib.parse import urljoin, urlparse
from typing import Optional
from fake_useragent import UserAgent
from loguru import logger
import requests
from config import HEADERS, TIMEOUT, MAX_RETRIES


def get_random_user_agent() -> str:
    """Retorna um User-Agent aleatório"""
    try:
        ua = UserAgent()
        return ua.random
    except Exception:
        return HEADERS.get('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')


def clean_filename(filename: str) -> str:
    """Remove caracteres inválidos do nome do arquivo"""
    # Remove caracteres especiais e substitui espaços por underscores
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = filename.strip('.')
    # Limita tamanho do nome
    if len(filename) > 200:
        filename = filename[:200]
    return filename


def clean_text(text: str) -> str:
    """Limpa e normaliza texto extraído"""
    if not text:
        return ""
    # Remove espaços extras e quebras de linha
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_price(price_text: str) -> float:
    """Extrai valor numérico do preço"""
    if not price_text:
        return 0.0
    # Remove tudo exceto números, vírgulas e pontos
    price_str = re.sub(r'[^\d.,]', '', price_text)
    # Substitui vírgula por ponto
    price_str = price_str.replace(',', '.')
    try:
        # Tenta extrair o valor
        price_match = re.search(r'\d+\.?\d*', price_str)
        if price_match:
            return float(price_match.group())
    except (ValueError, AttributeError):
        pass
    return 0.0


def build_absolute_url(base_url: str, relative_url: str) -> str:
    """Constrói URL absoluta a partir de URL relativa"""
    if not relative_url:
        return ""
    if validators.url(relative_url):
        return relative_url
    return urljoin(base_url, relative_url)


def get_file_extension(url: str) -> str:
    """Extrai extensão do arquivo da URL"""
    parsed = urlparse(url)
    path = parsed.path
    ext = Path(path).suffix.lower()
    # Se não tiver extensão, tenta inferir do tipo MIME
    if not ext:
        ext = '.jpg'  # Default
    return ext


def safe_request(url: str, headers: Optional[dict] = None, retries: int = MAX_RETRIES) -> Optional[requests.Response]:
    """
    Faz uma requisição HTTP segura com retry automático
    
    Args:
        url: URL para fazer requisição
        headers: Headers customizados
        retries: Número de tentativas
        
    Returns:
        Response object ou None em caso de falha
    """
    if headers is None:
        headers = HEADERS.copy()
        headers['User-Agent'] = get_random_user_agent()
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=TIMEOUT, stream=True)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.warning(f"Tentativa {attempt + 1}/{retries} falhou para {url}: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Backoff exponencial
            else:
                logger.error(f"Falha ao acessar {url} após {retries} tentativas")
                return None
    
    return None


def create_category_folder(base_path: Path, category: str) -> Path:
    """Cria pasta para categoria se não existir"""
    category_folder = base_path / clean_filename(category)
    category_folder.mkdir(parents=True, exist_ok=True)
    return category_folder


def format_currency(value: float, currency_symbol: str = "R$") -> str:
    """Formata valor como moeda"""
    return f"{currency_symbol} {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


def sanitize_category(category: str) -> str:
    """Sanitiza nome de categoria para uso em pastas"""
    if not category:
        return "Sem_Categoria"
    return clean_filename(category) or "Sem_Categoria"

