# 🚀 Instruções Rápidas - Adicionar URL de Categoria

## Problema Atual:
O erro "Nenhuma categoria configurada!" significa que a lista `category_urls` está vazia.

## Solução em 3 Passos:

### 1️⃣ Abra o site Utimix
Acesse: https://www.utimix.com/

### 2️⃣ Encontre uma categoria
- Navegue pelo menu do site
- Clique em qualquer categoria que tenha produtos
- **Copie a URL completa** da barra de endereço

Exemplos de URLs que você pode encontrar:
- `https://www.utimix.com/categoria/casa-e-cozinha/`
- `https://www.utimix.com/produtos/`
- `https://www.utimix.com/categoria/eletronicos/`

### 3️⃣ Edite o arquivo `main.py`

Abra o arquivo `main.py` e localize a linha ~65. Você verá:

```python
category_urls = [
    # URLs aqui
]
```

**Adicione a URL que você copiou:**

```python
category_urls = [
    "https://www.utimix.com/categoria/casa-e-cozinha/",  # Cole sua URL aqui
]
```

**IMPORTANTE:** 
- Remova os `#` (comentários) das linhas que você usar
- Coloque a URL entre aspas `" "`
- Adicione vírgula `,` se for adicionar mais URLs

### ✅ Execute novamente:
```bash
python main.py
```

---

## 💡 Dica Rápida:

Se você quer testar rapidamente, pode tentar essas URLs comuns:

1. Página de todos os produtos: `https://www.utimix.com/produtos/`
2. Categoria Casa e Cozinha: `https://www.utimix.com/categoria/casa-e-cozinha/`

Cole uma delas no `main.py` para testar!

