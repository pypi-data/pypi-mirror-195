import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pylynkz',
    version='0.0.3',
    author='Alexandre Desgagné',
    author_email='alexd@lynkz.ca',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Lynkz-Instruments/pylynkz',
    license='MIT',
    packages=['pylynkz'],
    install_requires=['requests', 'termcolor', 'colorama>=0.4.6'],
    classifiers=[
        'Development Status :: 3 - Alpha',                # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',                # Define that your audience are developers
    ],

)
