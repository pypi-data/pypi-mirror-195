
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os

import click

# initialize connection to our
# email server, we will use gmail here
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()

password = os.environ['pass_gmail_calculus_with_cig']
email = os.environ['mail_calculus_with_cig']
# Login with your email and password
smtp.login(email, password)

def message(subject, text, img, attachment):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    if img is not None:
        if type(img) is not list:
            img = [img]
        for one_img in img:
            img_data = open(one_img, 'rb').read()
            msg.attach(MIMEImage(img_data,name=os.path.basename(one_img)))


    if attachment is not None:
        if type(attachment) is not list:
            attachment = [attachment]
        for one_attachment in attachment:
            with open(one_attachment, 'rb') as f:
                file = MIMEApplication(f.read(),name=os.path.basename(one_attachment))
            file['Content-Disposition'] = f'attachment; filename="{os.path.basename(one_attachment)}"'
            msg.attach(file)


    return msg



@click.command()
@click.option(
        '-s',
        '--subject',
        prompt=True,
        default="Hello there",
        help="Subject of the email"
        )
@click.option(
        '-m',
        '--mail',
        prompt=True,
        default="Message",
        help="Message text"
        )
@click.option(
        '-i',
        '--image',
        prompt=True,
        default='None',
        help="Image path"
        )
@click.option(
        '-a',
        '--attachment',
        prompt=True,
        default='None',
        help="Document attachment"
        )
@click.option(
        '-t',
        '--to',
        prompt=True,
        default='vaibhavblayer@gmail.com',
        help="Email id to send to"
        )
def main(subject, mail, image, attachment, to):
   
    if image == 'None':
        image = None

    if attachment == 'None':
        attachment = None

    mail += f"\n\n\t\tsent from Vaibhav's MacBook-Air"

    if message != "":
        msg = message(subject, mail, image, attachment)
        tos = [to]
        smtp.sendmail(from_addr=email, to_addrs=tos, msg=msg.as_string())
        smtp.quit()
