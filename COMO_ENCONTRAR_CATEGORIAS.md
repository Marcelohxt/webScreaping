# Como Encontrar URLs das Categorias

## Passo a Passo:

1. **Acesse o site Utimix**: https://www.utimix.com/

2. **Navegue pelas categorias** no menu do site

3. **Clique em uma categoria** que deseja fazer scraping

4. **Copie a URL** da barra de endereço do navegador

5. **Adicione no `main.py`** na lista `category_urls`

## Exemplo:

Se você quer fazer scraping da categoria "Casa e Cozinha":

1. Vá para https://www.utimix.com/
2. Clique em "Casa e Cozinha" (ou como estiver no menu)
3. A URL ficará algo como: `https://www.utimix.com/categoria/casa-e-cozinha/`
4. Cole no `main.py`:

```python
category_urls = [
    "https://www.utimix.com/categoria/casa-e-cozinha/",
]
```

## Dica:

Você pode adicionar múltiplas categorias:

```python
category_urls = [
    "https://www.utimix.com/categoria/casa-e-cozinha/",
    "https://www.utimix.com/categoria/eletronicos/",
    "https://www.utimix.com/categoria/saude-e-beleza/",
    # Adicione quantas quiser
]
```

