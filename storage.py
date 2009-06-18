from __future__ import with_statement

import thread
import time
from datetime import datetime, timedelta
import smtplib
import string
import imaplib

#How long a chat remains iddle before it's archived to email.
#Smaller values lead to producing many emails for a single chat,
#larger values lead to longer archiving delay.
IDLE_TIMEOUT_SECONDS = 60 

class MailArchiver(object):
    """
    Base class for email-based log storages. Provides logic for grouping skype messages
    into email messages and delivery loop.
    """
    def __init__(self) :
        self._chats = {}
        self._lock = thread.allocate_lock()
        self._stopped = False
        self._email_queue = []
        

    def _get_chat_data(self, chat):
        cd =self._chats.get(chat.Timestamp, [])
        self._chats[chat.Timestamp] = cd
        return cd

    def add(self, message):
        """
        Add a chat message to archive.
        """
        with self._lock:
            self._get_chat_data(message.Chat).append(message)

    
    def start(self):
        thread.start_new_thread(self._delivery_loop, ())
        
    def stop(self):
        with self._lock:
            self._stopped = True

    def _delivery_loop(self):
        while not self._stopped:
            with self._lock:
                now = datetime.now()
                for chat_stamp, chat in self._chats.iteritems():
                    if len(chat) > 0 and\
                            now - datetime.fromtimestamp(chat[-1].Timestamp) > timedelta(minutes=1):
                        self.deliver_later(chat)
                        chat[:]=[]
            self.deliver_now()
            time.sleep(10)


    def deliver_later(self, chat):
        email_body = ''
        for msg in chat:
            email_body += "%s (%s): %s\n"%(msg.FromDisplayName, datetime.fromtimestamp(msg.Timestamp), msg.Body)
        email_subject = '[skype chat] "%s" (%s)'%(chat[0].Chat.FriendlyName, datetime.fromtimestamp(chat[0].Chat.Timestamp))
        self._email_queue.append((email_subject,email_body))


    def deliver_now(self):
        """
        Implement backend-specific logic of saving message queue to server in this method.
        """
        raise NotImplementedError('MailArchiver shouldn\'t be used directly, but rather via one of its descendats')



class SMTPMailArchiver(MailArchiver):
    """
    Mail archiver using SMTP protocol. 
    """

    def __init__(self,
                 smtp_host, 
                 smtp_port,
                 smtp_use_tls,
                 smtp_user,
                 smtp_password,
                 email_address):
        """
        email_address is the address to use for "from" and "to" fields (mailbox owner address)
        """

        super(SMTPMailArchiver, self).__init__()
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_use_tls = smtp_use_tls
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.email_address = email_address
        self.smtp = smtplib.SMTP(local_hostname='localhost')
        self.start()
        
    def deliver_now(self):
        if len(self._email_queue) == 0:
            return
        self.smtp.connect(self.smtp_host, self.smtp_port)
        if self.smtp_use_tls:
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.ehlo()
        self.smtp.login(self.smtp_user, self.smtp_password)
        for email in self._email_queue:
            body = string.join((
                    "From: %s" % self.email_address,
                    "To: %s" % self.email_address,
                    "Subject: %s" % email[0],
                    "",
                    email[1]), "\r\n")
            self.smtp.sendmail(self.email_address, [self.email_address], body.encode('utf-8'))
        self.smtp.quit()
        self._email_queue = []


IMAP_FOLDER_NAME = 'Skype chats'

class IMAPMailArchiver(MailArchiver):

    def __init__(self,
                 imap_host, 
                 imap_port,
                 imap_use_tls,
                 imap_user,
                 imap_password):
        super(IMAPMailArchiver, self).__init__()

        if imap_use_tls:
            self.imap = imaplib.IMAP4_SSL(imap_host, imap_port)
        else:
            self.imap = imaplib.IMAP4(imap_host, imap_port)
        self.imap.login(imap_user, imap_password)
        if not self.imap.list(IMAP_FOLDER_NAME)[1][0]:
            self.imap.create(IMAP_FOLDER_NAME)
        self.start()
        
    def deliver_now(self):
        if len(self._email_queue) == 0:
            return
        for email in self._email_queue:
            body = string.join((
                    "Subject: %s" % email[0],
                    "",
                    email[1]), "\r\n")
            self.imap.append(IMAP_FOLDER_NAME, 'STORE', '"' + str(datetime.now()) + '"',body.encode('utf-8'))
        self._email_queue = []
