from setuptools import setup,find_packages

setup(
    name='vget',
    version='0.31',
    description='A simple tool with m3u8 resouce download package',
    author='xiaotech',
    author_email='xiaotech@163.com',
    packages=find_packages(),
    license="Apache 2.0",
    url="https://vget.readthedocs.io",
    install_requires=[
        'loguru',
        'requests',
        'beautifulsoup4',
        'tqdm',
        'pycryptodome',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'vget=em3u8.cmd:main'
        ]
    }
)
