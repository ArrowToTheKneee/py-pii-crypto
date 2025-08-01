# 🔐 Different Types of Encryption

## 1. Symmetric Encryption
- Uses a **single key** for both encryption and decryption.
- Fast and suitable for large volumes of data.
- Examples:
  - AES (Advanced Encryption Standard)
  - DES, Triple DES

## 2. Asymmetric Encryption
- Uses a **key pair**: public key (encrypt) and private key (decrypt).
- Slower, used for secure key exchange and digital signatures.
- Examples:
  - RSA
  - ECC (Elliptic Curve Cryptography)

## 3. Hashing (One-way encryption)
- Irreversible transformation of data.
- Used for integrity checks and password storage.
- Examples:
  - SHA-256, SHA-3
  - bcrypt, scrypt (with salt for security)

## 4. Hybrid Encryption
- Combines symmetric and asymmetric encryption.
- Commonly used in SSL/TLS.
- Encrypts the symmetric key with an asymmetric algorithm for secure transmission.