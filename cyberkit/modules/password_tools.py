"""
Password Tools Module - Hash Cracking and Password Utilities
"""

import os
import sys
import hashlib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.helpers import *

class PasswordTools:
    def __init__(self):
        self.output_dir = create_output_dir("output/passwords")
        
    def show_menu(self):
        """Display password tools menu"""
        while True:
            clear_screen()
            print_banner("""
╔═══════════════════════════════════════════════════════════╗
║                  PASSWORD TOOLS                            ║
╚═══════════════════════════════════════════════════════════╝
            """)
            print(f"""
{Colors.CYAN}[1]{Colors.END} Hash Identifier
{Colors.CYAN}[2]{Colors.END} Hash Generator
{Colors.CYAN}[3]{Colors.END} John The Ripper
{Colors.CYAN}[4]{Colors.END} Hashcat
{Colors.CYAN}[5]{Colors.END} Hydra - Brute Force
{Colors.CYAN}[6]{Colors.END} Medusa - Brute Force
{Colors.CYAN}[7]{Colors.END} Wordlist Generator (Crunch)
{Colors.CYAN}[8]{Colors.END} CeWL - Custom Wordlist
{Colors.CYAN}[9]{Colors.END} Hash Lookup (Online)
{Colors.CYAN}[10]{Colors.END} Password Strength Check
{Colors.CYAN}[0]{Colors.END} Back to Main Menu
            """)
            
            choice = get_input("Your choice")
            
            if choice == "0":
                break
            elif choice == "1":
                self.hash_identifier()
            elif choice == "2":
                self.hash_generator()
            elif choice == "3":
                self.john_ripper()
            elif choice == "4":
                self.hashcat_crack()
            elif choice == "5":
                self.hydra_attack()
            elif choice == "6":
                self.medusa_attack()
            elif choice == "7":
                self.crunch_wordlist()
            elif choice == "8":
                self.cewl_wordlist()
            elif choice == "9":
                self.hash_lookup()
            elif choice == "10":
                self.password_strength()
            else:
                print_error("Invalid selection!")
                input("\nPress Enter to continue...")

    def hash_identifier(self):
        """Identify hash type"""
        clear_screen()
        print_banner("=== HASH IDENTIFIER ===\n")
        
        hash_value = get_input("Hash değeri")
        
        if hash_value:
            hash_len = len(hash_value)
            possible_types = []
            
            hash_patterns = {
                32: ["MD5", "NTLM", "MD4"],
                40: ["SHA1", "MySQL5"],
                56: ["SHA224"],
                64: ["SHA256", "SHA3-256"],
                96: ["SHA384", "SHA3-384"],
                128: ["SHA512", "SHA3-512", "Whirlpool"],
            }
            
            if hash_len in hash_patterns:
                possible_types = hash_patterns[hash_len]
            
            if hash_value.startswith("$1$"):
                possible_types = ["MD5crypt"]
            elif hash_value.startswith("$2"):
                possible_types = ["Bcrypt"]
            elif hash_value.startswith("$5$"):
                possible_types = ["SHA256crypt"]
            elif hash_value.startswith("$6$"):
                possible_types = ["SHA512crypt"]
            elif hash_value.startswith("$apr1$"):
                possible_types = ["Apache MD5"]
            elif ":" in hash_value and len(hash_value.split(":")[0]) == 32:
                possible_types = ["NTLM with salt", "MySQL"]
            
            if possible_types:
                print_success("Olası hash türleri:")
                for ht in possible_types:
                    print(f"  - {Colors.CYAN}{ht}{Colors.END}")
            else:
                print_warning(f"Hash türü belirlenemedi (uzunluk: {hash_len})")
            
            if check_tool("hashid"):
                print_info("\nHashID ile analiz:")
                cmd = f"hashid '{hash_value}'"
                run_command_live(cmd)
            
            if check_tool("hash-identifier"):
                if confirm("\nhash-identifier ile de kontrol edilsin mi?"):
                    cmd = f"echo '{hash_value}' | hash-identifier"
                    run_command_live(cmd)
            
            input("\nPress Enter to continue...")

    def hash_generator(self):
        """Generate various hash types"""
        clear_screen()
        print_banner("=== HASH GENERATOR ===\n")
        
        text = get_input("Hash'lenecek metin")
        
        if text:
            print_info("\nÜretilen Hash'ler:\n")
            
            hashes = {
                "MD5": hashlib.md5(text.encode()).hexdigest(),
                "SHA1": hashlib.sha1(text.encode()).hexdigest(),
                "SHA224": hashlib.sha224(text.encode()).hexdigest(),
                "SHA256": hashlib.sha256(text.encode()).hexdigest(),
                "SHA384": hashlib.sha384(text.encode()).hexdigest(),
                "SHA512": hashlib.sha512(text.encode()).hexdigest(),
            }
            
            for name, value in hashes.items():
                print(f"{Colors.CYAN}{name}:{Colors.END} {value}")
            
            if confirm("\nResults dosyaya kaydedilsin mi?"):
                timestamp = get_timestamp()
                output_file = f"{self.output_dir}/hashes_{timestamp}.txt"
                with open(output_file, 'w') as f:
                    f.write(f"Input: {text}\n\n")
                    for name, value in hashes.items():
                        f.write(f"{name}: {value}\n")
                print_success(f"Kaydedildi: {output_file}")
            
            input("\nPress Enter to continue...")

    def john_ripper(self):
        """John The Ripper password cracking"""
        clear_screen()
        print_banner("=== JOHN THE RIPPER ===\n")
        
        if not check_tool("john"):
            print_error("John The Ripper is not installed!")
            input("\nPress Enter to continue...")
            return
        
        print(f"""
{Colors.YELLOW}Mod Seçin:{Colors.END}
[1] Wordlist saldırısı
[2] Incremental (brute force)
[3] Rules ile wordlist
[4] Show cracked passwords
[5] Özel format
        """)
        
        mode = get_input("Seçim", "1")
        hash_file = get_input("Hash dosyası yolu")
        
        if not hash_file:
            return
            
        if mode == "1":
            wordlist = get_input("Wordlist", "/usr/share/wordlists/rockyou.txt")
            cmd = f"john --wordlist={wordlist} {hash_file}"
        elif mode == "2":
            cmd = f"john --incremental {hash_file}"
        elif mode == "3":
            wordlist = get_input("Wordlist", "/usr/share/wordlists/rockyou.txt")
            cmd = f"john --wordlist={wordlist} --rules {hash_file}"
        elif mode == "4":
            cmd = f"john --show {hash_file}"
        elif mode == "5":
            fmt = get_input("Format (e.g.: raw-md5, ntlm, sha512crypt)")
            wordlist = get_input("Wordlist", "/usr/share/wordlists/rockyou.txt")
            cmd = f"john --format={fmt} --wordlist={wordlist} {hash_file}"
        else:
            return
        
        print_info(f"Running command: {cmd}")
        run_command_live(cmd)
        input("\nPress Enter to continue...")

    def hashcat_crack(self):
        """Hashcat password cracking"""
        clear_screen()
        print_banner("=== HASHCAT ===\n")
        
        if not check_tool("hashcat"):
            print_error("Hashcat is not installed!")
            input("\nPress Enter to continue...")
            return
        
        print_info("Yaygın hash modları:")
        print(f"""
  {Colors.CYAN}0{Colors.END}    - MD5
  {Colors.CYAN}100{Colors.END}  - SHA1
  {Colors.CYAN}1000{Colors.END} - NTLM
  {Colors.CYAN}1400{Colors.END} - SHA256
  {Colors.CYAN}1700{Colors.END} - SHA512
  {Colors.CYAN}1800{Colors.END} - SHA512crypt
  {Colors.CYAN}3200{Colors.END} - bcrypt
  {Colors.CYAN}500{Colors.END}  - MD5crypt
        """)
        
        hash_mode = get_input("Hash modu")
        hash_file = get_input("Hash dosyası")
        wordlist = get_input("Wordlist", "/usr/share/wordlists/rockyou.txt")
        
        if hash_mode and hash_file:
            timestamp = get_timestamp()
            output_file = f"{self.output_dir}/hashcat_{timestamp}.txt"
            
            cmd = f"hashcat -m {hash_mode} -a 0 {hash_file} {wordlist} -o {output_file}"
            print_info(f"Running command: {cmd}")
            run_command_live(cmd)
            input("\nPress Enter to continue...")

    def hydra_attack(self):
        """Hydra brute force attack"""
        clear_screen()
        print_banner("=== HYDRA BRUTE FORCE ===\n")
        
        if not check_tool("hydra"):
            print_error("Hydra is not installed!")
            input("\nPress Enter to continue...")
            return
        
        print(f"""
{Colors.YELLOW}Protokol Seçin:{Colors.END}
[1] SSH
[2] FTP
[3] HTTP-POST-FORM
[4] HTTP-GET
[5] SMB
[6] MySQL
[7] RDP
[8] Telnet
[9] Özel
        """)
        
        proto_choice = get_input("Seçim", "1")
        target = get_input("Target IP/Domain")
        
        protocols = {
            "1": "ssh", "2": "ftp", "3": "http-post-form",
            "4": "http-get", "5": "smb", "6": "mysql",
            "7": "rdp", "8": "telnet"
        }
        
        if proto_choice == "9":
            protocol = get_input("Protokol adı")
        else:
            protocol = protocols.get(proto_choice, "ssh")
        
        user_opt = get_input("Kullanıcı adı (-l) veya liste (-L)")
        if user_opt.endswith(".txt"):
            user_param = f"-L {user_opt}"
        else:
            user_param = f"-l {user_opt}"
        
        pass_opt = get_input("Şifre (-p) veya liste (-P)", "/usr/share/wordlists/rockyou.txt")
        if pass_opt.endswith(".txt") or "/" in pass_opt:
            pass_param = f"-P {pass_opt}"
        else:
            pass_param = f"-p {pass_opt}"
        
        threads = get_input("Thread sayısı", "16")
        
        if proto_choice == "3":
            path = get_input("Login path (e.g.: /login.php)")
            form_data = get_input("Form data (e.g.: user=^USER^&pass=^PASS^)")
            fail_msg = get_input("Başarısız mesajı (e.g.: 'Login failed')")
            cmd = f"hydra {user_param} {pass_param} {target} {protocol} \"{path}:{form_data}:{fail_msg}\" -t {threads}"
        else:
            port = get_input("Port (empty=varsayılan)", "")
            port_param = f"-s {port}" if port else ""
            cmd = f"hydra {user_param} {pass_param} {target} {protocol} {port_param} -t {threads}"
        
        print_info(f"Running command: {cmd}")
        print_warning("This may take a long time...")
        run_command_live(cmd)
        input("\nPress Enter to continue...")

    def medusa_attack(self):
        """Medusa brute force"""
        clear_screen()
        print_banner("=== MEDUSA BRUTE FORCE ===\n")
        
        if not check_tool("medusa"):
            print_error("Medusa is not installed!")
            input("\nPress Enter to continue...")
            return
        
        target = get_input("Target IP")
        user = get_input("Kullanıcı adı")
        wordlist = get_input("Password wordlist", "/usr/share/wordlists/rockyou.txt")
        module = get_input("Modül (ssh, ftp, http, smb, mysql)", "ssh")
        
        if target and user:
            cmd = f"medusa -h {target} -u {user} -P {wordlist} -M {module}"
            print_info(f"Running command: {cmd}")
            run_command_live(cmd)
            input("\nPress Enter to continue...")

    def crunch_wordlist(self):
        """Generate wordlist with Crunch"""
        clear_screen()
        print_banner("=== CRUNCH WORDLIST GENERATOR ===\n")
        
        if not check_tool("crunch"):
            print_error("Crunch is not installed!")
            input("\nPress Enter to continue...")
            return
        
        min_len = get_input("Minimum uzunluk", "6")
        max_len = get_input("Maximum uzunluk", "8")
        charset = get_input("Karakter seti (empty=varsayılan)", "")
        pattern = get_input("Pattern (@ küçük, , büyük, % rakam, ^ sembol)", "")
        
        timestamp = get_timestamp()
        output_file = f"{self.output_dir}/wordlist_{timestamp}.txt"
        
        cmd = f"crunch {min_len} {max_len}"
        if charset:
            cmd += f" {charset}"
        if pattern:
            cmd += f" -t {pattern}"
        cmd += f" -o {output_file}"
        
        print_info(f"Running command: {cmd}")
        print_warning("Bu işlem büyük dosyalar oluşturabilir!")
        
        if confirm("Devam edilsin mi?"):
            run_command_live(cmd)
            print_success(f"Wordlist oluşturuldu: {output_file}")
        
        input("\nPress Enter to continue...")

    def cewl_wordlist(self):
        """Generate wordlist from website with CeWL"""
        clear_screen()
        print_banner("=== CeWL CUSTOM WORDLIST ===\n")
        
        if not check_tool("cewl"):
            print_error("CeWL is not installed!")
            input("\nPress Enter to continue...")
            return
        
        url = get_input("Target URL")
        depth = get_input("Spider derinliği", "2")
        min_word = get_input("Minimum kelime uzunluğu", "5")
        
        if url:
            timestamp = get_timestamp()
            output_file = f"{self.output_dir}/cewl_{timestamp}.txt"
            
            cmd = f"cewl {url} -d {depth} -m {min_word} -w {output_file}"
            print_info(f"Running command: {cmd}")
            run_command_live(cmd)
            print_success(f"Wordlist oluşturuldu: {output_file}")
            input("\nPress Enter to continue...")

    def hash_lookup(self):
        """Online hash lookup"""
        clear_screen()
        print_banner("=== ONLINE HASH LOOKUP ===\n")
        
        hash_value = get_input("Hash değeri")
        
        if hash_value:
            print_info("Online veritabanları kontrol ediliyor...\n")
            
            print_info("Manuel kontrol için siteler:")
            sites = [
                "https://crackstation.net/",
                "https://hashes.com/en/decrypt/hash",
                "https://md5decrypt.net/",
                "https://hashkiller.io/",
            ]
            for site in sites:
                print(f"  - {site}")
            
            input("\nPress Enter to continue...")

    def password_strength(self):
        """Check password strength"""
        clear_screen()
        print_banner("=== PASSWORD STRENGTH CHECK ===\n")
        
        password = get_input("Şifre")
        
        if password:
            score = 0
            feedback = []
            
            if len(password) >= 8:
                score += 1
            else:
                feedback.append("En az 8 karakter olmalı")
            
            if len(password) >= 12:
                score += 1
            
            if len(password) >= 16:
                score += 1
            
            if any(c.islower() for c in password):
                score += 1
            else:
                feedback.append("Küçük harf ekleyin")
            
            if any(c.isupper() for c in password):
                score += 1
            else:
                feedback.append("Büyük harf ekleyin")
            
            if any(c.isdigit() for c in password):
                score += 1
            else:
                feedback.append("Rakam ekleyin")
            
            if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
                score += 1
            else:
                feedback.append("Özel karakter ekleyin")
            
            common_passwords = ["password", "123456", "qwerty", "admin", "letmein"]
            if password.lower() in common_passwords:
                score = 0
                feedback.append("Çok yaygın bir şifre!")
            
            print(f"\n{Colors.CYAN}Şifre Uzunluğu:{Colors.END} {len(password)}")
            print(f"{Colors.CYAN}Güç Skoru:{Colors.END} {score}/7")
            
            if score <= 2:
                print(f"{Colors.RED}Güç: ZAYIF{Colors.END}")
            elif score <= 4:
                print(f"{Colors.YELLOW}Güç: ORTA{Colors.END}")
            elif score <= 6:
                print(f"{Colors.GREEN}Güç: İYİ{Colors.END}")
            else:
                print(f"{Colors.GREEN}Güç: ÇOK GÜÇLÜ{Colors.END}")
            
            if feedback:
                print(f"\n{Colors.YELLOW}Öneriler:{Colors.END}")
                for f in feedback:
                    print(f"  - {f}")
            
            input("\nPress Enter to continue...")
