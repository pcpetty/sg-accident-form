from setuptools import setup, find_packages

setup(
    name="sg_accident_form",               # Name of the package
    version="1.0.0",                       # Package version
    description="Safety Generalist Accident Reporting System",  # Short description
    long_description=open("README.md").read(),  # Use README for a detailed description
    long_description_content_type="text/markdown",  # Specify Markdown content
    author="Cole Petty",                    # Author name
    author_email="colepetty57@gmail.com",   # Author email
    url="https://github.com/pcpetty/sg_accident_form",  # URL to GitHub repository
    packages=find_packages(),               # Automatically find packages
    include_package_data=True,              # Include non-Python files (e.g., templates, static files)
    install_requires=[
        "fpdf2>=2.7.0",                     # PDF generation library
        "psycopg2>=2.9.0",                  # PostgreSQL database driver
        "questionary>=1.10.0",              # CLI interaction library
        "openpyxl>=3.1.0",                  # Excel file creation and manipulation
    ],
    python_requires=">=3.8",                # Specify Python version compatibility
    entry_points={                          # Create CLI entry point
        "console_scripts": [
            "sg-accident-form=sg_accident_form.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",               # Supported Python version
        "License :: OSI Approved :: Proprietary License Agreement",  # Custom license
        "Operating System :: OS Independent",                  # OS compatibility
    ],
)
