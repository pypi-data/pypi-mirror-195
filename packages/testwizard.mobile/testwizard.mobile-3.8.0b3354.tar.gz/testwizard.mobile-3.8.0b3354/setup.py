import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testwizard.mobile",
    version="3.8.0b3354",
    author="Eurofins Digital Testing - Belgium",
    author_email="testwizard-support@eurofins-digitaltesting.com",
    description="Testwizard for Mobile testobjects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.eurofins-digitaltesting.com/testwizard/",
    packages=['testwizard.mobile'],
    install_requires=[
        'testwizard.test==3.8.0b3354',
        'testwizard.testobjects-core==3.8.0b3354',
        'testwizard.commands-audio==3.8.0b3354',
        'testwizard.commands-mobile==3.8.0b3354',
        'testwizard.commands-video==3.8.0b3354'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
    ],
)













