from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='shawid',
  version='0.0.1',
  description='Hardware-Id Auth using pastebin.com and SHA256 for whitelisting',
  long_description='This is a authentification for your Python projects. It uses my Shacrypt library for encrypting the hardware-ids. The hwids are stored on Pastebin, where you can easily add and remove the hwids, giving you full control of your software at any time.',
  url='',  
  author='64biit',
  author_email='sixtyfourblit@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=[''] 
)
