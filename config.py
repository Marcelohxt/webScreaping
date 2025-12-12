"""
Configurações do projeto de Web Scraping
"""
import os
from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = DATA_DIR / "images"
PLANILHAS_DIR = DATA_DIR / "planilhas"

# Criar diretórios se não existirem
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
PLANILHAS_DIR.mkdir(parents=True, exist_ok=True)

# Configurações de scraping
BASE_URL = "https://www.utimix.com"  # URL base do site Utimix
DELAY_BETWEEN_REQUESTS = 2  # Delay em segundos entre requisições
MAX_RETRIES = 3  # Número máximo de tentativas em caso de falha
TIMEOUT = 30  # Timeout para requisições em segundos

# Headers padrão
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Configurações de imagens
IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB em bytes
RESIZE_IMAGES = False  # Se True, redimensiona imagens muito grandes
MAX_IMAGE_DIMENSION = 2000  # Dimensão máxima (largura ou altura)

# Configurações da planilha
EXCEL_FILENAME = "produtos_scraping.xlsx"
CSV_FILENAME = "produtos_scraping.csv"
SHEET_NAME = "Produtos"

# Configurações de logging
LOG_LEVEL = "INFO"
LOG_FILE = "scraping.log"

# Seletores CSS (ajustar conforme o site Utimix)
# Execute: python inspect_selectors.py para ajudar a identificar os seletores
SELECTORS = {
    'product_container': '',  # Seletor do container de produtos (ex: '.product-item', '.woocommerce li.product')
    'product_name': '',       # Seletor do nome do produto (ex: 'h2.woocommerce-loop-product__title', '.product-title')
    'product_price': '',      # Seletor do preço (ex: '.price', '.woocommerce-Price-amount')
    'product_image': '',      # Seletor da imagem (ex: 'img.attachment-woocommerce_thumbnail', '.product-image img')
    'product_category': '',   # Seletor da categoria (ex: '.product-category', 'nav.breadcrumb')
    'product_link': '',       # Seletor do link do produto (ex: 'a.woocommerce-LoopProduct-link', 'a.product-link')
    'next_page': '',          # Seletor do botão "próxima página" (ex: 'a.next', '.pagination .next')
}

# Configurações de Selenium (se necessário)
# IMPORTANTE: O site Utimix bloqueia requisições HTTP normais (403)
# Para fazer scraping, é necessário usar Selenium com undetected-chromedriver:
USE_SELENIUM = True  # Mude para True para usar Selenium
USE_UNDETECTED_CHROMEDRIVER = False  # Usa undetected-chromedriver (desabilitado - incompatível com Python 3.14)
SELENIUM_DRIVER = "chrome"  # "chrome" ou "firefox"
SELENIUM_HEADLESS = False  # True = sem abrir navegador (pode não funcionar em alguns sites)
SELENIUM_WAIT_TIME = 10  # Tempo de espera em segundos

