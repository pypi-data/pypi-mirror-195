from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='SidsFirstmod',
  version='0.0.1',
  description='A funny module for trying out',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Siddharth Narayanan',
  author_email='siddharth1210@outlook.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Funny', 
  packages=find_packages(),
  install_requires=['webbrowser','time','pywhatkit'] 
)
