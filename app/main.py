import argparse
from pathlib import Path
from app.crawler.YahooEquityCrawler import  YahooEquityCrawler
from app.services.csv_exporter import CSVExporter


def main():
    parser = argparse.ArgumentParser(
        description="Crawler para extrair dados de equities do Yahoo Finance"
    )
    parser.add_argument("--region", required=True, help="Região para filtrar (ex: Argentina, Brazil)")
    parser.add_argument("--output", default="equities.csv", help="Caminho do arquivo CSV de saída (padrão: equities.csv)")
    parser.add_argument("--headless", action="store_true", help="Executar navegador em modo headless")
    args = parser.parse_args()

    crawler = YahooEquityCrawler(headless=args.headless)
    try:
        print(f"Extraindo dados para região: {args.region}")
        equities = crawler.fetch(args.region)
        
        print(f"Total de equities encontradas: {len(equities)}")
        
        output_path = Path(args.output)
        CSVExporter.export(equities, str(output_path))
        
        print(f"Dados exportados com sucesso para: {output_path.absolute()}")
        
    finally:
        crawler.close()


if __name__ == "__main__":
    main()
