import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sr_calculator',
    version='0.0.2',
    author='Alishan Dhukka',
    author_email='alishandhukka@gmail.com',
    description='Tool for calculating key support and resistance levels',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/adhukka477/support_and_resistance_calculator.git',
    project_urls = {
        "Bug Tracker": "https://github.com/adhukka477/support_and_resistance_calculator.git"
    },
    license='MIT',
    packages=['sr_calculator'],
    install_requires=['numpy', 'datetime', 'yahoo-finance @ git+https://github.com/adhukka477/yahoo_finance.git'],
)
