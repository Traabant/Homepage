from scripts.DbOperations import DbOperations
import os

class Compare:
    """
    compers two list, list given in parameter is one that is parsed from dowloaded HTML
    the other one is pulled from DB of previous entries
    """
    def __init__(self, list_to_compare, db_file_name):
        self.list = list_to_compare
        self.status = False
        self.db_file_name = db_file_name

    # porovna stazene udalosti s udalostmi nactenych ze souboru
    def compare(self, table):
        """
        :param table: specifi table in DB for comparasion
        :return: returns new list of additional entries
        """
        self.new_events = []
        self.table = table
        new_events = []

        db = DbOperations(self.db_file_name)
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
