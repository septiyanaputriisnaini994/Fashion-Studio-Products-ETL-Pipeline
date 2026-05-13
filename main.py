import logging

from utils.extract import scrape_products
from utils.transform import transform_data

from utils.load import (
    save_to_csv,
    save_to_google_sheets,
    save_to_postgresql
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():

    try:

        logging.info(
            "Starting ETL Pipeline..."
        )

        # Extract
        raw_data = scrape_products()

        logging.info(
            f"Jumlah raw data: {len(raw_data)}"
        )

        if not raw_data:

            logging.warning(
                "Tidak ada data yang berhasil diambil."
            )

            return

        # Transform
        clean_data = transform_data(raw_data)

        logging.info(
            f"Jumlah clean data: {len(clean_data)}"
        )

        if clean_data.empty:

            logging.warning(
                "Data hasil transform kosong."
            )

            return

        # Load to CSV
        save_to_csv(clean_data)

        # Load to Google Sheets
        save_to_google_sheets(
            clean_data,
            "Fashion Studio Products"
        )

        # Load to PostgreSQL
        save_to_postgresql(clean_data)

        logging.info(
            "ETL Pipeline selesai."
        )

    except Exception as e:

        logging.error(
            f"Terjadi error pada ETL Pipeline: {e}"
        )


if __name__ == "__main__":
    main()