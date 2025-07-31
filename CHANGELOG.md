# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-07-28

### Added
- Field-level AES-GCM encryption with nonce and tag included in output.
- CSV encryption/decryption support.
- Key generation and rotation features.

---

## [0.2.0] - 2025-07-30

### Added
- Fuzzy matching of fields to map to appropriate keys
- Row level nonce instead of a new nonce for each field

---

## [0.3.0] - 2025-07-31

### Added
- Adding logic to skip encrypting row numbering/id column
