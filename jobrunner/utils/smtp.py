# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Cloudbase Solutions Srl
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import smtplib

from email.mime import text
from oslo.config import cfg
from jobrunner.openstack.common import log as logging

opts = [
    cfg.StrOpt('host', default='localhost', help='SMTP host'),
    cfg.StrOpt('auth_username', default='', help='SMTP authentication username'),
    cfg.StrOpt('auth_password', default='', help='SMTP authentication password'),
    cfg.StrOpt("auth_method", default='LOGIN PLAIN', help='SMTP authentication method'),
    cfg.StrOpt('email_from', default='Cloudbase Job Runner <jobrunner@change.me>', help='Email "from" field'),
    cfg.StrOpt('email_subject', default='[Cloudbase Job Runner] Job Status Update', help='Email subject'),
]

CONF = cfg.CONF
CONF.register_opts(opts, 'smtp')

LOG = logging.getLogger(__name__)


def send_email(from_email, to_email, subject, body):
    if not from_email:
        from_email = CONF.smtp.email_from
    if not subject:
        subject = CONF.smtp.email_subject 

    msg = text.MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    s = smtplib.SMTP(CONF.smtp.host)
    s.ehlo()
    if CONF.smtp.auth_username:
        s.esmtp_features["auth"] = CONF.smtp.auth_method
        s.login(CONF.smtp.auth_username, CONF.smtp.auth_password)

    s.sendmail(from_email, [to_email], msg.as_string())
    s.quit()

