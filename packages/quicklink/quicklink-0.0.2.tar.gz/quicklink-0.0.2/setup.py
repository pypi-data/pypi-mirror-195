from setuptools import setup

with open('README.md', 'r') as md:
      long_description = md.read()

setup(name='quicklink',
      version='0.0.2',
      description='A simple command line tool to save a web URL as a file on your system.',
      url='https://github.com/CarlJKurtz/quicklink',
      author='Carl J. Kurtz',
      license='BSD 3-Clause',
      scripts=['src/quicklink'],
      py_modules=['quicklink'],
      package_dir={'': 'src'},
      long_description=long_description,
      long_description_content_type='text/markdown',
      keywords='url weblink file',
      classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Operating System :: OS Independent',
            'License :: OSI Approved :: BSD License',],
      )
