from setuptools import setup

setup(
    name='autoacu',
    version='0.3.0',
    # author='Your Name',
    description='Interpretable and Efficient Automatic Summarization Evaluation Metrics',
    packages=["autoacu"],
    extras_require={
        'stable': [
            'torch==1.12.1',
            'transformers==4.21.2',
        ]},
    url="https://github.com/Yale-LILY/AutoACU",
)