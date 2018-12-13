from setuptools import setup

setup(
    name='PlaymateAPI',
    version='0.1',
    long_description=__doc__,
    author="Maulana Yusuf",
    author_email="im.idiiot@gmail.com",
    packages=['playmate', 'playmate.resources', 'playmate.models', 'playmate.helpers'],
    include_package_data=True,
    install_requires=[
        'flask>=0.10.1',
        'flask-restful',
        'flask-restful-swagger',
        'raven[flask]',
        'Flask-PyMongo',
        'pymongo',
        'bcrypt',
        'flask-FCM',
        'python-dateutil',
        'flask-cors'
    ],
    dependency_links=[
    ]
)
