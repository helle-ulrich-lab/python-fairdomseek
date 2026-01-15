# python-fairdomseek

This is a VERY basic implementation of the [FAIRDOM-SEEK API](https://docs.seek4science.org/help/user-guide/api.html) in Python. No tests, no guarantees 😉.

# Pre-requisites

```shell
python>=3.10
requests>=2.32.3
```

## Installation

`git clone https://github.com/helle-ulrich-lab/python-fairdomseek`

with conda

`conda create -n fairdomseek_api python>=3.10 requests # ipykernel, for Jupyter`

with mamba

`mamba create -n fairdomseek_api python>=3.10 requests # ipykernel, for Jupyter`

## Usage

```python
from fairdomseek import fairdomseek

fs = fairdomseek()

# Log in
fs.login() # with username and password
# fs.login(token='my-token') # with token

fs.list('projects')
fs.fetch('projects', object_id='1')
fs.delete('projects', object_id='1')

# create and update methods are also available
```
