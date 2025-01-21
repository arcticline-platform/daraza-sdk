# Daraza Python SDK

The Daraza Python SDK provides an easy-to-use interface for interacting with the Daraza API. This SDK allows developers to integrate Daraza's features into their applications with minimal effort.

## Features

- Remit funds: Send money to a specified phone number.
- Request payment: Request payment from a phone number.
- Check wallet balance: Retrieve the current balance of your app wallet.
- Transfer funds to app wallet: Transfer a percentage of funds to your app wallet.

## Installation

Install the SDK via pip:

```bash
pip install daraza-sdk
```

## Quick Start

### Initialize the Client

Start by importing and initializing the client:

```python
from daraza_sdk.daraza import DarazaClient

# Replace YOUR_API_KEY with your actual API key
client = DarazaClient(api_key="YOUR_API_KEY")
```

### Remit Funds

```python
response = client.remit(
    method=1,
    amount="15000",
    phone="+2567800000000",
    note="Checkout"
)
print(response)
```

### Request Payment

```python
response = client.request_to_pay(
    method=1,
    amount="15000",
    phone="+2567800000000",
    note="Checkout"
)
print(response)
```

### Check Wallet Balance

```python
response = client.get_balance()
print(response)
```

### Transfer Funds to App Wallet

```python
response = client.transfer_to_app_wallet(percentage=25)
print(response)
```

## Error Handling

The SDK returns a dictionary with an error key in case of a failure:

```python
response = client.get_balance()
if "error" in response:
    print("Error:", response["error"])
else:
    print("Balance:", response)
```

## Full API Reference

### DarazaClient(api_key, base_url)

**Parameters:**
- `api_key` (str): Your Daraza API key.
- `base_url` (str): Base URL for the API. Defaults to https://daraza.net/api/.

### Methods

#### remit(method, amount, phone, note)
Send money to a specified phone number.

**Parameters:**
- `method` (int): Remittance method.
- `amount` (str): Amount to send.
- `phone` (str): Recipient's phone number.
- `note` (str): Transaction note.

**Returns:** Response JSON or an error message.

#### request_to_pay(method, amount, phone, note)
Request payment from a phone number.

**Parameters:**
- `method` (int): Payment method.
- `amount` (str): Amount to request.
- `phone` (str): Payer's phone number.
- `note` (str): Transaction note.

**Returns:** Response JSON or an error message.

#### get_balance()
Retrieve the current balance of the app wallet.

**Returns:** Response JSON or an error message.

#### transfer_to_app_wallet(percentage)
Transfer a percentage of funds to the app wallet.

**Parameters:**
- `percentage` (int): Percentage of funds to transfer.

**Returns:** Response JSON or an error message.

## Contribution

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and submit a pull request.

## License

This SDK is licensed under the GNU General Public License.

## Support

For issues or feature requests, please open an issue on the GitHub repository.