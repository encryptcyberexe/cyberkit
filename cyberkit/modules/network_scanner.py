"""
Network Scanner Module - Nmap Integration and Network Utilities
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.helpers import *

class NetworkScanner:
    def __init__(self):
        self.output_dir = create_output_dir("output/network")
        
    def show_menu(self):
        """Display network scanner menu"""
        while True:
            clear_screen()
            print_banner("""
╔═══════════════════════════════════════════════════════════╗
║               NETWORK SCANNER MODULE                       ║
╚═══════════════════════════════════════════════════════════╝
            """)
            print(f"""
{Colors.CYAN}[1]{Colors.END} Quick Port Scan
{Colors.CYAN}[2]{Colors.END} Full Port Scan
{Colors.CYAN}[3]{Colors.END} Service Version Detection
{Colors.CYAN}[4]{Colors.END} OS Detection
{Colors.CYAN}[5]{Colors.END} Vulnerability Scan (NSE Scripts)
{Colors.CYAN}[6]{Colors.END} Stealth Scan (SYN)
{Colors.CYAN}[7]{Colors.END} UDP Scan
{Colors.CYAN}[8]{Colors.END} Network Discovery
{Colors.CYAN}[9]{Colors.END} Aggressive Scan
{Colors.CYAN}[10]{Colors.END} Custom Nmap Command
{Colors.CYAN}[11]{Colors.END} Ping Sweep
{Colors.CYAN}[12]{Colors.END} ARP Scan
{Colors.CYAN}[0]{Colors.END} Back to Main Menu
            """)
            
            choice = get_input("Your choice")
            
            if choice == "0":
                break
            elif choice == "1":
                self.quick_scan()
            elif choice == "2":
                self.full_port_scan()
            elif choice == "3":
                self.service_version_scan()
            elif choice == "4":
                self.os_detection()
            elif choice == "5":
                self.vuln_scan()
            elif choice == "6":
                self.stealth_scan()
            elif choice == "7":
                self.udp_scan()
            elif choice == "8":
                self.network_discovery()
            elif choice == "9":
                self.aggressive_scan()
            elif choice == "10":
                self.custom_nmap()
            elif choice == "11":
                self.ping_sweep()
            elif choice == "12":
                self.arp_scan()
            else:
                print_error("Invalid selection!")
                input("\nPress Enter to continue...")

    def _run_nmap(self, target, options, scan_name):
        """Run nmap with given options"""
        if not check_tool("nmap"):
            print_error("Nmap is not installed! Install with 'apt install nmap'.")
            return
            
        timestamp = get_timestamp()
        output_file = f"{self.output_dir}/{scan_name}_{target.replace('/', '_')}_{timestamp}"
        
        cmd = f"nmap {options} -oN {output_file}.txt -oX {output_file}.xml {target}"
        print_info(f"Running command: {cmd}")
        print_status("Starting scan...\n")
        
        output, returncode = run_command_live(cmd)
        
        if returncode == 0:
            print_success(f"\nScan completed! Results: {output_file}.txt")
        else:
            print_error("Error occurred during scan!")
        
        input("\nPress Enter to continue...")

    def quick_scan(self):
        """Quick port scan - top 1000 ports"""
        clear_screen()
        print_banner("=== QUICK PORT SCAN ===\n")
        target = get_input("Target IP/Domain/CIDR")
        if target:
            self._run_nmap(target, "-T4 -F", "quick_scan")

    def full_port_scan(self):
        """Full port scan - all 65535 ports"""
        clear_screen()
        print_banner("=== FULL PORT SCAN ===\n")
        target = get_input("Target IP/Domain/CIDR")
        if target:
            print_warning("This may take a long time...")
            self._run_nmap(target, "-p- -T4", "full_port_scan")

    def service_version_scan(self):
        """Service version detection"""
        clear_screen()
        print_banner("=== SERVICE VERSION DETECTION ===\n")
        target = get_input("Target IP/Domain")
        ports = get_input("Ports (empty=top 1000)", "")
        port_opt = f"-p {ports}" if ports else ""
        if target:
            self._run_nmap(target, f"-sV {port_opt} -T4", "service_version")

    def os_detection(self):
        """OS detection scan"""
        clear_screen()
        print_banner("=== OS DETECTION ===\n")
        if not check_root():
            print_error("This scan requires root privileges!")
            input("\nPress Enter to continue...")
            return
        target = get_input("Target IP/Domain")
        if target:
            self._run_nmap(target, "-O -T4", "os_detection")

    def vuln_scan(self):
        """Vulnerability scan using NSE scripts"""
        clear_screen()
        print_banner("=== VULNERABILITY SCAN ===\n")
        target = get_input("Target IP/Domain")
        if target:
            print_info("Running NSE vuln scripts...")
            self._run_nmap(target, "-sV --script=vuln -T4", "vuln_scan")

    def stealth_scan(self):
        """SYN stealth scan"""
        clear_screen()
        print_banner("=== STEALTH SCAN (SYN) ===\n")
        if not check_root():
            print_error("This scan requires root privileges!")
            input("\nPress Enter to continue...")
            return
        target = get_input("Target IP/Domain")
        if target:
            self._run_nmap(target, "-sS -T4", "stealth_scan")

    def udp_scan(self):
        """UDP port scan"""
        clear_screen()
        print_banner("=== UDP SCAN ===\n")
        if not check_root():
            print_error("This scan requires root privileges!")
            input("\nPress Enter to continue...")
            return
        target = get_input("Target IP/Domain")
        ports = get_input("Ports (empty=top 1000)", "")
        port_opt = f"-p {ports}" if ports else "--top-ports 1000"
        if target:
            print_warning("UDP scan can be slow...")
            self._run_nmap(target, f"-sU {port_opt} -T4", "udp_scan")

    def network_discovery(self):
        """Network discovery - find live hosts"""
        clear_screen()
        print_banner("=== NETWORK DISCOVERY ===\n")
        target = get_input("Target network (e.g.: 192.168.1.0/24)")
        if target:
            self._run_nmap(target, "-sn -T4", "network_discovery")

    def aggressive_scan(self):
        """Aggressive scan - OS, version, scripts, traceroute"""
        clear_screen()
        print_banner("=== AGGRESSIVE SCAN ===\n")
        if not check_root():
            print_error("This scan requires root privileges!")
            input("\nPress Enter to continue...")
            return
        target = get_input("Target IP/Domain")
        if target:
            print_warning("This scan generates heavy traffic!")
            self._run_nmap(target, "-A -T4", "aggressive_scan")

    def custom_nmap(self):
        """Run custom nmap command"""
        clear_screen()
        print_banner("=== CUSTOM NMAP COMMAND ===\n")
        print_info("Example: -sV -sC -p 22,80,443 192.168.1.1")
        options = get_input("Nmap parameters (after nmap)")
        if options:
            cmd = f"nmap {options}"
            print_info(f"Running command: {cmd}")
            run_command_live(cmd)
            input("\nPress Enter to continue...")

    def ping_sweep(self):
        """Ping sweep to find live hosts"""
        clear_screen()
        print_banner("=== PING SWEEP ===\n")
        target = get_input("Target network (e.g.: 192.168.1.0/24)")
        if target:
            self._run_nmap(target, "-sn -PE -T4", "ping_sweep")

    def arp_scan(self):
        """ARP scan for local network"""
        clear_screen()
        print_banner("=== ARP SCAN ===\n")
        if not check_tool("arp-scan"):
            print_error("arp-scan is not installed! Install with 'apt install arp-scan'.")
            input("\nPress Enter to continue...")
            return
        if not check_root():
            print_error("This scan requires root privileges!")
            input("\nPress Enter to continue...")
            return
            
        interface = get_input("Network interface", "eth0")
        cmd = f"arp-scan -l -I {interface}"
        print_info(f"Running command: {cmd}")
        run_command_live(cmd)
        input("\nPress Enter to continue...")
