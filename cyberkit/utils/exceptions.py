"""
Exception Handling System for CyberKit
Custom exceptions and error handling decorators
"""

import functools
import traceback
from .colors import print_error, print_warning

class CyberKitException(Exception):
    """Base exception for CyberKit"""
    pass

class ToolNotFoundException(CyberKitException):
    """Raised when a required tool is not found"""
    pass

class InvalidTargetException(CyberKitException):
    """Raised when target format is invalid"""
    pass

class ConfigurationException(CyberKitException):
    """Raised when configuration is invalid"""
    pass

class PermissionException(CyberKitException):
    """Raised when insufficient permissions"""
    pass

class ScanException(CyberKitException):
    """Raised when a scan fails"""
    pass

class NetworkException(CyberKitException):
    """Raised when network operation fails"""
    pass


def handle_exceptions(show_traceback=False, default_return=None):
    """
    Decorator to handle exceptions gracefully
    
    Args:
        show_traceback (bool): Whether to show full traceback
        default_return: Default value to return on exception
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                print_warning("\n[!] Operation interrupted by user (Ctrl+C)")
                return default_return
            except ToolNotFoundException as e:
                print_error(f"Tool not found: {e}")
                print_warning("Install the tool and try again.")
                return default_return
            except InvalidTargetException as e:
                print_error(f"Invalid target: {e}")
                return default_return
            except PermissionException as e:
                print_error(f"Permission denied: {e}")
                print_warning("Try running with sudo/administrator privileges.")
                return default_return
            except ScanException as e:
                print_error(f"Scan failed: {e}")
                if show_traceback:
                    traceback.print_exc()
                return default_return
            except NetworkException as e:
                print_error(f"Network error: {e}")
                print_warning("Check your network connection and target availability.")
                return default_return
            except CyberKitException as e:
                print_error(f"CyberKit error: {e}")
                if show_traceback:
                    traceback.print_exc()
                return default_return
            except Exception as e:
                print_error(f"Unexpected error: {e}")
                if show_traceback:
                    traceback.print_exc()
                
                # Log the error if logger is available
                try:
                    from .logger import get_logger
                    logger = get_logger()
                    logger.log_error_with_trace(e, context=f"In function: {func.__name__}")
                except:
                    pass
                
                return default_return
        return wrapper
    return decorator


def safe_execute(func, *args, on_error=None, **kwargs):
    """
    Safely execute a function with error handling
    
    Args:
        func: Function to execute
        *args: Function arguments
        on_error: Value to return on error
        **kwargs: Function keyword arguments
        
    Returns:
        Function result or on_error value
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print_error(f"Error executing {func.__name__}: {e}")
        
        # Log the error if logger is available
        try:
            from .logger import get_logger
            logger = get_logger()
            logger.log_error_with_trace(e, context=f"Safe execute: {func.__name__}")
        except:
            pass
        
        return on_error


def validate_target(target, target_type='ip'):
    """
    Validate target format and raise exception if invalid
    
    Args:
        target (str): Target to validate
        target_type (str): Type of target ('ip', 'domain', 'url')
        
    Raises:
        InvalidTargetException: If target is invalid
    """
    from .helpers import validate_ip, validate_domain, validate_url
    
    if not target or not target.strip():
        raise InvalidTargetException("Target cannot be empty")
    
    target = target.strip()
    
    if target_type == 'ip':
        if not validate_ip(target):
            raise InvalidTargetException(f"Invalid IP address: {target}")
    elif target_type == 'domain':
        if not validate_domain(target):
            raise InvalidTargetException(f"Invalid domain: {target}")
    elif target_type == 'url':
        if not validate_url(target):
            raise InvalidTargetException(f"Invalid URL: {target}")
    
    return target


def require_tool(*tools):
    """
    Decorator to check if required tools are installed
    
    Args:
        *tools: Tool names to check
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            from .helpers import check_tool
            
            missing_tools = []
            for tool in tools:
                if not check_tool(tool):
                    missing_tools.append(tool)
            
            if missing_tools:
                raise ToolNotFoundException(
                    f"Missing required tools: {', '.join(missing_tools)}"
                )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_root(func):
    """
    Decorator to check if running with root privileges
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from .helpers import check_root
        
        if not check_root():
            raise PermissionException(
                f"{func.__name__} requires root/administrator privileges"
            )
        
        return func(*args, **kwargs)
    return wrapper


class ErrorHandler:
    """Context manager for error handling"""
    
    def __init__(self, error_message="An error occurred", 
                 raise_error=False, log_error=True):
        """
        Initialize ErrorHandler
        
        Args:
            error_message (str): Message to display on error
            raise_error (bool): Whether to re-raise the error
            log_error (bool): Whether to log the error
        """
        self.error_message = error_message
        self.raise_error = raise_error
        self.log_error = log_error
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print_error(f"{self.error_message}: {exc_val}")
            
            if self.log_error:
                try:
                    from .logger import get_logger
                    logger = get_logger()
                    logger.log_error_with_trace(exc_val, context=self.error_message)
                except:
                    pass
            
            if self.raise_error:
                return False  # Re-raise the exception
            
            return True  # Suppress the exception
        
        return True
