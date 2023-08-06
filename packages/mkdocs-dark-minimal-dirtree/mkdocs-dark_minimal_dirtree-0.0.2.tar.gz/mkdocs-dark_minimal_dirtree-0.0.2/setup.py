from setuptools import setup, find_packages

VERSION = "0.0.2"

setup(
    name="mkdocs-dark_minimal_dirtree",
    version=VERSION,
    url="https://github.com/Jakkins/dark_minimal_dirtree",
    license="MIT License",
    description="simple minimal dark theme for mkdocs with a holy dir tree.",
    author="jakkins",
    author_email="sjakkins@proton.me",
    packages=[
        "dark_minimal_dirtree/content",
        "dark_minimal_dirtree/css",
        "dark_minimal_dirtree/highlight",
        "dark_minimal_dirtree/js",
        "dark_minimal_dirtree/nav",
    ].append(find_packages()),
    package_data={
        "content": ["*.html"],
        "css": ["*.css"],
        "highlight": ["*.css", "*.js"],
        "js": ["*.js"],
        "nav": ["*.html"],
    },
    include_package_data=True,
    entry_points={
        "mkdocs.themes": [
            "dark_minimal_dirtree = dark_minimal_dirtree",
        ]
    },
    zip_safe=False,
)
