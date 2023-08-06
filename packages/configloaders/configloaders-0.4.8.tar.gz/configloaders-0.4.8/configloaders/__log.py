import logging


logger = logging.getLogger(__package__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s : %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)