import csv
import logging
from typing import List
from app.models.equity import Equity

logger = logging.getLogger(__name__)
class CSVExporter:
    """Serviço responsável por exportar dados de Equity para arquivo CSV."""

    @staticmethod
    def export(equities: List[Equity], output_path: str) -> None:
        logger.info(f"Criando arquivo csv")

        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            writer.writerow(["symbol", "name", "price"])
            
            for equity in equities:
                price_str = f"{equity.price:.2f}" if equity.price is not None else ""
                writer.writerow([
                    equity.symbol or "",
                    equity.name or "",
                    price_str
                ])
