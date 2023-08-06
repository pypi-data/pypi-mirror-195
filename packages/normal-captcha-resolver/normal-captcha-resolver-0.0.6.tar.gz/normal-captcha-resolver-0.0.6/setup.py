from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='normal-captcha-resolver',
      version='0.0.6',
      license='MIT License',
      author='Marcone Santos',
      long_description=readme,
      long_description_content_type="text/markdown",
      author_email='ms5806166@gmail.com',
      keywords='normalcaptcha captcha normal normal-captcha',
      description=u'normal captcha resolver não oficial',
      packages=['normal_captcha'],
      install_requires=['pytesseract', 'opencv-python'], )
