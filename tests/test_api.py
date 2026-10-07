from unittest.mock import MagicMock, patch

from app import create_app


def test_health():
    app = create_app()
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"


@patch("app.get_collection")
def test_list_transactions(mock_get_collection):
    mock_collection = MagicMock()

    mock_collection.find.return_value = [
        {
            "reference": "TX001",
            "amount": 150.50
        }
    ]

    mock_get_collection.return_value = mock_collection

    app = create_app()
    client = app.test_client()

    response = client.get("/transactions")

    assert response.status_code == 200
    assert response.json == [
        {
            "reference": "TX001",
            "amount": 150.50
        }
    ]


@patch("app.get_collection")
def test_create_transaction(mock_get_collection):
    mock_collection = MagicMock()
    mock_get_collection.return_value = mock_collection

    app = create_app()
    client = app.test_client()

    response = client.post(
        "/transactions",
        json={
            "reference": "TX002",
            "amount": 250.75
        }
    )

    assert response.status_code == 201
    assert response.json == {
        "message": "Transaction created"
    }

    mock_collection.insert_one.assert_called_once_with({
        "reference": "TX002",
        "amount": 250.75
    })


@patch("app.get_collection")
def test_create_transaction_without_reference(mock_get_collection):
    mock_collection = MagicMock()
    mock_get_collection.return_value = mock_collection

    app = create_app()
    client = app.test_client()

    response = client.post(
        "/transactions",
        json={
            "amount": 100.00
        }
    )

    assert response.status_code == 400
    assert response.json["error"] == "reference and amount are required"


@patch("app.get_collection")
def test_create_transaction_without_amount(mock_get_collection):
    mock_collection = MagicMock()
    mock_get_collection.return_value = mock_collection

    app = create_app()
    client = app.test_client()

    response = client.post(
        "/transactions",
        json={
            "reference": "TX003"
        }
    )

    assert response.status_code == 400
    assert response.json["error"] == "reference and amount are required"


@patch("app.get_collection")
def test_create_transaction_with_negative_amount(mock_get_collection):
    mock_collection = MagicMock()
    mock_get_collection.return_value = mock_collection

    app = create_app()
    client = app.test_client()

    response = client.post(
        "/transactions",
        json={
            "reference": "TX004",
            "amount": -50.00
        }
    )

    assert response.status_code == 400
    assert response.json["error"] == "amount must be a positive number"