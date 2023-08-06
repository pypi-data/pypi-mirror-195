from setuptools import setup
setup(
    name='ShellChat',
    author='Adriano R. de Sousa',
    version='0.5.0',
    packages=['shellchat'],
    description='A simple chat client for the terminal',
    long_description=open('README.md').read(),
    requires=[
        'click',
        'flask',
        # 'flask-socketio',
        # 'python-socketio',
        'aiohttp',
        'requests',
        'rich',
    ],
    license='MIT',
    entry_points={
        'console_scripts': [
            'ext = shellchat.__main__:main'
        ]
    },
)
