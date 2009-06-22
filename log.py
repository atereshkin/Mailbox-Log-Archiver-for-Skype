from gettext import gettext as _
import sys
import logging

def _init_logging(debug=False):
    log = logging.getLogger('mlas')
    handler = logging.StreamHandler(sys.stderr)
               
    if debug:
        log.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.WARNING)
        handler.setLevel(logging.WARNING)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.info(_("Logging has been initialized"))
