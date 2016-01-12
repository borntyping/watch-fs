import setuptools

setuptools.setup(
    name='watch-fs',
    version='1.4.1',

    author="Sam Clements",
    author_email="sam@borntyping.co.uk",

    url="https://github.com/borntyping/watch-fs",
    description="Run commands when files change",
    long_description=open('README.rst').read(),
    license='MIT',

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
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities'
    ],
)
