import datetime
import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://ojp.nationalrail.co.uk'


class TrainRoute(object):
    """A data structure to hold train route information"""

    def __init__(self, due, dest, status, platform, details):
        self.dept = due  # This is the time of departure
        self.dest = ' '.join([name.capitalize() for name in dest.split(' ')])
        self.status = status
        self.platform = platform
        self.details = details # self.find_arrival(details)

    def __lt__(self, other):
        return self.format_time(self.dept) <= self.format_time(other.dept)

    def format_time(self, str_time):
        t = str_time.split(':')
        return datetime.time(int(t[0]), int(t[1]))

    def output(self):
        return {
            'dept': self.dept, 'dest': self.dest, 'status': self.status,
            'platform': self.platform, 'details': self.details
        }

    def find_arrival(self, postfix):
        r = requests.get(BASE_URL + postfix)
        soup = BeautifulSoup(r.text, features='html.parser')
        soup_tbl = soup.find('div', class_='tbl-cont')
        # TODO - seems that the content on this page loads
        # when it returns from the server. The page does not
        # render the same as when I view it in the browser.
        # content = extract_content(soup_tbl)
        # print('yo')



def extract_headers(soup_tbl):
    return [th.text for th in soup_tbl.find_all('th')]


def extract_content(soup_tbl):
    """Each row in the table extract the text or link"""
    return [[data.a.get('href') if sanitise(data.text).startswith('details') else sanitise(data.text) for data in row.find_all('td')]
            for row in soup_tbl.find('tbody').find_all('tr')]


def sanitise(data):
    return data.replace('\n', '').replace('\xa0', '').strip(' ').lower()


class TrainFinder(object):
    """Find the earliest train to leave the station"""

    def __init__(self, dept, dest):
        self.dept = dept  # departure
        self.dest = dest  # destination

    def create_url(self):
        return '{base}/service/ldbboard/dep/{dept}/{dest}/To'.format(base=BASE_URL, dept=self.dept, dest=self.dest)

    def parse_html(self):
        r = requests.get(self.create_url())
        return BeautifulSoup(r.text, features='html.parser')

    def find_data(self):
        soup = self.parse_html()
        soup_tbl = soup.find('div', class_='tbl-cont')
        # headers = extract_headers(soup_tbl)
        headers = ['due', 'dest', 'status', 'platform', 'details']
        content = extract_content(soup_tbl)

        return sorted([TrainRoute(**dict(zip(headers, train))) for train in content])

if __name__ == '__main__':
    x = TrainFinder('LST', 'CHM').find_data()
    print(x)