import setuptools

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="thai-citizen-id",
    version="0.1.3",
    author="Nopparut Saelim",
    author_email="ak3.nopparut@gmail.com",
    description="Thailand citizen ID tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nopparuts/thai-citizen-id",
    package_dir={"": "."},
    packages=['thai_citizen_id'],
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ]
)
