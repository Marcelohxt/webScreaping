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
BASE_URL = ""  # URL base do site (definir conforme necessário)
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

# Seletores CSS (ajustar conforme o site)
SELECTORS = {
    'product_container': '',  # Seletor do container de produtos
    'product_name': '',       # Seletor do nome do produto
    'product_price': '',      # Seletor do preço
    'product_image': '',      # Seletor da imagem
    'product_category': '',   # Seletor da categoria
    'product_link': '',       # Seletor do link do produto
    'next_page': '',          # Seletor do botão "próxima página"
}

# Configurações de Selenium (se necessário)
USE_SELENIUM = False
SELENIUM_DRIVER = "chrome"  # "chrome" ou "firefox"
SELENIUM_HEADLESS = True
SELENIUM_WAIT_TIME = 10

