import argparse
import logging
from pathlib import Path
from app.crawler.YahooEquityCrawler import  YahooEquityCrawler
from app.services.csv_exporter import CSVExporter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Cria um logger específico para este ficheiro
logger = logging.getLogger(__name__)

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
        logger.info(f"Extraindo dados para região: {args.region}")
        equities = crawler.fetch(args.region)
        
        logger.info(f"Total de equities encontradas: {len(equities)}")
        
        output_path = Path(args.output)
        CSVExporter.export(equities, output_path)
        
        logger.info(f"Dados exportados com sucesso para: {output_path.absolute()}")
    except Exception as e:
        logger.error(f"Ocorreu um erro crítico durante a execução: {e}", exc_info=True)
    finally:
        crawler.close()
        logger.info("Aplicação finalizada")


if __name__ == "__main__":
    main()
