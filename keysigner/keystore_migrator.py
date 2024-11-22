# -*- coding: utf-8 -*-

import os
import subprocess
from .utils import *

class KeystoreMigrator:
    def __init__(self):
        self.src_path = None
        self.src_store_type = None
        self.src_store_pass = None
        self.src_alias = None
        self.src_key_pass = None
        self.dest_store_name = None
        self.dest_store_type = None
        self.dest_store_pass = None
        self.dest_alias = None
        self.dest_key_pass = None
        self.output_path = None
        self.dest_path = None
        self.provider_class = None
        self.provider_path = None

    def get_migration_input(self):
        print_blue("\n--- JKS/BKS/PKCS12 Keystore Migration ---")
        self.src_path = validate_input(cyan_text("Enter source keystore path: "), path=True)
        
        file_extension = os.path.splitext(self.src_path)[1].lower()
        if file_extension == '.jks':
            self.src_store_type = 'JKS'
        elif file_extension == '.bks':
            self.src_store_type = 'BKS'
        elif file_extension == '.p12':
            self.src_store_type = 'PKCS12'
        else:
            while True:
                keystore_type = validate_input(cyan_text("Enter source keystore type (JKS/BKS/PKCS12): ")).upper()
                if keystore_type in ['JKS', 'BKS', 'PKCS12']:
                    self.src_store_type = keystore_type
                    break
                else:
                    print_red("Invalid source keystore type. Please try again.")
                    
        self.src_store_pass = validate_input(cyan_text("Enter source keystore password: "), password=True, min_length=6)
        self.src_alias = validate_input(cyan_text("Enter source alias name: "))
        
        if self.src_store_type != 'PKCS12':
            self.src_key_pass = validate_input(cyan_text("Enter source alias password (default: same as source keystore password): "), pass_opt=self.src_store_pass, min_length=6)
        else:
            self.src_key_pass = self.src_store_pass
        
        self.dest_store_name = os.path.splitext(os.path.basename(self.src_path))[0]
        
        valid_dest_types = {'JKS', 'BKS', 'PKCS12'} - {self.src_store_type.upper()}
        while True:
            keystore_type = validate_input(cyan_text(f"Enter destination keystore type ({'/'.join(valid_dest_types)}): "), required=True).upper()
            if keystore_type in valid_dest_types:
                self.dest_store_type = keystore_type
                break
            else:
                print_red("Invalid destination keystore type. Please try again.")
        
        self.dest_store_pass = validate_input(cyan_text("Enter destination keystore password (default: same as source keystore password): "), pass_opt=self.src_store_pass, min_length=6)
        self.dest_alias = validate_input(cyan_text("Enter destination alias name (default: same as source alias name): "), required=False) or self.src_alias
        
        if self.dest_store_type != 'PKCS12':
            self.dest_key_pass = validate_input(cyan_text("Enter destination alias password (default: same as source alias password): "), pass_opt=self.src_key_pass, min_length=6)
        else:
            self.dest_key_pass = self.dest_store_pass
            
        self.output_path = validate_input(cyan_text(f"Enter output path (default: {os.path.abspath('keystore')}): "), required=False)
        if not self.output_path or not os.path.exists(self.output_path):
            self.output_path = ensure_directory(self.output_path)
        else:
            self.output_path = ensure_directory(self.output_path, dir_name=os.path.basename(self.output_path))

        store_type = 'p12' if self.dest_store_type.lower() == 'pkcs12' else self.dest_store_type.lower()
        self.dest_path = os.path.join(self.output_path, f"{os.path.splitext(os.path.basename(self.src_path))[0]}.{store_type}")
        
        if self.src_store_type == 'BKS' or self.dest_store_type == "BKS":
            self.provider_class = "org.bouncycastle.jce.provider.BouncyCastleProvider"
            root_dir = os.path.dirname(__file__)
            self.provider_path = os.path.join(root_dir, 'lib', 'bcprov-jdk18on-1.78.jar')

        print_green("Migration input successfully gathered!")

    def generate_migration_command(self):
        cmd = [
            'keytool', '-importkeystore',
            '-srckeystore', self.src_path,
            '-srcstoretype', self.src_store_type,
            '-srcstorepass', self.src_store_pass,
            '-srcalias', self.src_alias,
            '-srckeypass', self.src_key_pass,
            '-destkeystore', self.dest_path,
            '-deststoretype', self.dest_store_type,
            '-deststorepass', self.dest_store_pass,
            '-destalias', self.dest_alias,
            '-destkeypass', self.dest_key_pass
        ]

        if self.src_store_type == 'BKS' or self.dest_store_type == 'BKS':
            cmd.extend(['-providerclass', self.provider_class, '-providerpath', self.provider_path])

        return cmd

    def generate_apksigner_command(self):
        print_blue("\n--- Generating APK Signer Command ---")
        cmd = [
            "apksigner", "sign",
            "--ks", self.dest_path,
            "--ks-pass", f"pass:{self.dest_store_pass}",
            "--ks-key-alias", self.dest_alias,
            "--key-pass", f"pass:{self.dest_key_pass}",
            "--v1-signing-enabled", "true",
            "--v2-signing-enabled", "true",
            "--v3-signing-enabled", "true",
            "--v4-signing-enabled", "false",
            "--out", "signed.apk", "unsigned.apk"
        ]

        self.handle_and_generate_command(cmd, "APK Signer Command")

    def migrate_keystore(self):
        try:
            self.get_migration_input()
            self.cmd = self.generate_migration_command()
            print_blue("\n--- Executing Keystore Migration Command ---")
            result = subprocess.run(self.cmd)

            if result.returncode != 0:
                print_red("Keystore migration failed.")
                return

            print_green("Keystore migration executed successfully!")
            print_green(f"{self.src_store_type} migrated to {self.dest_store_type} at: {self.dest_path}")
            self.handle_and_generate_command(self.cmd, f"{self.src_store_type} to {self.dest_store_type} Keystore Migration Command")
            if self.dest_store_type != 'BKS':
                self.generate_apksigner_command()
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

        cmd_file = os.path.abspath(os.path.join(self.output_path, f"{self.dest_store_name}_{self.dest_store_type}_commands.txt"))
        with open(cmd_file, 'a') as f:
            f.write(f"{description}:\n")
            f.write(full_command)
            f.write("\n\n")
        print_green(f"{description} exported to {cmd_file}")