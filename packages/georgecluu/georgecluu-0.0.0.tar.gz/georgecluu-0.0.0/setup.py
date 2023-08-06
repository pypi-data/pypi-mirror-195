from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
    name = "georgecluu",
    version = "0.0.0",
    author = "George",
    author_email = "pavlovgeorgem@yandex.ru",
    url = "https://github.com/Georgepop/api_my_task",
    description='A very basic calculator',
    long_description=open('README.txt').read(), 
    license='MIT', 
    classifiers=classifiers,
    keywords='calculator', 
    packages=find_packages(),
    install_requires=[
    'requests',
    'importlib-metadata; python_version == "3.5"',
    ],
    python_requires='>=3.5',
)