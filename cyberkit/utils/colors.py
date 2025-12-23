"""
Color utilities for terminal output
"""

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}[+] {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}[-] {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}[!] {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}[*] {msg}{Colors.END}")

def print_status(msg):
    print(f"{Colors.CYAN}[~] {msg}{Colors.END}")

def print_banner(text):
    print(f"{Colors.MAGENTA}{Colors.BOLD}{text}{Colors.END}")
