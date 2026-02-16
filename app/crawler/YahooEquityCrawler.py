from typing import List
from app.models.equity import Equity
from app.scrapers.yahoo_finance_scraper import YahooFinanceScraper
from app.parsers.yahoo_finance_parser import YahooFinanceParser


class YahooEquityCrawler:
    """Estratégia de extração usando Selenium."""

    def __init__(self, headless: bool = False):
        self.scraper = YahooFinanceScraper(headless=headless)
        self.parser = YahooFinanceParser()

    def fetch(self, region: str) -> List[Equity]:
        """
        Busca todas as equities de uma região.
        """
        self.scraper.open_screener()
        self.scraper.apply_region_filter(region)
        self.scraper.set_page_size(100)

        return self._extract_all_pages()

    def close(self):
        """Fecha recursos."""
        self.scraper.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ==================== EXTRAÇÃO ====================

    def _extract_all_pages(self) -> List[Equity]:
        """Percorre todas as páginas e extrai equities."""
        all_equities = []

        while True:
            html = self.scraper.get_current_page_html()
            current_page = self.parser.parse_table(html)
            all_equities.extend(current_page)

            if not self.scraper.go_to_next_page():
                break

        return all_equities
