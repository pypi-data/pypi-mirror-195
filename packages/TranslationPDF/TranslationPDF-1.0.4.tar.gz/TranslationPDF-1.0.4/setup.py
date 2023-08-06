from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='TranslationPDF',
    version='1.0.4',
    license='MIT License',
    author='Willians Silva',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='09willians@gmail.com',
    keywords='pdf translation',
    description=u'TranslationPDF é um pacote para a tradução de PDF.',
    packages=['PDF_read'],
    install_requires=['pypdf2', 'googletrans==4.0.0rc1', 'fpdf2', 'pytesseract'])