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
{Colors.CYAN}[1]{Colors.END} Hızlı Port Tarama (Quick Scan)
{Colors.CYAN}[2]{Colors.END} Tam Port Tarama (Full Port Scan)
{Colors.CYAN}[3]{Colors.END} Servis Versiyon Tespiti
{Colors.CYAN}[4]{Colors.END} OS Detection
{Colors.CYAN}[5]{Colors.END} Vulnerability Scan (NSE Scripts)
{Colors.CYAN}[6]{Colors.END} Stealth Scan (SYN)
{Colors.CYAN}[7]{Colors.END} UDP Scan
{Colors.CYAN}[8]{Colors.END} Ağ Keşfi (Network Discovery)
{Colors.CYAN}[9]{Colors.END} Agresif Tarama (Aggressive Scan)
{Colors.CYAN}[10]{Colors.END} Özel Nmap Komutu
{Colors.CYAN}[11]{Colors.END} Ping Sweep
{Colors.CYAN}[12]{Colors.END} ARP Scan
{Colors.CYAN}[0]{Colors.END} Ana Menüye Dön
            """)
            
            choice = get_input("Seçiminiz")
            
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
                print_error("Geçersiz seçim!")
                input("\nDevam etmek için Enter'a basın...")

    def _run_nmap(self, target, options, scan_name):
        """Run nmap with given options"""
        if not check_tool("nmap"):
            print_error("Nmap yüklü değil! 'apt install nmap' ile yükleyin.")
            return
            
        timestamp = get_timestamp()
        output_file = f"{self.output_dir}/{scan_name}_{target.replace('/', '_')}_{timestamp}"
        
        cmd = f"nmap {options} -oN {output_file}.txt -oX {output_file}.xml {target}"
        print_info(f"Çalıştırılan komut: {cmd}")
        print_status("Tarama başlatılıyor...\n")
        
        output, returncode = run_command_live(cmd)
        
        if returncode == 0:
            print_success(f"\nTarama tamamlandı! Sonuçlar: {output_file}.txt")
        else:
            print_error("Tarama sırasında hata oluştu!")
        
        input("\nDevam etmek için Enter'a basın...")

    def quick_scan(self):
        """Quick port scan - top 1000 ports"""
        clear_screen()
        print_banner("=== HIZLI PORT TARAMA ===\n")
        target = get_input("Hedef IP/Domain/CIDR")
        if target:
            self._run_nmap(target, "-T4 -F", "quick_scan")

    def full_port_scan(self):
        """Full port scan - all 65535 ports"""
        clear_screen()
        print_banner("=== TAM PORT TARAMA ===\n")
        target = get_input("Hedef IP/Domain/CIDR")
        if target:
            print_warning("Bu işlem uzun sürebilir...")
            self._run_nmap(target, "-p- -T4", "full_port_scan")

    def service_version_scan(self):
        """Service version detection"""
        clear_screen()
        print_banner("=== SERVİS VERSİYON TESPİTİ ===\n")
        target = get_input("Hedef IP/Domain")
        ports = get_input("Portlar (boş=top 1000)", "")
        port_opt = f"-p {ports}" if ports else ""
        if target:
            self._run_nmap(target, f"-sV {port_opt} -T4", "service_version")

    def os_detection(self):
        """OS detection scan"""
        clear_screen()
        print_banner("=== OS TESPİTİ ===\n")
        if not check_root():
            print_error("Bu tarama root yetkisi gerektirir!")
            input("\nDevam etmek için Enter'a basın...")
            return
        target = get_input("Hedef IP/Domain")
        if target:
            self._run_nmap(target, "-O -T4", "os_detection")

    def vuln_scan(self):
        """Vulnerability scan using NSE scripts"""
        clear_screen()
        print_banner("=== GÜVENLİK AÇIĞI TARAMASI ===\n")
        target = get_input("Hedef IP/Domain")
        if target:
            print_info("NSE vuln scriptleri çalıştırılıyor...")
            self._run_nmap(target, "-sV --script=vuln -T4", "vuln_scan")

    def stealth_scan(self):
        """SYN stealth scan"""
        clear_screen()
        print_banner("=== STEALTH SCAN (SYN) ===\n")
        if not check_root():
            print_error("Bu tarama root yetkisi gerektirir!")
            input("\nDevam etmek için Enter'a basın...")
            return
        target = get_input("Hedef IP/Domain")
        if target:
            self._run_nmap(target, "-sS -T4", "stealth_scan")

    def udp_scan(self):
        """UDP port scan"""
        clear_screen()
        print_banner("=== UDP TARAMASI ===\n")
        if not check_root():
            print_error("Bu tarama root yetkisi gerektirir!")
            input("\nDevam etmek için Enter'a basın...")
            return
        target = get_input("Hedef IP/Domain")
        ports = get_input("Portlar (boş=top 1000)", "")
        port_opt = f"-p {ports}" if ports else "--top-ports 1000"
        if target:
            print_warning("UDP taraması yavaş olabilir...")
            self._run_nmap(target, f"-sU {port_opt} -T4", "udp_scan")

    def network_discovery(self):
        """Network discovery - find live hosts"""
        clear_screen()
        print_banner("=== AĞ KEŞFİ ===\n")
        target = get_input("Hedef ağ (örn: 192.168.1.0/24)")
        if target:
            self._run_nmap(target, "-sn -T4", "network_discovery")

    def aggressive_scan(self):
        """Aggressive scan - OS, version, scripts, traceroute"""
        clear_screen()
        print_banner("=== AGRESİF TARAMA ===\n")
        if not check_root():
            print_error("Bu tarama root yetkisi gerektirir!")
            input("\nDevam etmek için Enter'a basın...")
            return
        target = get_input("Hedef IP/Domain")
        if target:
            print_warning("Bu tarama yoğun trafik oluşturur!")
            self._run_nmap(target, "-A -T4", "aggressive_scan")

    def custom_nmap(self):
        """Run custom nmap command"""
        clear_screen()
        print_banner("=== ÖZEL NMAP KOMUTU ===\n")
        print_info("Örnek: -sV -sC -p 22,80,443 192.168.1.1")
        options = get_input("Nmap parametreleri (nmap sonrası)")
        if options:
            cmd = f"nmap {options}"
            print_info(f"Çalıştırılan komut: {cmd}")
            run_command_live(cmd)
            input("\nDevam etmek için Enter'a basın...")

    def ping_sweep(self):
        """Ping sweep to find live hosts"""
        clear_screen()
        print_banner("=== PING SWEEP ===\n")
        target = get_input("Hedef ağ (örn: 192.168.1.0/24)")
        if target:
            self._run_nmap(target, "-sn -PE -T4", "ping_sweep")

    def arp_scan(self):
        """ARP scan for local network"""
        clear_screen()
        print_banner("=== ARP SCAN ===\n")
        if not check_tool("arp-scan"):
            print_error("arp-scan yüklü değil! 'apt install arp-scan' ile yükleyin.")
            input("\nDevam etmek için Enter'a basın...")
            return
        if not check_root():
            print_error("Bu tarama root yetkisi gerektirir!")
            input("\nDevam etmek için Enter'a basın...")
            return
            
        interface = get_input("Ağ arayüzü", "eth0")
        cmd = f"arp-scan -l -I {interface}"
        print_info(f"Çalıştırılan komut: {cmd}")
        run_command_live(cmd)
        input("\nDevam etmek için Enter'a basın...")
