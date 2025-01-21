import requests
from pydantic import BaseModel, ValidationError
from typing import Optional


# Custom Exceptions
class DarazaException(Exception):
    """Base class for all Daraza exceptions."""
    pass


class BadRequestError(DarazaException):
    """Exception for 400 Bad Request."""
    pass


class UnauthorizedError(DarazaException):
    """Exception for 401 Unauthorized."""
    pass


class ForbiddenError(DarazaException):
    """Exception for 403 Forbidden."""
    pass


class NotFoundError(DarazaException):
    """Exception for 404 Not Found."""
    pass


class ServerError(DarazaException):
    """Exception for 500 Internal Server Error."""
    pass


# Response Schemas
class WalletBalanceResponse(BaseModel):
    code: str
    message: str
    details: dict


class TransferResponse(BaseModel):
    code: str
    message: str
    details: Optional[dict]


class RemittanceResponse(BaseModel):
    code: str
    message: str
    data: Optional[dict]
    response_details: Optional[str]


class RequestToPayResponse(BaseModel):
    code: str
    message: str
    data: Optional[dict]
    response_details: Optional[str]


# Main SDK Class
class DarazaClient:
    def __init__(self, api_key: str, base_url: str = "https://daraza.net/api/"):
        """
        Initialize the Daraza Client.
        :param api_key: Your Daraza API key.
        :param base_url: The base URL for the Daraza API.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json",
        }

    def remit(self, method: int, amount: str, phone: str, note: str) -> RemittanceResponse:
        """
        Make a remittance request.
        :param method: The remittance method (integer).
        :param amount: The amount to remit (string).
        :param phone: The phone number to remit to (string).
        :param note: A note for the transaction (string).
        :return: Parsed RemittanceResponse object.
        """
        endpoint = f"{self.base_url}sandbox/remit/"
        payload = {"method": method, "amount": amount, "phone": phone, "note": note}
        response = self._post(endpoint, payload)
        return self._validate_response(RemittanceResponse, response)

    def request_to_pay(self, method: int, amount: str, phone: str, note: str) -> RequestToPayResponse:
        """
        Request payment from a user.
        :param method: The payment method (integer).
        :param amount: The amount to request (string).
        :param phone: The phone number to request payment from (string).
        :param note: A note for the transaction (string).
        :return: Parsed RequestToPayResponse object.
        """
        endpoint = f"{self.base_url}sandbox/request_to_pay/"
        payload = {"method": method, "amount": amount, "phone": phone, "note": note}
        response = self._post(endpoint, payload)
        return self._validate_response(RequestToPayResponse, response)

    def get_balance(self) -> WalletBalanceResponse:
        """
        Get the balance of the application wallet.
        :return: Parsed WalletBalanceResponse object.
        """
        endpoint = f"{self.base_url}app_wallet/balance/"
        response = self._get(endpoint)
        return self._validate_response(WalletBalanceResponse, response)

    def transfer_to_app_wallet(self, percentage: int) -> TransferResponse:
        """
        Transfer a percentage of funds to the app wallet.
        :param percentage: The percentage of funds to transfer (integer).
        :return: Parsed TransferResponse object.
        """
        endpoint = f"{self.base_url}app_wallet/transfer/"
        payload = {"percentage": percentage}
        response = self._post(endpoint, payload)
        return self._validate_response(TransferResponse, response)

    def _post(self, url: str, payload: dict) -> dict:
        """Internal helper to make POST requests."""
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            return self._handle_response(response)
        except requests.exceptions.Timeout:
            raise DarazaException("Request timed out. Please try again later.")
        except requests.exceptions.ConnectionError:
            raise DarazaException("Connection error. Please check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise DarazaException(f"An unexpected error occurred: {str(e)}")

    def _get(self, url: str) -> dict:
        """Internal helper to make GET requests."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            return self._handle_response(response)
        except requests.exceptions.Timeout:
            raise DarazaException("Request timed out. Please try again later.")
        except requests.exceptions.ConnectionError:
            raise DarazaException("Connection error. Please check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise DarazaException(f"An unexpected error occurred: {str(e)}")

    def _handle_response(self, response) -> dict:
        """Handle the response from the API and raise appropriate errors."""
        try:
            response.raise_for_status()  # Raise HTTPError for bad status codes
            return response.json()
        except requests.exceptions.HTTPError:
            error_data = response.json()
            code = error_data.get("code")
            message = error_data.get("message")
            details = error_data.get("details", {})
            if response.status_code == 400:
                raise BadRequestError(f"{message}: {details}")
            elif response.status_code == 401:
                raise UnauthorizedError(f"{message}: {details}")
            elif response.status_code == 403:
                raise ForbiddenError(f"{message}: {details}")
            elif response.status_code == 404:
                raise NotFoundError(f"{message}: {details}")
            elif response.status_code == 500:
                raise ServerError(f"{message}: {details}")
            else:
                raise DarazaException(f"Unexpected Error: {message}")

    def _validate_response(self, schema, response: dict):
        """
        Validate and parse the API response using the given schema.
        :param schema: The schema class to validate against.
        :param response: The API response data.
        :return: Parsed schema object.
        """
        try:
            return schema(**response)
        except ValidationError as e:
            raise DarazaException(f"Response validation failed: {e}")


# Example Usage
if __name__ == "__main__":
    client = DarazaClient(api_key="your_api_key")
    try:
        balance = client.get_balance()
        print("Wallet Balance:", balance)
    except DarazaException as e:
        print("Error:", e)
