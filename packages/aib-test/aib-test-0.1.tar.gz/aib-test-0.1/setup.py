from setuptools import setup

setup(
    name='aib-test',
    version='0.1',
    description='',
    long_description='',
    author='',
    author_email='',
    url='',
    license='MIT',
    python_requires='>=3.10',
    install_requires=[
        "ray==2.2.0",
        "scikit-learn==1.2.1",
        "xgboost==1.7.3",
        "mysql-connector-python==8.0.32",
        "dill==0.3.6"
    ],
    packages=["aib"]
)
