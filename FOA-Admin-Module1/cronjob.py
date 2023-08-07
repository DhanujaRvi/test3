import subprocess
import smtplib
from email.mime.text import MIMEText
import os
from email.mime.multipart import MIMEMultipart

MAILING_LOGIN="no-reply@in-d.ai"
MAILING_PASSWORD="Intain@12345"

email_list = ["rachel.priyadarshini@in-d.ai","ridhanya.manoharan@in-d.ai","krishmitha.mohan@in-d.ai"]

try:
    ip_details = (subprocess.check_output('dig +short myip.opendns.com @resolver1.opendns.com',shell=True)).decode("utf-8")
except:
    ip_details="Couldn't get ip"

b = '''
    <div style="background-color:#fff;margin:0 auto 0 auto;padding:30px 0 30px 0;color:#4f565d;font-size:13px;line-height:20px;font-family:'Helvetica Neue',Arial,sans-serif;text-align:left">
        <center>
        <table style="width:550px;text-align:center">
            <tbody><tr>
                <td style="padding:0 0 20px 0;border-bottom:1px solid #e9edee; text-align:left; ">
                    <h2 style="font-family: trebuchet ms,sans-serif;">
                        Hi! 
                    </h2>
                    <br>
                </td>
            </tr>
            <tr>
                <td colspan="2" style="padding-bottom:10px; border-bottom:1px solid #e9edee; ">               
                    </span>
                        <p style="margin:20 10px 10px 10px;padding:0">
                            <span style="font-family: trebuchet ms,sans-serif; color: #4f565d; font-size: 15px; line-height: 20px;">
                                The {api} Api running on IP {ip} with the below port is down
                            </span>
                        </p>
                    <span>
                        <p>
                            <a style="display:inline-block;text-decoration:none;padding:15px 20px;background-color:#048c88;border:1px solid #048c88;border-radius:3px;color:#fff;font-weight:bold; font-size: medium" >
                                {pt}
                            </a>
                        </p>
                    </span>
                    
                </td>
            </tr>

        </tbody></table>
        </center>
    </div></div>
'''
#print("54")
def mailing(email, api, port):
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    #print("success")
    s.ehlo()
    s.starttls() 
    s.ehlo()
    s.login(MAILING_LOGIN, MAILING_PASSWORD)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Api Down'
    msg['From'] = MAILING_LOGIN
    msg['To'] = email
    body= b.format(api=api,pt=port,ip=ip_details)
    body = MIMEText(body,'html')
    msg.attach(body) 
    s.sendmail("no-reply@in-d.ai", email, msg.as_string()) 
    s.quit()

try:
    message = "Payables Admin Module SIT"
    port = 5000
    grep_command =f"sudo lsof -Pi | grep {port}"
    output = subprocess.check_output(grep_command, shell=True)
    runningcount = len(output.decode("utf-8").splitlines())
    if runningcount==0:
        for email in email_list:
            mailing(email, message, port)
except:
    for email in email_list:
        mailing(email, message, port)
