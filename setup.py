import setuptools

setuptools.setup(
    name='watch-fs',
    version='0.6.0',

    author="Sam Clements",
    author_email="sam@borntyping.co.uk",

    url="https://github.com/borntyping/watch-fs",
    description="A command line tool to run commands when files change",
    long_description=open('README.rst').read(),

    py_modules=[
        'watch_fs'
    ],

    install_requires=[
        'click>=3.3',
        'pyinotify>=0.9.4'
    ],

    entry_points={
        'console_scripts': [
            'watch-fs = watch_fs:main',
        ]
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities'
    ],
)
