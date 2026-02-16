import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)
class YahooFinanceScraper:
    """Gerencia a navegação no Yahoo Finance usando Selenium."""

    BASE_URL = "https://finance.yahoo.com/research-hub/screener/equity/"

    def __init__(self, headless: bool = True):
        options = Options()
        options.page_load_strategy = "eager"

        if headless:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def close(self):
        """Fecha o driver do Selenium."""
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ==================== NAVEGAÇÃO ====================

    def open_screener(self):
        logger.info(f"Acessando URL: {self.BASE_URL}")
        """Abre a página do screener."""
        self.driver.get(self.BASE_URL)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.screener-table"))
        )

    def apply_region_filter(self, region: str):
        """Aplica filtro de região."""
        logger.info(f"Aplicando filtro de região: {region}")
        wait = WebDriverWait(self.driver, 20)

        self._open_region_filter_panel(wait)
        self._select_region_checkbox(wait, region)
        self._deselect_us_if_needed(wait, region)
        self._apply_filter_and_wait(wait)

    def set_page_size(self, size: int = 100):
        """Define o tamanho da página."""
        logger.info(f"Alterando número de itens na página: {size}")
        wait = WebDriverWait(self.driver, 20)

        menu_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".paginationContainer .menuContainer button")
            )
        )
        menu_button.click()

        option = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"div[role='option'][data-value='{size}']")
            )
        )

        old_rows_count = len(self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr"))
        option.click()

        wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "table tbody tr")) > old_rows_count)

    def go_to_next_page(self) -> bool:
        """
        Avança para a próxima página.
        """
        wait = WebDriverWait(self.driver, 10)

        try:
            next_button = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button[data-testid='next-page-button']")
                )
            )
        except TimeoutException:
            return False

        if not next_button.is_enabled() or next_button.get_attribute("disabled"):
            return False


        first_symbol_before = self.driver.find_element(
            By.CSS_SELECTOR, '.screener-table tbody tr:first-child [data-testid-cell="ticker"]'
        ).text.strip()

        next_button.click()

        wait.until(
            lambda d: d.find_element(
                By.CSS_SELECTOR, '.screener-table tbody tr:first-child [data-testid-cell="ticker"]'
            ).text.strip() != first_symbol_before
        )

        return True

    def get_current_page_html(self) -> str:
        """Retorna o HTML da tabela atual."""
        table_element = self.driver.find_element(By.CSS_SELECTOR, ".screener-table")
        return table_element.get_attribute("outerHTML")

    # ==================== MÉTODOS AUXILIARES ====================

    def _open_region_filter_panel(self, wait: WebDriverWait, max_attempts: int = 2):
        """Abre o painel de filtro de região."""
        region_button_locator = (
            By.XPATH,
            "//div[@data-testid='filter-selector'][.//div[text()='Region']]//button",
        )

        for attempt in range(max_attempts):
            region_button = wait.until(EC.element_to_be_clickable(region_button_locator))
            self._safe_click(region_button)

            try:
                wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[contains(@class,'options')]//label")
                    )
                )
                return
            except TimeoutException:
                if attempt == max_attempts - 1:
                    raise Exception("Não foi possível abrir o painel de filtro de região")

    def _select_region_checkbox(self, wait: WebDriverWait, region: str):
        """Seleciona o checkbox da região."""
        region_checkbox_locator = (
            By.XPATH,
            f"//div[contains(@class,'options')]//span[normalize-space()='{region}']/ancestor::label//input",
        )

        region_checkbox = wait.until(EC.presence_of_element_located(region_checkbox_locator))

        if not region_checkbox.is_selected():
            self._safe_click(region_checkbox)

    def _deselect_us_if_needed(self, wait: WebDriverWait, region: str):
        """Desmarca 'United States' se necessário."""
        if region.lower() == "united states":
            return

        try:
            us_checkbox = wait.until(EC.presence_of_element_located((By.ID, "us")))
            if us_checkbox.is_selected():
                self._safe_click(us_checkbox)
        except TimeoutException:
            pass

    def _apply_filter_and_wait(self, wait: WebDriverWait):
        """Aplica o filtro e aguarda atualização."""
        apply_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Apply']"))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            apply_button,
        )

        self._safe_click(apply_button)

        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.table-container table"))
        )

    def _safe_click(self, element):
        """Clica com fallback para JavaScript."""
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)