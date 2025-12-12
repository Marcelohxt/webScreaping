# Solução para Erro 403 no Utimix.com

## 🔴 Problema Identificado

O site **https://www.utimix.com/** está retornando **403 Forbidden** quando acessado via requisições HTTP normais. Isso significa que o site tem proteção anti-bot ativa.

## ✅ Solução: Usar Selenium

Para contornar essa proteção, precisamos usar **Selenium**, que simula um navegador real e pode executar JavaScript.

## 📋 Passos para Configurar

### 1. Instalar ChromeDriver

O Selenium precisa do ChromeDriver para controlar o Chrome:

**Opção A - Automático (Recomendado):**
```bash
pip install webdriver-manager
```

**Opção B - Manual:**
1. Baixe o ChromeDriver de: https://chromedriver.chromium.org/
2. Coloque na pasta do projeto ou no PATH do sistema

### 2. Atualizar config.py

Edite o arquivo `config.py` e altere:

```python
USE_SELENIUM = True
SELENIUM_DRIVER = "chrome"  # ou "firefox"
SELENIUM_HEADLESS = False  # True para executar sem abrir navegador
```

### 3. Executar o Scraping

```bash
python main.py
```

## 🔧 Configuração Alternativa (Com webdriver-manager)

Se você instalou o `webdriver-manager`, podemos atualizar o código para usá-lo automaticamente. Isso evita ter que baixar o ChromeDriver manualmente.

### Instalar:
```bash
pip install webdriver-manager
```

### Atualizar requirements.txt:
Adicione `webdriver-manager` ao arquivo requirements.txt

## ⚠️ Observações Importantes

1. **Selenium é mais lento** que requisições HTTP normais
2. **Requer um navegador** (Chrome ou Firefox) instalado no sistema
3. **Headless mode** pode não funcionar em alguns sites (desabilite se necessário)
4. **Delay recomendado**: Mantenha `DELAY_BETWEEN_REQUESTS` em pelo menos 3-5 segundos

## 🐛 Troubleshooting

### Erro: "chromedriver not found"
- Instale o ChromeDriver ou use `webdriver-manager`
- Verifique se o Chrome está instalado

### Erro: "selenium not installed"
```bash
pip install selenium
```

### Site ainda bloqueia mesmo com Selenium
- Tente desabilitar headless: `SELENIUM_HEADLESS = False`
- Aumente o delay: `DELAY_BETWEEN_REQUESTS = 5`
- Adicione mais tempo de espera: `SELENIUM_WAIT_TIME = 15`

## 📝 Próximos Passos

1. Configure `USE_SELENIUM = True` em `config.py`
2. Execute `python inspect_selectors.py` para identificar os seletores CSS
3. Configure os seletores encontrados em `config.py`
4. Adicione as URLs das categorias em `main.py`
5. Execute `python main.py`

