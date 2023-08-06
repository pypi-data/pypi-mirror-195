from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name='IBLearning',
    version='1.0.0',
    description='IBLearning is a Python module that contains a set of tools to help you to make your own machine learning algorithms.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/IB-Solution/IBLearning',
    author='Alix Hamidou',
    author_email='alix.hamidou@gmail.com',
    license='MIT',
    packages=['IBLearning'],
    install_requires=[
        'nltk>=1.1.0',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],
)
