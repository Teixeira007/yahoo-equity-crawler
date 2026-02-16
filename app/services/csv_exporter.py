import csv
from typing import List
from app.models.equity import Equity


class CSVExporter:
    """Serviço responsável por exportar dados de Equity para arquivo CSV."""

    @staticmethod
    def export(equities: List[Equity], output_path: str) -> None:
        if not equities:
            raise ValueError("Lista de equities não pode estar vazia")

        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Cabeçalho
            writer.writerow(["symbol", "name", "price"])
            
            # Dados
            for equity in equities:
                # Formata price como string com 2 casas decimais se não for None
                price_str = f"{equity.price:.2f}" if equity.price is not None else ""
                writer.writerow([
                    equity.symbol or "",
                    equity.name or "",
                    price_str
                ])
