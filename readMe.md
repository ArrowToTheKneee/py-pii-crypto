# 🔐 PII Crypto

A Python-based CLI tool and library for encrypting and decrypting Personally Identifiable Information (PII) in CSV files using AES-GCM encryption with field-level key management.

---

## ✅ Features

### 🔑 Key Management
- AES-256 key generation per field
- Versioned key storage (v1, v2, ...)
- Key rotation support for seamless key updates

### 🔒 AES-GCM Encryption
- Per-field encryption with authentication tags
- Random 12-byte nonces per row
- Version-tagged ciphertexts for forward compatibility

### 📂 CSV Processing
- Field-level encryption/decryption in CSV files
- Intelligent field matching via aliases (fuzzy matching with RapidFuzz)
- Skips empty fields and non-PII columns (like row counters, or non-matching aliases)

---

## 🧰 Requirements

- Python 3.7+

### Installation

Install via pip from your local directory:
```

pip install .

```

Or install only the dependencies directly:
```

pip install typer pycryptodome rapidfuzz

```

---

## 🚀 Usage Guide

The CLI is exposed as `pii-crypto`.

### 🔧 Generate Keys

```

pii-crypto generate-keys --fields "name,email,ssn" --json-file keys.json

```
Creates a `keys.json` file with AES-256 keys under version v1.

### ♻️ Rotate Keys

```

pii-crypto rotate-keys --json-file keys.json

```
Adds a new key version (e.g., v2) for each existing field.

### 🔐 Encrypt CSV

```

pii-crypto encrypt-csv \
--input-file input.csv \
--output-file encrypted.csv \
--keys-file keys.json \
--aliases-file aliases.json

```
- Fields are matched against aliases (if provided)
- Adds a `row_iv` column to each row
- Automatically skips row numbers, empty fields, etc.

### 🔓 Decrypt CSV

```

pii-crypto decrypt-csv \
--input-file encrypted.csv \
--output-file decrypted.csv \
--keys-file keys.json \
--aliases-file aliases.json

```
- Only fields encrypted with the current key version are decrypted
- Fields not recognized in keys or aliases remain unchanged

### 🔐 Encrypt Raw Data

```

pii-crypto encrypt-data \
--key <base64_key> \
--data "Sensitive Info" \
--nonce <base64_nonce>

```

### 🔓 Decrypt Raw Data

```

pii-crypto decrypt-data \
--key <base64_key> \
--data <ciphertext> \
--nonce <base64_nonce>

```

---

## 🧠 Field Aliasing with Fuzzy Matching

The CLI supports field aliasing via an optional `aliases.json` file:
```

{
"ssn": ["social_security_number", "ss_number"],
"dob": ["date_of_birth", "birthdate"]
}

```
This allows the tool to encrypt/decrypt even if column names vary.

---

## 📦 Project Structure

```

.
├── cli.py               \# CLI entry point using Typer
├── encryptor.py         \# CSV and string encryption logic
├── decryptor.py         \# CSV and string decryption logic
├── key_manager.py       \# Key generation, rotation, and loading
├── helpers.py           \# Utility functions: nonce generation, alias matching
├── pyproject.toml       \# Build system and dependencies
└── readMe.md            \# 📘 You're here!

```

---

## 🧪 Sample Workflow

```


# Generate initial keys

pii-crypto generate-keys --fields "name,email" --json-file keys.json

# Encrypt a CSV

pii-crypto encrypt-csv --input-file raw.csv --output-file encrypted.csv --keys-file keys.json

# Decrypt it back

pii-crypto decrypt-csv --input-file encrypted.csv --output-file decrypted.csv --keys-file keys.json

# Rotate keys as needed

pii-crypto rotate-keys --json-file keys.json

```

