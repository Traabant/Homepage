class Testing:
    
    def __init__(self, data):
        self.data = data

    def print(self):
        print(self.data)
        pass

    def write_to_file(self):
        with open("temp.txt", mode="w", encoding="UTF-8") as f:
            f.write(self.data)


    def load_from_file(self):
        with open("temp.txt", mode="r", encoding="UTF-8") as f:
            data = f.read()
        return data


    def parse(self):       

        data = self.data.splitlines()   
        data = self.remove_blank_lines(data)
        data = self.create_dics_from_list(data)
        pass

    def parse_local(self, data):       

        data = data.splitlines()   
        data = self.remove_blank_lines(data)
        data = self.create_dics_from_list(data)
        pass


    def remove_blank_lines(self, data):
        list_to_return = []
        for line in data:
            if line != '':
                list_to_return.append(line)
        return list_to_return


    def create_dics_from_list(self, input_data):
        """
        converts input data to DICS
        """

        list_keys = []
        list_vals = []

        for i, item in enumerate(input_data):
                input_data[i] = item.split(sep=":", maxsplit=1)
                if (len(input_data[i]) == 1):
                    if (i == 0 ):
                        list_keys.append(f'Name')
                        list_vals.append(self.get_name_from_str(input_data[i][0]))
                elif (len(input_data[i]) == 2):                
                    list_keys.append(input_data[i][0])
                    list_vals.append(input_data[i][1])
        zip_of_lists = zip(list_keys,list_vals)
        dics = dict(zip_of_lists)
        return dics
        
    def get_name_from_str(self, input_string):
        """
        removes prefix from given string,
        expects string in this format:
        Duplicati Backup report for Test_S3
        """

        STRING_PREFIX = 28
        return(input_string[STRING_PREFIX:])



if __name__ == "__main__":
    t = Testing("tmp")
    data = t.load_from_file()
    t.parse_local(data)
    