"""
Wireless Security Tools - WiFi Auditing
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.helpers import *

class WirelessTools:
    def __init__(self):
        self.output_dir = create_output_dir("output/wireless")
    
    def show_menu(self):
        while True:
            clear_screen()
            print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                   WIRELESS TOOLS                             ║
╠══════════════════════════════════════════════════════════════╣{Colors.END}
║   {Colors.CYAN}[1]{Colors.END}  List Wireless Interfaces                           ║
║   {Colors.CYAN}[2]{Colors.END}  Enable Monitor Mode                                ║
║   {Colors.CYAN}[3]{Colors.END}  Disable Monitor Mode                               ║
║   {Colors.CYAN}[4]{Colors.END}  Scan WiFi Networks                                 ║
║   {Colors.CYAN}[5]{Colors.END}  Airodump-ng Capture                                ║
║   {Colors.CYAN}[6]{Colors.END}  Deauth Attack                                      ║
║   {Colors.CYAN}[7]{Colors.END}  Capture Handshake                                  ║
║   {Colors.CYAN}[8]{Colors.END}  Crack WPA with Wordlist                            ║
║   {Colors.CYAN}[9]{Colors.END}  Create Evil Twin AP                                ║
║   {Colors.RED}[0]{Colors.END}  Back                                               ║
{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.END}
            """)
            choice = get_input("  Select")
            if choice == "0": break
            elif choice == "1": self.list_interfaces()
            elif choice == "2": self.enable_monitor()
            elif choice == "3": self.disable_monitor()
            elif choice == "4": self.scan_wifi()
            elif choice == "5": self.airodump_capture()
            elif choice == "6": self.deauth_attack()
            elif choice == "7": self.capture_handshake()
            elif choice == "8": self.crack_wpa()
            elif choice == "9": self.evil_twin()

    def list_interfaces(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  WIRELESS INTERFACES{Colors.END}\n")
        run_command_live("iwconfig 2>/dev/null | grep -E '^[a-z]'")
        print()
        run_command_live("ip link show | grep -E '^[0-9]+:|state'")
        input("\n  Press Enter...")

    def enable_monitor(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  ENABLE MONITOR MODE{Colors.END}\n")
        if not check_root():
            print_error("Root required!"); input("\n  Enter..."); return
        iface = get_input("  Interface", "wlan0")
        print_info("  Killing interfering processes...")
        run_command("airmon-ng check kill")
        print_info(f"  Enabling monitor mode on {iface}...")
        run_command_live(f"airmon-ng start {iface}")
        print_success(f"  Monitor mode enabled (probably {iface}mon)")
        input("\n  Press Enter...")

    def disable_monitor(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  DISABLE MONITOR MODE{Colors.END}\n")
        iface = get_input("  Interface", "wlan0mon")
        run_command_live(f"airmon-ng stop {iface}")
        run_command("service NetworkManager restart")
        print_success("  Monitor mode disabled")
        input("\n  Press Enter...")

    def scan_wifi(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  SCAN WIFI NETWORKS{Colors.END}\n")
        iface = get_input("  Interface", "wlan0")
        print_info("  Scanning (Ctrl+C to stop)...")
        run_command_live(f"iwlist {iface} scan 2>/dev/null | grep -E 'Cell|ESSID|Channel|Signal|Encryption'")
        input("\n  Press Enter...")

    def airodump_capture(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  AIRODUMP-NG CAPTURE{Colors.END}\n")
        if not check_tool("airodump-ng"):
            print_error("aircrack-ng not installed!"); input("\n  Enter..."); return
        iface = get_input("  Monitor interface", "wlan0mon")
        print_warning("  Press Ctrl+C to stop capture")
        run_command_live(f"airodump-ng {iface}")
        input("\n  Press Enter...")

    def deauth_attack(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  DEAUTH ATTACK{Colors.END}\n")
        print_warning("  Use only on networks you own or have permission!")
        if not confirm("  Continue?"): return
        
        iface = get_input("  Monitor interface", "wlan0mon")
        bssid = get_input("  Target BSSID (AP MAC)")
        client = get_input("  Client MAC (or 'all')", "FF:FF:FF:FF:FF:FF")
        count = get_input("  Packet count", "10")
        
        if client.lower() == "all":
            cmd = f"aireplay-ng -0 {count} -a {bssid} {iface}"
        else:
            cmd = f"aireplay-ng -0 {count} -a {bssid} -c {client} {iface}"
        
        print_info(f"  {cmd}")
        run_command_live(cmd)
        input("\n  Press Enter...")

    def capture_handshake(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  CAPTURE WPA HANDSHAKE{Colors.END}\n")
        iface = get_input("  Monitor interface", "wlan0mon")
        bssid = get_input("  Target BSSID")
        channel = get_input("  Channel")
        outfile = get_input("  Output prefix", f"{self.output_dir}/capture")
        
        cmd = f"airodump-ng -c {channel} --bssid {bssid} -w {outfile} {iface}"
        print_info(f"  {cmd}")
        print_warning("  Wait for handshake, then Ctrl+C")
        run_command_live(cmd)
        input("\n  Press Enter...")

    def crack_wpa(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  CRACK WPA HANDSHAKE{Colors.END}\n")
        capfile = get_input("  Capture file (.cap)")
        wordlist = get_input("  Wordlist", "/usr/share/wordlists/rockyou.txt")
        
        if check_tool("aircrack-ng"):
            cmd = f"aircrack-ng -w {wordlist} {capfile}"
            print_info(f"  {cmd}")
            run_command_live(cmd)
        else:
            print_error("aircrack-ng not found!")
        input("\n  Press Enter...")

    def evil_twin(self):
        clear_screen()
        print(f"\n{Colors.BOLD}  EVIL TWIN AP{Colors.END}\n")
        print_warning("  Educational purposes only!")
        
        if not check_tool("hostapd"):
            print_error("hostapd required: apt install hostapd")
            input("\n  Enter..."); return
        
        ssid = get_input("  SSID name")
        iface = get_input("  Interface", "wlan0")
        channel = get_input("  Channel", "6")
        
        config = f"""interface={iface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel={channel}
macaddr_acl=0
ignore_broadcast_ssid=0
"""
        conf_file = f"{self.output_dir}/hostapd.conf"
        with open(conf_file, 'w') as f: f.write(config)
        print_success(f"  Config saved: {conf_file}")
        print_info(f"  Run: hostapd {conf_file}")
        input("\n  Press Enter...")
