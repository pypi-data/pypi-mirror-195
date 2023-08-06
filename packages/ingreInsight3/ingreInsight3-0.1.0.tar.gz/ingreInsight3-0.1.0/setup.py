from setuptools import setup, find_packages

setup(
    name='ingreInsight3',
    version='0.1.0',
    py_modules=['appCode'],
    description='A library for the Ingredient Insight app',
    author='Hunter White',
    packages=find_packages(),
    install_requires=[
        'pyzbar',
        'tenacity',
        'openai',
        'openfoodfacts',
    ],
)