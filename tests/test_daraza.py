import pytest
import responses
from daraza_sdk.daraza import DarazaClient, UnauthorizedError, NotFoundError, BadRequestError, ServerError

BASE_URL = "https://daraza.net/api/"


@pytest.fixture
def client():
    """Fixture to initialize the DarazaClient."""
    return DarazaClient(api_key="test_api_key", base_url=BASE_URL)


@responses.activate
def test_get_balance_success(client):
    """Test successful wallet balance retrieval."""
    responses.add(
        responses.GET,
        f"{BASE_URL}app_wallet/balance/",
        json={
            "code": "200",
            "message": "Success",
            "details": {"balance": "500000 UGX"}
        },
        status=200,
    )

    response = client.get_balance()
    assert response.code == "200"
    assert response.message == "Success"
    assert response.details["balance"] == "500000 UGX"


@responses.activate
def test_get_balance_unauthorized(client):
    """Test unauthorized error for get_balance."""
    responses.add(
        responses.GET,
        f"{BASE_URL}app_wallet/balance/",
        json={
            "code": "401",
            "message": "Unauthorized",
            "details": "Authorization header is missing",
        },
        status=401,
    )

    with pytest.raises(UnauthorizedError, match="Unauthorized: Authorization header is missing"):
        client.get_balance()


@responses.activate
def test_remit_success(client):
    """Test successful remittance."""
    responses.add(
        responses.POST,
        f"{BASE_URL}sandbox/remit/",
        json={
            "code": "Success",
            "message": "Remittance Successful",
            "data": {
                "method": 1,
                "amount": "10000",
                "phone": "+256789123456",
                "note": "Refund"
            },
            "response_details": "A remittance of UGX 10000/= was successfully processed"
        },
        status=200,
    )

    response = client.remit(method=1, amount="10000", phone="+256789123456", note="Refund")
    assert response.code == "Success"
    assert response.message == "Remittance Successful"
    assert response.data["method"] == 1
    assert response.response_details == "A remittance of UGX 10000/= was successfully processed"


@responses.activate
def test_remit_bad_request(client):
    """Test bad request error for remittance."""
    responses.add(
        responses.POST,
        f"{BASE_URL}sandbox/remit/",
        json={
            "status": "Error",
            "message": "Validation Failed",
            "details": {"phone": ["This field is required."]}
        },
        status=400,
    )

    with pytest.raises(BadRequestError, match="Validation Failed: {'phone': ['This field is required.']}"):
        client.remit(method=1, amount="10000", phone="", note="Refund")


@responses.activate
def test_transfer_to_app_wallet_success(client):
    """Test successful wallet transfer."""
    responses.add(
        responses.POST,
        f"{BASE_URL}app_wallet/transfer/",
        json={
            "code": "200",
            "message": "Successfully transferred 250000 to Client Wallet.",
            "details": {"remaining_app_wallet_balance": "250000 UGX"}
        },
        status=200,
    )

    response = client.transfer_to_app_wallet(percentage=50)
    assert response.code == "200"
    assert response.message == "Successfully transferred 250000 to Client Wallet."
    assert response.details["remaining_app_wallet_balance"] == "250000 UGX"


@responses.activate
def test_transfer_to_app_wallet_server_error(client):
    """Test server error for wallet transfer."""
    responses.add(
        responses.POST,
        f"{BASE_URL}app_wallet/transfer/",
        json={
            "code": "500",
            "message": "Internal Server Error",
            "details": "An error occurred during the transfer"
        },
        status=500,
    )

    with pytest.raises(ServerError, match="Internal Server Error: An error occurred during the transfer"):
        client.transfer_to_app_wallet(percentage=50)
