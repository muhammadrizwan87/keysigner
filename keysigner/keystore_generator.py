# -*- coding: utf-8 -*-

import os
import subprocess
from .utils import *

class KeystoreGenerator:
    def __init__(self):
        self.store_type = None
        self.store_name = None
        self.store_pass = None
        self.alias = None
        self.key_pass = None
        self.validity = '36500'
        self.dname = None
        self.output_path = None
        self.store_path = None
        self.provider_class = None
        self.provider_path = None

    def set_keystore_details(self):
        print_blue("\n--- Setting Keystore Details ---")
        while True:
            keystore_type = validate_input(cyan_text("Enter new keystore type (JKS/BKS/PKCS12): ")).upper()
            if keystore_type in ['JKS', 'BKS', 'PKCS12']:
                self.store_type = keystore_type
                break
            else:
                print_red("Invalid keystore type. Please try again.")
        self.store_name = validate_input(cyan_text("Enter keystore name: "))
        self.store_pass = validate_input(cyan_text("Enter keystore password: "), password=True, min_length=8)
        self.alias = validate_input(cyan_text("Enter alias name: "))
        if self.store_type == 'PKCS12':
            self.key_pass = self.store_pass
        else:
            self.key_pass = validate_input(cyan_text("Enter alias password (default: same as keystore password): "), pass_opt=self.store_pass, min_length=8)
        self.validity = validate_input(cyan_text("Enter validity (days, default 36500): "), required=False) or '36500'
        self.dname = self.generate_dname()
        if self.store_type == 'BKS':
            self.provider_class = 'org.bouncycastle.jce.provider.BouncyCastleProvider'
            root_dir = os.path.dirname(__file__)
            self.provider_path = os.path.join(root_dir, 'lib', 'bcprov-jdk18on-1.78.jar')
        print_green("Keystore details successfully set!")
        
        self.output_path = validate_input(cyan_text(f"\nEnter output path (default: {os.path.abspath('keystore')}): "), required=False)
        if not self.output_path or not os.path.exists(self.output_path):
            self.output_path = ensure_directory(self.output_path)
        else:
            self.output_path = ensure_directory(self.output_path, dir_name=os.path.basename(self.output_path))
        
        if self.store_type == 'PKCS12':
            self.store_path = os.path.join(self.output_path, f"{self.store_name}.p12")
        else:
            self.store_path = os.path.join(self.output_path, f"{self.store_name}.{self.store_type.lower()}")

    def generate_dname(self):
        print_blue("\n--- Generating Distinguished Name (Press enter to skip) ---")
        cn = validate_input(cyan_text("Enter CN (Common Name): "), required=False)
        ou = validate_input(cyan_text("Enter OU (Organizational Unit): "), required=False)
        o = validate_input(cyan_text("Enter O (Organization): "), required=False)
        l = validate_input(cyan_text("Enter L (Locality): "), required=False)
        st = validate_input(cyan_text("Enter ST (State): "), required=False)
        c = validate_input(cyan_text("Enter C (Country Code): "), required=False)
    
        if not any([cn, ou, o, l, st, c]):
            return "CN=Unknown"
        
        dname_parts = []
        if cn: dname_parts.append(f"CN={cn}")
        if ou: dname_parts.append(f"OU={ou}")
        if o: dname_parts.append(f"O={o}")
        if l: dname_parts.append(f"L={l}")
        if st: dname_parts.append(f"ST={st}")
        if c: dname_parts.append(f"C={c}")
        
        return ", ".join(dname_parts)

    def generate_keytool_command(self):
        cmd = [
            'keytool', '-genkeypair',
            '-keyalg', 'RSA',
            '-keysize', '2048',
            '-storetype', self.store_type,
            '-keystore', self.store_path,
            '-storepass', self.store_pass,
            '-validity', self.validity,
            '-dname', self.dname,
            '-alias', self.alias,
        ]
        if self.store_type == 'PKCS12':
            cmd.extend(['-keypass', self.store_pass,])
        else:
            cmd.extend(['-keypass', self.key_pass,])
        
        if self.provider_class and self.provider_path:
            cmd.extend(['-providerclass', self.provider_class, '-providerpath', self.provider_path])
        return cmd

    def generate_keystore(self):
        try:
            self.set_keystore_details()
            self.cmd = self.generate_keytool_command()
            print_blue("\n--- Executing KeyTool Command ---")
            result = subprocess.run(self.cmd)
            
            if result.returncode != 0:
                print_red("Keystore generation failed.")
                return
            
            print_green("KeyTool command executed successfully!")
            print_green(f"Keystore {self.store_type} generated at: {self.store_path}")
            self.handle_and_generate_command(self.cmd, f"Keystore command to generate new {self.store_type}")
            
            if self.store_type != 'BKS':
                self.generate_apksigner_command(self.store_path, self.store_pass, self.alias, self.key_pass)
        except Exception as e:
            print_red(f"Error occurred: {e}")
            exit()

    def handle_and_generate_command(self, cmd_list, description):
        print_blue(f"\n--- {description} ---")
        full_command = []
        for cmd in cmd_list:
            if ' ' in cmd:
                full_command.append(f'"{cmd}"')
            else:
                full_command.append(cmd)
        full_command = " ".join(full_command)
        
        cmd_file = os.path.abspath(os.path.join(self.output_path, f"{self.store_name}_{self.store_type}_commands.txt"))
        with open(cmd_file, 'a') as f:
            f.write(f"{description}:\n")
            f.write(full_command)
            f.write("\n\n")
        print_green(f"{description} exported to {cmd_file}")

    def generate_apksigner_command(self, keystore_path, store_pass, alias, key_pass):
        cmd = [
            "apksigner", "sign",
            "--ks", keystore_path,
            "--ks-pass", f"pass:{store_pass}",
            "--ks-key-alias", alias,
            "--key-pass", f"pass:{key_pass}",
            "--v1-signing-enabled", "true",
            "--v2-signing-enabled", "true",
            "--v3-signing-enabled", "true",
            "--v4-signing-enabled", "false",
            "--out", "signed.apk", "unsigned.apk"
        ]
    
        self.handle_and_generate_command(cmd, "APK Signer Command")