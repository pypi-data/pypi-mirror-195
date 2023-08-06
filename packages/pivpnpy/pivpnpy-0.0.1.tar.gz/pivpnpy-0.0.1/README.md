## Description
A thin python wrapper for pivpn

## Installation

###From pypi
```shell
pip3 install pivpnpy
```

###From this git repo:
```shell
# Ensure you have setuptools >= 21.3
python3 -m pip install --upgrade pip

git clone https://github.com/m00ninite/pivpnpy.git
cd pivpnpy
python3 -m pip install -e .
```


## Usage
```python3
from pivpnpy import pivpn

# Create a user
pivpn.create_profile(user="Hello_World", ttl=1080)

# List users
profiles = pivpn.list_profiles()
print(profiles[0]['status'])  # Prints "Valid"

# Delete a user
pivpn.delete_profile(user="Hello_World") 
```