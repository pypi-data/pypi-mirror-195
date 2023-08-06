from distutils.core import setup

# get packages from requirements.txt
with open('req.txt') as f:
    required = f.read().splitlines()



setup(name='Supbot-api',
        version='0.2',
        description='Supbot is a customer service bot can be integrated with any website',
        author='Supbot L.T.D',
        author_email="yousef.gamal.2951@gmail.com",
        install_requires=required,
        packages=['supbot-api'],
        classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],)

