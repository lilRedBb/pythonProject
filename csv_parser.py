import re
import os
import csv


class Parse_txt():

    def __init__(self, file_path):
        self.file_path = file_path
        self.li_file = []
        self.device_length = None

    def get_path(self):
        file_path = self.file_path
        for a,b,c in os.walk(file_path):
            for file in c:
                file_name = os.path.join(a, file)
                if re.search("txt", file_name):
                    self.li_file.append(file_name)
        li_file = self.li_file
        return li_file


    def to_csv(self,li_file):
        for i in li_file:
            cursor = 0
            csv_path = i.replace("txt", "csv")
            with open(i,'r') as f,open(csv_path, 'w') as f2:
                csv_writer = csv.writer(f2)
                f_txt = f.readlines()
                for i in f_txt:
                    if ("Device" in i or "await" in i) and cursor == 0:
                        cursor =1
                        if i != "\n":
                            li_split = re.split(r'\s+', i.strip('\n'))
                            self.device_length = len(li_split)
                            csv_writer.writerow(li_split)

                    if ("Device" not in i or "await" not in i) and cursor == 1:
                        if i != "\n":
                            li_split = re.split(r'\s+', i.strip('\n'))
                            if len(li_split) != self.device_length:
                                continue

                            csv_writer.writerow(li_split)
                            f.close()
        return None









