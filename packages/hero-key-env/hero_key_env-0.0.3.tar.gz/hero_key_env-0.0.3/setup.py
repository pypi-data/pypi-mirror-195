# Author: xuejinlin
# Date: 2023/3/7 22:48
# Author: xuejinlin
# Date: 2023/3/7 22:31
import setuptools
from pathlib import Path
setuptools.setup(
    name="hero_key_env",
    version="0.0.3",
    description="test",
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(include='hero_key_env*'),
    install_requires=['gym']
)