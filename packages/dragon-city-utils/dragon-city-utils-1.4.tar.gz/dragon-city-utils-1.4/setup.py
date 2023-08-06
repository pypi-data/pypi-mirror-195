from setuptools import setup, find_packages

with open("README.md", "r") as file:
    readme_content = file.read()

setup(
    name="dragon-city-utils",
    version="1.4",
    license="MIT License",
    author="Marcuth",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    author_email="marcuth2006@gmail.com",
    keywords="dragoncity dcutils tools",
    description=f"Utilities and tools for things related to Dragon City",
    packages=[
        "dcutils",
        "dcutils/static",
        "dcutils/static/animations",
        "dcutils/static/animations/flash",
        "dcutils/static/animations/spine",
        "dcutils/static/sprites",
        "dcutils/static/islands",
        "dcutils/static/sounds",
        "dcutils/calculators",
        "dcutils/calculators/elements",
        "dcutils/calculators/food",
        "dcutils/calculators/orb_recall"
    ],
    install_requires=["httpx", "pydantic", "python-filter"],
)