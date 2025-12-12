"""
Script principal para executar o web scraping
"""
import sys
from pathlib import Path
from loguru import logger
from datetime import datetime

# Adiciona diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from config import BASE_URL, LOG_LEVEL, LOG_FILE
from src.scraper import WebScraper
from src.image_downloader import ImageDownloader
from src.data_exporter import DataExporter


def setup_logging():
    """Configura sistema de logging"""
    logger.remove()  # Remove handler padrão
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level=LOG_LEVEL,
        colorize=True
    )
    logger.add(
        LOG_FILE,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        level=LOG_LEVEL,
        rotation="10 MB",
        retention="7 days"
    )


def main():
    """Função principal"""
    setup_logging()
    
    logger.info("=" * 60)
    logger.info("Iniciando Web Scraping de Produtos")
    logger.info("=" * 60)
    
    # Verifica se BASE_URL está configurado
    if not BASE_URL:
        logger.error("BASE_URL não configurado em config.py!")
        logger.info("Por favor, configure a URL base do site em config.py")
        return
    
    # Verifica se seletores estão configurados
    from config import SELECTORS
    if not SELECTORS.get('product_container'):
        logger.warning("Seletores CSS não configurados em config.py!")
        logger.info("Por favor, configure os seletores CSS apropriados antes de continuar")
    
    try:
        # Inicializa componentes
        scraper = WebScraper(BASE_URL)
        image_downloader = ImageDownloader(BASE_URL)
        data_exporter = DataExporter()
        
        # ============================================
        # CONFIGURAR AQUI: URLs das categorias para fazer scraping
        # ============================================
        category_urls = [
            # Exemplo:
            # "https://exemplo.com/categoria1",
            # "https://exemplo.com/categoria2",
        ]
        
        if not category_urls:
            logger.warning("Nenhuma categoria configurada!")
            logger.info("Por favor, adicione URLs de categorias na lista 'category_urls' em main.py")
            return
        
        # ============================================
        # CONFIGURAR: Número máximo de páginas por categoria
        # ============================================
        max_pages_per_category = 1
        
        # Faz scraping dos produtos
        logger.info(f"Iniciando scraping de {len(category_urls)} categoria(s)...")
        products = scraper.scrape_categories(category_urls, max_pages_per_category)
        
        if not products:
            logger.warning("Nenhum produto foi encontrado!")
            return
        
        logger.info(f"Total de produtos coletados: {len(products)}")
        
        # Faz download das imagens
        logger.info("Iniciando download de imagens...")
        image_paths = image_downloader.download_product_images(products, BASE_URL)
        
        # Adiciona caminhos das imagens aos produtos
        products = data_exporter.add_image_paths(products, image_paths)
        
        # Exporta para planilhas
        logger.info("Exportando dados para planilhas...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        files = data_exporter.export_both(products, f"produtos_{timestamp}")
        
        # Mostra estatísticas finais
        logger.info("=" * 60)
        logger.info("RESUMO FINAL")
        logger.info("=" * 60)
        logger.info(f"Produtos coletados: {len(products)}")
        
        stats = image_downloader.get_stats()
        logger.info(f"Imagens baixadas: {stats['downloaded']}")
        logger.info(f"Imagens com falha: {stats['failed']}")
        
        logger.info(f"Planilha Excel: {files['excel']}")
        logger.info(f"Planilha CSV: {files['csv']}")
        logger.info("=" * 60)
        logger.info("Processo concluído com sucesso!")
        
    except KeyboardInterrupt:
        logger.warning("Processo interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Erro durante execução: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

