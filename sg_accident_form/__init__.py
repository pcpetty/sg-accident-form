# sg_accident_form/__init__.py

from .main import main
from .data_collection import collect_accident_data
from .db_operations import connect_postgresql, insert_into_postgresql
from .report_generation import export_to_excel, export_to_pdf
from .utils import utils

__all__ = [
    "main",
    "collect_accident_data",
    "connect_postgresql",
    "insert_into_postgresql",
    "export_to_excel",
    "export_to_pdf",
    "utils"
]

__version__ = "1.1.2"
__author__ = "Cole Petty"
