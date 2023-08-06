from setuptools import setup
setup(
    name='ShellChat',
    author='Adriano R. de Sousa',
    version='0.3.0',
    packages=['shellchat'],

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
