from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="INFO") 
logger.add(
    "logs/products.log",
    rotation="15 MB",
    retention="7 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO"
)