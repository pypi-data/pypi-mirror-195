from termcolor import cprint
from colorama import just_fix_windows_console

just_fix_windows_console()

# LOGGER colors
LOG_LYNKZ_COLOR = "green"
LOG_INFO_COLOR = "cyan"
LOG_ERROR_COLOR = "red"
LOG_WARNING_COLOR = "yellow"

def print_lynkz(message):
    cprint(message, LOG_LYNKZ_COLOR)

def print_info(message):
    cprint(f'INFO: {message}', LOG_INFO_COLOR)

def print_error(message):
    cprint(f'ERROR: {message}', LOG_ERROR_COLOR)

def print_warning(message):
    cprint(f'WARNING: {message}', LOG_WARNING_COLOR)

def print_debug(message):
    cprint(f'DEBUG: {message}', LOG_LYNKZ_COLOR)
