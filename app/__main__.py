from app.client import run
from app.utils import logging

if __name__ == "__main__":
    _logger = logging.setup_logger().bind(type="business")
    try:
        run()
    except (KeyboardInterrupt, SystemExit):
        _logger.info("Client stopped")
