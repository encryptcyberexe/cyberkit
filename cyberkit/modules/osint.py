"""
OSINT Module - Information Gathering Tools
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.helpers import *

class OSINTModule:
    def __init__(self):
        self.output_dir = create_output_dir("output/osint")
        
    def show_menu(self):
        """Display OSINT menu"""
        while True:
            clear_screen()
            print_banner("""
╔═══════════════════════════════════════════════════════════╗
║              OSINT / INFORMATION GATHERING                 ║
╚═══════════════════════════════════════════════════════════╝
            """)
            print(f"""
{Colors.CYAN}[1]{Colors.END} WHOIS Sorgulama
{Colors.CYAN}[2]{Colors.END} DNS Enumeration
{Colors.CYAN}[3]{Colors.END} Email Harvesting (theHarvester)
{Colors.CYAN}[4]{Colors.END} Google Dork Generator
{Colors.CYAN}[5]{Colors.END} Shodan Search
{Colors.CYAN}[6]{Colors.END} Social Media Username Check
{Colors.CYAN}[7]{Colors.END} IP Geolocation
{Colors.CYAN}[8]{Colors.END} Reverse DNS Lookup
{Colors.CYAN}[9]{Colors.END} ASN Lookup
{Colors.CYAN}[10]{Colors.END} Website Technology Stack
{Colors.CYAN}[11]{Colors.END} Wayback Machine Check
{Colors.CYAN}[12]{Colors.END} Certificate Transparency Logs
{Colors.CYAN}[0]{Colors.END} Back to Main Menu
            """)
            
            choice = get_input("Your choice")
            
            if choice == "0":
                break
            elif choice == "1":
                self.whois_lookup()
            elif choice == "2":
                self.dns_enum()
            elif choice == "3":
                self.email_harvest()
            elif choice == "4":
                self.google_dork()
            elif choice == "5":
                self.shodan_search()
            elif choice == "6":
                self.username_check()
            elif choice == "7":
                self.ip_geolocation()
            elif choice == "8":
                self.reverse_dns()
            elif choice == "9":
                self.asn_lookup()
            elif choice == "10":
                self.tech_stack()
            elif choice == "11":
                self.wayback_check()
            elif choice == "12":
                self.cert_transparency()
            else:
                print_error("Invalid selection!")
                input("\nPress Enter to continue...")

    def whois_lookup(self):
        """WHOIS lookup"""
        clear_screen()
        print_banner("=== WHOIS SORGULAMA ===\n")
        
        target = get_input("Domain veya IP")
        
        if target:
            cmd = f"whois {target}"
            print_info(f"Running command: {cmd}")
            run_command_live(cmd)
            input("\nPress Enter to continue...")

    def dns_enum(self):
        """DNS enumeration"""
        clear_screen()
        print_banner("=== DNS ENUMERATION ===\n")
        
        domain = get_input("Target domain")
        
        if domain:
            print_info("DNS kayıtları sorgulanıyor...\n")
            
            record_types = ["A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME"]
            
            for rtype in record_types:
                print(f"\n{Colors.YELLOW}[{rtype} Records]{Colors.END}")
                cmd = f"dig {domain} {rtype} +short"
                stdout, _, _ = run_command(cmd)
                if stdout.strip():
                    print(stdout)
                else:
                    print("  Kayıt bulunamadı")
            
            if check_tool("dnsrecon"):
                if confirm("\nDNSRecon ile detaylı tarama yapılsın mı?"):
                    cmd = f"dnsrecon -d {domain}"
                    run_command_live(cmd)
            
            input("\nPress Enter to continue...")

    def email_harvest(self):
        """Email harvesting with theHarvester"""
        clear_screen()
        print_banner("=== EMAIL HARVESTING ===\n")
        
        if not check_tool("theHarvester"):
            print_error("theHarvester is not installed! 'apt install theharvester' Install with.")
            input("\nPress Enter to continue...")
            return
            
        domain = get_input("Target domain")
        source = get_input("Kaynak (google,bing,linkedin,all)", "all")
        limit = get_input("Sonuç limiti", "500")
        
        if domain:
            timestamp = get_timestamp()
            output_file = f"{self.output_dir}/harvest_{domain}_{timestamp}"
            
            cmd = f"theHarvester -d {domain} -b {source} -l {limit} -f {output_file}"
            print_info(f"Running command: {cmd}")
            run_command_live(cmd)
            input("\nPress Enter to continue...")

    def google_dork(self):
        """Google dork generator"""
        clear_screen()
        print_banner("=== GOOGLE DORK GENERATOR ===\n")
        
        domain = get_input("Target domain")
        
        if domain:
            print_info("Kullanışlı Google Dorkları:\n")
            
            dorks = [
                f'site:{domain}',
                f'site:{domain} filetype:pdf',
                f'site:{domain} filetype:doc OR filetype:docx',
                f'site:{domain} filetype:xls OR filetype:xlsx',
                f'site:{domain} filetype:sql',
                f'site:{domain} filetype:log',
                f'site:{domain} filetype:conf OR filetype:config',
                f'site:{domain} inurl:admin',
                f'site:{domain} inurl:login',
                f'site:{domain} inurl:wp-admin',
                f'site:{domain} intitle:"index of"',
                f'site:{domain} intext:"password"',
                f'site:{domain} ext:php intitle:phpinfo',
                f'site:{domain} inurl:backup',
                f'site:{domain} filetype:env',
                f'"{domain}" email',
                f'"{domain}" password leak',
            ]
            
            for i, dork in enumerate(dorks, 1):
                print(f"{Colors.CYAN}[{i}]{Colors.END} {dork}")
            
            timestamp = get_timestamp()
            output_file = f"{self.output_dir}/dorks_{domain}_{timestamp}.txt"
            with open(output_file, 'w') as f:
                f.write('\n'.join(dorks))
            print_success(f"\nDorklar kaydedildi: {output_file}")
            
            input("\nPress Enter to continue...")

    def shodan_search(self):
        """Shodan search"""
        clear_screen()
        print_banner("=== SHODAN SEARCH ===\n")
        
        if check_tool("shodan"):
            query = get_input("Shodan sorgusu (ip, hostname, vs)")
            if query:
                cmd = f"shodan search {query}"
                print_info(f"Running command: {cmd}")
                run_command_live(cmd)
        else:
            print_warning("Shodan CLI is not installed.")
            print_info("Manuel arama için: https://www.shodan.io/")
            ip = get_input("IP adresi (host bilgisi için)")
            if ip:
                cmd = f"shodan host {ip}"
                print_info(f"Alternatif: curl ile shodan.io API kullanabilirsiniz")
        
        input("\nPress Enter to continue...")

    def username_check(self):
        """Social media username check"""
        clear_screen()
        print_banner("=== USERNAME CHECK ===\n")
        
        username = get_input("Kullanıcı adı")
        
        if username:
            if check_tool("sherlock"):
                cmd = f"sherlock {username}"
                print_info(f"Running command: {cmd}")
                run_command_live(cmd)
            else:
                print_warning("Sherlock is not installed.")
                print_info("Manuel kontrol için platformlar:")
                platforms = [
                    f"https://twitter.com/{username}",
                    f"https://instagram.com/{username}",
                    f"https://github.com/{username}",
                    f"https://linkedin.com/in/{username}",
                    f"https://facebook.com/{username}",
                ]
                for p in platforms:
                    print(f"  - {p}")
            
            input("\nPress Enter to continue...")

    def ip_geolocation(self):
        """IP geolocation"""
        clear_screen()
        print_banner("=== IP GEOLOCATION ===\n")
        
        ip = get_input("IP adresi")
        
        if ip:
            cmd = f"curl -s http://ip-api.com/json/{ip}"
            print_info(f"Running command: {cmd}")
            stdout, _, _ = run_command(cmd)
            
            try:
                import json
                data = json.loads(stdout)
                print(f"\n{Colors.GREEN}Results:{Colors.END}")
                for key, value in data.items():
                    print(f"  {Colors.CYAN}{key}:{Colors.END} {value}")
            except:
                print(stdout)
            
            input("\nPress Enter to continue...")

    def reverse_dns(self):
        """Reverse DNS lookup"""
        clear_screen()
        print_banner("=== REVERSE DNS LOOKUP ===\n")
        
        ip = get_input("IP adresi")
        
        if ip:
            cmd = f"dig -x {ip} +short"
            print_info(f"Running command: {cmd}")
            stdout, _, _ = run_command(cmd)
            
            if stdout.strip():
                print(f"\n{Colors.GREEN}Hostname:{Colors.END} {stdout}")
            else:
                print_warning("Reverse DNS kaydı bulunamadı")
            
            cmd2 = f"host {ip}"
            print_info(f"\nAlternatif kontrol: {cmd2}")
            run_command_live(cmd2)
            
            input("\nPress Enter to continue...")

    def asn_lookup(self):
        """ASN lookup"""
        clear_screen()
        print_banner("=== ASN LOOKUP ===\n")
        
        target = get_input("IP veya ASN numarası")
        
        if target:
            cmd = f"whois -h whois.radb.net {target}"
            print_info(f"Running command: {cmd}")
            run_command_live(cmd)
            
            input("\nPress Enter to continue...")

    def tech_stack(self):
        """Website technology detection"""
        clear_screen()
        print_banner("=== TECHNOLOGY STACK ===\n")
        
        url = get_input("Target URL")
        
        if url:
            if check_tool("whatweb"):
                cmd = f"whatweb -a 3 -v {url}"
                print_info(f"Running command: {cmd}")
                run_command_live(cmd)
            else:
                print_info("Curl ile header kontrolü yapılıyor...")
                cmd = f"curl -s -I {url}"
                run_command_live(cmd)
            
            input("\nPress Enter to continue...")

    def wayback_check(self):
        """Wayback Machine check"""
        clear_screen()
        print_banner("=== WAYBACK MACHINE ===\n")
        
        url = get_input("Target URL/Domain")
        
        if url:
            if check_tool("waybackurls"):
                timestamp = get_timestamp()
                output_file = f"{self.output_dir}/wayback_{timestamp}.txt"
                cmd = f"echo {url} | waybackurls | tee {output_file}"
                print_info(f"Running command: {cmd}")
                run_command_live(cmd)
            else:
                api_url = f"http://web.archive.org/cdx/search/cdx?url={url}/*&output=text&fl=original&collapse=urlkey"
                print_info(f"Wayback API sorgulanıyor...")
                cmd = f"curl -s \"{api_url}\" | head -50"
                run_command_live(cmd)
            
            input("\nPress Enter to continue...")

    def cert_transparency(self):
        """Certificate Transparency logs"""
        clear_screen()
        print_banner("=== CERTIFICATE TRANSPARENCY ===\n")
        
        domain = get_input("Target domain")
        
        if domain:
            print_info("crt.sh sorgulanıyor...")
            cmd = f"curl -s \"https://crt.sh/?q=%25.{domain}&output=json\" | jq -r '.[].name_value' | sort -u"
            
            if not check_tool("jq"):
                print_warning("jq is not installed, ham çıktı gösterilecek")
                cmd = f"curl -s \"https://crt.sh/?q=%25.{domain}&output=json\""
            
            print_info(f"Running command: {cmd}")
            run_command_live(cmd)
            
            input("\nPress Enter to continue...")
