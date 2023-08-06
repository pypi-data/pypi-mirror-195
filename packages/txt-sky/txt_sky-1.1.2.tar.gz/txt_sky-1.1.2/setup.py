from distutils.core import setup
from setuptools import find_packages

setup(name='txt_sky',  # 包名
      version='1.1.2',  # 版本号
      description='A package for writing txt.',
      long_description='',
      author='Sky Vega Yang',
      author_email='xjgis@126.com',
      #maintainer='Bob Yang', 
      #maintainer_email='17511246@qq.com' ,
      url='https://pythonsky.com.cn/projects/txt_sky',
      license='',
      dependency_links=[
          "https://pypi.tuna.tsinghua.edu.cn/simple",
          "http://mirrors.aliyun.com/pypi/simple"
      ],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7'
          'Programming Language :: Python :: 3.8'
          'Programming Language :: Python :: 3.9'
          'Programming Language :: Python :: 3.10'
          'Programming Language :: Python :: 3.11',
          'Topic :: Utilities'
      ],
      keywords='',
      packages=find_packages('src'),  # 必填
      package_dir={'': 'src'},  # 必填
      include_package_data=True,
      )
