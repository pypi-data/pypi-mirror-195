from setuptools import setup

setup(
    name='helios-sim',
    version='0.1.0',
    description="6 DOF Rocket Simulator",
    author="Ronan",
    author_email="ronanmarkdsouza@gmail.com",
    packages=['helios'],
    install_requires=["numpy", "scipy", "python-dotenv", "matplotlib", "openpyxl", "pandas", "fpdf"],
    entry_points={
        "console_scripts": [
            "helios = helios.main:main"
        ]
    }

)