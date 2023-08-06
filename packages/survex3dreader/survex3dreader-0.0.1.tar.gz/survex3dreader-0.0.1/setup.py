from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='survex3dreader',
      version='0.0.1',
      description='Reader for Survex 3d files .3d',
      url='https://github.com/RadostW/survex-3d-reader',
      author='Radost Waszkiewicz',
      author_email='radost.waszkiewicz@gmail.com',
      long_description=long_description,
      long_description_content_type='text/markdown',  # This is important!
      project_urls = {
          'Source': 'https://github.com/RadostW/survex-3d-reader'
      },
      license='GPL 2.0',
      install_requires = [],
      packages=['survex3dreader'],
      zip_safe=False)
