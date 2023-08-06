from setuptools import setup, find_packages


VERSION = '1.0.0'
DESCRIPTION = 'Free and open-source libary, use of calculating mathematician Questions.'
LONG_DESCRIPTION = f'{DESCRIPTION}\nIt contains few Classes with they functions. User can use it by Easily.'

setup(
    name='Mathematician',
    version=VERSION,
    author='Kartikey Baghel',
    author_email='kartikeybaghel@hotmail.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['arithmetics', 'math', 'python math', 'simple math', 'python geometry', 'mathematician', 'pcm', 'math for sci'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)