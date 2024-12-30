from setuptools import setup, find_packages

setup(
    name="risk_ranger",
    version="1.0.0",
    description="Safety Generalist Accident Reporting System",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Cole Petty",
    author_email="colepetty57@gmail.com",
    url="https://github.com/pcpetty/sg_accident_form",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fpdf2>=2.7.0",
        "psycopg2>=2.9.0",
        "questionary>=1.10.0",
        "openpyxl>=3.1.0",
        "tkinter",
        "fpdf2>=2.7.0",
        "psycopg2==2.9.0",
        "questionary==1.10.0",
        "openpyxl==3.1.0",
        "PyQt6",
        "pyfiglet==0.8.post1",
        "streamlit",
        "pandas",
        "sqlalchemy",
        "numpy"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "sg-accident-form=sg_accident_form.main:main",  # CLI entry point
            "sg-accident-form-gui=sg_accident_form.gui:run_gui", # GUI Entry Point
            "risk_ranger_dashboard=risk_ranger.streamlit_dashboard:main" # WUI entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Proprietary License Agreement",
        "Operating System :: OS Independent",
    ],
)
