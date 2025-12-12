# ✅ Checklist - O que falta configurar

## 🔴 CRÍTICO - Precisa ser feito antes de executar:

### 1. ⚠️ Configurar Seletores CSS no `config.py`

Os seletores estão vazios. Você precisa identificar os seletores CSS do site Utimix:

**Como fazer:**
1. Abra https://www.utimix.com/ no navegador
2. Navegue até uma página com produtos (ex: categoria ou busca)
3. Pressione **F12** para abrir DevTools
4. Use a ferramenta de inspeção (**Ctrl+Shift+C** ou ícone de seleção)
5. Clique em um produto na página
6. No painel do DevTools, clique com botão direito no elemento HTML
7. Selecione **Copy** → **Copy selector**
8. Cole o seletor no arquivo `config.py`

**Editar `config.py`:**
```python
SELECTORS = {
    'product_container': 'COLAR_SELETOR_AQUI',  # Container de cada produto
    'product_name': 'COLAR_SELETOR_AQUI',       # Nome do produto
    'product_price': 'COLAR_SELETOR_AQUI',      # Preço
    'product_image': 'COLAR_SELETOR_AQUI',      # Imagem
    'product_category': 'COLAR_SELETOR_AQUI',   # Categoria (opcional)
    'product_link': 'COLAR_SELETOR_AQUI',       # Link do produto
    'next_page': 'COLAR_SELETOR_AQUI',          # Botão próxima página (opcional)
}
```

### 2. ⚠️ Adicionar URLs das Categorias no `main.py`

**Editar `main.py` (linha ~65):**
```python
category_urls = [
    "https://www.utimix.com/categoria/exemplo1/",
    "https://www.utimix.com/categoria/exemplo2/",
    # Adicione mais URLs aqui
]
```

**Como encontrar as URLs:**
- Navegue pelo site Utimix
- Entre em cada categoria que deseja fazer scraping
- Copie a URL da barra de endereço
- Cole na lista `category_urls`

---

## 🟡 PROBLEMA CONHECIDO:

### 3. ⚠️ Site bloqueando acesso (403 Forbidden)

O site Utimix está retornando **403 Forbidden** mesmo com Selenium.

**Status atual:**
- ✅ Selenium configurado
- ✅ Código preparado
- ❌ Site ainda bloqueia acesso automatizado

**Soluções possíveis:**
1. **Inspeção Manual (Recomendado)**: Use o navegador normal para identificar os seletores CSS
2. **Testar com navegador visível**: Certifique-se de que `SELENIUM_HEADLESS = False` em `config.py`
3. **Aguardar mais tempo**: O site pode precisar de tempo para carregar

---

## 📋 RESUMO DO QUE JÁ ESTÁ PRONTO:

✅ Estrutura do projeto criada
✅ Código de scraping implementado
✅ Download de imagens por categoria
✅ Exportação para Excel e CSV
✅ Sistema de retry e logging
✅ Selenium configurado
✅ Script de inspeção criado

---

## 🚀 PRÓXIMOS PASSOS:

1. **Identificar seletores CSS manualmente** (usando DevTools do navegador)
2. **Configurar os seletores** no `config.py`
3. **Adicionar URLs das categorias** no `main.py`
4. **Testar com uma categoria** primeiro
5. **Executar o scraping completo**

---

## 💡 DICA:

Se você conseguir acessar o site manualmente no navegador, você pode:
1. Salvar o HTML da página (Ctrl+S → Salvar como HTML)
2. Me enviar ou colar aqui o HTML
3. Eu posso ajudar a identificar os seletores CSS

Ou você pode me dizer qual categoria quer fazer scraping e posso tentar ajudar a identificar os seletores.

