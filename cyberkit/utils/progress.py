"""
Progress Bar utilities for CyberKit
Provides visual feedback for long-running operations
"""

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    print("[!] tqdm not installed. Progress bars disabled. Install with: pip install tqdm")

from .colors import Colors

class ProgressBar:
    """Progress bar wrapper with fallback"""
    
    def __init__(self, total=100, desc="Processing", unit="it", disable=False):
        """
        Initialize progress bar
        
        Args:
            total (int): Total number of iterations
            desc (str): Description text
            unit (str): Unit name
            disable (bool): Disable progress bar
        """
        self.total = total
        self.desc = desc
        self.unit = unit
        self.disable = disable or not TQDM_AVAILABLE
        self.current = 0
        
        if TQDM_AVAILABLE and not self.disable:
            self.pbar = tqdm(
                total=total,
                desc=desc,
                unit=unit,
                bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]',
                colour='cyan'
            )
        else:
            self.pbar = None
            if not self.disable:
                print(f"{Colors.CYAN}[~] {desc}...{Colors.END}")
    
    def update(self, n=1):
        """Update progress by n steps"""
        self.current += n
        if self.pbar:
            self.pbar.update(n)
        elif not self.disable:
            percentage = (self.current / self.total) * 100 if self.total > 0 else 0
            if self.current % max(1, self.total // 10) == 0:  # Update every 10%
                print(f"{Colors.CYAN}[~] {self.desc}: {percentage:.1f}%{Colors.END}")
    
    def set_description(self, desc):
        """Update description text"""
        self.desc = desc
        if self.pbar:
            self.pbar.set_description(desc)
    
    def close(self):
        """Close progress bar"""
        if self.pbar:
            self.pbar.close()
        elif not self.disable:
            print(f"{Colors.GREEN}[+] {self.desc}: Complete!{Colors.END}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
        return False


def progress_wrapper(iterable, desc="Processing", unit="it", total=None):
    """
    Wrap an iterable with progress bar
    
    Args:
        iterable: Iterable to wrap
        desc (str): Description
        unit (str): Unit name
        total (int): Total items (auto-detected if None)
        
    Returns:
        Iterator with progress tracking
    """
    if TQDM_AVAILABLE:
        return tqdm(iterable, desc=desc, unit=unit, total=total, colour='cyan')
    else:
        # Fallback to simple iteration
        total = total or (len(iterable) if hasattr(iterable, '__len__') else None)
        if total:
            print(f"{Colors.CYAN}[~] {desc} ({total} {unit})...{Colors.END}")
        else:
            print(f"{Colors.CYAN}[~] {desc}...{Colors.END}")
        return iterable


class MultiProgress:
    """
    Manage multiple progress bars
    """
    
    def __init__(self):
        """Initialize multi-progress manager"""
        self.bars = {}
    
    def add_bar(self, name, total, desc=None):
        """
        Add a new progress bar
        
        Args:
            name (str): Unique identifier for this bar
            total (int): Total iterations
            desc (str): Description (uses name if None)
        """
        desc = desc or name
        self.bars[name] = ProgressBar(total=total, desc=desc)
        return self.bars[name]
    
    def update(self, name, n=1):
        """Update specific progress bar"""
        if name in self.bars:
            self.bars[name].update(n)
    
    def close_all(self):
        """Close all progress bars"""
        for bar in self.bars.values():
            bar.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_all()
        return False


# Convenience functions

def scan_progress(targets, desc="Scanning targets"):
    """
    Create progress bar for scanning operations
    
    Args:
        targets (list): List of targets
        desc (str): Description
        
    Returns:
        Progress bar iterator
    """
    return progress_wrapper(targets, desc=desc, unit="target")


def port_scan_progress(ports, desc="Scanning ports"):
    """
    Create progress bar for port scanning
    
    Args:
        ports (list): List of ports
        desc (str): Description
        
    Returns:
        Progress bar iterator
    """
    return progress_wrapper(ports, desc=desc, unit="port")


def file_progress(files, desc="Processing files"):
    """
    Create progress bar for file operations
    
    Args:
        files (list): List of files
        desc (str): Description
        
    Returns:
        Progress bar iterator
    """
    return progress_wrapper(files, desc=desc, unit="file")


# Example usage:
"""
# Simple usage
from cyberkit.utils.progress import progress_wrapper

targets = ['192.168.1.1', '192.168.1.2', '192.168.1.3']
for target in progress_wrapper(targets, desc="Scanning"):
    scan_target(target)

# With context manager
from cyberkit.utils.progress import ProgressBar

with ProgressBar(total=100, desc="Scanning") as pbar:
    for i in range(100):
        # Do work
        pbar.update(1)

# Multiple progress bars
from cyberkit.utils.progress import MultiProgress

with MultiProgress() as mp:
    mp.add_bar('nmap', 100, desc="Nmap scan")
    mp.add_bar('gobuster', 50, desc="Gobuster")
    
    for i in range(100):
        # Nmap work
        mp.update('nmap', 1)
    
    for i in range(50):
        # Gobuster work
        mp.update('gobuster', 1)
"""
