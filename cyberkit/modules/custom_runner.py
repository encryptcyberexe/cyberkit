"""
Custom Multi-Tool Runner - Execute multiple tools in sequence
"""

import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.helpers import *

class CustomRunner:
    def __init__(self):
        self.output_dir = create_output_dir("output/custom")
        self.tools = self._define_tools()
    
    def _define_tools(self):
        return {
            1: {"name": "Nmap Quick Scan", "cat": "Network", "cmd": "nmap -T4 -F {target}", "inputs": ["target"]},
            2: {"name": "Nmap Full Port", "cat": "Network", "cmd": "nmap -p- -T4 {target}", "inputs": ["target"]},
            3: {"name": "Nmap Service Scan", "cat": "Network", "cmd": "nmap -sV -sC {target}", "inputs": ["target"]},
            4: {"name": "Nmap Vuln Scan", "cat": "Network", "cmd": "nmap --script=vuln {target}", "inputs": ["target"]},
            5: {"name": "Nmap UDP Scan", "cat": "Network", "cmd": "nmap -sU --top-ports 100 {target}", "inputs": ["target"]},
            6: {"name": "Ping Sweep", "cat": "Network", "cmd": "nmap -sn {target}", "inputs": ["target"]},
            7: {"name": "ARP Scan", "cat": "Network", "cmd": "arp-scan -l", "inputs": []},
            10: {"name": "Gobuster Dir", "cat": "Web", "cmd": "gobuster dir -u {url} -w {wordlist}", "inputs": ["url", "wordlist"]},
            11: {"name": "Ffuf Fuzzing", "cat": "Web", "cmd": "ffuf -u {url}/FUZZ -w {wordlist}", "inputs": ["url", "wordlist"]},
            12: {"name": "Nikto Scan", "cat": "Web", "cmd": "nikto -h {url}", "inputs": ["url"]},
            13: {"name": "WhatWeb", "cat": "Web", "cmd": "whatweb -a 3 {url}", "inputs": ["url"]},
            14: {"name": "WPScan", "cat": "Web", "cmd": "wpscan --url {url} -e vp,vt,u", "inputs": ["url"]},
            15: {"name": "SQLMap", "cat": "Web", "cmd": "sqlmap -u \"{url}\" --batch --dbs", "inputs": ["url"]},
            16: {"name": "SSLScan", "cat": "Web", "cmd": "sslscan {target}", "inputs": ["target"]},
            17: {"name": "Nuclei Scan", "cat": "Web", "cmd": "nuclei -u {url}", "inputs": ["url"]},
            20: {"name": "WHOIS", "cat": "OSINT", "cmd": "whois {target}", "inputs": ["target"]},
            21: {"name": "DNS Enum", "cat": "OSINT", "cmd": "dig {target} ANY +noall +answer", "inputs": ["target"]},
            22: {"name": "theHarvester", "cat": "OSINT", "cmd": "theHarvester -d {target} -b all", "inputs": ["target"]},
            23: {"name": "Subfinder", "cat": "OSINT", "cmd": "subfinder -d {target}", "inputs": ["target"]},
            24: {"name": "DNSRecon", "cat": "OSINT", "cmd": "dnsrecon -d {target}", "inputs": ["target"]},
            25: {"name": "Sherlock", "cat": "OSINT", "cmd": "sherlock {username}", "inputs": ["username"]},
            30: {"name": "John Wordlist", "cat": "Password", "cmd": "john --wordlist={wordlist} {hashfile}", "inputs": ["hashfile", "wordlist"]},
            31: {"name": "Hashcat MD5", "cat": "Password", "cmd": "hashcat -m 0 {hashfile} {wordlist}", "inputs": ["hashfile", "wordlist"]},
            32: {"name": "Hydra SSH", "cat": "Password", "cmd": "hydra -l {user} -P {wordlist} ssh://{target}", "inputs": ["target", "user", "wordlist"]},
            33: {"name": "Hydra FTP", "cat": "Password", "cmd": "hydra -l {user} -P {wordlist} ftp://{target}", "inputs": ["target", "user", "wordlist"]},
            34: {"name": "CeWL Wordlist", "cat": "Password", "cmd": "cewl {url} -d 2 -m 5", "inputs": ["url"]},
            40: {"name": "SearchSploit", "cat": "Exploit", "cmd": "searchsploit {query}", "inputs": ["query"]},
            41: {"name": "Netcat Listen", "cat": "Exploit", "cmd": "nc -lvnp {port}", "inputs": ["port"]},
            50: {"name": "Airmon Start", "cat": "Wireless", "cmd": "airmon-ng start {interface}", "inputs": ["interface"]},
            51: {"name": "Airodump Scan", "cat": "Wireless", "cmd": "airodump-ng {interface}", "inputs": ["interface"]},
        }
    
    def show_menu(self):
        while True:
            clear_screen()
            print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║               CUSTOM MULTI-TOOL RUNNER                       ║
╠══════════════════════════════════════════════════════════════╣{Colors.END}
║   {Colors.CYAN}[1]{Colors.END}  Run Multiple Tools (Custom Selection)              ║
║   {Colors.CYAN}[2]{Colors.END}  View All Available Tools                           ║
║   {Colors.CYAN}[3]{Colors.END}  Quick Recon Preset                                 ║
║   {Colors.CYAN}[4]{Colors.END}  Web Pentest Preset                                 ║
║   {Colors.CYAN}[5]{Colors.END}  Full Enumeration Preset                            ║
║   {Colors.RED}[0]{Colors.END}  Back to Main Menu                                  ║
{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.END}
            """)
            choice = get_input("  Select")
            if choice == "0": break
            elif choice == "1": self.run_custom()
            elif choice == "2": self.view_tools()
            elif choice == "3": self.run_preset([1, 3, 13, 20, 21], "quick_recon")
            elif choice == "4": self.run_preset([10, 12, 13, 14, 16], "web_pentest")
            elif choice == "5": self.run_preset([1, 3, 4, 10, 12, 20, 21, 22], "full_enum")

    def view_tools(self):
        clear_screen()
        print(f"\n{Colors.CYAN}{'═'*60}{Colors.END}")
        print(f"{Colors.BOLD}  AVAILABLE TOOLS{Colors.END}")
        print(f"{Colors.CYAN}{'═'*60}{Colors.END}\n")
        cats = {}
        for n, t in self.tools.items():
            if t["cat"] not in cats: cats[t["cat"]] = []
            cats[t["cat"]].append((n, t))
        for cat, tools in cats.items():
            print(f"\n  {Colors.YELLOW}━━━ {cat.upper()} ━━━{Colors.END}")
            for n, t in tools:
                inp = ", ".join(t["inputs"]) if t["inputs"] else "none"
                print(f"  {Colors.CYAN}[{n:2d}]{Colors.END} {t['name']:<18} {Colors.GRAY}({inp}){Colors.END}")
        input("\n  Press Enter...")

    def run_custom(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  CUSTOM TOOL RUNNER{Colors.END}")
        print(f"  Network: 1-7 | Web: 10-17 | OSINT: 20-25 | Pass: 30-34 | Exploit: 40-41")
        sel = get_input("\n  Tool numbers (e.g., 1,10,20)")
        if not sel: return
        try:
            nums = [int(x.strip()) for x in sel.split(",")]
        except:
            print_error("Invalid input!"); input("\n  Enter..."); return
        tools = [(n, self.tools[n]) for n in nums if n in self.tools]
        if not tools: print_error("No valid tools!"); input("\n  Enter..."); return
        
        print(f"\n  {Colors.GREEN}Selected:{Colors.END}")
        for n, t in tools: print(f"    [{n}] {t['name']}")
        
        out_name = get_input("\n  Output filename", f"custom_{get_timestamp()}")
        out_name = "".join(c if c.isalnum() or c in '-_' else '_' for c in out_name)
        
        inputs = {}
        all_inp = set()
        for n, t in tools: all_inp.update(t["inputs"])
        
        defaults = {"wordlist": "/usr/share/wordlists/dirb/common.txt", "port": "4444", "interface": "wlan0"}
        prompts = {"target": "Target IP/Domain", "url": "URL (http://...)", "wordlist": "Wordlist", 
                   "hashfile": "Hash file", "user": "Username", "username": "Username", "query": "Search query",
                   "port": "Port", "interface": "Interface"}
        
        if all_inp:
            print(f"\n  {Colors.CYAN}Enter values:{Colors.END}")
            for inp in all_inp:
                p = prompts.get(inp, inp)
                d = defaults.get(inp, "")
                inputs[inp] = get_input(f"  {p}", d) if d else get_input(f"  {p}")
        
        if not confirm("\n  Execute?"): return
        self._execute(tools, inputs, out_name)

    def run_preset(self, nums, name):
        clear_screen()
        tools = [(n, self.tools[n]) for n in nums if n in self.tools]
        print(f"\n  {Colors.BOLD}PRESET: {name.upper()}{Colors.END}")
        for n, t in tools: print(f"    [{n}] {t['name']}")
        target = get_input("\n  Target")
        if not target: return
        out = get_input("  Output name", f"{name}_{get_timestamp()}")
        inputs = {"target": target, "url": target if "http" in target else f"http://{target}",
                  "wordlist": "/usr/share/wordlists/dirb/common.txt"}
        if confirm("\n  Start?"): self._execute(tools, inputs, out)

    def _execute(self, tools, inputs, out_name):
        clear_screen()
        print(f"\n{Colors.BOLD}  EXECUTING {len(tools)} TOOLS{Colors.END}\n")
        out_file = f"{self.output_dir}/{out_name}.txt"
        
        with open(out_file, 'w') as f:
            f.write(f"CYBERKIT SCAN - {datetime.now()}\n{'='*60}\n\n")
            for i, (n, t) in enumerate(tools, 1):
                print(f"\n  {Colors.YELLOW}[{i}/{len(tools)}] {t['name']}{Colors.END}")
                try:
                    cmd = t["cmd"].format(**inputs)
                except KeyError as e:
                    print_error(f"Missing: {e}"); continue
                print_info(f"  {cmd}")
                f.write(f"\n{'='*60}\n{t['name']}\nCMD: {cmd}\n{'='*60}\n")
                stdout, stderr, rc = run_command(cmd)
                if stdout:
                    print(stdout[:300] + "..." if len(stdout) > 300 else stdout)
                    f.write(stdout)
                if rc == 0: print_success("  Done!")
                else: print_warning(f"  Exit: {rc}")
        
        print_success(f"\n  Results saved: {out_file}")
        input("\n  Press Enter...")
