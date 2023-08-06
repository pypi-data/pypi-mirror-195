from setuptools import setup, find_packages
setup(name='qztest',
      version='0.0.3',
      description='A Test Software With Python',
      author='WangZidi',
      author_email='wangzd@shanghaitech.edu.cn',
      requires= ['numpy','matplotlib','pywindow','scipy','rdkit','pyvoro','multiprocessing','sklearn','networkx','openbabel'],
      packages=find_packages(),  
      license="MIT License"
      )

