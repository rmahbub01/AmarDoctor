import logging
import asyncio
from doctor.db.init_db import init_db
from doctor.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    db = SessionLocal()
    await init_db(db)


async def main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())