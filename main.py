#!/usr/bin/env python3
"""
Dead by Daylight Communication App
Main entry point for the application
"""

from dbd_app import DbDCommunicationApp
import sys
import os
import logging
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def setup_logging():
    """Setup logging configuration"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "dbd_app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main entry point"""
    try:
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting DbD Communication App")

        # Create and run the application
        app = DbDCommunicationApp()
        app.run()

    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
