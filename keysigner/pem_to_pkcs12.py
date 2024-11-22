# -*- coding: utf-8 -*-

import os
import subprocess
from .utils import *

class PEMToPKCS12:
    def __init__(self):
        self.cert_path = None
        self.key_path = None
        self.pem_key_path = None
        self.store_name = None
        self.alias = None
        self.store_pass = None
        self.output_path = None
        self.keystore_path = None

    def get_conversion_input(self):
        print_blue("\n--- Gathering PEM to PKCS12 Conversion Input ---")
        self.cert_path = validate_input(cyan_text("Enter x509 certificate path: "), path=True)
        self.key_path = validate_input(cyan_text("Enter private key path (PKCS8 format - .pk8): "), path=True)
        self.store_name = validate_input(cyan_text("Enter new keystore name: "))
        self.alias = validate_input(cyan_text("Enter alias for the key: "))
        self.store_pass = validate_input(cyan_text("Enter keystore password: "), password=True, min_length=8)
        self.output_path = validate_input(cyan_text(f"Enter output path (default: {os.path.abspath('keystore')}): "), required=False)

        if not self.output_path or not os.path.exists(self.output_path):
            self.output_path = ensure_directory(self.output_path)
        else:
            self.output_path = ensure_directory(self.output_path, dir_name=os.path.basename(self.output_path))

        self.keystore_path = os.path.join(self.output_path, f"{self.store_name}.p12")
        base_filename = os.path.splitext(os.path.basename(self.key_path))[0]
        self.pem_key_path = os.path.join(self.output_path, f"{base_filename}_key.pem")
        print_green("Conversion input successfully gathered!")

    def convert_pk8_to_pem(self):
        try:
            self.get_conversion_input()
            print_blue("\n--- Converting PKCS8 (PK8) Key to PEM Format ---")
            pk8_to_pem_cmd = [
                "openssl", "pkcs8",
                "-inform", "DER",
                "-outform", "PEM",
                "-nocrypt",
                "-in", self.key_path,
                "-out", self.pem_key_path
            ]

            result = subprocess.run(pk8_to_pem_cmd)
            if result.returncode != 0:
                print_red("Private key conversion to PEM format failed.")
                exit()

            print_green("Private key successfully converted to PEM format!")
            print_green(f"Private key exported to: {self.pem_key_path}")
            self.handle_and_generate_command([pk8_to_pem_cmd], "OpenSSL Command for PK8 to PEM Conversion")
        except Exception as e:
            print_red(f"Error occurred: {e}")
            exit()

    def convert_pem_to_p12(self):
        try:
            self.convert_pk8_to_pem()

            print_blue("\n--- Converting PEM Certificate and Key to PKCS12 Keystore ---")
            self.p12_cmd = [
                "openssl", "pkcs12",
                "-export",
                "-in", self.cert_path,
                "-inkey", self.pem_key_path,
                "-name", self.alias,
                "-out", self.keystore_path,
                "-password", f"pass:{self.store_pass}"
            ]

            self.execute_command()
            self.generate_apksigner_command()
        except Exception as e:
            print_red(f"Error occurred: {e}")
            exit()

    def execute_command(self):
        try:
            result = subprocess.run(self.p12_cmd)
            if result.returncode != 0:
                print_red("PKCS12 conversion failed.")
                return

            print_green("OpenSSL command executed successfully!")
            if os.path.exists(self.keystore_path):
                print_green(f"Keystore PKCS12 exported to: {self.keystore_path}")
                self.handle_and_generate_command([self.p12_cmd], "OpenSSL Command for PEM to PKCS12 Conversion")
            else:
                print_red("Error: Keystore file missing after conversion.")
        except Exception as e:
            print_red(f"Error occurred: {e}")
            exit()

    def generate_apksigner_command(self):
        try:
            print_blue("\n--- Generating APKSigner Command ---")
            self.apksigner_cmd = [
                "apksigner", "sign",
                "--ks", self.keystore_path,
                "--ks-pass", f"pass:{self.store_pass}",
                "--ks-key-alias", self.alias,
                "--key-pass", f"pass:{self.store_pass}",
                "--v1-signing-enabled", "true",
                "--v2-signing-enabled", "true",
                "--v3-signing-enabled", "true",
                "--v4-signing-enabled", "false",
                "--out", "signed.apk", "unsigned.apk"
            ]

            print_green("APKSigner command generated successfully!")
            self.handle_and_generate_command([self.apksigner_cmd], "APKSigner Command")
        except Exception as e:
            print_red(f"Error occurred: {e}")
            exit()

    def handle_and_generate_command(self, cmd_list, description):
        print_blue(f"\n--- {description} ---")
        if any(isinstance(i, list) for i in cmd_list):
            cmd_list = [item for sublist in cmd_list for item in sublist]

        def format_cmd(cmd):
            full_cmd = []
            for c in cmd:
                if ' ' in c:
                    full_cmd.append(f'"{c}"')
                else:
                    full_cmd.append(c)
            return " ".join(full_cmd)

        commands = []

        if "PK8 to PEM" in description:
            commands.append("OpenSSL command to convert PKCS8 (PK8) Key to PEM:")
            commands.append(format_cmd(cmd_list))
        elif "PEM to PKCS12" in description:
            commands.append("OpenSSL command to convert PEM to PKCS12:")
            commands.append(format_cmd(self.p12_cmd))
        elif "APKSigner" in description:
            commands.append("APKSigner command to sign APK:")
            commands.append(format_cmd(self.apksigner_cmd))
        else:
            commands.append(f"{description}:")
            commands.append(format_cmd(cmd_list))

        full_command_output = "\n".join(commands)

        cmd_file = os.path.abspath(os.path.join(self.output_path, f"{self.store_name}_PKCS12_commands.txt"))
        with open(cmd_file, 'a') as f:
            f.write(f"{full_command_output}\n\n")
        print_green(f"{description} exported to {cmd_file}")