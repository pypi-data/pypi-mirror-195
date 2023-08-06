from setuptools import setup

setup(
    name='PyModuleGenerator',
    version='1.0.0',
    description='A simple python module generator',
    url='https://github.com/ProfesseurIssou/PyModuleGenerator',
    author='Alix Hamidou',
    author_email='alix.hamidou@gmail.com',
    license='MIT',
    packages=['PyModuleGenerator'],
    install_requires=[
        'setuptools==63.2.0',
        'twine==3.8.0',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
