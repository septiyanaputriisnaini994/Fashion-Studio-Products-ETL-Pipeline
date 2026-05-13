from utils.transform import transform_data


def test_transform_data():

    sample_data = [
        {
            "Title": "T-Shirt",
            "Price": "$10",
            "Rating": "4.5 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2025-01-01"
        }
    ]

    df = transform_data(sample_data)

    assert df["Price"].iloc[0] == 160000
    assert df["Rating"].iloc[0] == 4.5
    assert df["Colors"].iloc[0] == 3
    assert df["Size"].iloc[0] == "M"
    assert df["Gender"].iloc[0] == "Men"


def test_transform_remove_duplicate():

    sample_data = [
        {
            "Title": "T-Shirt",
            "Price": "$10",
            "Rating": "4.5 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2025-01-01"
        },
        {
            "Title": "T-Shirt",
            "Price": "$10",
            "Rating": "4.5 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2025-01-01"
        }
    ]

    df = transform_data(sample_data)

    assert len(df) == 1


def test_transform_remove_null():

    sample_data = [
        {
            "Title": "T-Shirt",
            "Price": None,
            "Rating": "4.5 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2025-01-01"
        }
    ]

    df = transform_data(sample_data)

    assert df.empty


def test_transform_remove_unknown_product():

    sample_data = [
        {
            "Title": "Unknown Product",
            "Price": "$10",
            "Rating": "4.5 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2025-01-01"
        }
    ]

    df = transform_data(sample_data)

    assert df.empty


def test_transform_remove_unavailable_price():

    sample_data = [
        {
            "Title": "T-Shirt",
            "Price": "Price Unavailable",
            "Rating": "4.5 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2025-01-01"
        }
    ]

    df = transform_data(sample_data)

    assert df.empty


def test_transform_remove_invalid_rating():

    sample_data = [
        {
            "Title": "T-Shirt",
            "Price": "$10",
            "Rating": "Invalid Rating",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2025-01-01"
        }
    ]

    df = transform_data(sample_data)

    assert df.empty

def test_transform_data_error():

    sample_data = "data tidak valid"

    df = transform_data(sample_data)

    assert df.empty

def test_transform_invalid_format():

    sample_data = [
        {
            "Title": "T-Shirt",
            "Price": "$10",
            "Rating": "Rating Tidak Valid",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2025-01-01"
        }
    ]

    df = transform_data(sample_data)

    assert df.empty