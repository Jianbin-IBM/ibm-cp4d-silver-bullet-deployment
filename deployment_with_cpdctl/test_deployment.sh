# test deploy with CPD Control

## python script
python deploy_with_cpdctl.py --yaml_file prod_py_test.yaml
python run_job_with_cpdctl.py --yaml_file prod_py_test.yaml

## python notebook
python deploy_with_cpdctl.py --yaml_file prod_py_notebook_test.yaml
python run_job_with_cpdctl.py --yaml_file prod_py_notebook_test.yaml

# r script
python deploy_r_with_cpdctl.py --yaml_file prod_r_script_test.yaml
python run_r_job_with_cpdctl.py --yaml_file prod_r_script_test.yaml

# r notebook
python deploy_r_with_cpdctl.py --yaml_file prod_r_notebook_test.yaml
python run_r_job_with_cpdctl.py --yaml_file prod_r_notebook_test.yaml

# r shiny
python deploy_r_with_cpdctl.py --yaml_file prod_r_shiny_test.yaml