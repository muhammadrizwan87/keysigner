#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import readline
from .keystore_manager import KeystoreManager
from .keystore_migrator import KeystoreMigrator
from .pkcs12_converter import PKCS12Converter
from .keystore_info import KeystoreInfo
from .signer import APKSigner
from .utils import *

def show_notes():
    print(color_text("1. If you want to add multiple entries to the existing keystore, just keep the 'keystore name', 'keystore password', and 'output path' the same, and tweak the other details for each new entry.", 36))
    print(color_text("\n2. During migration from JKS or BKS to PKCS12, there are opportunity to adjust the source information. So, feel free to change the 'keystore password' and 'alias name'. Don’t worry, your certificate and key will stay unchanged. You can check integrity of your certificate using option seven.", 36))
    print(color_text("\n3. PKCS12 format doesn’t deal with different passwords for the keystore and aliases. So, the alias password will automatically be set to the keystore password.", 36))
    print(color_text("\n4. Before you convert from PKCS12 to PEM, remember that 'x509.pem' and '.pk8' files will only come from the first entry. If you’ve got more entries, you’ll need to handle those one by one.", 36))
    print(color_text("\n5. Each time you create a keystore, make sure to generate its '.x509.pem' and '.pk8' files too. This way, you don’t have to keep re-entering passwords and names when you’re signing your APK.", 36))
    print(color_text("\n6. Direct signing of an APK file using apksigner with a BKS-type keystore is not supported. Therefore, it is necessary to first migrate from BKS to PKCS12 or convert from BKS to PEM.", 36))
    print(color_text("\n7. If you sign your APK using apksigner and make further changes to the APK, the APK's signature is invalidated. If you use zipalign to align your APK, use it before signing the APK.", 36))
    print(color_text("\n8. Backup all generated keystores and their details. Losing them could result in significant damage.", 36))
    print(color_text("\n9. Do not trust untrusted sources or servers for saving such confidential information.", 36))
    print(color_text("\n10. If you want to perform a detailed analysis of your keystore to check integrity, we recommend using our other tool, Sigtool. This tool provides a deeper analysis of signatures. Currently, version 1.0 analyzes information from APK files, while the upcoming update, version 2.0, will expand its capabilities to include direct certificate analysis. You can find Sigtool here:", 36))
    print("https://github.com/muhammadrizwan87/sigtool")
    print(color_text("\n11. Documentations:", 36))
    print(color_text("Keystore:", 36))
    print("https://docs.oracle.com/en/java/javase/21/docs/specs/man/keytool.html")
    print(color_text("Apksigner:", 36))
    print("https://developer.android.com/tools/apksigner")

def main():
    logo_ascii_art()
    meta_data()
    while True:
        print_magenta("\nSelect an option:")
        print_yellow("1. Create new JKS keystore")
        print_yellow("2. Create new BKS keystore")
        print_yellow("3. Create new PKCS12 keystore")
        print_yellow("4. Migrate JKS to PKCS12")
        print_yellow("5. Migrate BKS to PKCS12")
        print_yellow("6. Convert PKCS12 to PEM and extract x509 certificate and private key")
        print_yellow("7. Show keystore information")
        print_yellow("8. Sign APK")
        print_yellow("9. Show Notes")
        print_blue("q. Quit")

        choice = input(cyan_text("\nEnter choice (1-9 or q to quit): ")).lower()

        if choice == '1':
            print_blue("\nCreating new JKS keystore...")
            keystore_manager = KeystoreManager('JKS')
            keystore_manager.create_keystore()
        elif choice == '2':
            print_blue("\nCreating new BKS keystore...")
            keystore_manager = KeystoreManager('BKS')
            keystore_manager.create_keystore()
        elif choice == '3':
            print_blue("\nCreating new PKCS12 keystore...")
            keystore_manager = KeystoreManager('PKCS12')
            keystore_manager.create_keystore()
        elif choice == '4':
            print_blue("\nMigrating JKS to PKCS12...")
            migrator = KeystoreMigrator('JKS')
            migrator.migrate_keystore()
        elif choice == '5':
            print_blue("\nMigrating BKS to PKCS12...")
            migrator = KeystoreMigrator('BKS')
            migrator.migrate_keystore()
        elif choice == '6':
            print_blue("\nConverting PKCS12 to PEM and extracting x509 and private key...")
            converter = PKCS12Converter()
            converter.convert_p12_to_pem()
        elif choice == '7':
            print_blue("\nShowing keystore information...")
            keystore_info = KeystoreInfo()
            keystore_info.show_keystore_info()
        elif choice == '8':
            print_blue("\nSigning APK...")
            signer = APKSigner()
            signer.sign_with_keystores()
        elif choice == '9':
            print_blue("\nShowing Notes...")
            show_notes()
        elif choice in ['q', 'x']:
            print_blue("\nExiting keySigner. Goodbye!")
            break
        else:
            print_red("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()