from setuptools import setup, find_packages

setup(
    name='denari',
    version='1.0.21',
    description='DenariAnalytics OpenSouce Business and Tax Tools',
    author='Fadil Karim',
    author_email='insights@denarianalytics.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'plotly',
        'dash'
    ],
    package_data={
        'TaxTools': find_packages(include=['TaxTools', 'TaxTools.*']) + ['UK Tax Tables/*']
    }

)