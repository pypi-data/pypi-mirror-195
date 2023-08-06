from setuptools import setup, find_packages

setup(
    name='motivate-me',
    version='0.1.0-alpha.1',
    author='Brandon Molyneaux',
    author_email='brandon@learningcodeonline.com',
    description='A package leveraging ChatGPT to print out motivational quotes and one-liners.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wxbdm/motivate-me',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'openai==0.27.0'
    ],
    python_requires='>=3.6',
)
