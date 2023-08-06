import os

import setuptools

"""
The python version should be 3.7 since 3.8 will cause errors in multiprocessing for macOS X.
Then, make sure you have installed
  numpy==1.21.5
  scipy==1.7.3
  pandas==1.3.5
  pytorch==1.13.1
  torchtext==0.5.0
  torchaudio==0.13.1
  torchvision==0.14.1
to avoid environment conflict.

The following packages are then required to support the *_test.py and running of this project:
  sentencepiece
  pytest
  requests
  autograd>=1.3
  portpicker>=1.3.1
  redis>=3.3.8
  semver>=2.13.0
  
The best way is to use pipreqs to generate the dependencies for kubega, and install with 
`python setup.py install --record installed.txt` or 
`pip install -r requirements.txt`.
"""


def read_requirements(file_path):
    requirements = []
    with open(file_path) as f:
        for line in f:
            if "#" in line:
                line = line[:line.index("#")]
            line = line.strip()
            if line and not line.startswith("-"):
                requirements.append(line)
    return requirements


if __name__ == '__main__':
    setuptools.setup(
        name="kubega",
        version=os.getenv("KUBEGA_VERSION", "0.0.0"),
        author="Petuum Inc. & The AdaptDL Authors",
        author_email="aurick.qiao@petuum.com",
        description="A copy of the adaptdl project "
                    "(Use is strictly limited to non-commercial areas, "
                    "only for studying and testing)",
        url="https://github.com/hliangzhao/kubega",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: Other/Proprietary License",
            "Operating System :: POSIX :: Linux",
        ],
        packages=setuptools.find_packages(include=["kubega",
                                                   "kubega.*"]),
        python_requires='>=3.7',
        install_requires=read_requirements("requirements.txt")
    )
