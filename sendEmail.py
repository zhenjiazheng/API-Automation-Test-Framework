# coding=UTF-8
__author__ = 'zhengandy'

import time
# Import the needed email libraries
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
    
def sendEMail(fileTosend, mailto):
    """
    This function takes in recipient and will send the email to that email address with an attachment.
    :param recipient: the email of the person to get the text file attachment
    """

    time_strf = time.strftime("%Y-%m-%d %X", time.localtime())
    # Set the server and the message details
    send_from = 'ceshi@echiele.com'
    subject = "TestReport For XW API %s." % time_strf
    # Create the multipart
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['To'] = ",".join(mailto)  # recipient

    # msg preable for those that do not have a email reader
    msg.preamble = 'Multipart message.\n'

    # Text part of the message
    part = MIMEText("Dear Receiver,\n\nThis is the latest XW API test report,and it is an automated sent email. \nNo need to reply... it won't be answered anyway.\nAny issue please contact with the sender, \n\nThanks!")
    msg.attach(part)

    # The attachment part of the message
    fp = open("%s" % fileTosend, "rb")
    part = MIMEApplication(fp.read())
    fp.close()
    part.add_header('Content-Disposition', 'attachment', filename="%s" % fileTosend)
    msg.attach(part)

    # Create an instance of a SMTP server
    sp = SMTP()
    sp.connect('smtp.exmail.qq.com')
    # Start the server
    sp.set_debuglevel(1)
    # sp.ehlo()
    sp.starttls()
    sp.login('ceshi@echiele.com', 'cs123456')

    # Send the email
    sp.sendmail(msg['From'], mailto, msg.as_string())
    sp.quit()
