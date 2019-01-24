from setuptools import setup, find_packages

setup(
    name='flask-rest',
    version='0.1.0',
    description='The skeleton rest app for flask on mongodb',
    long_description='',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='flask rest micro-service skeleton mongodb',
    url='http://github.com/alex-pro27/flask_rest',
    author='Aleksandr Protsenko',
    author_email='al.pro@mail.ru',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        "flask==1.0.2",
        "python-socketio==2.0.0",
        "Flask-SocketIO==3.0.2",
        "flask-mongoengine==0.9.5",
        "simplejson==3.16.0",
        "fire==0.1.3"
    ],
    include_package_data=True,
    zip_safe=True,
)