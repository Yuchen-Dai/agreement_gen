import datetime
from pathlib import Path
from exception import IllegalDate


class Quote:
    def __init__(self, project_name='', date= ('1970', '01', '01',), buyer_name='', buyer_contact='', buyer_tel='',
                 quote_contact='', quote_tel='', qq=''):
        self.project_name = project_name
        try:
            self.sign_date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
        except ValueError:
            raise IllegalDate
        self.buyer_name = buyer_name
        self.buyer_contact = buyer_contact
        self.buyer_tel = buyer_tel
        self.quote_contact = quote_contact
        self.quote_tel = quote_tel
        self.qq = qq
        self._modify = True

    def save(self, dir):
        pass

    @staticmethod
    def get_today():
        """ Get today's date: (year, month, day)"""
        today = datetime.date.today()
        return str(today.year), str(today.month), str(today.day)
