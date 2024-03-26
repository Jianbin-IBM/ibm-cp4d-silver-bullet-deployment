# DO NOT modify this code and file name

import subprocess

p = subprocess.run("r42_env/bin/Rscript install_r_pkgs.R".split(), capture_output=True, text=True)
# stdout = p.stdout
# print('stdout:', stdout)
# stderr = p.stderr
# print('stderr:', stderr)