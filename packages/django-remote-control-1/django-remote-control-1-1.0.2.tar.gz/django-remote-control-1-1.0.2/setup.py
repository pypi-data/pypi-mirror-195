from distutils.core import setup

setup(
    name = 'django-remote-control-1',
    packages = ['remote_control'],
    version = '1.0.2',
    install_requires=[
        'requests',
    ],
    description = 'Securely call commands in other django applications.',
    author = 'Luke Sapan',
    author_email = 'lukevsapan@gmail.com',
    url = 'https://github.com/ramkasula2019/django-remote-control',
    download_url = 'https://github.com/ramkasula2019/django-remote-control/archive/1.0.2.tar.gz',
    keywords = ['django', 'remote' 'commands', 'rpc'],
    classifiers = [],
)
