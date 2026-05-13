from unittest.mock import patch, Mock
import os
import pandas as pd

from utils.load import (
    save_to_csv,
    save_to_google_sheets,
    save_to_postgresql
)


def test_save_to_csv():

    df = pd.DataFrame({
        "Title": ["Test Product"]
    })

    filename = "test_products.csv"

    save_to_csv(df, filename)

    assert os.path.exists(filename)

    loaded_df = pd.read_csv(filename)

    assert not loaded_df.empty

    os.remove(filename)


def test_save_empty_dataframe():

    df = pd.DataFrame()

    filename = "empty_products.csv"

    save_to_csv(df, filename)

    assert os.path.exists(filename)

    os.remove(filename)


def test_save_to_csv_error():

    df = pd.DataFrame({
        "Title": ["Test Product"]
    })

    save_to_csv(df, "folder_tidak_ada/test.csv")


@patch("utils.load.gspread.authorize")
@patch("utils.load.ServiceAccountCredentials.from_json_keyfile_name")
def test_save_to_google_sheets_success(
    mock_credentials,
    mock_authorize
):

    df = pd.DataFrame({
        "Title": ["Test Product"],
        "Price": [160000]
    })

    mock_client = Mock()
    mock_spreadsheet = Mock()
    mock_sheet = Mock()

    mock_credentials.return_value = Mock()
    mock_authorize.return_value = mock_client
    mock_client.open.return_value = mock_spreadsheet
    mock_spreadsheet.sheet1 = mock_sheet

    save_to_google_sheets(
        df,
        "Fashion Studio Products"
    )

    mock_sheet.clear.assert_called_once()
    mock_sheet.update.assert_called_once()


@patch("utils.load.ServiceAccountCredentials.from_json_keyfile_name")
def test_save_to_google_sheets_error(mock_credentials):

    df = pd.DataFrame({
        "Title": ["Test Product"]
    })

    mock_credentials.side_effect = Exception("Credential Error")

    save_to_google_sheets(
        df,
        "Fashion Studio Products"
    )


@patch("utils.load.create_engine")
@patch.dict("os.environ", {
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
    "DB_NAME": "test_db",
    "DB_USER": "postgres",
    "DB_PASSWORD": "12345"
})
def test_save_to_postgresql_success(mock_create_engine):

    df = pd.DataFrame({
        "Title": ["Test Product"],
        "Price": [160000]
    })

    mock_engine = Mock()
    mock_create_engine.return_value = mock_engine

    with patch.object(df, "to_sql") as mock_to_sql:

        save_to_postgresql(
            df,
            "fashion_products"
        )

        mock_create_engine.assert_called_once_with(
            "postgresql+psycopg2://postgres:12345@localhost:5432/test_db"
        )

        mock_to_sql.assert_called_once_with(
            "fashion_products",
            mock_engine,
            if_exists="replace",
            index=False
        )


@patch("utils.load.create_engine")
def test_save_to_postgresql_error(mock_create_engine):

    df = pd.DataFrame({
        "Title": ["Test Product"]
    })

    mock_create_engine.side_effect = Exception("Database Error")

    save_to_postgresql(df)

    mock_create_engine.assert_called_once()