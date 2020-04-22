import datetime

class MyLog():
    """
    Custom log Class, loggs into BASE_DIR + log.txt
    takes single parametr and that is the message
    TODO: take status parm(info, err, message)
    """
    def __init__(self, message):
        self.message = message
        self.log()

    def log(self):
        """
        log envets to log file
        """
        log_name = 'log.txt'
        time = datetime.datetime.now().strftime("%Y-%m-%d")
        log_message = time + '\t' + self.message + '\n' 
        # + '********************************'
        with open(log_name, 'a') as file:
            file.write(log_message)
        
