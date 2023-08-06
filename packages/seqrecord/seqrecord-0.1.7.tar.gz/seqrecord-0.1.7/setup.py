from setuptools import setup, find_packages

setup(
    name="seqrecord",
    version="0.1.7",
    description="update iterate record files and frame pairs for dealing with sequential record",
    author_email="shuhang0chen@gmail.com",
    maintainer_email="shuhang0chen@gmail.com",
    packages=find_packages(),
    install_requires=["numpy", "torch", "torchdata", "aiofiles"],
)
