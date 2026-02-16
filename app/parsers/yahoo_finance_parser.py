from bs4 import BeautifulSoup
from typing import List
from app.models.equity import Equity


class YahooFinanceParser:
    """Extrai dados de equity do HTML do Yahoo Finance."""

    @staticmethod
    def parse_table(html: str) -> List[Equity]:
        soup = BeautifulSoup(html, "html.parser")
        table = soup.select_one(".screener-table table")

        if not table:
            return []

        rows = table.select("tbody tr")
        equities = []

        for row in rows:
            equity = YahooFinanceParser._parse_row(row)
            if equity:
                equities.append(equity)

        return equities

    @staticmethod
    def _parse_row(row) -> Equity | None:
        """Extrai dados de uma linha da tabela."""
        symbol_cell = row.select_one('[data-testid-cell="ticker"]')
        name_cell = row.select_one('[data-testid-cell="companyshortname.raw"]')
        price_cell = row.select_one('[data-testid-cell="intradayprice"]')

        return Equity(
            symbol=YahooFinanceParser._parse_symbol(symbol_cell),
            name=name_cell.get_text(strip=True) if name_cell else None,
            price=YahooFinanceParser._parse_price(price_cell.get_text(strip=True)) if price_cell else None,
        )

    @staticmethod
    def _parse_symbol(cell) -> str | None:
        """Extrai o símbolo de uma célula."""
        if not cell:
            return None

        link = cell.select_one('a')
        if link and link.div and link.div.span:
            return link.div.span.text.strip()

        return None

    @staticmethod
    def _parse_price(text: str) -> float | None:
        """Converte texto de preço para float."""
        if not text:
            return None

        text = text.strip()

        if text in {"—", "N/A", "-"}:
            return None

        text = text.replace(",", "")

        try:
            return float(text)
        except ValueError:
            return None