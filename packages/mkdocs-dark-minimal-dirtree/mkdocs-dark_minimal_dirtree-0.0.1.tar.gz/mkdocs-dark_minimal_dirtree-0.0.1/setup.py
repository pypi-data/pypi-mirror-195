from setuptools import setup, find_packages

VERSION = '0.0.1'

setup(
    name="mkdocs-dark_minimal_dirtree",
    version=VERSION,
    url='https://github.com/Jakkins/dark_minimal_dir_tree',
    license='MIT License',
    description='simple minimal dark theme for mkdocs with a holy dir tree.',
    author='jakkins',
    author_email='sjakkins@proton.me',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.themes': [
            'dark_minimal_dirtree = dark_minimal_dirtree',
        ]
    },
    zip_safe=False
)