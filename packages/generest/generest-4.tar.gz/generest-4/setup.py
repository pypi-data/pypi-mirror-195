"""Generest setup.py module."""
import gituptools

cli = 'generest'

if __name__ == '__main__':
    gituptools.setup(
        python_requires='>=3.9',
        install_requires=[
            'click'
            ],
        entry_points={
            'console_scripts': [
                f'{cli!s} = generest.cli:main'
                ]
            }
        )
