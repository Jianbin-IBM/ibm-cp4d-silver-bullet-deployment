# MNIST example

To get deployed as online deployment using https://github.com/Jianbin-IBM/ibm-cp4d-silver-bullet-deployment

Simply modify the template: 
```
prj_info:
  code_dir: [code dir]/mnist
  main_file: main_online.py

```

Please use "test_main_online.py" to test your deployment before the deployment, 
which has exactly same behavior of online deployment.

An example "payload" input can be found in "test_main_online.py" 
when you want to test online through deployment space Web UI.