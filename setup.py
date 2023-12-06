import setuptools

setuptools.setup(
    name='coupon_validating_system',
    version='1.0.0',
    author='Lav Sharma',
    author_email='lavsharma2016@gmail.com',
    description='Coupon Validating System',
    long_description='',
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=['uvicorn>=0.16.0', 'fastapi>=0.83.0', 'sqlalchemy>=1.4.46', 'mysql_connector_python>=8.0.25',
                      'configparser>=6.0.0', 'retrying>=1.3.4']
)
