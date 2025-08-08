import os
import pathlib
import logging
import psutil

# Reference to current file
try:
    FILE = pathlib.Path(__file__)
except NameError:
    FILE = pathlib.Path("logger.py")
BASE = FILE.parent

# Global logger instance
logger = logging.getLogger('app_logger')

__all__ = ['log_memory_usage_function', 'configure_logger', 'logger']

# Process for memory measurements
_process = psutil.Process(os.getpid())

# Define emojis for log levels
LOG_EMOJIS = {
    'DEBUG': '🐛',
    'INFO': 'ℹ️',
    'WARNING': '⚠️',
    'ERROR': '❌',
    'CRITICAL': '🚨',
}

# -----------------------------
# Custom LogRecord Factory
# -----------------------------
_old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = _old_factory(*args, **kwargs)

    # Docker container ID
    record.container_id = os.getenv('HOSTNAME', 'unknown')

    # Memory info
    mem = _process.memory_info()
    record.mem_rss = mem.rss / (1024 ** 2)
    record.mem_vms = mem.vms / (1024 ** 2)

    # Add emoji based on log level
    record.emoji = LOG_EMOJIS.get(record.levelname, '❓')

    return record

# -----------------------------
# Function for Memory Profiling
# -----------------------------
def log_memory_usage_function(tag: str):
    proc = psutil.Process(os.getpid())
    rss = proc.memory_info().rss  / (1024 * 1024)
    vms = proc.memory_info().vms  / (1024 * 1024)
    logger.info(f"{tag} | 🧠 RSS={rss:.2f}MB 💾 VMS={vms:.2f}MB")
    return rss, vms


def configure_logger():
    # Set the custom LogRecord factory here, ensuring it's applied before any logs
    logging.setLogRecordFactory(record_factory)

    # Remove existing root handlers to prevent duplication
    root_logger = logging.getLogger()
    for h in root_logger.handlers[:]:
        root_logger.removeHandler(h)

    # Configure the global application logger
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Remove existing handlers from 'app_logger' to prevent duplicate logs
    for h in logger.handlers[:]:
        logger.removeHandler(h)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s+00:00 | [%(container_id)s] | %(emoji)s %(levelname)s | %(pathname)s:%(funcName)s:%(lineno)d | ' 
        '🧠 RSS=%(mem_rss).2fMB 💾 VMS=%(mem_vms).2fMB | %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Initialization log
    logger.info("✅ Logger initialized successfully")
    return logger