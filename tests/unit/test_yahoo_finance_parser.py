import pytest
from app.parsers.yahoo_finance_parser import YahooFinanceParser
from app.models.equity import Equity


class TestYahooFinanceParser:
    """Testes unitários para o parser do Yahoo Finance."""

    @pytest.fixture
    def sample_html(self):
        """HTML de exemplo da tabela do Yahoo Finance."""
        return """
        <div class="screener-table">
            <table>
                <tbody>
                    <tr>
                        <td data-testid-cell="ticker">
                            <a>
                                <div><span>AAPL.BA</span></div>
                            </a>
                        </td>
                        <td data-testid-cell="companyshortname.raw">Apple Inc.</td>
                        <td data-testid-cell="intradayprice">150.25</td>
                    </tr>
                    <tr>
                        <td data-testid-cell="ticker">
                            <a>
                                <div><span>GOOGL.BA</span></div>
                            </a>
                        </td>
                        <td data-testid-cell="companyshortname.raw">Alphabet Inc.</td>
                        <td data-testid-cell="intradayprice">2,800.50</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """

    @pytest.fixture
    def empty_html(self):
        """HTML sem dados."""
        return """
        <div class="screener-table">
            <table>
                <tbody></tbody>
            </table>
        </div>
        """

    @pytest.fixture
    def parser(self):
        """Instância do parser."""
        return YahooFinanceParser()

    def test_parse_table_returns_list_of_equities(self, parser, sample_html):
        """Deve retornar lista de equities do HTML."""
        equities = parser.parse_table(sample_html)

        assert isinstance(equities, list)
        assert len(equities) == 2
        assert all(isinstance(eq, Equity) for eq in equities)

    def test_parse_table_extracts_correct_data(self, parser, sample_html):
        """Deve extrair dados corretos de cada equity."""
        equities = parser.parse_table(sample_html)

        # Primeira equity
        assert equities[0].symbol == "AAPL.BA"
        assert equities[0].name == "Apple Inc."
        assert equities[0].price == 150.25

        # Segunda equity
        assert equities[1].symbol == "GOOGL.BA"
        assert equities[1].name == "Alphabet Inc."
        assert equities[1].price == 2800.50

    def test_parse_table_with_empty_table_returns_empty_list(self, parser, empty_html):
        """Deve retornar lista vazia quando tabela está vazia."""
        equities = parser.parse_table(empty_html)

        assert equities == []

    def test_parse_price_with_valid_number(self, parser):
        """Deve converter string numérica para float."""
        assert parser._parse_price("100.50") == 100.50
        assert parser._parse_price("1,234.56") == 1234.56

    def test_parse_price_with_invalid_values(self, parser):
        """Deve retornar None para valores inválidos."""
        assert parser._parse_price("—") is None
        assert parser._parse_price("N/A") is None
        assert parser._parse_price("-") is None
        assert parser._parse_price("") is None
        assert parser._parse_price(None) is None

    def test_parse_price_with_comma_separator(self, parser):
        """Deve remover vírgulas de separador de milhar."""
        assert parser._parse_price("1,000.00") == 1000.00
        assert parser._parse_price("10,000,000.50") == 10000000.50

    def test_parse_symbol_with_valid_cell(self, parser):
        """Deve extrair símbolo de célula válida."""
        from bs4 import BeautifulSoup

        html = """
        <td data-testid-cell="ticker">
            <a>
                <div><span>TSLA.BA</span></div>
            </a>
        </td>
        """
        soup = BeautifulSoup(html, "html.parser")
        cell = soup.select_one('td')

        assert parser._parse_symbol(cell) == "TSLA.BA"

    def test_parse_symbol_with_none_returns_none(self, parser):
        """Deve retornar None quando célula é None."""
        assert parser._parse_symbol(None) is None

    def test_parse_table_handles_missing_fields(self, parser):
        """Deve lidar com campos ausentes"""
        html = """
        <div class="screener-table">
            <table>
                <tbody>
                    <tr>
                        <td data-testid-cell="ticker">
                            <a>
                                <div><span>TEST.BA</span></div>
                            </a>
                        </td>
                        <!-- Nome ausente -->
                        <td data-testid-cell="intradayprice">—</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """

        equities = parser.parse_table(html)

        assert len(equities) == 1
        assert equities[0].symbol == "TEST.BA"
        assert equities[0].name is None
        assert equities[0].price is None