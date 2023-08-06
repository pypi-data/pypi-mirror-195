from setuptools import setup,find_packages
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
def get_long_description():
    with open(os.path.join(THIS_FOLDER, 'README.md'), 'rb') as f:
        long_description = f.read().decode('utf-8')
    return long_description

setup(
    name = 'uadatasdk',
    version = '0.0.1',
    description = 'Widening data acquisition program',
    author = '',
    author_email='',
    license='Apache License v2',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    install_requires=['numpy','pandas','thriftpy2','pymysql'],
    padkages = find_packages(),
    zip_safe=False,
    platforms=["all"],
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],

)
