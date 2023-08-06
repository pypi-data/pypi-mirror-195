from setuptools import setup, find_packages


setup(
    name='bridgeaihub',
    version='0.0.2',
    license='MIT',
    author="bridgeaihub",
    author_email='contactus@bridgeaihub.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/bridgeaihub/AIModel_GPT2_TextGeneration',
    keywords='bridge gpt2',
    install_requires=[
          'streamlit',
          'tensorflow',
          'transformers',
      ],

)