from setuptools import setup, find_packages

setup(
    name='ntru',
    version='0.1',
    description='NTRU Public Key Encryption in Python',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'docopt',
        'numpy',
        'sympy'
    ],
    extras_require={
    'dev': ['pytest', 'coverage']
    },
    entry_points={
        'console_scripts': [
            'ntru=ntru.cli:main'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Security :: Cryptography',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)

