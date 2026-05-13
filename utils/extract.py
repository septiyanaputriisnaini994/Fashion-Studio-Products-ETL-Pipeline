import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://fashion-studio.dicoding.dev"


def fetch_content(url):
    """
    Mengambil HTML content dari sebuah URL website.

    Parameters
    ----------
    url : str
        URL website yang akan diambil HTML-nya.

    Returns
    -------
    str | None
        HTML content dalam bentuk string jika berhasil,
        None jika terjadi error request.
    """

    try:
        response = requests.get(url, timeout=10)

        response.raise_for_status()

        return response.text

    except requests.exceptions.RequestException as e:

        logging.error(
            f"Error fetching website: {e}"
        )

        return None


def extract_product(card):
    """
    Mengekstrak informasi produk dari HTML card.

    Parameters
    ----------
    card : bs4.element.Tag
        HTML tag product card dari BeautifulSoup.

    Returns
    -------
    dict | None
        Dictionary berisi data produk jika berhasil,
        None jika proses ekstraksi gagal.
    """

    try:

        title = (
            card.find(
                "h3",
                class_="product-title"
            )
            .text
            .strip()
        )

        # Handle price normal dan unavailable
        price_tag = card.find(
            "span",
            class_="price"
        )

        if price_tag:

            price = (
                price_tag
                .text
                .strip()
            )

        else:

            unavailable_price = card.find(
                "p",
                class_="price"
            )

            price = (
                unavailable_price.text.strip()
                if unavailable_price
                else None
            )

        details = card.find_all("p")

        rating = (
            details[0]
            .text
            .strip()
            .replace("Rating: ", "")
        )

        colors = (
            details[1]
            .text
            .strip()
        )

        size = (
            details[2]
            .text
            .strip()
        )

        gender = (
            details[3]
            .text
            .strip()
        )

        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:

        logging.error(
            f"Error extracting product: {e}"
        )

        return None


def scrape_products():
    """
    Melakukan scraping data produk dari seluruh halaman website.

    Returns
    -------
    list
        List berisi dictionary data produk hasil scraping.
    """

    products = []

    try:

        for page in range(1, 51):

            if page == 1:
                url = BASE_URL

            else:
                url = f"{BASE_URL}/page{page}"

            html = fetch_content(url)

            if html is None:
                continue

            soup = BeautifulSoup(
                html,
                "html.parser"
            )

            cards = soup.find_all(
                "div",
                class_="collection-card"
            )

            for card in cards:

                product = extract_product(card)

                if product:
                    products.append(product)

        return products

    except Exception as e:

        logging.error(
            f"Error during scraping: {e}"
        )

        return []