import logging

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("backend/error.log"), logging.StreamHandler()],
)

logger = logging.getLogger()
