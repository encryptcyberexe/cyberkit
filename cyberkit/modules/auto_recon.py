"""
Automated Recon Pipeline - Full target reconnaissance
"""

import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.helpers import *

class AutoRecon:
    def __init__(self):
        self.output_dir = create_output_dir("output/recon")
    
    def show_menu(self):
        while True:
            clear_screen()
            print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║              AUTOMATED RECON PIPELINE                        ║
╠══════════════════════════════════════════════════════════════╣{Colors.END}
║   {Colors.CYAN}[1]{Colors.END}  Full Auto Recon (All-in-One)                       ║
║   {Colors.CYAN}[2]{Colors.END}  Network Recon Only                                 ║
║   {Colors.CYAN}[3]{Colors.END}  Web Recon Only                                     ║
║   {Colors.CYAN}[4]{Colors.END}  OSINT Recon Only                                   ║
║   {Colors.CYAN}[5]{Colors.END}  Subdomain Discovery                                ║
║   {Colors.RED}[0]{Colors.END}  Back                                               ║
{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.END}
            """)
            choice = get_input("  Select")
            if choice == "0": break
            elif choice == "1": self.full_recon()
            elif choice == "2": self.network_recon()
            elif choice == "3": self.web_recon()
            elif choice == "4": self.osint_recon()
            elif choice == "5": self.subdomain_recon()

    def full_recon(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  FULL AUTO RECON{Colors.END}\n")
        target = get_input("  Target (IP/Domain)")
        if not target: return
        
        ts = get_timestamp()
        out_dir = f"{self.output_dir}/{target.replace('.','_')}_{ts}"
        os.makedirs(out_dir, exist_ok=True)
        
        stages = [
            ("WHOIS Lookup", f"whois {target}", "whois.txt"),
            ("DNS Records", f"dig {target} ANY +noall +answer", "dns.txt"),
            ("Port Scan", f"nmap -sV -sC -T4 {target}", "nmap.txt"),
            ("Web Fingerprint", f"whatweb -a 3 {target}", "whatweb.txt"),
        ]
        
        if check_tool("subfinder"):
            stages.append(("Subdomains", f"subfinder -d {target}", "subdomains.txt"))
        if check_tool("theHarvester"):
            stages.append(("Email Harvest", f"theHarvester -d {target} -b google,bing", "harvester.txt"))
        
        print(f"\n  {Colors.YELLOW}Starting {len(stages)} stages...{Colors.END}\n")
        
        for i, (name, cmd, outfile) in enumerate(stages, 1):
            print(f"  [{i}/{len(stages)}] {Colors.CYAN}{name}{Colors.END}")
            stdout, _, rc = run_command(cmd)
            with open(f"{out_dir}/{outfile}", 'w') as f:
                f.write(f"# {name}\n# CMD: {cmd}\n\n{stdout}")
            if rc == 0: print_success(f"    Saved: {outfile}")
            else: print_warning(f"    Partial: {outfile}")
        
        self._generate_summary(out_dir, target)
        print_success(f"\n  All results: {out_dir}/")
        input("\n  Press Enter...")

    def network_recon(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  NETWORK RECON{Colors.END}\n")
        target = get_input("  Target (IP/CIDR)")
        if not target: return
        
        ts = get_timestamp()
        out_dir = f"{self.output_dir}/net_{ts}"
        os.makedirs(out_dir, exist_ok=True)
        
        stages = [
            ("Ping Sweep", f"nmap -sn {target}", "hosts.txt"),
            ("Quick Ports", f"nmap -T4 -F {target}", "ports_quick.txt"),
            ("Service Scan", f"nmap -sV --top-ports 1000 {target}", "services.txt"),
        ]
        
        for i, (name, cmd, outfile) in enumerate(stages, 1):
            print(f"  [{i}/{len(stages)}] {name}")
            stdout, _, _ = run_command(cmd)
            with open(f"{out_dir}/{outfile}", 'w') as f: f.write(stdout)
            print_success(f"    Done")
        
        print_success(f"\n  Results: {out_dir}/")
        input("\n  Press Enter...")

    def web_recon(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  WEB RECON{Colors.END}\n")
        url = get_input("  Target URL")
        if not url: return
        if not url.startswith("http"): url = f"http://{url}"
        
        ts = get_timestamp()
        out_dir = f"{self.output_dir}/web_{ts}"
        os.makedirs(out_dir, exist_ok=True)
        
        stages = [
            ("Fingerprint", f"whatweb -a 3 {url}", "fingerprint.txt"),
            ("Headers", f"curl -sI {url}", "headers.txt"),
            ("Robots.txt", f"curl -s {url}/robots.txt", "robots.txt"),
        ]
        
        if check_tool("gobuster"):
            stages.append(("Dir Enum", f"gobuster dir -u {url} -w /usr/share/wordlists/dirb/common.txt -q", "dirs.txt"))
        if check_tool("nikto"):
            stages.append(("Nikto", f"nikto -h {url} -maxtime 300", "nikto.txt"))
        
        for i, (name, cmd, outfile) in enumerate(stages, 1):
            print(f"  [{i}/{len(stages)}] {name}")
            stdout, _, _ = run_command(cmd)
            with open(f"{out_dir}/{outfile}", 'w') as f: f.write(stdout)
            print_success(f"    Done")
        
        print_success(f"\n  Results: {out_dir}/")
        input("\n  Press Enter...")

    def osint_recon(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  OSINT RECON{Colors.END}\n")
        target = get_input("  Target (Domain)")
        if not target: return
        
        ts = get_timestamp()
        out_dir = f"{self.output_dir}/osint_{ts}"
        os.makedirs(out_dir, exist_ok=True)
        
        stages = [
            ("WHOIS", f"whois {target}", "whois.txt"),
            ("DNS", f"dig {target} ANY", "dns.txt"),
            ("MX Records", f"dig {target} MX +short", "mx.txt"),
            ("NS Records", f"dig {target} NS +short", "ns.txt"),
        ]
        
        if check_tool("theHarvester"):
            stages.append(("Harvester", f"theHarvester -d {target} -b all -l 200", "harvester.txt"))
        
        for i, (name, cmd, outfile) in enumerate(stages, 1):
            print(f"  [{i}/{len(stages)}] {name}")
            stdout, _, _ = run_command(cmd)
            with open(f"{out_dir}/{outfile}", 'w') as f: f.write(stdout)
        
        print_success(f"\n  Results: {out_dir}/")
        input("\n  Press Enter...")

    def subdomain_recon(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  SUBDOMAIN DISCOVERY{Colors.END}\n")
        domain = get_input("  Domain")
        if not domain: return
        
        ts = get_timestamp()
        outfile = f"{self.output_dir}/subs_{domain}_{ts}.txt"
        all_subs = set()
        
        tools = [
            ("subfinder", f"subfinder -d {domain} -silent"),
            ("amass", f"amass enum -passive -d {domain}"),
            ("assetfinder", f"assetfinder --subs-only {domain}"),
        ]
        
        for name, cmd in tools:
            if check_tool(name):
                print_info(f"  Running {name}...")
                stdout, _, _ = run_command(cmd)
                subs = [s.strip() for s in stdout.split('\n') if s.strip()]
                all_subs.update(subs)
                print_success(f"    Found {len(subs)} subdomains")
        
        with open(outfile, 'w') as f:
            f.write('\n'.join(sorted(all_subs)))
        
        print_success(f"\n  Total unique: {len(all_subs)}")
        print_success(f"  Saved: {outfile}")
        input("\n  Press Enter...")

    def _generate_summary(self, out_dir, target):
        summary = f"{out_dir}/SUMMARY.txt"
        with open(summary, 'w') as f:
            f.write(f"RECON SUMMARY - {target}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*50 + "\n\n")
            for file in os.listdir(out_dir):
                if file != "SUMMARY.txt":
                    f.write(f"[+] {file}\n")
