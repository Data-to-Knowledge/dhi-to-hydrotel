# -*- coding: utf-8 -*-

#-Authorship information-###################################################################
__author__ = 'Wilco Terink'
__copyright__ = 'Environment Canterbury'
__version__ = '1.0'
__email__ = 'wilco.terink@ecan.govt.nz'
__date__ ='February 2021'
############################################################################################

import yaml, os
import smtplib
from email.message import EmailMessage


# Read the parameters
base_dir = os.path.realpath(os.path.dirname(__file__))
with open(os.path.join(base_dir, 'email_parameters.yml')) as param:
    param = yaml.safe_load(param)
# with open(r'C:\Active\Eclipse_workspace\email_send_test\email_parameters.yml') as param:
#     param = yaml.safe_load(param)
email_settings = param['email']

# Connect to the SMTP server
server = smtplib.SMTP()
server.connect(email_settings['smtp_server'], email_settings['smtp_port'])

# Initiate the message to be send
msg = EmailMessage()
msg.set_content(email_settings['msg_content'])
msg['Subject'] = email_settings['msg_subject']
msg['From'] = email_settings['sender']
msg['To'] = email_settings['recipients']

# Send the email
server.send_message(msg)
server.quit()
print('Email has been sent to the following recipient(s): %s' %email_settings['recipients'])


