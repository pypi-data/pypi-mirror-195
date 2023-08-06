"""Generest setup.py module."""
import gituptools

status = '4 - Beta'

if __name__ == '__main__':
    gituptools.setup(
        include_package_data=True,
        package_dir={'generest': 'generest'},
        package_data={'generest': ['static/*']},
        keywords=['Code Generation', 'DevOps', 'CICD', 'Packaging'],
        install_requires=[
            'black',
            'click',
            ],
        extras_require={},
        entry_points={
            'console_scripts': [],
            'gui_scripts': []
            },
        zip_safe=True,
        platforms=['Windows', 'Linux', 'Mac OS-X', 'Unix'],
        classifiers=[
            'Development Status :: %s' % status,
            'Topic :: Utilities',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Code Generators',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: OS Independent',
            'Typing :: Typed',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            ]
        )
