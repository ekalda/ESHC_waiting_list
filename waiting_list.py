import simplejson as json
from collections import OrderedDict
import smtplib
import email


class WaitingList(object):
    def __init__(self, pos_update=0, f_waiting_list = None):
        self.pos_update = pos_update
        self.to_delete = []
        self.wl_file = f_waiting_list
        with open(self.wl_file, 'r') as f:
            self.waiting_list = json.load(f)
        # separate file with the email account data
        with open('email_account.dat', 'r') as f_email:
            self.email_dat = json.load(f_email)

    # method to update the json file with the waiting list
    def update_waiting_list(self):
        # update all the positions and determine which entries from the file should be deleted
        for key in self.waiting_list.keys():
            self.waiting_list[key] -= self.pos_update
            if self.waiting_list[key] <= 0:
                self.to_delete.append(key)

    # method for deleting people from the list who have been offered a place
    def delete_emails(self):
        for email in self.to_delete:
            print('deleting', email)
            del self.waiting_list[email]

    # writing updated data back to the file
    def write_to_json(self):
        with open(self.wl_file, 'w') as f:
            json.dump(self.waiting_list, f)

    def create_message(self, position):
        msg = 'Hello,' + '<br>' + '<br>' + 'This email is to notify you that your position in the ' \
                                              'waiting list for the June/September intake has changed! Your new ' \
                                              'position is:' + '<br>' + str(position) + '<br>' + \
              '<br>' + 'If you have any questions, send an email to ' \
                       'eshc.logistics@gmail.com (don\'t respond to this email)!' + '<br>' + '<br>' + 'Best wishes,' + \
              '<br>' + 'The applications team'
        return msg

    def send_email(self, to_address, position):
        to_addr = to_address # address of the recipient
        pos = position # recipients position
        from_addr = self.email_dat["email"] # email address of the main it will be sent from
        username = self.email_dat["username"]
        password = self.email_dat["password"] # password :o :o
        # The actual mail to send
        header = "\r\n".join(["from: " + from_addr,
                              "subject: " + 'Your position in the waiting list has changed!',
                              "to: " + to_addr,
                              "mime-version: 1.0",
                              "content-type: text/html"])
        message = header + "\r\n\r\n" + self.create_message(pos)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(from_addr, to_addr, message)
        server.quit()

    def send_update_emails(self):
        for email in self.waiting_list.keys():
            print('sending email to', email)
            self.send_email(email, self.waiting_list[email])
        print('all emails sent!')



def main():
    waiting_list = WaitingList(pos_update=2, f_waiting_list='waiting_list.dat')
    print('updating the waiting list...')
    waiting_list.update_waiting_list()
    waiting_list.delete_emails()
    waiting_list.write_to_json()
    print('sending the emails...')
    waiting_list.send_update_emails()


if __name__ == '__main__':
    main()




