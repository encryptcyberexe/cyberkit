"""
Logging System for CyberKit
Provides centralized logging functionality
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class CyberKitLogger:
    """Centralized logging system for CyberKit"""
    
    def __init__(self, log_file='./logs/cyberkit.log', level='INFO', 
                 max_bytes=10485760, backup_count=5):
        """
        Initialize logger
        
        Args:
            log_file (str): Path to log file
            level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            max_bytes (int): Maximum log file size before rotation
            backup_count (int): Number of backup files to keep
        """
        self.log_file = log_file
        self.level = getattr(logging, level.upper(), logging.INFO)
        self.logger = self._setup_logger(max_bytes, backup_count)
        
    def _setup_logger(self, max_bytes, backup_count):
        """
        Set up logger with file and console handlers
        
        Args:
            max_bytes (int): Maximum file size
            backup_count (int): Number of backups
            
        Returns:
            logging.Logger: Configured logger instance
        """
        # Create logger
        logger = logging.getLogger('CyberKit')
        logger.setLevel(self.level)
        
        # Prevent duplicate handlers
        if logger.handlers:
            return logger
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler with rotation
        try:
            file_handler = RotatingFileHandler(
                self.log_file, 
                maxBytes=max_bytes, 
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(self.level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"[!] Warning: Could not create log file handler: {e}")
        
        return logger
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log critical message"""
        self.logger.critical(message)
    
    def log_command(self, command, module='Unknown'):
        """
        Log executed command
        
        Args:
            command (str): Command that was executed
            module (str): Module name that executed the command
        """
        self.info(f"[{module}] Executing: {command}")
    
    def log_scan_start(self, target, scan_type, module='Unknown'):
        """
        Log scan start
        
        Args:
            target (str): Scan target
            scan_type (str): Type of scan
            module (str): Module name
        """
        self.info(f"[{module}] Starting {scan_type} scan on target: {target}")
    
    def log_scan_complete(self, target, scan_type, status='Success', module='Unknown'):
        """
        Log scan completion
        
        Args:
            target (str): Scan target
            scan_type (str): Type of scan
            status (str): Scan status (Success/Failed)
            module (str): Module name
        """
        self.info(f"[{module}] {scan_type} scan on {target} - Status: {status}")
    
    def log_error_with_trace(self, error, context=''):
        """
        Log error with traceback
        
        Args:
            error (Exception): Exception object
            context (str): Additional context information
        """
        import traceback
        error_msg = f"Error: {str(error)}"
        if context:
            error_msg = f"{context} - {error_msg}"
        self.error(error_msg)
        self.debug(traceback.format_exc())
    
    def log_user_action(self, action, details=''):
        """
        Log user action
        
        Args:
            action (str): Action performed
            details (str): Additional details
        """
        msg = f"User Action: {action}"
        if details:
            msg += f" - {details}"
        self.info(msg)
    
    def log_tool_check(self, tool_name, is_installed):
        """
        Log tool availability check
        
        Args:
            tool_name (str): Name of the tool
            is_installed (bool): Whether tool is installed
        """
        status = "Available" if is_installed else "Missing"
        self.debug(f"Tool Check: {tool_name} - {status}")


# Global logger instance
_logger = None

def get_logger():
    """
    Get global logger instance
    
    Returns:
        CyberKitLogger: Logger instance
    """
    global _logger
    if _logger is None:
        try:
            from .config_loader import get_config
            config = get_config()
            
            if config.is_logging_enabled():
                _logger = CyberKitLogger(
                    log_file=config.get_log_file(),
                    level=config.get_log_level(),
                    max_bytes=config.get('logging.max_size', 10485760),
                    backup_count=config.get('logging.backup_count', 5)
                )
            else:
                # Create a null logger if logging is disabled
                _logger = NullLogger()
        except:
            # Fallback to default logger if config fails
            _logger = CyberKitLogger()
    
    return _logger


class NullLogger:
    """Null logger that does nothing (used when logging is disabled)"""
    
    def debug(self, message): pass
    def info(self, message): pass
    def warning(self, message): pass
    def error(self, message): pass
    def critical(self, message): pass
    def log_command(self, command, module='Unknown'): pass
    def log_scan_start(self, target, scan_type, module='Unknown'): pass
    def log_scan_complete(self, target, scan_type, status='Success', module='Unknown'): pass
    def log_error_with_trace(self, error, context=''): pass
    def log_user_action(self, action, details=''): pass
    def log_tool_check(self, tool_name, is_installed): pass
