# Guia de Configuração - Utimix.com

Este guia ajuda a configurar o web scraping especificamente para o site **https://www.utimix.com/**

## 📋 Passo a Passo

### 1. Inspecionar o Site

Execute o script auxiliar para analisar a estrutura do site:

```bash
python inspect_selectors.py
```

Este script irá:
- Tentar identificar automaticamente os seletores CSS
- Mostrar a estrutura HTML encontrada
- Salvar o HTML da página em `page_inspection.html` para análise manual

### 2. Identificar os Seletores Manualmente (Recomendado)

1. **Abra o site no navegador**: https://www.utimix.com/
2. **Navegue até uma página de produtos** (ex: categoria ou busca)
3. **Abra o DevTools** (pressione F12)
4. **Use a ferramenta de inspeção** (Ctrl+Shift+C ou ícone de seleção)
5. **Clique em um produto** na página
6. **No painel do DevTools**, clique com botão direito no elemento HTML > **Copy** > **Copy selector**

### 3. Configurar os Seletores no config.py

Edite o arquivo `config.py` e preencha os seletores encontrados:

```python
SELECTORS = {
    'product_container': '.woocommerce ul.products li',  # Exemplo (ajustar)
    'product_name': 'h2.woocommerce-loop-product__title',
    'product_price': '.price .woocommerce-Price-amount',
    'product_image': 'img.attachment-woocommerce_thumbnail',
    'product_category': '.breadcrumb',
    'product_link': 'a.woocommerce-LoopProduct-link',
    'next_page': 'a.next.page-numbers',
}
```

### 4. Configurar URLs das Categorias

Edite o arquivo `main.py` e adicione as URLs das categorias que deseja fazer scraping:

```python
category_urls = [
    "https://www.utimix.com/categoria/casa-e-cozinha/",
    "https://www.utimix.com/categoria/eletronicos/",
    "https://www.utimix.com/categoria/saude-e-beleza/",
    # Adicione mais categorias aqui
]
```

**Como encontrar as URLs das categorias:**
- Navegue pelo site
- Entre em cada categoria
- Copie a URL da barra de endereço

### 5. Testar a Configuração

Execute o script principal:

```bash
python main.py
```

## 🔍 Seletores Comuns em Sites WooCommerce

O site Utimix pode usar WooCommerce. Seletores comuns:

| Elemento | Seletor WooCommerce Típico |
|----------|---------------------------|
| Container do produto | `.woocommerce ul.products li.product` ou `.products li` |
| Nome do produto | `h2.woocommerce-loop-product__title` ou `.product-title` |
| Preço | `.price .woocommerce-Price-amount` ou `.woocommerce-Price-amount` |
| Imagem | `img.attachment-woocommerce_thumbnail` ou `.product-image img` |
| Link do produto | `a.woocommerce-LoopProduct-link` ou `.product a` |
| Próxima página | `a.next.page-numbers` ou `.woocommerce-pagination a.next` |

## ⚠️ Considerações Importantes

1. **Termos de Uso**: Verifique os termos de uso do site antes de fazer scraping
2. **Robots.txt**: Acesse https://www.utimix.com/robots.txt para verificar permissões
3. **Delays**: O projeto já inclui delays entre requisições (2 segundos por padrão)
4. **Rate Limiting**: Não aumente muito a velocidade para não sobrecarregar o servidor

## 🐛 Troubleshooting

### Nenhum produto encontrado

- Verifique se os seletores CSS estão corretos
- Execute `python inspect_selectors.py` novamente
- Verifique se a página requer JavaScript (pode precisar usar Selenium)

### Imagens não estão sendo baixadas

- Verifique se o seletor da imagem está correto
- Alguns sites usam `data-src` ao invés de `src` (o código já trata isso)

### Preços não estão sendo extraídos

- Verifique o formato do preço no site
- O código tenta extrair valores de vários formatos
- Verifique o seletor do preço

## 📝 Exemplo de Configuração Completa

```python
# config.py
BASE_URL = "https://www.utimix.com"

SELECTORS = {
    'product_container': '.products li.product',
    'product_name': 'h2.woocommerce-loop-product__title a',
    'product_price': '.price .woocommerce-Price-amount',
    'product_image': 'img.attachment-woocommerce_thumbnail',
    'product_category': '.woocommerce-breadcrumb',
    'product_link': 'a.woocommerce-LoopProduct-link',
    'next_page': '.woocommerce-pagination a.next',
}

# main.py
category_urls = [
    "https://www.utimix.com/categoria/exemplo/",
]
```

