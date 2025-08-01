# 🔒 Why Use AES-GCM for PII Encryption

## 🔍 AES-GCM Overview
- AES: Symmetric block cipher (AES-128, AES-192, AES-256)
- GCM (Galois/Counter Mode): Provides confidentiality and integrity

## ✅ Why It’s Better for PII
- **Authenticated Encryption**: Detects tampering with a 16-byte tag
- **Nonce Support**: Random nonces protect against ciphertext pattern detection
- **Fast**: Hardware-accelerated in modern CPUs (AES-NI)
- **Standardized & Trusted**: Widely adopted in FIPS 140-2, TLS, and cloud platforms

## 🛡️ PII Suitability
- Encrypts structured fields (e.g., name, SSN) efficiently
- Tag verification ensures no silent corruption of sensitive data
- Easy key management and rotation using versioning