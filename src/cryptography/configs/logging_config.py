import logging


def setup_logging(name: str, log_level: str = "INFO", *, format_string: str | None = None) -> None:
    log_level = log_level.upper()

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    console_handler: logging.Handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    formatter: logging.Formatter = logging.Formatter(format_string)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.propagate = False
    return logger
