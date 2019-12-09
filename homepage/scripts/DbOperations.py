import sqlite3

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

    def dump_data_to_info_table(self, info, info_date):
        string_to_execute = "INSERT INTO weather_info(%s, %s) VALUES('%s', '%s')" \
                            % ('Date', 'Info', info_date, info)
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
