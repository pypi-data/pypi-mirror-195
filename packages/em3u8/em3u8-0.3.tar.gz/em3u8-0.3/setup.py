from setuptools import setup

setup(
    name='em3u8',
    version='0.3',
    description='A simple m3u8 package',
    author='xiaotech',
    author_email='xiaotech@163.com',
    packages=['em3u8','em3u8.sites'],
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
