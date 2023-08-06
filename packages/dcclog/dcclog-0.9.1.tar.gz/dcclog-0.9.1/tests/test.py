import logging

import dcclog
from dcclog.cipher.rsa import RSAEncryption

with open(".logs/app.log", "w") as f:
    pass

abc = dcclog.getLogger("abc")
abcsss = dcclog.getLogger("abc.sss")
dcclog.default_config(
    # level=dcclog.WARNING,
    filename=".logs/app.log",
    cipher=RSAEncryption("pubkey.pem"),
)
logger = dcclog.getLogger()


logger.error("error message.")
logger.warning("warning message.")
abc.info("info message.")
abc.debug("debug message.")
abcsss.debug("debug message22222.")
abcsss.warning("warn message22222.")
