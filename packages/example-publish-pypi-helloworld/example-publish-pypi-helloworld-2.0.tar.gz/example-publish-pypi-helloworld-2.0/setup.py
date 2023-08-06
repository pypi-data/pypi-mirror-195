from setuptools import setup, find_packages


setup(
    name='example-publish-pypi-helloworld',
    version='2.0',
    author="ab cd",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='sample abc project',
    install_requires=[
         "cognite-sdk"
      ],

)