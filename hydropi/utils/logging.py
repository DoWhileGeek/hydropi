import logging


def setup_logging():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        filename="~/hydropi.log",
        level=logging.DEBUG,
    )
