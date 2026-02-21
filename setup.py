"""Setup for Universal Screenshot Agent."""

from setuptools import setup, find_packages
import os

here = os.path.dirname(os.path.abspath(__file__))

# Read requirements
with open(os.path.join(here, "requirements.txt")) as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Read README for long description
readme_path = os.path.join(here, "README.md")
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="universal-screenshot-agent",
    version="1.0.0",
    description="Product-agnostic documentation screenshot pipeline using Playwright + PIL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["knowledge_base*", "knowledge_base.*"]),
    include_package_data=True,
    package_data={
        "universal_screenshot_agent": [
            "products/_template/*.yaml",
            "products/_template/*.py",
            "products/thrive_apprentice/*.yaml",
            "products/thrive_apprentice/*.py",
            "products/thrive_apprentice/docs/*.md",
            "products/thrive_apprentice/*.json",
        ],
    },
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "screenshot-agent=universal_screenshot_agent.run:main",
        ],
    },
)
