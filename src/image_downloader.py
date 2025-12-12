"""
Módulo para download e organização de imagens dos produtos
"""
import time
from pathlib import Path
from typing import Optional, Dict
from PIL import Image
import io
from loguru import logger
from tqdm import tqdm

from config import IMAGES_DIR, IMAGE_FORMATS, MAX_IMAGE_SIZE, RESIZE_IMAGES, MAX_IMAGE_DIMENSION, DELAY_BETWEEN_REQUESTS
from src.utils import (
    safe_request, 
    build_absolute_url, 
    get_file_extension, 
    clean_filename,
    create_category_folder,
    sanitize_category
)


class ImageDownloader:
    """Classe para gerenciar download de imagens"""
    
    def __init__(self, base_url: str = ""):
        self.base_url = base_url
        self.downloaded_count = 0
        self.failed_count = 0
        
    def download_image(self, image_url: str, save_path: Path) -> bool:
        """
        Faz download de uma imagem
        
        Args:
            image_url: URL da imagem
            save_path: Caminho onde salvar a imagem
            
        Returns:
            True se download foi bem-sucedido, False caso contrário
        """
        try:
            # Faz requisição para a imagem
            response = safe_request(image_url)
            if not response:
                return False
            
            # Verifica tamanho do arquivo
            content_length = response.headers.get('Content-Length')
            if content_length and int(content_length) > MAX_IMAGE_SIZE:
                logger.warning(f"Imagem muito grande: {image_url}")
                return False
            
            # Lê conteúdo da imagem
            image_data = response.content
            if len(image_data) > MAX_IMAGE_SIZE:
                logger.warning(f"Imagem muito grande: {image_url}")
                return False
            
            # Verifica se é uma imagem válida
            try:
                image = Image.open(io.BytesIO(image_data))
                image_format = image.format.lower() if image.format else 'jpeg'
                
                # Redimensiona se necessário
                if RESIZE_IMAGES:
                    image = self._resize_image_if_needed(image)
                
                # Garante que a pasta existe
                save_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Salva imagem
                # Converte para RGB se necessário (PNG com transparência)
                if image_format == 'png' and image.mode in ('RGBA', 'LA', 'P'):
                    rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                    if image.mode == 'P':
                        image = image.convert('RGBA')
                    rgb_image.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                    image = rgb_image
                
                # Salva como JPEG
                save_path = save_path.with_suffix('.jpg')
                image.save(save_path, 'JPEG', quality=85, optimize=True)
                
                self.downloaded_count += 1
                logger.debug(f"Imagem salva: {save_path}")
                return True
                
            except Exception as e:
                logger.error(f"Erro ao processar imagem {image_url}: {e}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao baixar imagem {image_url}: {e}")
            self.failed_count += 1
            return False
    
    def _resize_image_if_needed(self, image: Image.Image) -> Image.Image:
        """Redimensiona imagem se exceder dimensões máximas"""
        width, height = image.size
        if width <= MAX_IMAGE_DIMENSION and height <= MAX_IMAGE_DIMENSION:
            return image
        
        # Calcula novo tamanho mantendo proporção
        if width > height:
            new_width = MAX_IMAGE_DIMENSION
            new_height = int(height * (MAX_IMAGE_DIMENSION / width))
        else:
            new_height = MAX_IMAGE_DIMENSION
            new_width = int(width * (MAX_IMAGE_DIMENSION / height))
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def download_product_images(self, products: list, base_url: str = "") -> Dict[str, str]:
        """
        Faz download de imagens de uma lista de produtos
        
        Args:
            products: Lista de dicionários com informações dos produtos
            base_url: URL base para construir URLs absolutas
            
        Returns:
            Dicionário mapeando product_id -> caminho da imagem salva
        """
        self.base_url = base_url or self.base_url
        downloaded_images = {}
        
        logger.info(f"Iniciando download de {len(products)} imagens...")
        
        for product in tqdm(products, desc="Baixando imagens"):
            try:
                product_id = product.get('id', '')
                category = product.get('categoria', 'Sem_Categoria')
                image_url = product.get('imagem_url', '')
                
                if not image_url:
                    logger.warning(f"Produto {product_id} sem URL de imagem")
                    continue
                
                # Constrói URL absoluta se necessário
                image_url = build_absolute_url(self.base_url, image_url)
                
                # Cria pasta da categoria
                category_folder = create_category_folder(IMAGES_DIR, sanitize_category(category))
                
                # Gera nome do arquivo
                product_name = clean_filename(product.get('nome', product_id))
                if not product_name:
                    product_name = f"produto_{product_id}"
                
                # Adiciona extensão se necessário
                ext = get_file_extension(image_url)
                if not ext or ext not in IMAGE_FORMATS:
                    ext = '.jpg'
                
                filename = f"{product_name}{ext}"
                save_path = category_folder / filename
                
                # Se já existe, adiciona sufixo
                counter = 1
                original_save_path = save_path
                while save_path.exists():
                    stem = original_save_path.stem
                    save_path = category_folder / f"{stem}_{counter}{ext}"
                    counter += 1
                
                # Faz download
                if self.download_image(image_url, save_path):
                    # Salva caminho relativo
                    relative_path = save_path.relative_to(IMAGES_DIR)
                    downloaded_images[product_id] = str(relative_path).replace('\\', '/')
                
                # Delay entre downloads
                if DELAY_BETWEEN_REQUESTS > 0:
                    time.sleep(DELAY_BETWEEN_REQUESTS)
                    
            except Exception as e:
                logger.error(f"Erro ao processar produto {product.get('id', 'unknown')}: {e}")
                continue
        
        logger.info(f"Download concluído: {self.downloaded_count} sucessos, {self.failed_count} falhas")
        return downloaded_images
    
    def get_stats(self) -> Dict[str, int]:
        """Retorna estatísticas de download"""
        return {
            'downloaded': self.downloaded_count,
            'failed': self.failed_count,
            'total': self.downloaded_count + self.failed_count
        }

