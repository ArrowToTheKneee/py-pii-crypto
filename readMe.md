# py-pii-crypto

**py-pii-crypto** is a Python package for encrypting and decrypting Personally Identifiable Information (PII) using AES-GCM.
It supports multiple key providers (local and vault), metadata generation, and a CLI for CSV and single-value workflows.

---

## ✨ Features
- AES-GCM encryption/decryption for CSV fields and single values.
- Per-row 12-byte nonce stored as `row_iv` in encrypted CSVs.
- Fuzzy header–to–field alias matching with a similarity threshold.
- Alias system for fields defined in the provider config.
- Field-level selection (encrypt true/false) and optional key version pinning via `key_id`.
- Schema and field validation using validation json and Pydantic
- Versioned, per-field Base64 keys in `keys.json` (e.g., `v1`, `v2`, …).
- Key lifecycle: generate initial keys and rotate to new versions via CLI/KeyManager.
- Pluggable key providers via factory (`local` implemented; `vault` scaffolded).
- Optional structured metadata output (`<output>.metadata.json`) with operation context.
- Robust CSV handling: skip typical ID columns and annotate per-cell decrypt errors.
- Typer-based CLI with `csv`, `data`, and `keys` subcommands.
- Rotating file logging under `logs/` with timestamped entries.
- Ready-to-use examples and configs (`unified_local_provider.json`, `validation_config.json`, `keys.json`, `input_test.csv`, `enc.csv`, `dec.csv`).
- Python API for programmatic encryption/decryption and key management.

---

## 📦 Project Structure
```
py-pii-crypto/
├── src/piicrypto/
│   ├── encrypt_decrypt/          # Encryption & decryption logic
│   ├── helpers/                  # Logging, utils, config parser
│   └── key_provider/             # Key provider interface + implementations
├── examples/                     # Sample CSVs, keys, and config
├── learnings/                    # Design notes
├── pyproject.toml
└── README.md
```

---

## 🚀 Installation
```bash
pip install .
# or
pipx install .
```

---

## 🔑 CLI Usage

### CSV
Encrypt:
```bash
pii-crypto csv encrypt   --input examples/input_test.csv   --output examples/enc.csv   --config-file examples/unified_local_provider.json   --mode local   --create-metadata --validate-json examples/validation_config.json
```

Decrypt:
```bash
pii-crypto csv decrypt   --input examples/enc.csv   --output examples/dec.csv   --config-file examples/unified_local_provider.json   --mode local   --create-metadata
```

### Single values
```bash
# These commands expect a base64 key and nonce (see Key Management).
pii-crypto data encrypt --key <b64-key> --data "Sensitive" --nonce <b64-12-byte-nonce>
pii-crypto data decrypt --key <b64-key> --data "<cipher_b64>" --nonce <b64-12-byte-nonce>
```

---

## 📝 Logging, Metadata and Validation

### Logging
- Configured in `src/piicrypto/helpers/logger_helper.py`.
- Logs go to **rotating files** under `logs/` with filenames like `piicrypto_YYYY-MM-DD.log`.
- Default format includes timestamp, level, logger name, and message.

### Metadata
- If `--create-metadata` is passed, a file named `<output>.metadata.json` is created.
- Created by `helpers/utils.py::generate_metadata` and contains:
  - `key_provider_mode`, `operation` (`encrypt`/`decrypt`), `operation_fields`, `output_file`,
    `created_at`, and package version.
- For CSV encryption, a per-row Base64 IV is written to the `row_iv` column.

### Validation
- If `--validate-json` is passed along with a validation json, like `examples/validation_config.json` the input file fields will be validated against a schema and validation rules
- If a row fails validation, it is logged, like `Validation error for field 'Social Security Number': String should match pattern '^[0-9]{3}-[0-9]{2}-[0-9]{4}$'` and the row is skipped from being encrypted

---

## 🔐 Key Management (Generation, Rotation, Selection)

The project uses a **versioned key store** (e.g., `examples/keys.json`) and a **provider config** (e.g., `examples/unified_local_provider.json`).

### 1) Provider Config (`unified_local_provider.json`)
- Defines **which fields are encrypted**, optional **aliases**, and (optionally) a **pinned key version**.
- Also points to the key source (`key_source`) or a vault URL.
Example:
```json
{
  "fields": {
    "ssn":    { "alias": ["social_security_number", "ssn"], "encrypt": true,  "key_id": "v1" },
    "dob":    { "alias": ["date_of_birth", "dob"],          "encrypt": false              },
    "name":   { "alias": ["full_name", "name"],             "encrypt": true,  "key_id": "v1" },
    "address":{ "alias": ["home_address", "address"],       "encrypt": true               }
  },
  "key_source": "examples/keys.json"
}
```

**Notes**
- `encrypt: true` marks a field for encryption.
- `key_id` (optional) **pins** that field to a specific key **version** (e.g., always use `v1` for `ssn`). If omitted, the **latest version** is used.
- Ensure `key_source` points to a valid path on your machine.

### 2) Keys File (`keys.json`)
- A top-level mapping from **version** ➜ **field** ➜ **Base64 key**.
- Example (abbreviated from `examples/keys.json`):
```json
{
  "v1": {
    "ssn": "f2IfwQDGku5UAoO0GrpHA6QZ/Z22R+s7mQeeYvJh230=",
    "dob": "rjuaBUJWSQrlpDobQCNKgWBiNCVoLCIANj1hq63b8ZA=",
    "name": "xTnsJPzpRBaY2A1D1jWUZBl/Ub2lPAZBXHZWQjo9aeA=",
    "address": "9RsRJtaowblmjm24m+LX1k39o36+oGs6ZRAJruDGVQE="
  },
  "v2": { "... per-field Base64 keys ..." },
  "v3": { "... per-field Base64 keys ..." }
}
```
- Keys are **Base64-encoded 256-bit (32-byte) AES keys**.

### 3) Generation & Rotation via CLI
Implemented in `src/piicrypto/cli.py` and routed through `KeyManager` ➜ the selected provider (`local` or `vault`).

**Generate (create initial version if needed):**
```bash
pii-crypto keys generate   --config-file examples/unified_local_provider.json   --mode local
```
- Creates a new version (e.g., `v1`) in `keys.json` with keys for fields defined in the provider config.

**Rotate (add a new version for future encryptions):**
```bash
pii-crypto keys rotate   --config-file examples/unified_local_provider.json   --mode local
```
- Adds a new version (e.g., `v3` ➜ `v4`) with **fresh random keys for every encryptable field**.
- Existing data remains decryptable because ciphertext is associated with the version used at the time of encryption.

### 4) Selection Logic at Encryption Time
- `LocalKeyProvider.load_keys()` returns a mapping: **field ➜ (version, key)**.
  - If the field has a `key_id` in the provider config, that version is used.
  - Otherwise, the **highest version** present in `keys.json` is used.
- This enables gradual migrations: pin critical fields to an older version until their data is re-encrypted.

### 5) Python API
```python
from piicrypto.key_provider.key_manager import KeyManager

km = KeyManager(provider_type="local", config_file="examples/unified_local_provider.json")

# Create initial keys (v1) if missing
km.generate_keys()

# Rotate to a new key version (e.g., v2 -> v3)
km.rotate_keys()

# Load the mapping used for encryption: {"ssn": ("v3", "<b64key>"), ...}
field_to_version_key = km.load_keys()

# Access a specific historical version
v1_keys = km.get_keys_by_version("v1")  # -> {"ssn": "<b64>", "name": "<b64>", ...}
```

---

## ⚙️ Configuration Tips
- Update the `key_source` path in your provider config to a valid, writable file.
- For Vault, provide `vault_url` in the config and implement the read/write in `VaultKeyProvider` (placeholders exist).

---

## 🛡️ Security Best Practices
- Use **256-bit** keys (already the default in `helpers/utils.generate_aes_key()`).
- Rotate keys on a schedule; pin fields to old versions until re-encryption is completed.
- Protect `keys.json` with strict filesystem permissions or switch to a KMS/Vault.
- Never commit real keys to source control.

---

## 🧠 Possible Enhancements

| Enhancement | Description | Status |
|-------------|-------------|--------|
| ✅ Field-level policy control | Allow users to specify which fields to encrypt or skip via config | Done. Can be specified via unified config json
| ✅ Schema validation | Add input CSV schema validation using Pydantic or similar | Done. Pydanctic is used for schema validation. A validation json is provided and option specified in cli
| ✅ Multiple encryption algorithms | Support RSA or other ciphers optionally |
| ✅ UI layer | A web UI to upload CSV, select fields, and download encrypted results |
| ✅ Integration with cloud KMS | Support AWS KMS, GCP KMS, or Azure Key Vault |
| ✅ Metadata storage | Store nonce and encryption metadata in structured headers or external files | Done. Nonce is stored per row, in row_iv column, in the enc or dec file. Metadata creation enabled by create_metadata option in cli for csv encryption and csv decryption
| ✅ Docker support & CI/CD | Add Dockerfile for containerization and GH workflows |
| ✅ Unittest | Add Unittests to the repo |

---

## 👩‍💻 Contributing

Contributions, suggestions, and issues are welcome! Please fork the repo and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.
