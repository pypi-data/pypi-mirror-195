from setuptools import setup, find_packages

setup(
    name='mailer_otphero',
    version='0.0.1',
    author="Yakov Wildfluss",
    author_email='yakov@otphero.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/wildfluss/mailer',
)
