# -*- coding: utf-8 -*-

import os
from getpass import getpass

def color_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def bold_text(text):
    return f"\033[1m{text}\033[0m"

def cyan_text(prompt):
    # Cyan Colour, Bold Style
    return bold_text(color_text(prompt, '36'))

def print_green(message):
    # Bright Green Colour, Bold Style
    print(bold_text(color_text(message, '92')))

def print_red(message):
    # Red Colour, Normal Style
    print(color_text(message, '31'))

def print_blue(message):
    # Bright Blue Colour, Normal Style
    print(color_text(message, '94'))
    
def print_magenta(message):
    # Bright Magenta Colour, Bold Style
    print(bold_text(color_text(message, '95')))
    
def print_yellow(message):
    # Bright Yellow Colour, Normal Style
    print(color_text(message, '93'))

def logo_ascii_art():
    logo_art = """
+---------Welcome to-----------------------------+
|    __                   _                 v4.0 |
|   / /_____  __  _______(_)___ _____  ___  _____|
|  / //_/ _ \/ / / / ___/ / __ `/ __ \/ _ \/ ___/|
| / ,< /  __/ /_/ (__  ) / /_/ / / / /  __/ /    |
|/_/|_|\___/\__, /____/_/\__, /_/ /_/\___/_/     |
|          /____/       /____/                   |
+------------------------------by MuhammadRizwan-+
    """
    return print_magenta(logo_art)

def meta_data():
    print(color_text("To generate and manage keystore using keytool.\nAnd sign APK with custom keystore using apksigner.", 96))
    print(color_text("\nVersion:", 94), color_text("4.0", 92))
    print(color_text("Author:", 94), color_text("MuhammadRizwan", 92))
    print(color_text("Repository:", 94), color_text("https://github.com/muhammadrizwan87/keysigner", 92))
    print(color_text("Telegram Channel:", 94), color_text("https://TDOhex.t.me", 92))
    print(color_text("Second Channel:", 94), color_text("https://Android_Patches.t.me", 92))
    print(color_text("Discussion Group:", 94), color_text("https://TDOhex_Discussion.t.me", 92))

def ensure_directory(user_path=None, dir_name='keystore', caller=None):
    try:
        default_directory = os.getcwd()

        if caller == 'signer':
            dir_name = 'signed_apks'

        if user_path:
            if not isinstance(user_path, str):
                raise TypeError("Invalid path type. Path must be a string.")

            if os.path.isabs(user_path):
                if not os.path.exists(user_path):
                    os.makedirs(user_path)
                return user_path

            else:
                full_path = os.path.join(default_directory, user_path)
                if not os.path.exists(full_path):
                    os.makedirs(full_path)
                return full_path

        else:
            final_path = os.path.join(default_directory, dir_name)
            if not os.path.exists(final_path):
                os.makedirs(final_path)
            return final_path

    except FileNotFoundError as fnf_error:
        print_red(f"Directory or file not found: {fnf_error}")
        raise FileNotFoundError(f"Directory or file not found: {fnf_error}")
    except PermissionError as perm_error:
        print_red(f"Permission denied: {perm_error}. Please check the directory permissions.")
        raise PermissionError(f"Permission denied: {perm_error}. Please check the directory permissions.")
    except OSError as os_error:
        print_red(f"OS error occurred: {os_error}. Could not create or access the directory.")
        raise OSError(f"OS error occurred: {os_error}. Could not create or access the directory.")
    except TypeError as type_error:
        print_red(f"Type error: {type_error}. Expected a string for the path.")
        raise TypeError(f"Type error: {type_error}. Expected a string for the path.")
    except Exception as e:
        print_red(f"An unexpected error occurred: {e}")
        raise Exception(f"An unexpected error occurred: {e}")

def validate_input(prompt, required=True, password=False, path=False, pass_opt=None, min_length=None):
    while True:
        if pass_opt:
            user_input = getpass(cyan_text(prompt)) or pass_opt
            if len(user_input) < min_length:
                print_red(f"Password must be at least {min_length} characters long.")
                continue
        else:
            user_input = getpass(prompt) if (password) else input(prompt)
            
            if user_input.lower() in ['q', 'x']:
                print_blue("\nExiting keySigner. Goodbye!")
                exit()
    
            if required and not user_input:
                print_red("This field is required. Please enter a value.")
                continue
    
            if password and len(user_input) < min_length:
                print_red(f"Password must be at least {min_length} characters long.")
                continue
            
            if path:
                user_input = os.path.abspath(user_input)
                if not os.path.exists(user_input):
                    print_red("Invalid path. Please enter a valid path.")
                    continue
                if not os.access(user_input, os.R_OK):
                    print_red("Path is not accessible. Please check permissions.")
                    continue
                
        return user_input