from setuptools import setup

setup(
    name='EZ-AppInstaller',
    version='1.0',
    author='bananapizzuh',
    description="A cli tool to easily install applications that don't have an installer.",
    packages=['ez_appinstaller'],
    install_requires=[
        'rich_click',
        'pyyaml',
        'pywin32',
    ],
    entry_points={
        'console_scripts': [
            'ez-install=ez_appinstaller.cli:cli',
        ],
    },
    platforms=['win32', 'win64'],
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bananapizzuh/ez-appinstaller',
)