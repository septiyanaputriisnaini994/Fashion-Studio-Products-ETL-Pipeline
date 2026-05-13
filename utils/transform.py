import logging

import pandas as pd


EXCHANGE_RATE = 16000


def transform_data(data):
    """
    Membersihkan dan mentransformasi data hasil scraping.

    Proses transformasi meliputi:
    - Menghapus data null
    - Menghapus duplicate data
    - Menghapus invalid data
    - Konversi harga USD ke IDR
    - Membersihkan kolom rating, colors, size, dan gender

    Parameters
    ----------
    data : list
        List berisi dictionary data hasil scraping.

    Returns
    -------
    pandas.DataFrame
        Dataframe hasil transformasi data.
        Akan mengembalikan dataframe kosong jika terjadi error.
    """

    try:

        df = pd.DataFrame(data)

        # Hapus null
        df = df.dropna()

        # Hapus duplicate
        df = df.drop_duplicates()

        # Hapus invalid data
        df = df[
            df["Title"] != "Unknown Product"
        ]

        df = df[
            ~df["Price"].str.contains(
                "Unavailable",
                na=False
            )
        ]

        df = df[
            ~df["Rating"].str.contains(
                "Invalid|Not Rated",
                na=False
            )
        ]

        # Transform Price ke rupiah
        df["Price"] = (
            df["Price"]
            .str.replace(
                "$",
                "",
                regex=False
            )
            .astype(float)
            * EXCHANGE_RATE
        )

        # Transform Rating
        df["Rating"] = (
            df["Rating"]
            .str.extract(r"(\d+\.\d+)")[0]
            .astype(float)
        )

        # Transform Colors
        df["Colors"] = (
            df["Colors"]
            .str.extract(r"(\d+)")[0]
            .astype(int)
        )

        # Transform Size
        df["Size"] = (
            df["Size"]
            .str.replace(
                "Size: ",
                "",
                regex=False
            )
            .str.strip()
        )

        # Transform Gender
        df["Gender"] = (
            df["Gender"]
            .str.replace(
                "Gender: ",
                "",
                regex=False
            )
            .str.strip()
        )

        # Hapus NaN hasil transform
        df = df.dropna()

        return df

    except Exception as e:

        logging.error(
            f"Error transforming data: {e}"
        )

        return pd.DataFrame()