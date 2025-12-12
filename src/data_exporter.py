"""
Módulo para exportar dados dos produtos para planilhas
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from loguru import logger

from config import PLANILHAS_DIR, EXCEL_FILENAME, CSV_FILENAME, SHEET_NAME


class DataExporter:
    """Classe para exportar dados para planilhas"""
    
    def __init__(self):
        self.planilhas_dir = PLANILHAS_DIR
        
    def export_to_excel(self, products: List[Dict], filename: str = None) -> Path:
        """
        Exporta produtos para arquivo Excel
        
        Args:
            products: Lista de dicionários com dados dos produtos
            filename: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo salvo
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"produtos_{timestamp}.xlsx"
        
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        file_path = self.planilhas_dir / filename
        
        try:
            # Cria DataFrame
            df = pd.DataFrame(products)
            
            # Reordena colunas (se existirem)
            preferred_order = ['id', 'nome', 'categoria', 'preco', 'preco_original', 
                             'descricao', 'imagem_url', 'link', 'data_coleta']
            
            # Reordena colunas mantendo as que existem
            existing_cols = [col for col in preferred_order if col in df.columns]
            other_cols = [col for col in df.columns if col not in preferred_order]
            df = df[existing_cols + other_cols]
            
            # Salva Excel
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=SHEET_NAME, index=False)
                
                # Ajusta largura das colunas
                worksheet = writer.sheets[SHEET_NAME]
                for idx, col in enumerate(df.columns, 1):
                    max_length = max(
                        df[col].astype(str).map(len).max(),
                        len(str(col))
                    )
                    # Limita largura máxima
                    max_length = min(max_length, 50)
                    worksheet.column_dimensions[chr(64 + idx)].width = max_length + 2
            
            logger.info(f"Planilha Excel salva: {file_path}")
            logger.info(f"Total de produtos exportados: {len(df)}")
            
            return file_path
            
        except Exception as e:
            logger.error(f"Erro ao exportar para Excel: {e}")
            raise
    
    def export_to_csv(self, products: List[Dict], filename: str = None, encoding: str = 'utf-8-sig') -> Path:
        """
        Exporta produtos para arquivo CSV
        
        Args:
            products: Lista de dicionários com dados dos produtos
            filename: Nome do arquivo (opcional)
            encoding: Codificação do arquivo (utf-8-sig para Excel)
            
        Returns:
            Caminho do arquivo salvo
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"produtos_{timestamp}.csv"
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        file_path = self.planilhas_dir / filename
        
        try:
            # Cria DataFrame
            df = pd.DataFrame(products)
            
            # Salva CSV
            df.to_csv(file_path, index=False, encoding=encoding, sep=';')
            
            logger.info(f"Planilha CSV salva: {file_path}")
            logger.info(f"Total de produtos exportados: {len(df)}")
            
            return file_path
            
        except Exception as e:
            logger.error(f"Erro ao exportar para CSV: {e}")
            raise
    
    def export_both(self, products: List[Dict], base_filename: str = None) -> Dict[str, Path]:
        """
        Exporta para Excel e CSV
        
        Args:
            products: Lista de dicionários com dados dos produtos
            base_filename: Nome base do arquivo (sem extensão)
            
        Returns:
            Dicionário com caminhos dos arquivos salvos
        """
        if base_filename:
            excel_filename = f"{base_filename}.xlsx"
            csv_filename = f"{base_filename}.csv"
        else:
            excel_filename = None
            csv_filename = None
        
        excel_path = self.export_to_excel(products, excel_filename)
        csv_path = self.export_to_csv(products, csv_filename)
        
        return {
            'excel': excel_path,
            'csv': csv_path
        }
    
    def add_image_paths(self, products: List[Dict], image_paths: Dict[str, str]) -> List[Dict]:
        """
        Adiciona caminhos das imagens baixadas aos produtos
        
        Args:
            products: Lista de produtos
            image_paths: Dicionário mapeando product_id -> caminho da imagem
            
        Returns:
            Lista de produtos atualizada
        """
        for product in products:
            product_id = str(product.get('id', ''))
            if product_id in image_paths:
                product['imagem_local'] = image_paths[product_id]
        
        return products

