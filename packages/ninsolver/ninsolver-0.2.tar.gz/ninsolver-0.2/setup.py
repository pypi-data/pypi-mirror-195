import setuptools

with open("readme.md") as file:
	big_descr = file.read()

setuptools.setup(name='ninsolver',
      description='library for solving captchas using https://api.api-ninjas.com/v1',
      version = "0.2",
      packages=["ninsolver"],
      long_description = big_descr,
      long_description_content_type='text/markdown',
      author_email='bonnita1900432@gmail.com')
