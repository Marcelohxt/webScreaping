# ⚠️ Aviso: Dificuldade de Acesso ao Site Utimix

## Situação Atual

O site **https://www.utimix.com/** está implementando proteções anti-bot muito rigorosas, retornando **403 Forbidden** mesmo quando usamos Selenium (que simula um navegador real).

## Possíveis Causas

1. **Cloudflare ou proteção similar**: Detecta automação mesmo com Selenium
2. **Verificação de JavaScript complexa**: Requer interação humana ou tempo de navegação
3. **Rate limiting agressivo**: Bloqueia IPs suspeitos
4. **Verificação de cookies/sessão**: Requer autenticação ou cookies específicos

## Soluções Alternativas

### 1. Usar Selenium com Modo Não-Headless

No `config.py`, configure:
```python
USE_SELENIUM = True
SELENIUM_HEADLESS = False  # Importante: False
```

Isso abrirá o navegador visível, que pode ajudar a passar pela proteção.

### 2. Navegação Manual Inicial

1. Execute o script com `SELENIUM_HEADLESS = False`
2. Quando o navegador abrir, navegue manualmente pelo site
3. Faça login se necessário
4. Deixe o script continuar automaticamente

### 3. Usar undetected-chromedriver (Recomendado)

Este é um driver do Chrome modificado especificamente para evitar detecção:

```bash
pip install undetected-chromedriver
```

Depois, podemos modificar o código para usá-lo.

### 4. Inspeção Manual do Site

Como alternativa, você pode:

1. Abrir o site manualmente no navegador
2. Inspecionar os elementos (F12)
3. Identificar os seletores CSS manualmente
4. Salvar o HTML da página
5. Testar os seletores localmente

### 5. Verificar se há API do Site

Alguns sites têm APIs que podem ser acessadas diretamente. Verifique se há endpoints de API que possam ser usados.

## Recomendação Imediata

**Opção 1: Inspeção Manual (Mais Rápido)**
1. Abra https://www.utimix.com/ no seu navegador
2. Navegue até uma página de produtos/categoria
3. Pressione F12 para abrir DevTools
4. Use a ferramenta de inspeção (Ctrl+Shift+C)
5. Clique em um produto e copie o seletor CSS
6. Configure manualmente no `config.py`

**Opção 2: Usar undetected-chromedriver**
Posso atualizar o código para usar `undetected-chromedriver` que é mais eficaz contra proteções anti-bot.

Qual opção você prefere?

