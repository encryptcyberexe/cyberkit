"""
Encoding/Decoding Tools - Data transformation utilities
"""

import os
import sys
import base64
import hashlib
import urllib.parse
import binascii
import html
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.helpers import *

class EncodingTools:
    def __init__(self):
        self.output_dir = create_output_dir("output/encoding")
    
    def show_menu(self):
        while True:
            clear_screen()
            print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║               ENCODING / DECODING TOOLS                      ║
╠══════════════════════════════════════════════════════════════╣{Colors.END}
║   {Colors.CYAN}[1]{Colors.END}  Base64 Encode/Decode                               ║
║   {Colors.CYAN}[2]{Colors.END}  URL Encode/Decode                                  ║
║   {Colors.CYAN}[3]{Colors.END}  HTML Encode/Decode                                 ║
║   {Colors.CYAN}[4]{Colors.END}  Hex Encode/Decode                                  ║
║   {Colors.CYAN}[5]{Colors.END}  Binary Encode/Decode                               ║
║   {Colors.CYAN}[6]{Colors.END}  ROT13 / Caesar Cipher                              ║
║   {Colors.CYAN}[7]{Colors.END}  Hash Generator (MD5/SHA)                           ║
║   {Colors.CYAN}[8]{Colors.END}  JWT Decoder                                        ║
║   {Colors.CYAN}[9]{Colors.END}  Unicode Encode/Decode                              ║
║   {Colors.CYAN}[10]{Colors.END} Auto Detect & Decode                               ║
║   {Colors.RED}[0]{Colors.END}  Back                                               ║
{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.END}
            """)
            choice = get_input("  Select")
            if choice == "0": break
            elif choice == "1": self.base64_tool()
            elif choice == "2": self.url_tool()
            elif choice == "3": self.html_tool()
            elif choice == "4": self.hex_tool()
            elif choice == "5": self.binary_tool()
            elif choice == "6": self.rot_cipher()
            elif choice == "7": self.hash_gen()
            elif choice == "8": self.jwt_decode()
            elif choice == "9": self.unicode_tool()
            elif choice == "10": self.auto_decode()

    def base64_tool(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  BASE64 ENCODE/DECODE{Colors.END}\n")
        print(f"  [1] Encode  [2] Decode")
        choice = get_input("  Select", "1")
        data = get_input("  Input")
        if not data: return
        
        try:
            if choice == "1":
                result = base64.b64encode(data.encode()).decode()
                print_success(f"\n  Encoded: {result}")
            else:
                result = base64.b64decode(data).decode()
                print_success(f"\n  Decoded: {result}")
        except Exception as e:
            print_error(f"  Error: {e}")
        input("\n  Press Enter...")

    def url_tool(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  URL ENCODE/DECODE{Colors.END}\n")
        print(f"  [1] Encode  [2] Decode")
        choice = get_input("  Select", "1")
        data = get_input("  Input")
        if not data: return
        
        if choice == "1":
            result = urllib.parse.quote(data, safe='')
            print_success(f"\n  Encoded: {result}")
        else:
            result = urllib.parse.unquote(data)
            print_success(f"\n  Decoded: {result}")
        input("\n  Press Enter...")

    def html_tool(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  HTML ENCODE/DECODE{Colors.END}\n")
        print(f"  [1] Encode  [2] Decode")
        choice = get_input("  Select", "1")
        data = get_input("  Input")
        if not data: return
        
        if choice == "1":
            result = html.escape(data)
            print_success(f"\n  Encoded: {result}")
        else:
            result = html.unescape(data)
            print_success(f"\n  Decoded: {result}")
        input("\n  Press Enter...")

    def hex_tool(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  HEX ENCODE/DECODE{Colors.END}\n")
        print(f"  [1] Text to Hex  [2] Hex to Text")
        choice = get_input("  Select", "1")
        data = get_input("  Input")
        if not data: return
        
        try:
            if choice == "1":
                result = data.encode().hex()
                print_success(f"\n  Hex: {result}")
            else:
                data = data.replace(" ", "").replace("0x", "")
                result = bytes.fromhex(data).decode()
                print_success(f"\n  Text: {result}")
        except Exception as e:
            print_error(f"  Error: {e}")
        input("\n  Press Enter...")

    def binary_tool(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  BINARY ENCODE/DECODE{Colors.END}\n")
        print(f"  [1] Text to Binary  [2] Binary to Text")
        choice = get_input("  Select", "1")
        data = get_input("  Input")
        if not data: return
        
        try:
            if choice == "1":
                result = ' '.join(format(ord(c), '08b') for c in data)
                print_success(f"\n  Binary: {result}")
            else:
                data = data.replace(" ", "")
                chars = [data[i:i+8] for i in range(0, len(data), 8)]
                result = ''.join(chr(int(c, 2)) for c in chars)
                print_success(f"\n  Text: {result}")
        except Exception as e:
            print_error(f"  Error: {e}")
        input("\n  Press Enter...")

    def rot_cipher(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  ROT / CAESAR CIPHER{Colors.END}\n")
        data = get_input("  Input text")
        shift = int(get_input("  Shift (13 for ROT13)", "13"))
        if not data: return
        
        result = ""
        for char in data:
            if char.isalpha():
                ascii_off = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - ascii_off + shift) % 26 + ascii_off)
            else:
                result += char
        
        print_success(f"\n  Result: {result}")
        
        if confirm("\n  Show all rotations?"):
            print(f"\n  {'ROT':<5} {'Result'}")
            print(f"  {'-'*40}")
            for i in range(1, 26):
                r = ""
                for char in data:
                    if char.isalpha():
                        off = ord('A') if char.isupper() else ord('a')
                        r += chr((ord(char) - off + i) % 26 + off)
                    else:
                        r += char
                print(f"  ROT{i:<2} {r}")
        input("\n  Press Enter...")

    def hash_gen(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  HASH GENERATOR{Colors.END}\n")
        data = get_input("  Input text")
        if not data: return
        
        hashes = {
            "MD5": hashlib.md5(data.encode()).hexdigest(),
            "SHA1": hashlib.sha1(data.encode()).hexdigest(),
            "SHA256": hashlib.sha256(data.encode()).hexdigest(),
            "SHA512": hashlib.sha512(data.encode()).hexdigest(),
        }
        
        print(f"\n  {Colors.BOLD}Results:{Colors.END}")
        for name, h in hashes.items():
            print(f"  {Colors.CYAN}{name:8}{Colors.END} {h}")
        input("\n  Press Enter...")

    def jwt_decode(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  JWT DECODER{Colors.END}\n")
        token = get_input("  JWT Token")
        if not token: return
        
        try:
            parts = token.split(".")
            if len(parts) != 3:
                print_error("  Invalid JWT format!"); return
            
            header = base64.b64decode(parts[0] + "==").decode()
            payload = base64.b64decode(parts[1] + "==").decode()
            
            print(f"\n  {Colors.CYAN}Header:{Colors.END}")
            print(f"  {header}")
            print(f"\n  {Colors.CYAN}Payload:{Colors.END}")
            print(f"  {payload}")
            print(f"\n  {Colors.CYAN}Signature:{Colors.END}")
            print(f"  {parts[2][:50]}...")
        except Exception as e:
            print_error(f"  Error: {e}")
        input("\n  Press Enter...")

    def unicode_tool(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  UNICODE ENCODE/DECODE{Colors.END}\n")
        print(f"  [1] Text to Unicode  [2] Unicode to Text")
        choice = get_input("  Select", "1")
        data = get_input("  Input")
        if not data: return
        
        try:
            if choice == "1":
                result = ''.join(f'\\u{ord(c):04x}' for c in data)
                print_success(f"\n  Unicode: {result}")
            else:
                result = data.encode().decode('unicode_escape')
                print_success(f"\n  Text: {result}")
        except Exception as e:
            print_error(f"  Error: {e}")
        input("\n  Press Enter...")

    def auto_decode(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  AUTO DETECT & DECODE{Colors.END}\n")
        data = get_input("  Input")
        if not data: return
        
        print(f"\n  {Colors.BOLD}Attempting decodes:{Colors.END}\n")
        
        # Base64
        try:
            decoded = base64.b64decode(data).decode()
            if decoded.isprintable():
                print(f"  {Colors.GREEN}[Base64]{Colors.END} {decoded}")
        except: pass
        
        # Hex
        try:
            clean = data.replace(" ", "").replace("0x", "")
            decoded = bytes.fromhex(clean).decode()
            if decoded.isprintable():
                print(f"  {Colors.GREEN}[Hex]{Colors.END} {decoded}")
        except: pass
        
        # URL
        try:
            decoded = urllib.parse.unquote(data)
            if decoded != data:
                print(f"  {Colors.GREEN}[URL]{Colors.END} {decoded}")
        except: pass
        
        # HTML
        decoded = html.unescape(data)
        if decoded != data:
            print(f"  {Colors.GREEN}[HTML]{Colors.END} {decoded}")
        
        # ROT13
        rot13 = ""
        for c in data:
            if c.isalpha():
                off = ord('A') if c.isupper() else ord('a')
                rot13 += chr((ord(c) - off + 13) % 26 + off)
            else:
                rot13 += c
        if rot13 != data:
            print(f"  {Colors.GREEN}[ROT13]{Colors.END} {rot13}")
        
        input("\n  Press Enter...")
