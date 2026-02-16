# Yahoo Finance Equity Crawler

Crawler desenvolvido para extrair dados de equities do Yahoo Finance Research Hub utilizando Selenium e BeautifulSoup.

O projeto aplica filtro por região, ajusta paginação para 100 itens por página e percorre todas as páginas disponíveis, exportando os resultados para CSV.

---

## Objetivo

Extrair:

- Símbolo (ticker)
- Nome da empresa
- Preço atual

A partir do Yahoo Finance Research Hub:

https://finance.yahoo.com/research-hub/screener/equity/

---

##  Arquitetura

O projeto foi estruturado separando responsabilidades:


### 🔹 Responsabilidades

- **Crawler** -> Controlador principal do fluxo
- **Scrapers** -> Automação Selenium 
- **Parser** -> Extração de dados com BeautifulSoup
- **Model** -> Representa entidade de domínio.
- **Service** -> Exporta dados para CSV.
- **Tests** -> Validam parsing de forma isolada.

Essa separação permite testar a lógica de parsing independentemente da automação do navegador.

---

## ⚙️ Tecnologias Utilizadas

- Python 3.10+
- Selenium
- BeautifulSoup4
- pytest
- webdriver-manager

---

## 🚀 Instalação

Clone o repositório:

```bash
git clone <repo-url>
cd <repo-folder>
```

**Crie um ambiente virtual (Opcional, mas recomendado):**
* Linux/macOS:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
* Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

 **Instale as dependências:**
    ```
    pip install -r requirements.txt
    ```

## 💻 Como Utilizar

A aplicação deve ser executada como um módulo a partir da raiz do projeto.

### Comando Básico
```bash
python -m app.main --region "Brazil"
```
**Argumentos:**

| Argumento     | Obrigatório | Descrição | Padrão       |
|---------------|------------|-----------|--------------|
| --region      | Sim        | Região para filtrar |              |
| --output      | Não        | Caminho do CSV de saída | equities.csv |
| --headless    | Não        | Executa navegador em modo headless | False        | 

* Exemplo
  ```bash
  python main.py --region "Brazil" --output brazil.csv --headless
  ```
  
## Funcionamento Interno

1. Abre o Yahoo Finance Screener
2. Aplica filtro de região
3. Ajusta paginação para 100 itens por página
4. Percorre todas as páginas
5. Extrai dados da tabela
6. Exporta para CSV

##  Testes
Os testes cobrem a camada de parsing, garantindo:

- Extração correta de símbolo
- Conversão adequada de preços
- Tratamento de valores inválidos
- Robustez contra HTML incompleto


