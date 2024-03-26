# a wrapper
import yaml
import subprocess
import smtplib

def send_email(smtp_server, sender, receivers, message):
    try:
        smtpObj = smtplib.SMTP(smtp_server)
        smtpObj.sendmail(sender, receivers, message)
        print("Notification Email Sent Successfully")
    # except SMTPException:
    except:
        print("Error: unable to send email")

def get_date_str():
    from datetime import datetime
    date_str = datetime.now().strftime("%Y-%m-%d")
    return date_str

def score(deployment_info, prj_info, email_setting):

    if email_setting:
        send_email_when_successful = email_setting['send_email_when_successful']
        send_email_when_fail = email_setting['send_email_when_fail']
        sender = email_setting['sender']
        receivers = email_setting['receivers']
        smtp_server = email_setting['smtp_server']
    else:
        send_email_when_successful = False
        send_email_when_fail = False

    import json
    import ast
    p = subprocess.run(["python", prj_info['main_file']], capture_output=True, text=True)

    stdout = p.stdout
    # print('stdout:', stdout)
    stderr = p.stderr
    # print('stderr:', stderr)

    # # need to remove ending dummy output
    # idx = stderr.find('>>>', 0)
    # stderr = stderr[:idx]

    date_str = get_date_str()

    if p.returncode:

        if send_email_when_fail:
            ############### send email with error msg ##################
            message = """Subject: {} Error [{}]\r\n

Receipients: {}

This message is sent from Cloud Pak for Data platform.

### Start of Error Message ###

{}

### End of Error Message ###

CPD URL: {}
Deployment Space ID: {}""".format(date_str, deployment_info['code_pkg_name'], receivers, stderr,
                                              deployment_info['url'], deployment_info['space_id'])

            print(message)
            send_email(smtp_server, sender, receivers, message)

        output_json = {"stderr": stderr, "stdout": stdout}

    else:

        if send_email_when_successful:
            ############### send successful notification ###############
            message = """Subject: {} Success [{}]\r\n

Receipients: {}

This message is sent from Cloud Pak for Data platform.

### Start of Message ###

{}

### End of Message ###

CPD URL: {}
Deployment Space ID: {}""".format(date_str,deployment_info['code_pkg_name'], receivers, stdout,
                                              deployment_info['url'], deployment_info['space_id'])

            print(message)
            send_email(smtp_server, sender, receivers, message)

        output_json = {"stdout": stdout}

        # for online application, we may want to omit the stdout to reduce the unnecessary traffic
        # enable_stdout = deployment_info['enable_stdout']
        # if enable_stdout:
        #     output_json = jsondata
        #     jsondata.update({"stdout": stdout})
        # else:
        #     output_json = jsondata

    return output_json
    # deploy_mode = deployment_info['deploy_mode']
    # if deploy_mode == 'online':
    #     return {"predictions": [output_json]}  # work
    # else:
    #     # somehow batchmode will never finish with above formart, but below works
    #     return {"predictions": [{"values": [output_json]}]}


if __name__ == '__main__':

    # Read YAML file
    with open('dummy.yaml', 'r') as stream:
        configuration = yaml.safe_load(stream)

    prj_info = configuration['prj_info']
    deployment_info = configuration['deployment_info']

    if "email_setting" in configuration:
        email_setting = configuration['email_setting']
        print('\n\rsend_email_when_fail: ', email_setting['send_email_when_fail'])
        print('send_email_when_successful: ', email_setting['send_email_when_successful'])
    else:
        email_setting = []
        print('\n\rEmail not enabled')

    output_json = score(deployment_info, prj_info,email_setting)
    print(output_json)