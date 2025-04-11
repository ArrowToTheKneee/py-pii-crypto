# PII Encryption/Decryption Library

This Python library securely encrypts and decrypts Personally Identifiable Information (PII) fields. It integrates with Azure KeyVault to fetch unique encryption keys for each PII field (e.g., Name, SSN). Each field requires its own encryption key, ensuring data-specific security. The library also supports key rollover on a yearly basis, allowing decryption of previously encrypted data.

The library provides two main modes of operation:
- **Encrypt/Decrypt Endpoint:** Encrypt or decrypt PII fields directly in a CSV file using Azure KeyVault.
- **Local Key Import:** Import the keys locally for faster processing when working with large datasets.

## Features

- **Field-Specific Encryption:** Each PII field (e.g., Name, SSN) uses a unique encryption key fetched from Azure KeyVault.
- **Key Management:** Keys are securely retrieved from Azure KeyVault for each individual PII field.
- **Random Nonce/Salt:** A random nonce or salt is used during encryption to ensure data security.
- **Key Rollover:** The library supports automatic key rollover on a yearly basis, ensuring backward compatibility for decryption of previously encrypted PII.
- **Secure Storage:** Use the library to store encrypted PII fields in databases or CSV files securely.
- **CSV File Encryption/Decryption:** Encrypt or decrypt entire fields in a CSV file using the Azure KeyVault-based keys.
- **Local Key Import for Large Datasets:** Import encryption keys locally to handle large datasets more efficiently without hitting the Azure KeyVault endpoints every time.

## Requirements

- Python 3.7+
- Azure KeyVault
- `cryptography` library for encryption
- `azure-identity` for Azure authentication
- `azure-keyvault-secrets` for accessing secrets in KeyVault
- `pycryptodome` (or another preferred encryption library)
- `pandas` for handling CSV files

## Installation

Clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/your-username/pii-encryption-library.git
cd pii-encryption-library
pip install -r requirements.txt

