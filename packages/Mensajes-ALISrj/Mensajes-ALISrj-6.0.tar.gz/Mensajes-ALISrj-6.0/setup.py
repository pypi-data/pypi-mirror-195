from setuptools import setup, find_packages

# Distribuible nos permite instalarlo en python para poder usarlo en cualquiera de nuestros proyecyos

setup(
    name="Mensajes-ALISrj",
    version="6.0",
    description="Un paquete para saludar y despedir",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author="ALISrj",
    author_email="alexis.rj2110@gmail.com",
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite="tests",
    install_requires=[paquete.strip()
                      for paquete in open("requirements.txt").readlines()],
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License'
    ]
)
