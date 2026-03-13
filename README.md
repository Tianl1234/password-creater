# 🔐 Pro Password Manager & Generator

A secure, local password generator and manager with a graphical user interface (GUI), written in Python. 

This tool not only generates cryptographically secure passwords but also calculates their mathematical entropy in real-time. Generated passwords can be saved directly into a locally encrypted vault file.

## ✨ Features

* **Cryptographically Secure:** Uses Python's `secrets` module instead of `random` for true cryptographic randomness.
* **Real-Time Entropy Calculation:** Displays the actual strength of your password in bits using a dynamic progress bar.
* **Encrypted Local Vault:** Securely stores passwords using AES encryption (`cryptography.fernet`) tied to a master password.
* **Customizable Generation:**
  * Choose length and character types (letters, numbers, special characters).
  * Option to exclude easily confused characters (e.g., `l`, `1`, `I`, `O`, `0`).
* **Predefined Profiles:** Quick selection for typical use cases (e.g., "Ultra-Secure").
* **User-Friendly:** Intuitive GUI with Dark Mode (`tkinter`) and 1-click copy to clipboard.

## 🛠️ Installation

### Prerequisites
* **Python 3.x** must be installed on your system.

* Install dependencies:
* pip install cryptography
