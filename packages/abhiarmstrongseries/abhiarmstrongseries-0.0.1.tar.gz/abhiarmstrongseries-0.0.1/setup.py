from setuptools import setup, find_packages

classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
      name='abhiarmstrongseries',
      version='0.0.1',
      description='it checks and prints armstrong numbers',
      long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
      url='',
      author='Abhijith Krishna G',
      author_email='abhijithkrishnag234@gmail.com',
      license='MIT',
      classifiers=classifiers,
      keywords=['armstrong','strong','printarmstrong'],
      packages=find_packages(),
      install_requires=['']
)