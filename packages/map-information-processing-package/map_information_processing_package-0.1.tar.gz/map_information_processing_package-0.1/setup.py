from setuptools import setup, find_packages

# setup(
#     name='map_information_processing_package', # 自定义包名
#     version='1.0.1', # 包的版本号
#     description='test to create package', # 描述信息
#     author='Wang Cheng', # 作者
#     py_modules=[
#         'map_information_processing_package.my_module',
#         'map_information_processing_package.sum_package.sum_module'
#     ] # 包中包含的模块
# )

setup(
    name='map_information_processing_package',
    version='0.1',
    author='wangsongtao',
    author_email='732639860@qq.com',
    description='My Package for map information processing',
    packages=find_packages(),
    # install_requires=[
    #     'numpy>=1.18.0',
    #     'pandas>=1.0.0'
    # ]
)