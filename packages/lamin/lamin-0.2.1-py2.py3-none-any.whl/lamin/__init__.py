__version__ = "0.2.1"  # denote a pre-release for 0.1.0 with 0.1rc1
from lamin_logger import logger

logger.warning(
    "Please,\n"
    " - replace `import lamin` with `import lamindb.setup as lnsetup`\n"
    " - run `pip uninstall lamin`\n"
    "lamindb.setup now has all of the lamin functionality\n"
    "The lamindb API and lamin API will be integrated soon!\n"
    "The CLI remains as is!"
)
import lndb as _lndb
from lndb import *

from . import dev

__doc__ = _lndb.__doc__.replace("lndb", "lamin")
