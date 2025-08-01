
# 🔐 PII Crypto

A Python-based CLI tool and library for encrypting and decrypting Personally Identifiable Information (PII) in CSV files using AES-GCM encryption. It features pluggable key providers, versioned key rotation, and field-level encryption/decryption with fuzzy alias matching.

---

## ✅ Features

### 🔑 Key Management
- AES-256 key generation per field
- Versioned key storage (v1, v2, …)
- Key rotation via CLI
- Support for multiple key providers:
  - **LocalKeyProvider** (default)
  - **VaultKeyProvider** (template provided, extendable)

### 🔒 AES-GCM Encryption
- Per-field encryption with authentication tags
- 12-byte IV (nonce) generation per row
- Base64-encoded output with tag and version metadata
- Secure random IV and tag creation per record

### 📂 CSV Field-Level Processing
- Encrypt/decrypt selected fields in CSVs
- Skips empty cells and non-PII fields
- Row-level IV (nonce) included in output
- Optional alias mapping for flexible column names

---

## 🧰 Requirements

- Python 3.7+

### Installation

Install from source:

```bash
pip install .
```

Or install dependencies manually:

```bash
pip install typer pycryptodome rapidfuzz
```

---

## 🚀 CLI Usage

Main CLI entry point:

```bash
pii-crypto
```

### 🔑 Generate Keys

```bash
pii-crypto keys generate \
  --config-file local_provider.json \
  --mode local
```

### ♻️ Rotate Keys

```bash
pii-crypto keys rotate \
  --config-file local_provider.json \
  --mode local
```

### 🔐 Encrypt CSV

```bash
pii-crypto csv encrypt \
  --input-file input_test.csv \
  --output-file enc.csv \
  --config-file local_provider.json \
  --mode local \
  --aliases-file aliases.json
```

### 🔓 Decrypt CSV

```bash
pii-crypto csv decrypt \
  --input-file enc.csv \
  --output-file dec.csv \
  --config-file local_provider.json \
  --mode local \
  --aliases-file aliases.json
```

### 🔐 Encrypt Raw Data

```bash
pii-crypto data encrypt \
  --key <base64_key> \
  --data "Sensitive Info" \
  --nonce <base64_nonce>
```

### 🔓 Decrypt Raw Data

```bash
pii-crypto data decrypt \
  --key <base64_key> \
  --data <ciphertext> \
  --nonce <base64_nonce>
```

---

## 🧠 Field Aliasing

Alias matching for columns using JSON:

```json
{
  "ssn": ["social_security_number", "ss_number"],
  "dob": ["birthdate", "date_of_birth"]
}
```

---

## 📁 Project Structure

```
src/piicrypto/
├── cli.py                         # Typer CLI entry point
├── encrypt_decrypt/
│   ├── encryptor.py               # AES-GCM encryption logic
│   ├── decryptor.py               # AES-GCM decryption logic
├── key_provider/
│   ├── key_manager.py             # Versioned key generation and rotation
│   ├── key_provider_factory.py    # Provider interface handler
│   ├── local_key_provider.py      # Default local provider
│   └── vault_key_provider.py      # Template for remote providers
├── helpers/
│   └── utils.py                   # Nonce generation, alias matching, etc.
```

---

## 🧪 Sample Workflow

```bash
pii-crypto keys generate --config-file keys.json --mode local
pii-crypto csv encrypt --input-file input_test.csv --output-file enc.csv --config-file local_provider.json --mode local --aliases-file aliases.json
pii-crypto csv decrypt --input-file enc.csv --output-file dec.csv --config-file local_provider.json --mode local --aliases-file aliases.json
pii-crypto keys rotate --config-file keys.json --mode local
```

---

## 📜 License

MIT License
