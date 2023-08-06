from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='feature_engineer_hurlok',
    version='0.0.1',
    url='https://github.com/illiamw/PackagePiP',
    license='MIT License',
    author='William Ferreira',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='williambox37@gmail.com',
    keywords='Pacote',
    description=u'Exemplo de pacote PyPI',
    packages=['feature_engineer_hurlok'],
    install_requires=['numpy', 'pandas'])