# KeySigner: Keystore Management and APK Signing Tool

## Overview
KeySigner is a command-line python tool designed to simplify keystore management and APK signing. It integrates KeyTool and ApkSigner, allowing developers to easily generate and migrate keystores (JKS, BKS, PKCS12), extract certificates and private keys, and sign APKs with custom keystores, supporting multiple signature schemes (v1, v2, v3). Whether you need to create, migrate, or sign, KeySigner provides a user-friendly interface for developers of all levels and efficient workflow.

---

## Features

- **Generate Keystores**: Easily generate JKS, BKS, and PKCS12 keystores.
- **Keystore Migration**: Seamlessly migrate JKS, BKS and PKCS12 to each other.
- **Export PKCS12 to PEM**: Securely extract x509 certificates and private keys in PKCS8 format from PKCS12 keystores.
- **Import PEM to PKCS12**: Import the certificate and private key as new entries in the PKCS12 keystore.
- **Keystore Info Display**: Displays detailed information about the selected keystore, including certificate fingerprints, public key algorithm, expiries and more. If you want a detailed analysis of your keystores we recommend our other tool SigTool. [Check out SigTool...](https://github.com/muhammadrizwan87/sigtool)
- **APK Signing**: sign APK files with custom keystores, supporting multiple signing formats (v1, v2, v3).

---

## Why Use KeySigner?

- **User-Friendly CLI**: Interactive, step-by-step CLI to manage keystores and APK signing easily.
- **Time-Saving**: Automates repetitive tasks related to keystore management and signing.
- **Flexible**: Supports various keystore formats and all APK signing versions.
- **Secure**: Ensures that certificates and APKs are handled safely and professionally.
- **Automated Commands**: Automatically generates KeyTool and ApkSigner commands for easy use.

---

## Requirements

Before using KeySigner, ensure that the following system dependencies are installed:

1. **Python**: Required to run the KeySigner tool.
2. **Java**: Required for KeyTool and ApkSigner.
3. **KeyTool**: Part of the JDK, used for keystore management.
4. **ApkSigner**: Available through sdkmanager, used for signing APKs.
5. **OpenSSL**: Required for handling certificates and private keys.

---

## Installation

### Termux (Android)

To install KeySigner on Termux, use the following command to install all necessary dependencies:

```bash
pkg install python openjdk-17 apksigner openssl-tool
```

### Installation via pip (Recommended)

You can easily install KeySigner using pip:

```bash
pip install --force-reinstall keysigner
```

For the latest changes and features, install KeySigner directly from the GitHub repository:

```bash
pip install --force-reinstall -U git+https://github.com/muhammadrizwan87/keysigner.git
```

### Custom Build Installation

To build KeySigner from source:

1. Clone the repository:

    ```bash
    git clone https://github.com/muhammadrizwan87/keysigner.git
    ```

2. Navigate to the KeySigner directory:

    ```bash
    cd keysigner
    ```

3. Install the build tools:

    ```bash
    pip install build
    ```

4. Build and install the package:

    ```bash
    python -m build
    pip install --force-reinstall dist/keysigner-4.0-py3-none-any.whl
    ```

---

## Usage

To start using KeySigner, simply run the tool using the `keysigner` command and follow the interactive instructions.

Example:

```bash
$ keysigner

Select an option:
1. Generate new keystore (JKS/BKS/PKCS12)
2. Migrate keystores to each other (JKS/BKS/PKCS12)
3. Convert PKCS12 to PEM and extract certificate and key
4. Convert PEM to PKCS12
5. Show keystore information
6. Sign APK
7. Show Notes
q. Quit
```

---

## Contributing

We welcome contributions! Feel free to submit issues or pull requests on GitHub if you encounter any bugs or have suggestions for new features.

---

## License

This project is licensed under the **MIT License**. You can view the license details in the [LICENSE](https://github.com/muhammadrizwan87/keysigner/blob/main/LICENSE) file.

---

## Author

**MuhammadRizwan**


- **Telegram Channel**: [TDOhex](https://TDOhex.t.me)
- **Second Channel**: [Android Patches](https://Android_Patches.t.me)
- **Discussion Group**: [Discussion of TDOhex](https://TDOhex_Discussion.t.me)
- **GitHub**: [MuhammadRizwan87](https://github.com/MuhammadRizwan87)