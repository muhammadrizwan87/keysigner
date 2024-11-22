#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import readline
from .keystore_generator import KeystoreGenerator
from .keystore_migrator import KeystoreMigrator
from .pkcs12_to_pem import PKCS12ToPEM
from .pem_to_pkcs12 import PEMToPKCS12
from .keystore_info import KeystoreInfo
from .apk_signer import APKSigner
from .utils import *

def show_notes():
    print(color_text("1. '.keystore' is just an extension name that is actually another form of the '.jks' extension. So, if you have a '.keystore' extension, you should consider it as '.jks'.", 36))
    print(color_text("\n2. Our suggestion is that if you need to generate a new keystore, generate it in PKCS12. Or, if you have already generated a JKS, migrate it to PKCS12. This is because PKCS12 is modern, secure, and widely compatible. We do not recommend migrating from PKCS12 to JKS at all. This option is provided because some third-party tools do not consider users' independence and force them to use a specific keystore.", 36))
    print(color_text("\n3. If you want to add multiple entries to the existing keystore, just keep the 'keystore name', 'keystore password', and 'output path' the same, and tweak the other details for each new entry.", 36))
    print(color_text("\n4. During migration from keystores to each other, there are opportunity to adjust the source information. So, feel free to change the 'keystore password' and 'alias name'. Don’t worry, your certificate and key will stay unchanged. You can check integrity of your certificate using option five.", 36))
    print(color_text("\n5. PKCS12 format doesn’t deal with different passwords for the keystore and aliases. So, the alias password will automatically be set to the keystore password.", 36))
    print(color_text("\n6. The default workflow of keytool is to access the first entry of the source keystore and match the alias key password with the keystore password.", 36))
    print(color_text("\n7. Before you convert from PKCS12 to PEM, remember that 'x509.pem' and '.pk8' files will only come from the first entry. If you’ve got more entries, you’ll need to handle those one by one.", 36))
    print(color_text("\n8. Each time you create a keystore, make sure to generate its '.x509.pem' and '.pk8' files too. This way, you don’t have to keep re-entering passwords and names when you’re signing your APK.", 36))
    print(color_text("\n9. Direct signing of an APK file using apksigner with a BKS-type keystore is not supported. Therefore, it is necessary to first migrate from BKS to other keystores.", 36))
    print(color_text("\n10. If you sign your APK using apksigner and make further changes to the APK, the APK's signature is invalidated. If you use zipalign to align your APK, use it before signing the APK.", 36))
    print(color_text("\n11. Backup all generated keystores and their details. Losing them could result in significant damage.", 36))
    print(color_text("\n12. Do not trust untrusted sources or servers for saving such confidential information.", 36))
    print(color_text("\n13. If you want to add your keystore verification to your project, you should check out our other tool, SigTool. SigTool will generate all the details of your keystore for you, such as SHA-1, SHA-224, SHA-256, SHA-356, SHA-512, MD5, CRC32, Java-style HashCode, and their base64 encoded results. It will also generate the smali byte array format of your keystore. You can find Sigtool here:", 36))
    print("https://github.com/muhammadrizwan87/sigtool")
    print(color_text("\n14. Documentations:", 36))
    print(color_text("Keystore:", 36))
    print("https://docs.oracle.com/en/java/javase/21/docs/specs/man/keytool.html")
    print(color_text("Apksigner:", 36))
    print("https://developer.android.com/tools/apksigner")

def main():
    logo_ascii_art()
    meta_data()
    while True:
        print_magenta("\nSelect an option:")
        print_yellow("1. Generate new keystore (JKS/BKS/PKCS12)")
        print_yellow("2. Migrate keystores to each other (JKS/BKS/PKCS12)")
        print_yellow("3. Convert PKCS12 to PEM and extract certificate and key")
        print_yellow("4. Convert PEM to PKCS12")
        print_yellow("5. Show keystore information")
        print_yellow("6. Sign APK")
        print_yellow("7. Show Notes")
        print_blue("q. Quit")

        choice = input(cyan_text("\nEnter choice (1-7 or q to quit): ")).lower()

        if choice == '1':
            print_blue("\nGenerating new keystore (JKS/BKS/PKCS12)...")
            generator = KeystoreGenerator()
            generator.generate_keystore()
        elif choice == '2':
            print_blue("\nMigrating keystores (JKS/BKS/PKCS12)...")
            migrator = KeystoreMigrator()
            migrator.migrate_keystore()
        elif choice == '3':
            print_blue("\nConverting PKCS12 to PEM and extracting x509 and private key...")
            converter = PKCS12ToPEM()
            converter.convert_p12_to_pem()
        elif choice == '4':
            print_blue("\nConverting PEN to PKCS12...")
            converter = PEMToPKCS12()
            converter.convert_pem_to_p12()
        elif choice == '5':
            print_blue("\nShowing keystore information...")
            keystore_info = KeystoreInfo()
            keystore_info.show_keystore_info()
        elif choice == '6':
            print_blue("\nSigning APK...")
            signer = APKSigner()
            signer.sign_with_keystores()
        elif choice == '7':
            print_blue("\nShowing Notes...")
            show_notes()
        elif choice in ['q', 'x']:
            print_blue("\nExiting keySigner. Goodbye!")
            break
        else:
            print_red("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()