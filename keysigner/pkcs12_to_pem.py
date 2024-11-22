# -*- coding: utf-8 -*-

import os
import subprocess
from .utils import *

class PKCS12ToPEM:
    def __init__(self):
        self.p12_path = None
        self.store_pass = None
        self.output_path = None

    def get_conversion_input(self):
        print_blue("\n--- Gathering PKCS12 Conversion Input ---")
        self.p12_path = validate_input(cyan_text("Enter PKCS12 keystore path: "), path=True)
        self.store_pass = validate_input(cyan_text("Enter keystore password: "), password=True, min_length=6)
        self.output_path = validate_input(cyan_text(f"Enter output path (default: {os.path.abspath('keystore')}): "), required=False)

        if not self.output_path or not os.path.exists(self.output_path):
            self.output_path = ensure_directory(self.output_path)
        else:
            self.output_path = ensure_directory(self.output_path, dir_name=os.path.basename(self.output_path))

        print_green("Conversion input successfully gathered!")

    def convert_p12_to_pem(self):
        try:
            self.get_conversion_input()
            self.pem_path = os.path.join(self.output_path, os.path.basename(self.p12_path).replace(".p12", ".pem"))
            self.x509_path = os.path.join(self.output_path, os.path.basename(self.p12_path).replace(".p12", ".x509.pem"))
            self.key_path = os.path.join(self.output_path, os.path.basename(self.p12_path).replace(".p12", ".pk8"))
    
            self.pem_cmd = ['openssl', 'pkcs12', '-in', self.p12_path, '-out', self.pem_path, '-nodes', '-password', f'pass:{self.store_pass}']
            self.x509_cmd = ['openssl', 'x509', '-in', self.pem_path, '-out', self.x509_path, '-outform', 'PEM']
            self.key_cmd = ['openssl', 'pkcs8', '-topk8', '-inform', 'PEM', '-outform', 'DER', '-in', self.pem_path, '-out', self.key_path, '-nocrypt']
    
            self.execute_commands()
        except Exception as e:
            print_red(f"Error occurred: {e}")
            exit()

    def execute_commands(self):
        try:
            print_blue("\n--- Executing Openssl Command ---")
            result = subprocess.run(self.pem_cmd)
            if result.returncode != 0:
                print_red("PEM conversion failed.")
                return
    
            result = subprocess.run(self.x509_cmd)
            if result.returncode != 0:
                print_red("x509 certificate extraction failed.")
                return
    
            result = subprocess.run(self.key_cmd)
            if result.returncode != 0:
                print_red("Private key extraction failed.")
                return
    
            print_green("Openssl command executed successfully!")
            self.store_name = os.path.join(self.output_path, f"{os.path.basename(self.x509_path).split('.x509')[0]}")
            self.store_type = "PEM"
            
            if os.path.exists(self.x509_path) and os.path.exists(self.key_path):
                print_green(f"Files exported to: {self.output_path}")
                print_green(f"{'PEM file:'} {self.pem_path}")
                print_green(f"{'x509 certificate:'} {self.x509_path}")
                print_green(f"{'Private key (PKCS8 format):'} {self.key_path}")
                self.handle_and_generate_command([self.pem_cmd, self.x509_cmd, self.key_cmd], "Openssl Commands")
    
                self.generate_apksigner_command(self.x509_path, self.key_path)
            else:
                print_red("Error: x509 or private key file missing after conversion.")
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
        
        if "Openssl" in description:
            commands.append("Openssl command to convert PKCS12 to PEM:")
            commands.append(format_cmd(self.pem_cmd))
            commands.append("\nOpenssl command to extract x509 certificate:")
            commands.append(format_cmd(self.x509_cmd))
            commands.append("\nOpenssl command to extract private key:")
            commands.append(format_cmd(self.key_cmd))
        else:
            commands.append(f"{description}:")
            commands.append(format_cmd(cmd_list))
        
        full_command_output = "\n".join(commands)
        
        cmd_file = os.path.abspath(os.path.join(self.output_path, f"{self.store_name}_{self.store_type}_commands.txt"))
        with open(cmd_file, 'a') as f:
            f.write(f"{full_command_output}\n\n")
        print_green(f"{description} exported to {cmd_file}")
    
    def generate_apksigner_command(self, cert, key):
        if not cert or not key:
            raise ValueError("Certificate and key file paths are required for APK signing.")

        cmd = [
            "apksigner", "sign",
            "--v1-signing-enabled", "true",
            "--v2-signing-enabled", "true",
            "--v3-signing-enabled", "true",
            "--v4-signing-enabled", "false",
            "--cert", cert,
            "--key", key,
            "--out", "signed.apk", "unsigned.apk"
        ]

        self.handle_and_generate_command(cmd, "APK signer Command")