import datetime
import logging
import pickle
from pathlib import Path
from exception import IllegalDate, FileExceed


class Quote:
    def __init__(self, project_name='', date=('1970', '01', '01',), buyer_name='', buyer_contact='', buyer_tel='',
                 quote_contact='', quote_tel='', qq='', name=''):
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
        self.name = name
        self.qid = None
        self._modify = True

    def get_qid(self):
        return self.qid

    def save(self, dir):
        p = Path(dir) / 'quote'
        if not p.exists():
            logging.debug(f"Create saving directory: {p.resolve()}")
            p.mkdir(parents=True)

        if not self.qid:
            date = Quote.get_today()
            pre_six = '{}{:0>2d}{:0>2d}'.format(str(date[0])[-2:], int(date[1]), int(date[2]))
            pre_four = pre_six[:4]
            biggest = 1
            this_month = [i for i in p.iterdir() if i.stem.startswith(pre_four)]
            for i in this_month:
                number = int(i.stem[-4:-1])
                print(i.stem)
                if number >= biggest:
                    biggest = number + 1
            if biggest > 999:
                raise FileExceed(f'Contracts for this month {pre_six} exceed 100.')
            last_four = '{:0>3d}2'.format(biggest)
            self.qid = pre_six + last_four

        p = p / f'{self.qid}.data'
        if self._modify:
            self._modify = False
            logging.debug(f"Save quote: {p.resolve()}")
            with p.open('wb') as f:
                pickle.dump(self.__dict__, f)
        else:
            logging.debug(f"Quote no modify, did not save: {p.resolve()}")

    def delete(self, dir):
        qid = self.qid
        p = Path(dir) / 'quote' / f'{qid}.data'
        assert p.exists(), f"No existing file: {p}"
        logging.debug(f"Delete quote: {p.resolve()}")
        p.unlink()

    def get_name(self):
        return self.name if self.name else self.qid

    @staticmethod
    def load(qid, data_dir):
        q = Quote()
        p = Path(data_dir) / 'quote' / f'{qid}.data'
        assert p.exists()
        with p.open('rb') as pkl_file:
            q.__dict__ = pickle.load(pkl_file)
        logging.debug(f"Load quote from file: {p.resolve()}")
        q._modify = False
        return q

    @staticmethod
    def get_today():
        """ Get today's date: (year, month, day)"""
        today = datetime.date.today()
        return str(today.year), str(today.month), str(today.day)


if __name__ == '__main__':
    import os
    os.chdir('../')
    q = Quote()
    q.save('data')
