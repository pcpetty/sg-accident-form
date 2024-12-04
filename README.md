# Safety Generalist Accident Reporting System

The Safety Generalist Accident Reporting System is a Python-based tool designed to streamline accident data collection, storage, and reporting for safety professionals. With its modular design, the program efficiently handles driver and vehicle data, generates professional reports in multiple formats (Excel, PDF), and integrates seamlessly with PostgreSQL databases for long-term storage and analysis.

---

## **Features**
- **Accident Data Collection**: Collects detailed data about drivers, vehicles, weather conditions, and more.
- **Database Integration**: Stores and retrieves data from PostgreSQL.
- **Report Generation**: Exports reports in Excel and PDF formats.
- **Modular Design**: Clean separation of concerns for maintainability and scalability.
- **Editing Existing Reports**: Allows modification of stored reports.

---

## License
This program is proprietary software owned by [Phillip Cole Petty]. Unauthorized use, duplication, or modification is strictly prohibited.

For licensing inquiries, please contact: [colepetty57@gmail.com]

## Security
Please see the [Security Policy](SECURITY) for reporting vulnerabilities.

---

## **File Structure**
```
sg_accident_form/
│
├── sg_accident_form/       # Main package directory
│   ├── __init__.py         # Initialize the package
│   ├── main.py             # Main execution script
│   ├── data_collection.py  # Functions for data collection
│   ├── db_operations.py    # Database interaction functions
│   ├── report_generation.py # PDF/Excel export functions
│   └── utils.py            # Utility functions
│
├── tests/                  # Optional: Unit tests
│   ├── test_data_collection.py
│   ├── test_db_operations.py
│   └── test_report_generation.py
│
├── LICENSE                 # License file
├── README.md               # Project documentation
├── SECURITY.md             # Security information
├── requirements.txt        # Python dependencies
├── setup.py                # Setup script for packaging
├── pyproject.toml          # Optional: Modern build system configuration
└── .gitignore              # Git ignore file

```