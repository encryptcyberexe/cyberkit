"""
UI utilities for better terminal display
"""

import os
import shutil

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
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'

def get_terminal_width():
    """Get terminal width"""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80

def print_success(msg):
    print(f"{Colors.GREEN}[✓] {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}[✗] {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}[!] {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}[*] {msg}{Colors.END}")

def print_status(msg):
    print(f"{Colors.CYAN}[~] {msg}{Colors.END}")

def print_banner(text):
    print(f"{Colors.MAGENTA}{Colors.BOLD}{text}{Colors.END}")

def print_header(title):
    """Print a formatted header"""
    width = min(get_terminal_width(), 70)
    print(f"\n{Colors.CYAN}{'═' * width}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.WHITE}  {title}{Colors.END}")
    print(f"{Colors.CYAN}{'═' * width}{Colors.END}\n")

def print_section(title):
    """Print a section divider"""
    width = min(get_terminal_width(), 60)
    print(f"\n{Colors.YELLOW}{'─' * width}{Colors.END}")
    print(f"{Colors.BOLD}{title}{Colors.END}")
    print(f"{Colors.YELLOW}{'─' * width}{Colors.END}")

def print_table(headers, rows):
    """Print a formatted table"""
    if not rows:
        print_warning("No data to display")
        return
    
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    header_line = " │ ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
    print(f"{Colors.BOLD}{Colors.CYAN}{header_line}{Colors.END}")
    print(f"{Colors.GRAY}{'─' * (sum(col_widths) + 3 * (len(headers) - 1))}{Colors.END}")
    
    for row in rows:
        row_line = " │ ".join(f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row))
        print(row_line)

def print_menu_item(number, text, color=None):
    """Print a formatted menu item"""
    c = color if color else Colors.CYAN
    print(f"  {c}[{number}]{Colors.END}  {text}")

def print_box(title, content_lines, width=60):
    """Print content in a box"""
    print(f"\n{Colors.CYAN}╔{'═' * (width - 2)}╗{Colors.END}")
    print(f"{Colors.CYAN}║{Colors.BOLD}{title.center(width - 2)}{Colors.END}{Colors.CYAN}║{Colors.END}")
    print(f"{Colors.CYAN}╠{'═' * (width - 2)}╣{Colors.END}")
    for line in content_lines:
        padding = width - 4 - len(line)
        print(f"{Colors.CYAN}║{Colors.END}  {line}{' ' * padding}{Colors.CYAN}║{Colors.END}")
    print(f"{Colors.CYAN}╚{'═' * (width - 2)}╝{Colors.END}\n")

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def progress_bar(current, total, prefix='Progress', length=40):
    """Print a progress bar"""
    percent = current / total
    filled = int(length * percent)
    bar = '█' * filled + '░' * (length - filled)
    print(f"\r{Colors.CYAN}{prefix}: [{bar}] {percent:.1%}{Colors.END}", end='', flush=True)
    if current == total:
        print()
