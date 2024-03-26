import smtplib


def send_email(receivers, message, sender='jbtang@au1.ibm.com'):
    try:
        smtpObj = smtplib.SMTP('ap.relay.ibm.com')
        smtpObj.sendmail(sender, receivers, message)
        print("Notification Email Sent Successfully")
    # except SMTPException:
    except:
        print("Error: unable to send email")


def get_wml_date_str():
    from datetime import datetime
    from datetime import timedelta
    utc0_now = datetime.now()
    # to compensate the time zone difference
    hours_added = timedelta(hours=10)
    ut10_time = utc0_now + hours_added
    wml_date_str = ut10_time.strftime("%Y-%m-%d")

    return wml_date_str


if __name__ == '__main__':
    # example input:
    sender = 'jbtang@au1.ibm.com'
    receivers = ['jbtang@au1.ibm.com']
    # message = """\
    # Subject: Hi there

    # This message is sent from Python."""

    message = """Subject: {} Group Compliance Preprocessing has completed successfully
    ### Start of Message ###

    {} Rows by {} Columns Input Data has been preprocessed

    ### End of Message ###

    This message is sent from Cloud Pak for Data platform.""".format('2021-10-01', 99, 88)

    send_email(receivers, message, sender)
