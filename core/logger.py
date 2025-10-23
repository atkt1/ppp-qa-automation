import sys
from pathlib import Path
from loguru import logger


# Remove default handler
logger.remove()

# Configure console handler with custom format
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True,
)

# Add file handler for persistent logs
# Get project root (one level up from core/)
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logger.add(
    log_dir / "test_run_{time:YYYY-MM-DD}.log",
    rotation="10 MB",
    retention="10 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    compression="zip",
)

# Export configured logger
log = logger