# Introduction

- Support py script deployment as job or online API
- Support r script deployment as online API
- Do not support Jupyter notebook directly and only can be deployed after converting it to py.
- Do not support deploy to SPARK environment and any customised environment.

## Prerequisites
Need to install a python library: ibm-watson-machine-learning as below
```
pip install ibm-watson-machine-learning
```


## Usage

1. Deploy any python project as batch job or online API, 
   refer to: [Deploy Python job and online API](./Deploy%20Python%20job%20and%20online%20API.md)
   
2. Although above script does support "online" deployment as well. 
It will run the whole python project when is called and it can be slow because some python projects will have pre-process, 
for example, 
   - install needed libraries
   - load large ML into memory.
Hence, we recommend to use [Deploy Python Online API with preprocess](./Deploy%20Python%20Online%20API%20with%20preprocess.md)

3. Deploy any R project as online API, 
   refer to: [Deploy R Online API](./Deploy%20R%20Online%20API.md)