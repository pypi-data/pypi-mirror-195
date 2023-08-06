"""Generest setup.py module."""
import gituptools

status = '4 - Beta'

if __name__ == '__main__':
    gituptools.setup(
        python_requires='>=3.9',
        install_requires=['click'],
        classifiers=[
            'Development Status :: %s' % status,
            'Topic :: Utilities',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Typing :: Typed',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            ]
        )
