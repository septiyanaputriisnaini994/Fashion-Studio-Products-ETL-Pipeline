from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from utils.extract import (
    fetch_content,
    extract_product,
    scrape_products
)


@patch("utils.extract.requests.get")
def test_fetch_content_success(mock_get):

    mock_response = Mock()
    mock_response.text = "<html>Success</html>"
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = fetch_content("https://example.com")

    assert result == "<html>Success</html>"


@patch("utils.extract.requests.get")
def test_fetch_content_failed(mock_get):

    mock_get.side_effect = RequestException("Connection Error")

    result = fetch_content("https://example.com")

    assert result is None


def test_extract_product_success():

    html = """
    <div class="collection-card">
        <h3 class="product-title">T-Shirt</h3>
        <span class="price">$10</span>
        <p>Rating: 4.5 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Men</p>
    </div>
    """

    soup = BeautifulSoup(html, "html.parser")
    card = soup.find("div", class_="collection-card")

    result = extract_product(card)

    assert result["Title"] == "T-Shirt"
    assert result["Price"] == "$10"
    assert result["Rating"] == "4.5 / 5"
    assert result["Colors"] == "3 Colors"
    assert result["Size"] == "Size: M"
    assert result["Gender"] == "Gender: Men"
    assert "timestamp" in result


def test_extract_product_price_unavailable():

    html = """
    <div class="collection-card">
        <h3 class="product-title">T-Shirt</h3>
        <p class="price">Price Unavailable</p>
        <p>Rating: 4.5 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Men</p>
    </div>
    """

    soup = BeautifulSoup(html, "html.parser")
    card = soup.find("div", class_="collection-card")

    result = extract_product(card)

    assert result["Price"] == "Price Unavailable"


def test_extract_product_invalid():

    html = "<div></div>"

    soup = BeautifulSoup(html, "html.parser")

    result = extract_product(soup)

    assert result is None


@patch("utils.extract.fetch_content")
def test_scrape_products(mock_fetch_content):

    html = """
    <html>
        <body>
            <div class="collection-card">
                <h3 class="product-title">T-Shirt</h3>
                <span class="price">$10</span>
                <p>Rating: 4.5 / 5</p>
                <p>3 Colors</p>
                <p>Size: M</p>
                <p>Gender: Men</p>
            </div>
        </body>
    </html>
    """

    mock_fetch_content.return_value = html

    result = scrape_products()

    assert len(result) == 50
    assert result[0]["Title"] == "T-Shirt"


@patch("utils.extract.fetch_content")
def test_scrape_products_fetch_failed(mock_fetch_content):

    mock_fetch_content.return_value = None

    result = scrape_products()

    assert result == []

@patch("utils.extract.fetch_content")
def test_scrape_products_exception(mock_fetch_content):

    mock_fetch_content.side_effect = Exception("Unexpected Error")

    result = scrape_products()

    assert result == []