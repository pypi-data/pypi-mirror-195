# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name="torchdyn",
    version="1.0.4",
    author="Michael Poli and Stefano Massaroli",
    description="PyTorch package for all things neural differential equations.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/DiffEqML/torchdyn",
    install_requires=[
        "torch>=1.6.0",
        "pytorch-lightning>=0.8.4",
        "matplotlib",
        "scikit-learn",
        "torchsde>=0.2.5",
        "torchcde>=0.2.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
)
