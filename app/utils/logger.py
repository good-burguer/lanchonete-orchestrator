import logging

logger = logging.getLogger("orchestrator")
logger.setLevel(logging.INFO)

console = logging.StreamHandler()
console.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s"))
logger.addHandler(console)
