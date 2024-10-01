# -*- coding: utf-8 -*-

import os
import subprocess
from .utils import *

class APKSigner:
    def __init__(self):
        self.root_dir = os.path.dirname(__file__)
        self.lib_path = os.path.join(self.root_dir, 'lib')
        self.apksigner_jar = os.path.join(self.lib_path, 'apksigner.jar')
        self.v1_enabled = True
        self.v2_enabled = True
        self.v3_enabled = True
        self.v4_enabled = False
        self.output_path = None
        self.apk_file = None

    def set_signing_schemes(self):
        scheme_choice = input(cyan_text("(Scheme v1/v2/v3 Enabled!) Press enter to skip or 'y' to change: "))
        if scheme_choice == 'y':
            print_blue("\n--- Set Signing Schemes (press Enter to use default values) ---")
            self.v1_enabled = validate_input(cyan_text("Enable V1 signing? (default: True): "), required=False) or True
            self.v2_enabled = validate_input(cyan_text("Enable V2 signing? (default: True): "), required=False) or True
            self.v3_enabled = validate_input(cyan_text("Enable V3 signing? (default: True): "), required=False) or True
            self.v4_enabled = validate_input(cyan_text("Enable V4 signing? (default: False): "), required=False) or False

    def sign_with_test_key(self):
        print_blue("\n--- Signing APK with Test Key ---")
        cert = os.path.join(self.lib_path, 'testkey.x509.pem')
        key = os.path.join(self.lib_path, 'testkey.pk8')
        base_name = os.path.splitext(os.path.basename(self.apk_file))[0]
        signed_apk = os.path.join(self.output_path, f"{base_name}_signed.apk")
        self.run_apksigner(signed_apk, cert, key)

    def sign_with_keystores(self):
        try:
            self.apk_file = validate_input(cyan_text("Enter the APK file to sign: "), path=True)
            
            self.output_path = validate_input(cyan_text(f"Enter output path (default: {os.path.abspath('signed_apks')}): "), required=False)
            if not self.output_path or not os.path.exists(self.output_path):
                self.output_path = ensure_directory(self.output_path, caller='signer')
            
            self.set_signing_schemes()
            
            valid_options = ['jks', 'p12', 'pem', 'test']
    
            while True:
                store_type = validate_input(cyan_text("Enter keystore type (jks/p12/pem/test): ")).lower()
    
                if store_type in valid_options:
                    break
                else:
                    print_red(f"Invalid keystore type '{store_type}'. Please enter one of the following: jks, p12, pem, test.")
    
            print_blue("\n--- Signing APK with Keystore ---")
            
            if store_type == 'jks':
                self.sign_with_jks()
            elif store_type == 'p12':
                self.sign_with_p12()
            elif store_type == 'pem':
                self.sign_with_pem()
            elif store_type == 'test':
                self.sign_with_test_key()
        except Exception as e:
            print_red(f"Error occurred: {e}")
            exit()

    def sign_with_keystore(self, keystore_type):
        keystore_path = validate_input(cyan_text(f"Enter {keystore_type.upper()} keystore path: "), path=True)
        store_pass = validate_input(cyan_text("Enter keystore password: "), password_ck=True)
        alias = validate_input(cyan_text("Enter alias name: "))
        base_name = os.path.splitext(os.path.basename(self.apk_file))[0]
        signed_apk = os.path.join(self.output_path, f"{base_name}_signed.apk")
    
        cmd = [
            'apksigner', 'sign',
            '--ks', keystore_path,
            '--ks-pass', f'pass:{store_pass}',
            '--ks-key-alias', alias,
            f'--v1-signing-enabled={str(self.v1_enabled).lower()}',
            f'--v2-signing-enabled={str(self.v2_enabled).lower()}',
            f'--v3-signing-enabled={str(self.v3_enabled).lower()}',
            f'--v4-signing-enabled={str(self.v4_enabled).lower()}',
            '--out', signed_apk
        ]
    
        if keystore_type.lower() == 'jks':
            key_pass = validate_input(cyan_text("Enter alias password: "), password_ck=True)
            cmd.extend(['--key-pass', f'pass:{key_pass}'])
    
        cmd.extend([self.apk_file])
        self.run_command(cmd, signed_apk)
    
    def sign_with_jks(self):
        self.sign_with_keystore('jks')
    
    def sign_with_p12(self):
        self.sign_with_keystore('p12')
        
    def sign_with_pem(self):
        x509_path = validate_input(cyan_text("Enter x509 certificate path: "), path=True)
        key_path = validate_input(cyan_text("Enter private key path: "), path=True)
        base_name = os.path.splitext(os.path.basename(self.apk_file))[0]
        signed_apk = os.path.join(self.output_path, f"{base_name}_signed.apk")
        self.run_apksigner(signed_apk, x509_path, key_path)

    def run_apksigner(self, signed_apk, cert, key):
        cmd = [
            'apksigner', 'sign',
            f'--v1-signing-enabled={str(self.v1_enabled).lower()}',
            f'--v2-signing-enabled={str(self.v2_enabled).lower()}',
            f'--v3-signing-enabled={str(self.v3_enabled).lower()}',
            f'--v4-signing-enabled={str(self.v4_enabled).lower()}',
            '--cert', cert,
            '--key', key,
            '--out', signed_apk, self.apk_file
        ]
        self.run_command(cmd, signed_apk)

    def run_command(self, cmd, signed_apk):
        try:
            result = subprocess.run(cmd)
            if result.returncode != 0:
                print_red("Command execution failed.")
                return
            print_green(f"APK successfully signed at {signed_apk}")
        except Exception as e:
            print_red(f"Error occurred: {e}")
            exit()
