# 🔄 Solução Alternativa - Site Bloqueando Acesso

## Situação Atual

O site Utimix está bloqueando acesso automatizado mesmo com Selenium (erro 403 Forbidden).

## ✅ Soluções Alternativas

### Opção 1: Salvar HTML Manualmente e Processar Localmente

Se você conseguir acessar o site manualmente:

1. **Acesse o site** no navegador normal
2. **Navegue até uma categoria** com produtos
3. **Salve a página HTML**:
   - Pressione `Ctrl+S` (ou Cmd+S no Mac)
   - Escolha "Salvar como HTML completo"
   - Salve na pasta do projeto

4. **Crie um script para processar HTMLs salvos**:

```python
# process_html_salvo.py
from bs4 import BeautifulSoup
from src.scraper import WebScraper
from src.data_exporter import DataExporter
from src.image_downloader import ImageDownloader
from config import SELECTORS, BASE_URL

# Carrega HTML salvo
with open('pagina_salva.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'lxml')

# Extrai produtos usando os seletores
scraper = WebScraper(BASE_URL)
products = []

container_selector = SELECTORS.get('product_container', '')
if container_selector:
    product_containers = soup.select(container_selector)
    for container in product_containers:
        product_info = scraper.extract_product_info(container, BASE_URL)
        if product_info and product_info.get('nome'):
            products.append(product_info)

# Exporta dados
if products:
    exporter = DataExporter()
    exporter.export_both(products, "produtos_html_manual")
    print(f"✅ {len(products)} produtos extraídos!")
```

### Opção 2: Usar Modo Interativo

Modifique o código para pausar e permitir navegação manual:

1. Execute com `SELENIUM_HEADLESS = False`
2. Quando o navegador abrir, navegue manualmente
3. Pressione Enter no terminal para continuar o scraping

### Opção 3: Verificar se Há API

Alguns sites WooCommerce têm APIs REST. Você pode tentar:

```
https://www.utimix.com/wp-json/wc/v3/products
```

Mas geralmente requer autenticação.

### Opção 4: Aguardar e Tentar Novamente

Proteções anti-bot podem ter cooldown. Tente novamente depois de alguns minutos/horas.

---

## 💡 Recomendação

**Para começar rapidamente**, use a **Opção 1**: salve algumas páginas HTML manualmente e processe localmente. Assim você pode testar os seletores CSS e ver se estão funcionando corretamente antes de resolver o problema do acesso automatizado.

