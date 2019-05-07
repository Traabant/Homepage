import requests
from bs4 import BeautifulSoup
import unicodedata
import datetime
import sqlite3
import json
from sqlite3 import Error


def send_email(user, pwd, recipient, subject, body):
    """
    Sends email to recipients, log to log file if email was send or not

    """
    import smtplib

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        # print ('successfully sent the mail')
        log('successfully sent the mail')
    except:
        log("failed to send mail")


def log(event):
    """
    log envets to log file
    """
    log_name = 'log.txt'
    time = datetime.datetime.now().strftime("%Y-%m-%d")
    obsah_log = '\n' + time + '\n' + event + '\n' + '********************************'
    file = open(log_name, "a", encoding="utf-8")
    file.write(obsah_log)
    file.close()


def find_envents_in_url(url):
    """
    downloads HTML, parse it and returns list with only parsed paragraps
    :param url:
    :return: correct_list
    """
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        output = soup.find_all('p')
        correct_list = []
        for item in output:
            correct_list.append(item.text)
        return correct_list
    except:
        log("nepovedlo se stazeni informaci z webu")


def find_new_galery_in_url(url):
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        output = soup.find_all('li')
        list_to_return = []
        for item in output:
            if item.attrs.get("data-cat") == "1":
                list_to_return.append(item.text[4:-3])
        return list_to_return
    except:
        log("nepovedlo se stazeni informaci z webu")


def odstraneni_diakritiky(list):
    """
    delets special characters from Czech language and converts them to ASCI
    :param list:
    :return: list
    """
    list_to_return = []
    for item in list:
        item = unicodedata.normalize('NFKD', item)
        output = ''
        for c in item:
            if not unicodedata.combining(c):
                output += c
        list_to_return.append(output)
    return list_to_return


class Compare:
    """
    compers two list, list given in parameter is one that is parsed from dowloaded HTML
    the other one is pulled from DB of previous entries
    """
    def __init__(self, list_to_compare):
        self.list = list_to_compare
        self.status = False

    # porovna stazene udalosti s udalostmi nactenych ze souboru
    def compare(self, table):
        """
        :param table: specifi table in DB for comparasion
        :return: returns new list of additional entries
        """
        self.new_events = []
        self.table = table
        new_events = []
        db = DbOperations(db_file_name)
        source_file_lines = db.get_events_from_db(self.table)
        bad_str = 'Railsformers s.r.o.'
        bigger_file_len = len(self.list)
        i = 0
        while i < bigger_file_len:
            listBackUp = self.list[i]
            # radek s copyrigth delal problem, proto vynecham
            if not bad_str in self.list[i]:
                # self.list[i] = self.list[i] + '\n'
                if self.list[i] in source_file_lines:
                    # print('je rovno ' + listBackUp)
                    a = 1
                elif listBackUp == '\\n':   # Vynechava prazdny radek
                    a = 1
                elif listBackUp == " ":     # Vynechava prazdny radek
                    a = 1
                else:
                    # print('neni rovno pro ' + listBackUp)
                    new_events.append(listBackUp)
                    self.status = True
            i += 1
        self.new_events = new_events


class DbOperations:
    """
    class to manipulate SQlite DB, it can write new entries or give back all records in specific table
    Class creates coneciton to DB when first called
    """
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = self.create_connection_to_db()
        self.cursor = self.connection.cursor()

    def create_connection_to_db(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)

        return None

    def dump_data_to_events_table(self, event, event_date):
        string_to_execute = "INSERT INTO weather_events(%s, %s) VALUES('%s', '%s')" \
                            % ('Date', 'Event', event_date, event)
        self.cursor.execute(string_to_execute)
        self.connection.commit()

    def dump_data_to_galerry_table(self, gallery, gallery_date):
        string_to_execute = "INSERT INTO weather_gallery(%s, %s) VALUES('%s', '%s')" \
                            % ('Date', 'Gallery', gallery_date, gallery)
        self.cursor.execute(string_to_execute)
        self.connection.commit()

    def get_events_from_db(self, table):
        """
        :param table: it can be 'events' or 'galerry'
        :return: gives back all record in table specificed abowe
        """
        string_to_execute = "SELECT * FROM weather_%s" % table
        self.cursor.execute(string_to_execute)
        fetchedlist = self.cursor.fetchall()
        list_to_return = []
        for item in fetchedlist:
            list_to_return.append(item[2])
        return list_to_return

    def dump_data_pollution_table(self, date_time, index):
        string_to_execute = "INSERT INTO weather_pollution(datetime, pollution_index) VALUES('%s', '%d')" \
                            % (date_time, index)
        self.cursor.execute(string_to_execute)
        self.connection.commit()

    def dump_data_weather_table(self, temp, date):
        string_to_execute = "INSERT INTO weather_weather2(weather_today, date) VALUES('%.01f','%s')" \
                            % (temp, date)
        self.cursor.execute(string_to_execute)
        self.connection.commit()

    def dump_data_weather_forcast_table(self, temp, date, date_added):
        string_to_execute = "INSERT INTO weather_Weather_forcast(weather_tomorrow, date_tomorrow, date_added)\
         VALUES('%.01f','%s', '%s')" \
                            % (temp, date, date_added)
        self.cursor.execute(string_to_execute)
        self.connection.commit()


def check_events():
    """
    downloads two HTML sites, than parse them.
    Parsed data gets compared to the data in DB,
    new data is stored in DB and snd throw the mail
    Script should be run periodically once a day
    """

    url = 'http://www.msmartinov.cz/stranka71'
    ulr_gallery = "http://www.msmartinov.cz/galerie"

    user = "siba.robot@gmail.com"
    password = "lplojiju321"
    subject = "Nove udalosti MS"
    recipient = [
        "david.siba@gmail.com",
        "kristyna.sibova@gmail.com"
    ]

    print("downloading data")
    events = find_envents_in_url(url)
    galery_list = find_new_galery_in_url(ulr_gallery)

    print("deleting special characters")
    events = odstraneni_diakritiky(events)
    galery_list = odstraneni_diakritiky(galery_list)

    print("comparing")
    compare = Compare(events)
    compare.compare('events')
    events = compare.new_events

    galery_compare = Compare(galery_list)
    galery_compare.compare('gallery')
    galery_list = galery_compare.new_events

    # write_events_to_file(events, eventsFile)
    # write_events_to_file(galery_list, galeryFile)

    if (compare.status is True) or (galery_compare.status is True):
        body = "Nove udoalosti ve skolce jsou : \n"
        for line in events:
            body += line + '\n'

        body += "\nNove galerie jsou : \n"
        for line in galery_list:
            body += line + '\n'
        db = DbOperations(db_file_name)
        print("writing Events to DB")
        for item in events:
            db.dump_data_to_events_table(item, datetime.datetime.today().strftime("%Y-%m-%d"))
        print("Writing galerry to DB")
        for item in galery_list:
            db.dump_data_to_galerry_table(item, datetime.datetime.today().strftime("%Y-%m-%d"))
        print('Done')

        send_email(user, password, recipient, subject, body)
        print('poslal bych mail')
        print(body)
        log(body)
        compare.status = False
    else:
        log('nejsou nove udalosti')
        print('No new Events')


def analyze_air_polution(polutin_index):
    """
    :param polutin_index: index from CHMI json data
    :return: string corresponding to the index
    """
    if polutin_index == 1:
        return "Velmi dobra"
    elif polutin_index == 2:
        return "dobra"
    elif polutin_index == 3:
        return "uspokojiva"
    elif polutin_index == 4:
        return "vzhovujci"
    elif polutin_index == 5:
        return "spatna"
    elif polutin_index == 6:
        return "velmi spatna"
    else:
        return "Chyba spracovani"


def get_pollution():
    """
    dwonloads Json data about pollution, than i gets parsed for just Ostrava
    Parsed data is stored in DB
    should be run periodically every hour
    """

    db = DbOperations(db_file_name)

    url_json_file = 'http://portal.chmi.cz/files/portal/docs/uoco/web_generator/aqindex_cze.json'
    response = requests.get(url_json_file)
    air_pollution_data = json.loads(response.text)
    index_ostrava_portuba = air_pollution_data['States'][0]['Regions'][13]['Stations'][15]['Ix']
    date_pullution = air_pollution_data['States'][0]['DateFromUTC']
    date_pullution = datetime.datetime.strptime(date_pullution, '%Y-%m-%d %H:%M:%S.%f %Z')
    date_pullution = date_pullution + datetime.timedelta(hours=2)
    date_pullution = date_pullution.strftime('%Y-%m-%d %H:%M:%S')
    if index_ostrava_portuba != 0:
        db.dump_data_pollution_table(date_pullution, index_ostrava_portuba)
        print("data saved in DB")
    print(f'Aktualni index {index_ostrava_portuba} z {date_pullution} stazeno {datetime.datetime.now()}')


def get_weather():
    """
    Downloads focast for current day and stores it in DB
    data is pulled out of the DB in views when needed
    """

    url_forcast = 'http://api.openweathermap.org/data/2.5/forecast?q=ostrava&appid=f38cd70321c379afac4b55fb00a3be7a'

    response = requests.get(url_forcast)
    forcast_data = json.loads(response.text)

    db = DbOperations(db_file_name)
    index = 0
    while index <= 7:
        data_today_in_kelvin = {
            'date': datetime.datetime.strptime(forcast_data["list"][index]['dt_txt'], '%Y-%m-%d %H:%M:%S'),
            'temp': forcast_data["list"][index]['main']['temp_max'],
        }
        db.dump_data_weather_table(data_today_in_kelvin['temp'],
                                   data_today_in_kelvin['date'].strftime('%Y-%m-%d %H:%M:%S'))
        index += 1
    index = 8
    while index <= 15:
        data_tomorrow_in_kelvin = {
            'date_added': datetime.datetime.now(),
            'date_tomorrow': datetime.datetime.strptime(forcast_data["list"][index]['dt_txt'], '%Y-%m-%d %H:%M:%S') ,
            'temp': forcast_data["list"][index]['main']['temp_max'],
        }
        index += 1
        db.dump_data_weather_forcast_table(data_tomorrow_in_kelvin['temp'],
                                           data_tomorrow_in_kelvin['date_tomorrow'],
                                           data_tomorrow_in_kelvin['date_added']
                                           )

    print('weather downloaded')


fileDir = '/home/Traabant/Homepage/Homepage/homepage'
db_file_name = fileDir + '/db.sqlite3'
# db_file_name = 'D:\SIBA\Scripty\Homepage\homepage\db.sqlite3'
