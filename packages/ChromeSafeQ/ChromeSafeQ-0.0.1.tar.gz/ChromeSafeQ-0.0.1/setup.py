from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ChromeSafeQ',
  version='0.0.1',
  description='i dont know',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='SIR',
  author_email='sr.pentesters@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='chromepass', 
  packages=find_packages(),
  install_requires=[''] 
)
