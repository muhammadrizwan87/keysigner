# -*- coding: utf-8 -*-

import os
import subprocess
from getpass import getpass
from .keystore_manager import KeystoreManager
from .utils import *

class KeystoreMigrator(KeystoreManager):
    def __init__(self, store_type):
        super().__init__(store_type)

    def get_migration_input(self):
        print_blue(f"\n--- Migrating {self.store_type} Keystore ---")
        self.src_path = validate_input(cyan_text(f"Enter {self.store_type} keystore path: "), path=True)
        self.src_store_pass = validate_input(cyan_text("Enter source keystore password: "), password_ck=True)
        self.src_alias = validate_input(cyan_text("Enter source alias name: "))
        self.src_key_pass = validate_input(cyan_text("Enter source alias password: "), password_ck=True)
        self.dest_alias = validate_input(cyan_text("Enter destination alias name (default: same as source alias name): "), required=False) or self.src_alias
        self.dest_store_pass = getpass(cyan_text("Enter destination keystore password (default: same as source keystore password): ")) or self.src_store_pass
        
        if len(self.dest_store_pass) < 6:
            print_red(f"Password must be at least 6 characters long.")
            self.dest_store_pass = validate_input(cyan_text("Enter destination keystore password: "), password_ck=True)
        
        self.output_path = validate_input(cyan_text(f"Enter output path (default: {os.path.abspath('keystore')}): "), required=False)

        if not self.output_path or not os.path.exists(self.output_path):
            self.output_path = ensure_directory(self.output_path)
        else:
            self.output_path = ensure_directory(self.output_path, dir_name=os.path.basename(self.output_path))

        self.dest_path = os.path.join(self.output_path, f"{os.path.basename(self.src_path).replace(f'.{self.store_type.lower()}', '')}.p12")
        self.store_name = os.path.join(self.output_path, f"{os.path.splitext(os.path.basename(self.src_path))[0]}")

        print_green("Migration input successfully gathered!")

    def migrate_keystore(self):
        try:
            self.get_migration_input()
            
            self.cmd = [
                'keytool', '-importkeystore',
                '-srckeystore', self.src_path,
                '-srcstoretype', self.store_type,
                '-srcstorepass', self.src_store_pass,
                '-srcalias', self.src_alias,
                '-srckeypass', self.src_key_pass,
                '-destkeystore', self.dest_path,
                '-deststoretype', 'PKCS12',
                '-deststorepass', self.dest_store_pass,
                '-destalias', self.dest_alias,
                '-destkeypass', self.dest_store_pass
            ]
            
            if self.store_type == 'BKS':
                self.provider_class = 'org.bouncycastle.jce.provider.BouncyCastleProvider'
                root_dir = os.path.dirname(__file__)
                self.provider_path = os.path.join(root_dir, 'lib', 'bcprov-jdk18on-1.78.jar')
                self.cmd.extend(['-providerclass', self.provider_class, '-providerpath', self.provider_path])
    
            print_blue("\n--- Executing Keystore Command ---")
            result = subprocess.run(self.cmd)
            
            if result.returncode != 0:
                print_red("Keystore migration failed.")
                return
            
            print_green("KeyTool command executed successfully!")
            print_green(f"Keystore migrated to PKCS12 at: {self.dest_path}")
            
            self.store_type = "PKCS12"
            self.handle_and_generate_command(self.cmd, "Keystore Command")
            self.generate_apksigner_command(self.dest_path, self.dest_store_pass, self.dest_alias, self.dest_store_pass)
        except Exception as e:
            print_red(f"Error occurred: {e}")
            exit()