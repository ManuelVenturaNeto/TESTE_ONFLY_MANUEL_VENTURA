import logging
import os
import asyncio
from src.main import main_pipeline
from src.main.routes import app


async def run_pipeline():
    logging.info("Start pipeline")
    await main_pipeline.run_pipeline()
    logging.info("Ended pipeline")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)s %(levelname)s, %(message)s",
        filename="./pipeline_logs.log",
    )

    # Execute the pipeline asynchronously
    asyncio.run(run_pipeline())

    SHOULD_RUN_FLASK = False

    if SHOULD_RUN_FLASK:
        logging.info("Starting Flask server")
        app.run(host="0.0.0.0", port=5000)
    else:
        logging.info("Flask server is not needed. Shutting down the container.")
        os._exit(0)
