import logging
import os, time
import zipfile
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


class Zip_Sender(object):
    """
        Zip and Send files within a specified Directory.
    """
    def __init__(self,target_folder,verbosity=20):

        # verbosity levels:
        # CRITICAL = 50
        # ERROR = 40
        # WARNING = 30
        # INFO = 20
        # DEBUG = 10
        # NOTSET = 0
        logging.getLogger().setLevel(verbosity)

        self.target_folder = target_folder
        self.smtp_is_set = False
        self.login_is_required = False
        self.email_details_is_set = False

    def setup_smtp_server(self, smtp_address=None, smtp_port=None, require_tls=False):

        # GMAIL SMTP server is selected by default if no SMTP server is provided

        if smtp_address is None:
            self.smtp_address = "smtp.gmail.com"
            self.smtp_port = 587
            self.require_tls = True
        else:
            self.smtp_address = smtp_address
            self.smtp_port = smtp_port
            self.require_tls = require_tls

        self.smtp_is_set = True

    def setup_login_credentials(self, username, password):
        self.login_is_required = True
        self.login_username = username
        self.login_password = password

    def setup_email_details(self,subject_suffix,from_email,to_email,text):
        self.email_details_is_set = True
        self.subject_suffix = subject_suffix
        self.from_email = from_email
        self.text = text

        if isinstance(to_email,str):
            self.to_email = [to_email]
        else:
            self.to_email = to_email

    def run(self):
        if not self.smtp_is_set:
            logging.warning(" [+] SMTP is not set!")
            logging.info(" [+] Using gmail SMTP server...")
            self.setup_smtp_server()

        if not self.login_is_required:
            logging.warning(" [+] Login credentials not provided")
            logging.info(" [+] Setting login action as not required")

        if not self.email_details_is_set:
            logging.warning(" [+] Sender and Recipient Emails are not provided! print help for a demo code.")
            return

        self._fetch_zip_files()
        if self.zip_name:
            self._send_mail(self.zip_name)
            os.remove(self.zip_name)

    def _filter(self,name):
        # setup your own filter to determine which files to select
        return name.endswith(".txt")

    def _fetch_zip_files(self):
        try:
            logging.info(" [+] Setting target folder as home directory")
            os.chdir(self.target_folder)

            lst = os.listdir(os.getcwd())
            logging.info(" [+] %d files found"%(len(lst)))

            # I use this script on a daily basis so index with date was enough for my case.
            # Feel free to update this section
            date = time.strftime("%Y_%m_%d")
            self.subject = '%s_%s' % (self.subject_suffix,date)

            self.zip_name = self.subject+".zip"
            zipf = zipfile.ZipFile(self.zip_name, 'w')
            for file in lst:
                if self._filter(file):
                    zipf.write(file)

            zipf.close()

        except:
            logging.warning(" [+] There's an error please check your data!")
            self.zip_name = None

    def _send_mail(self, files=None):

        msg = MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = self.from_email
        msg['To'] = COMMASPACE.join(self.to_email)
        msg['Date'] = formatdate(localtime=True)

        with open(files, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s"' % basename(files),
                Name=basename(files)
            ))

        msg.attach(MIMEText(self.text))

        smtp = smtplib.SMTP(self.smtp_address, self.smtp_port)
        if self.require_tls:
            smtp.starttls()

        if self.login_is_required:
            smtp.login(self.login_username, self.login_password)
        logging.info(" [+] Sending email...")
        smtp.sendmail(self.from_email, self.to_email, msg.as_string())
        logging.info(" [+] Email is sent!")

        smtp.close()


if __name__ == "__main__":

    inst = Zip_Sender("./Source_folder")

    #inst.setup_smtp_server( "SMTP_ADDRESS","SMTP_PORT",require_tls=)
    inst.setup_login_credentials("Username","password")
    inst.setup_email_details("Subject","from_email","to_email","\n\nCheck attached files!\n\n")
    inst.run()
