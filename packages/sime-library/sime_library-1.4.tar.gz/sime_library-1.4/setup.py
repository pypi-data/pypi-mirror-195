from setuptools import setup
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='sime_library',
    version='1.4',
    description='Library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['sime_library'],
    license='MIT',
    author='Tudjewuj',
    author_email='dmiro306@gmail.com',
    url='https://dmitros-organization.gitbook.io/sime_library/',
    install_requires=[
        "colorama",
        "pyshorteners"
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
