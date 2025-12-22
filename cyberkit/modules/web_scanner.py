"""
Web Scanner Module - Web Application Security Testing
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.helpers import *

class WebScanner:
    def __init__(self):
        self.output_dir = create_output_dir("output/web")
        
    def show_menu(self):
        """Display web scanner menu"""
        while True:
            clear_screen()
            print_banner("""
╔═══════════════════════════════════════════════════════════╗
║                 WEB SCANNER MODULE                         ║
╚═══════════════════════════════════════════════════════════╝
            """)
            print(f"""
{Colors.CYAN}[1]{Colors.END} Directory/File Bruteforce (Gobuster)
{Colors.CYAN}[2]{Colors.END} Directory Fuzzing (Ffuf)
{Colors.CYAN}[3]{Colors.END} Nikto Web Scanner
{Colors.CYAN}[4]{Colors.END} WhatWeb - Web Fingerprint
{Colors.CYAN}[5]{Colors.END} SQLMap - SQL Injection
{Colors.CYAN}[6]{Colors.END} XSS Tarama (XSSer)
{Colors.CYAN}[7]{Colors.END} Subdomain Enumeration
{Colors.CYAN}[8]{Colors.END} SSL/TLS Analizi
{Colors.CYAN}[9]{Colors.END} CMS Detection (CMSMap)
{Colors.CYAN}[10]{Colors.END} WordPress Scan (WPScan)
{Colors.CYAN}[11]{Colors.END} HTTP Header Analizi
{Colors.CYAN}[12]{Colors.END} Virtual Host Discovery
{Colors.CYAN}[0]{Colors.END} Ana Menüye Dön
            """)
            
            choice = get_input("Seçiminiz")
            
            if choice == "0":
                break
            elif choice == "1":
                self.gobuster_scan()
            elif choice == "2":
                self.ffuf_scan()
            elif choice == "3":
                self.nikto_scan()
            elif choice == "4":
                self.whatweb_scan()
            elif choice == "5":
                self.sqlmap_scan()
            elif choice == "6":
                self.xss_scan()
            elif choice == "7":
                self.subdomain_enum()
            elif choice == "8":
                self.ssl_analysis()
            elif choice == "9":
                self.cms_detection()
            elif choice == "10":
                self.wpscan()
            elif choice == "11":
                self.http_headers()
            elif choice == "12":
                self.vhost_discovery()
            else:
                print_error("Geçersiz seçim!")
                input("\nDevam etmek için Enter'a basın...")

    def gobuster_scan(self):
        """Directory bruteforce with Gobuster"""
        clear_screen()
        print_banner("=== GOBUSTER DIRECTORY SCAN ===\n")
        if not check_tool("gobuster"):
            print_error("Gobuster yüklü değil! 'apt install gobuster' ile yükleyin.")
            input("\nDevam etmek için Enter'a basın...")
            return
            
        url = get_input("Hedef URL (http://example.com)")
        wordlist = get_input("Wordlist", "/usr/share/wordlists/dirb/common.txt")
        extensions = get_input("Uzantılar (boş bırakılabilir)", "php,html,txt")
        threads = get_input("Thread sayısı", "50")
        
        if url:
            timestamp = get_timestamp()
            output_file = f"{self.output_dir}/gobuster_{timestamp}.txt"
            
            ext_opt = f"-x {extensions}" if extensions else ""
            cmd = f"gobuster dir -u {url} -w {wordlist} {ext_opt} -t {threads} -o {output_file}"
            
            print_info(f"Çalıştırılan komut: {cmd}")
            print_status("Tarama başlatılıyor...\n")
            run_command_live(cmd)
            print_success(f"\nSonuçlar: {output_file}")
            input("\nDevam etmek için Enter'a basın...")

    def ffuf_scan(self):
        """Fuzzing with ffuf"""
        clear_screen()
        print_banner("=== FFUF FUZZING ===\n")
        if not check_tool("ffuf"):
            print_error("Ffuf yüklü değil! 'apt install ffuf' ile yükleyin.")
            input("\nDevam etmek için Enter'a basın...")
            return
            
        url = get_input("Hedef URL (FUZZ yerine fuzz edilecek: http://example.com/FUZZ)")
        wordlist = get_input("Wordlist", "/usr/share/wordlists/dirb/common.txt")
        
        if url:
            timestamp = get_timestamp()
            output_file = f"{self.output_dir}/ffuf_{timestamp}.json"
            
            cmd = f"ffuf -u {url} -w {wordlist} -o {output_file} -of json -c"
            
            print_info(f"Çalıştırılan komut: {cmd}")
            run_command_live(cmd)
            print_success(f"\nSonuçlar: {output_file}")
            input("\nDevam etmek için Enter'a basın...")

    def nikto_scan(self):
        """Web vulnerability scan with Nikto"""
        clear_screen()
        print_banner("=== NIKTO WEB SCANNER ===\n")
        if not check_tool("nikto"):
            print_error("Nikto yüklü değil! 'apt install nikto' ile yükleyin.")
            input("\nDevam etmek için Enter'a basın...")
            return
            
        url = get_input("Hedef URL")
        
        if url:
            timestamp = get_timestamp()
            output_file = f"{self.output_dir}/nikto_{timestamp}.txt"
            
            cmd = f"nikto -h {url} -o {output_file}"
            
            print_info(f"Çalıştırılan komut: {cmd}")
            print_warning("Bu tarama uzun sürebilir...")
            run_command_live(cmd)
            print_success(f"\nSonuçlar: {output_file}")
            input("\nDevam etmek için Enter'a basın...")

    def whatweb_scan(self):
        """Web fingerprinting with WhatWeb"""
        clear_screen()
        print_banner("=== WHATWEB FINGERPRINT ===\n")
        if not check_tool("whatweb"):
            print_error("WhatWeb yüklü değil! 'apt install whatweb' ile yükleyin.")
            input("\nDevam etmek için Enter'a basın...")
            return
            
        url = get_input("Hedef URL")
        aggression = get_input("Aggression level (1-4)", "3")
        
        if url:
            cmd = f"whatweb -a {aggression} -v {url}"
            print_info(f"Çalıştırılan komut: {cmd}")
            run_command_live(cmd)
            input("\nDevam etmek için Enter'a basın...")

    def sqlmap_scan(self):
        """SQL Injection testing with SQLMap"""
        clear_screen()
        print_banner("=== SQLMAP - SQL INJECTION ===\n")
        if not check_tool("sqlmap"):
            print_error("SQLMap yüklü değil! 'apt install sqlmap' ile yükleyin.")
            input("\nDevam etmek için Enter'a basın...")
            return
        
        print(f"""
{Colors.YELLOW}Tarama Türü Seçin:{Colors.END}
[1] URL ile tarama
[2] Request file ile tarama
[3] POST data ile tarama
        """)
        scan_type = get_input("Seçim", "1")
        
        if scan_type == "1":
            url = get_input("Hedef URL (parametreli: http://site.com/page.php?id=1)")
            if url:
                cmd = f"sqlmap -u \"{url}\" --batch --random-agent"
        elif scan_type == "2":
            req_file = get_input("Request dosyası yolu")
            if req_file:
                cmd = f"sqlmap -r {req_file} --batch --random-agent"
        elif scan_type == "3":
            url = get_input("Hedef URL")
            data = get_input("POST data (örn: username=admin&password=test)")
            if url and data:
                cmd = f"sqlmap -u \"{url}\" --data=\"{data}\" --batch --random-agent"
        else:
            return
            
        level = get_input("Test seviyesi (1-5)", "1")
        risk = get_input("Risk seviyesi (1-3)", "1")
        
        cmd += f" --level={level} --risk={risk}"
        
        if confirm("Database enumerate edilsin mi?"):
            cmd += " --dbs"
        
        print_info(f"Çalıştırılan komut: {cmd}")
        print_warning("Bu işlem uzun sürebilir...")
        run_command_live(cmd)
        input("\nDevam etmek için Enter'a basın...")

    def xss_scan(self):
        """XSS scanning"""
        clear_screen()
        print_banner("=== XSS TARAMA ===\n")
        
        url = get_input("Hedef URL (parametreli)")
        
        if url:
            if check_tool("xsser"):
                cmd = f"xsser -u \"{url}\" --auto"
                print_info(f"Çalıştırılan komut: {cmd}")
                run_command_live(cmd)
            else:
                print_warning("XSSer bulunamadı, basit XSS kontrolü yapılıyor...")
                payloads = [
                    "<script>alert('XSS')</script>",
                    "<img src=x onerror=alert('XSS')>",
                    "'\"><script>alert('XSS')</script>",
                ]
                print_info("Test edilen payloadlar:")
                for p in payloads:
                    print(f"  - {p}")
            
            input("\nDevam etmek için Enter'a basın...")

    def subdomain_enum(self):
        """Subdomain enumeration"""
        clear_screen()
        print_banner("=== SUBDOMAIN ENUMERATION ===\n")
        
        domain = get_input("Hedef domain (example.com)")
        
        if domain:
            timestamp = get_timestamp()
            output_file = f"{self.output_dir}/subdomains_{domain}_{timestamp}.txt"
            
            if check_tool("subfinder"):
                cmd = f"subfinder -d {domain} -o {output_file}"
                print_info(f"Çalıştırılan komut: {cmd}")
                run_command_live(cmd)
            elif check_tool("sublist3r"):
                cmd = f"sublist3r -d {domain} -o {output_file}"
                print_info(f"Çalıştırılan komut: {cmd}")
                run_command_live(cmd)
            elif check_tool("amass"):
                cmd = f"amass enum -passive -d {domain} -o {output_file}"
                print_info(f"Çalıştırılan komut: {cmd}")
                run_command_live(cmd)
            else:
                print_error("Subdomain aracı bulunamadı!")
                print_info("Şu araçlardan birini yükleyin: subfinder, sublist3r, amass")
            
            input("\nDevam etmek için Enter'a basın...")

    def ssl_analysis(self):
        """SSL/TLS analysis"""
        clear_screen()
        print_banner("=== SSL/TLS ANALİZİ ===\n")
        
        target = get_input("Hedef domain/IP")
        port = get_input("Port", "443")
        
        if target:
            if check_tool("sslscan"):
                cmd = f"sslscan {target}:{port}"
                print_info(f"Çalıştırılan komut: {cmd}")
                run_command_live(cmd)
            elif check_tool("testssl.sh"):
                cmd = f"testssl.sh {target}:{port}"
                print_info(f"Çalıştırılan komut: {cmd}")
                run_command_live(cmd)
            else:
                cmd = f"openssl s_client -connect {target}:{port} -showcerts"
                print_info(f"Çalıştırılan komut: {cmd}")
                stdout, stderr, _ = run_command(cmd)
                print(stdout)
            
            input("\nDevam etmek için Enter'a basın...")

    def cms_detection(self):
        """CMS Detection"""
        clear_screen()
        print_banner("=== CMS DETECTION ===\n")
        
        url = get_input("Hedef URL")
        
        if url:
            if check_tool("whatweb"):
                cmd = f"whatweb -a 3 {url}"
                print_info(f"Çalıştırılan komut: {cmd}")
                run_command_live(cmd)
            else:
                print_info("WhatWeb yüklü değil, curl ile kontrol ediliyor...")
                cmd = f"curl -s -I {url}"
                run_command_live(cmd)
            
            input("\nDevam etmek için Enter'a basın...")

    def wpscan(self):
        """WordPress vulnerability scan"""
        clear_screen()
        print_banner("=== WORDPRESS SCAN ===\n")
        if not check_tool("wpscan"):
            print_error("WPScan yüklü değil! 'apt install wpscan' ile yükleyin.")
            input("\nDevam etmek için Enter'a basın...")
            return
            
        url = get_input("WordPress URL")
        api_token = get_input("WPScan API Token (boş bırakılabilir)", "")
        
        if url:
            timestamp = get_timestamp()
            output_file = f"{self.output_dir}/wpscan_{timestamp}.txt"
            
            api_opt = f"--api-token {api_token}" if api_token else ""
            cmd = f"wpscan --url {url} {api_opt} -e vp,vt,u --output {output_file}"
            
            print_info(f"Çalıştırılan komut: {cmd}")
            run_command_live(cmd)
            print_success(f"\nSonuçlar: {output_file}")
            input("\nDevam etmek için Enter'a basın...")

    def http_headers(self):
        """HTTP header analysis"""
        clear_screen()
        print_banner("=== HTTP HEADER ANALİZİ ===\n")
        
        url = get_input("Hedef URL")
        
        if url:
            cmd = f"curl -s -I -L {url}"
            print_info(f"Çalıştırılan komut: {cmd}")
            print("\n")
            run_command_live(cmd)
            
            print_info("\nGüvenlik Header Kontrolü:")
            headers_to_check = [
                "X-Frame-Options",
                "X-Content-Type-Options", 
                "X-XSS-Protection",
                "Content-Security-Policy",
                "Strict-Transport-Security"
            ]
            
            stdout, _, _ = run_command(cmd)
            for header in headers_to_check:
                if header.lower() in stdout.lower():
                    print_success(f"{header}: Mevcut")
                else:
                    print_warning(f"{header}: Eksik!")
            
            input("\nDevam etmek için Enter'a basın...")

    def vhost_discovery(self):
        """Virtual host discovery"""
        clear_screen()
        print_banner("=== VIRTUAL HOST DISCOVERY ===\n")
        
        if not check_tool("gobuster"):
            print_error("Gobuster yüklü değil!")
            input("\nDevam etmek için Enter'a basın...")
            return
            
        url = get_input("Hedef URL")
        wordlist = get_input("Wordlist", "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt")
        
        if url:
            cmd = f"gobuster vhost -u {url} -w {wordlist}"
            print_info(f"Çalıştırılan komut: {cmd}")
            run_command_live(cmd)
            input("\nDevam etmek için Enter'a basın...")
