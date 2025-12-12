# Web Scraping - Produtos de Utilidade Doméstica

Projeto de web scraping para coletar produtos do site **Utimix.com** (https://www.utimix.com/), baixar imagens organizadas por categoria e gerar planilhas com os dados coletados.

> 📖 **Guia Específico**: Consulte o arquivo [GUIA_UTIMIX.md](GUIA_UTIMIX.md) para instruções detalhadas de configuração.

## 📋 Funcionalidades

- ✅ Scraping de produtos de múltiplas categorias
- ✅ Download automático de imagens organizadas por categoria
- ✅ Exportação para Excel e CSV
- ✅ Suporte a múltiplas páginas
- ✅ Sistema de retry automático
- ✅ Logging detalhado
- ✅ Progresso visual com barras de progresso
- ✅ Respeita rate limiting e delays

## 🚀 Instalação

1. Clone ou baixe este repositório

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### 1. Configurar URL Base

Edite `config.py` e defina a URL base do site:

```python
BASE_URL = "https://exemplo.com"
```

### 2. Identificar Seletores CSS (IMPORTANTE)

**Opção 1 - Script Automático:**
```bash
python inspect_selectors.py
```

**Opção 2 - Manual:**
Use o DevTools do navegador (F12) para inspecionar os elementos HTML.

Depois, no arquivo `config.py`, configure os seletores CSS encontrados:

```python
SELECTORS = {
    'product_container': '.produto',        # Container de cada produto
    'product_name': '.produto-nome',        # Nome do produto
    'product_price': '.produto-preco',      # Preço
    'product_image': '.produto-imagem img', # Imagem
    'product_category': '.categoria',       # Categoria
    'product_link': 'a.produto-link',       # Link do produto
    'next_page': '.proxima-pagina',         # Botão próxima página
}
```

**Dica:** Use o DevTools do navegador (F12) para inspecionar o HTML e encontrar os seletores corretos.

### 3. Configurar URLs das Categorias

Edite `main.py` e adicione as URLs das categorias que deseja fazer scraping:

```python
category_urls = [
    "https://exemplo.com/categoria1",
    "https://exemplo.com/categoria2",
    # Adicione mais URLs aqui
]
```

## 📖 Como Usar

1. Configure o `config.py` com a URL base e seletores
2. Configure as URLs de categorias em `main.py`
3. Execute o script:

```bash
python main.py
```

O script irá:
- Coletar produtos das categorias configuradas
- Baixar imagens organizadas em pastas por categoria
- Gerar planilhas Excel e CSV na pasta `data/planilhas/`

## 📁 Estrutura do Projeto

```
webScreaping/
├── src/
│   ├── scraper.py          # Lógica principal de scraping
│   ├── image_downloader.py # Download de imagens
│   ├── data_exporter.py    # Exportação para planilhas
│   └── utils.py            # Funções auxiliares
├── data/
│   ├── images/             # Imagens organizadas por categoria
│   └── planilhas/          # Planilhas geradas
├── config.py               # Configurações
├── main.py                 # Script principal
├── requirements.txt        # Dependências
└── README.md              # Este arquivo
```

## 📊 Estrutura dos Dados

Os produtos coletados terão a seguinte estrutura:

- `id`: ID único do produto
- `nome`: Nome do produto
- `categoria`: Categoria do produto
- `preco`: Preço numérico
- `preco_original`: Preço no formato original do site
- `imagem_url`: URL da imagem original
- `imagem_local`: Caminho da imagem baixada
- `link`: Link do produto no site
- `data_coleta`: Data e hora da coleta

## ⚠️ Importante

- **Respeite os termos de uso** do site que está fazendo scraping
- **Verifique o robots.txt** do site antes de iniciar
- **Use delays apropriados** entre requisições (já configurado)
- **Não sobrecarregue o servidor** com muitas requisições simultâneas

## 🛠️ Personalização

### Ajustar Delay entre Requisições

No `config.py`:
```python
DELAY_BETWEEN_REQUESTS = 2  # Segundos
```

### Limitar Tamanho de Imagens

No `config.py`:
```python
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
RESIZE_IMAGES = True  # Redimensionar imagens grandes
MAX_IMAGE_DIMENSION = 2000  # Pixels
```

### Usar Selenium (para sites com JavaScript)

1. Instale o driver do navegador (ChromeDriver ou GeckoDriver)
2. No `config.py`:
```python
USE_SELENIUM = True
SELENIUM_DRIVER = "chrome"  # ou "firefox"
```

## 📝 Logs

Os logs são salvos em `scraping.log` e também exibidos no console.

## 🤝 Contribuindo

Sinta-se livre para melhorar este projeto!

## 📄 Licença

Este projeto é para fins educacionais. Use com responsabilidade e respeitando os termos de uso dos sites.

