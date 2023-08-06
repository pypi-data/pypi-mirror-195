from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='polynomial_operations',
  version='0.0.2',
  description='A very basic polynomial calculator.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Sejal Farkya',
  author_email='sejalfarkya@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='polynomial', 
  packages=find_packages(),
  install_requires=[''] 
)