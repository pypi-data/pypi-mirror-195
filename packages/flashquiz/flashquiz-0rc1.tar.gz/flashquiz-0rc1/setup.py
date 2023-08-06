from setuptools import setup, find_packages


setup(
    name='flashquiz',
    version="0.rc1",
    description='Practice your flashcards using python',
    author='mike-fmh',
    author_email='mikemh@uri.edu',
    license='MIT',
    packages=find_packages(),
    entry_points={'console_scripts': ['flashquiz = flashquiz.quizzer:main']},
    install_requires=[
        'pygame',
        'argparse'
    ]
)
