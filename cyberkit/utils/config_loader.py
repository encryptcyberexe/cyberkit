"""
Configuration Loader for CyberKit
Loads settings from config.yml file
"""

import os
import yaml
from pathlib import Path

class ConfigLoader:
    """Handles configuration loading and management"""
    
    def __init__(self, config_file="config.yml"):
        """
        Initialize ConfigLoader
        
        Args:
            config_file (str): Path to configuration file
        """
        self.config_file = config_file
        self.config = self._load_config()
        
    def _load_config(self):
        """
        Load configuration from YAML file
        
        Returns:
            dict: Configuration dictionary
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    return config if config else self._get_default_config()
            else:
                return self._get_default_config()
        except Exception as e:
            print(f"[!] Warning: Could not load config file: {e}")
            return self._get_default_config()
    
    def _get_default_config(self):
        """
        Return default configuration
        
        Returns:
            dict: Default configuration dictionary
        """
        return {
            'output': {
                'base_dir': './output',
                'auto_create': True
            },
            'logging': {
                'enabled': True,
                'level': 'INFO',
                'file': './logs/cyberkit.log',
                'max_size': 10485760,
                'backup_count': 5,
                'console_output': False
            },
            'tools': {
                'nmap': {
                    'default_timing': 'T4',
                    'default_output_format': ['txt', 'xml']
                }
            },
            'ui': {
                'clear_screen': True,
                'show_banner': True,
                'color_output': True,
                'progress_bar': True
            },
            'safety': {
                'confirm_dangerous_ops': True,
                'max_scan_targets': 256,
                'rate_limit': True
            }
        }
    
    def get(self, key_path, default=None):
        """
        Get configuration value by key path
        
        Args:
            key_path (str): Dot-separated key path (e.g., 'output.base_dir')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        try:
            keys = key_path.split('.')
            value = self.config
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_output_dir(self, module_name=None):
        """
        Get output directory path
        
        Args:
            module_name (str): Module name (e.g., 'network', 'web')
            
        Returns:
            str: Output directory path
        """
        base_dir = self.get('output.base_dir', './output')
        if module_name:
            return os.path.join(base_dir, module_name)
        return base_dir
    
    def get_api_key(self, service):
        """
        Get API key for a service
        
        Args:
            service (str): Service name (e.g., 'shodan', 'virustotal')
            
        Returns:
            str: API key or None
        """
        return self.get(f'api_keys.{service}', None)
    
    def is_logging_enabled(self):
        """
        Check if logging is enabled
        
        Returns:
            bool: True if logging is enabled
        """
        return self.get('logging.enabled', True)
    
    def get_log_file(self):
        """
        Get log file path
        
        Returns:
            str: Log file path
        """
        return self.get('logging.file', './logs/cyberkit.log')
    
    def get_log_level(self):
        """
        Get logging level
        
        Returns:
            str: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        return self.get('logging.level', 'INFO')


# Global config instance
_config = None

def get_config():
    """
    Get global configuration instance
    
    Returns:
        ConfigLoader: Configuration loader instance
    """
    global _config
    if _config is None:
        _config = ConfigLoader()
    return _config
