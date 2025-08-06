
# 📦 PII Crypto

**PII Crypto** is a Python module and CLI tool designed to securely encrypt and decrypt Personally Identifiable Information (PII) in CSV files or string inputs using AES-GCM encryption. It supports configurable key management and provides a flexible framework for protecting sensitive data in transit and storage.

---

## 🔧 Features

- AES-GCM encryption and decryption
- Field-level encryption for CSV files
- Flexible key management using provider configs
- CLI support via `typer` for easy usage
- Logging support for auditability
- Alias-based field mapping

---

## 🗂️ Project Structure

```
src/piicrypto/
│
├── cli.py                  # CLI entry point
├── encrypt_decrypt/        # Encryption and decryption logic
├── helpers/                # Utility and logging functions
├── key_provider/           # Key management interface and implementation
└── __init__.py             # Module init
examples/                   # Example inputs, outputs, and key configs
```

---

## 🚀 Installation

```bash
git clone https://github.com/ArrowToTheKneee/py-pii-crypto
cd py-pii-crypto
pip install -e .
```

---

## 📌 Usage

### CLI Commands

**Generate Keys**
```bash
pii-crypto --log-dir logs keys generate --config-file examples/local_provider.json --mode local
```

**Encrypt CSV(with create metadata)**
```bash
pii-crypto --log-dir logs csv encrypt --input-file examples/input_test.csv --output-file examples/enc.csv --config-file examples/local_provider.json --mode local --create-metadata
```

**Decrypt CSV(with create metadata)**
```bash
pii-crypto --log-dir logs csv decrypt --input-file examples/enc.csv --output-file examples/dec.csv --config-file examples/local_provider.json --mode local --create-metadata
```

---

## 📁 Example Files

- `examples/input_test.csv`: Sample input file
- `examples/enc.csv`: Encrypted CSV output
- `examples/dec.csv`: Decrypted CSV output
- `examples/local_provider.json`: Sample key provider config
- `examples/aliases.json`: Optional field aliasing config

---

## ✅ Requirements

- Python 3.8+
- `pycryptodome`
- `typer`
- `pydantic`

Dependencies are listed in `pyproject.toml`.

---

## 🔒 Security Note

- AES-GCM is used with unique nonces for every encryption to ensure confidentiality and integrity.
- The system supports pluggable key providers. You can extend `BaseKeyProvider` to implement secure remote key stores.

---

## 🧠 Possible Enhancements

| Enhancement | Description | Status |
|-------------|-------------|--------|
| ✅ Field-level policy control | Allow users to specify which fields to encrypt or skip via config |
| ✅ Schema validation | Add input CSV schema validation using Pydantic or similar |
| ✅ Multiple encryption algorithms | Support RSA or other ciphers optionally |
| ✅ UI layer | A web UI to upload CSV, select fields, and download encrypted results |
| ✅ Integration with cloud KMS | Support AWS KMS, GCP KMS, or Azure Key Vault |
| ✅ Metadata storage | Store nonce and encryption metadata in structured headers or external files | Done. Nonce is stored per row, in row_iv column, in the enc or dec file. Metadata creation enabled by create_metadata option in cli for csv encryption and csv decryption
| ✅ Docker support | Add Dockerfile for containerization |

---

## 👩‍💻 Contributing

Contributions, suggestions, and issues are welcome! Please fork the repo and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.
