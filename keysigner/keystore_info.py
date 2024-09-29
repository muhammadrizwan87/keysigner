# -*- coding: utf-8 -*-

import os
import subprocess
from .utils import *

class KeystoreInfo:
    def __init__(self):
        self.keystore_path = None
        self.store_pass = None
        self.keystore_type = None

    def get_keystore_info(self):
        print_blue("\n--- Gathering Keystore Information ---")
        self.keystore_path = validate_input(cyan_text("Enter keystore path: "), path=True)
        self.store_pass = validate_input(cyan_text("Enter keystore password: "), password=True)
        self.determine_keystore_type()

    def determine_keystore_type(self):
        file_extension = os.path.splitext(self.keystore_path)[1].lower()
        if file_extension == '.jks':
            self.keystore_type = 'JKS'
        elif file_extension == '.bks':
            self.keystore_type = 'BKS'
        elif file_extension == '.p12':
            self.keystore_type = 'PKCS12'
        else:
            while True:
                keystore_type = validate_input(cyan_text("Keystore type not detected. Please enter keystore type (JKS/BKS/PKCS12): ")).upper()
                if keystore_type in ['JKS', 'BKS', 'PKCS12']:
                    self.keystore_type = keystore_type
                    break
                else:
                    print_red("Invalid keystore type. Please try again.")

    def show_keystore_info(self):
        try:
            self.get_keystore_info()
            if not self.keystore_path or not self.store_pass or not self.keystore_type:
                print_red("Keystore information is incomplete.")
                return
            cmd = [
                'keytool', '-list', '-v',
                '-keystore', self.keystore_path,
                '-storetype', self.keystore_type,
                '-storepass', self.store_pass
            ]
            if self.keystore_type == 'BKS':
                root_dir = os.path.dirname(__file__)
                provider_path = os.path.join(root_dir, 'lib', 'bcprov-jdk18on-1.78.jar')
                cmd.extend(['-providerclass', 'org.bouncycastle.jce.provider.BouncyCastleProvider', '-providerpath', provider_path])
            
            print_blue("\n--- Executing KeyTool Command ---")
            result = subprocess.run(cmd)
            
            if result.returncode != 0:
                print_red("Failed to show keystore information.")
                return
            
            print_green("KeyTool command executed successfully!")
        except Exception as e:
            print_red(f"Error occurred: {e}")
            exit()