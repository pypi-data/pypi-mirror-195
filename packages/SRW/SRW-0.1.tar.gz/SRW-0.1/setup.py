######################################################################################
# credits to: https://gist.github.com/afernandez119/52f2772a763f14a4bdae02fd5cfc791a #
######################################################################################
import pathlib
from setuptools import find_packages, setup

setup(
    name='SRW',
    version='0.1',
    description='Objects to make your own realistic games, simulators, and every thing you want',
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(encoding='utf-8'),
    long_description_content_type="text/markdown",
    author='Lucas Varela Correa',
    author_email='lucasvarelacorrea@gmail.com',
    url='https://github.com/SRW-Development/library',
    #install_requires=INSTALL_REQUIRES,
    license='MIT',
    #packages=find_packages(),
    include_package_data=True
)