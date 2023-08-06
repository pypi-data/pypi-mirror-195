"""
small code snippet that opens a gui window with a animated color

Author: Niels Maeder
"""
import pkg_resources

from colorbymood.color import hex_from_dict  # type:ignore
from colorbymood.window import Window  # type:ignore

__version__ = pkg_resources.get_distribution("colorbymood").version
