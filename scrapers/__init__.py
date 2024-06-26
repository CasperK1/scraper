import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from .verkkokauppa import get_data_verkkokauppa
from .datatronic import get_data_datatronic
from .jimms import get_data_jimms
from .proshop import get_data_proshop

