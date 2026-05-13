import logging
import os

import gspread
from dotenv import load_dotenv
from oauth2client.service_account import (
    ServiceAccountCredentials
)

from sqlalchemy import create_engine


load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def save_to_csv(
    df,
    filename="products.csv"
):
    """
    Menyimpan dataframe ke file CSV.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe hasil transformasi data.

    filename : str, optional
        Nama file CSV tujuan penyimpanan.
        Default adalah "products.csv".

    Returns
    -------
    None
    """

    try:

        df.to_csv(
            filename,
            index=False
        )

        logging.info(
            f"Data berhasil disimpan ke {filename}"
        )

    except Exception as e:

        logging.error(
            f"Error saving CSV: {e}"
        )


def save_to_google_sheets(
    df,
    spreadsheet_name
):
    """
    Menyimpan dataframe ke Google Sheets.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe hasil transformasi data.

    spreadsheet_name : str
        Nama spreadsheet Google Sheets tujuan.

    Returns
    -------
    None
    """

    try:

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        credentials = (
            ServiceAccountCredentials
            .from_json_keyfile_name(
                "google-sheets-api.json",
                scope
            )
        )

        client = gspread.authorize(
            credentials
        )

        spreadsheet = client.open(
            spreadsheet_name
        )

        sheet = spreadsheet.sheet1

        sheet.clear()

        data = (
            [df.columns.values.tolist()]
            + df.values.tolist()
        )

        sheet.update(data)

        logging.info(
            "Data berhasil upload ke Google Sheets"
        )

    except Exception as e:

        logging.error(
            f"Error upload Google Sheets: {e}"
        )


def save_to_postgresql(
    df,
    table_name="fashion_products"
):
    """
    Menyimpan dataframe ke database PostgreSQL.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe hasil transformasi data.

    table_name : str, optional
        Nama tabel PostgreSQL tujuan.
        Default adalah "fashion_products".

    Returns
    -------
    None
    """

    try:

        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")

        database_url = (
            f"postgresql+psycopg2://"
            f"{db_user}:{db_password}"
            f"@{db_host}:{db_port}/{db_name}"
        )

        engine = create_engine(
            database_url
        )

        df.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False
        )

        logging.info(
            "Data berhasil disimpan ke PostgreSQL"
        )

    except Exception as e:

        logging.error(
            f"Error saving PostgreSQL: {e}"
        )