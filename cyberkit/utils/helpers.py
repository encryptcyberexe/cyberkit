"""
Helper functions for CyberKit
Provides utility functions for system operations, validation, and command execution
"""

import subprocess
import os
import sys
import shutil
from datetime import datetime

def check_root():
    """
    Check if running as root/administrator
    
    Returns:
        bool: True if running with elevated privileges, False otherwise
    """
    try:
        return os.geteuid() == 0
    except AttributeError:
        # Windows doesn't have geteuid
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False

def check_tool(tool_name):
    """Check if a tool is installed"""
    return shutil.which(tool_name) is not None

def run_command(command, shell=True, capture=True):
    """Run a shell command and return output"""
    try:
        if capture:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True
            )
            return result.stdout, result.stderr, result.returncode
        else:
            result = subprocess.run(command, shell=shell)
            return "", "", result.returncode
    except Exception as e:
        return "", str(e), 1

def run_command_live(command):
    """Run command with live output"""
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        output = []
        for line in iter(process.stdout.readline, ''):
            print(line, end='')
            output.append(line)
        process.wait()
        return ''.join(output), process.returncode
    except Exception as e:
        return str(e), 1

def validate_ip(ip):
    """Validate IP address format"""
    import re
    pattern = r'^(\d{1,3}\.){3}\d{1,3}(/\d{1,2})?$'
    if re.match(pattern, ip):
        parts = ip.split('/')[0].split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    return False

def validate_domain(domain):
    """Validate domain format"""
    import re
    pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))

def validate_url(url):
    """Validate URL format"""
    import re
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url, re.IGNORECASE))

def get_timestamp():
    """Get current timestamp for reports"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def create_output_dir(base_dir="output"):
    """Create output directory if not exists"""
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    return base_dir

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def get_input(prompt, default=None):
    """Get user input with optional default"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()

def confirm(prompt):
    """Ask for yes/no confirmation"""
    response = input(f"{prompt} [y/N]: ").strip().lower()
    return response in ['y', 'yes']
