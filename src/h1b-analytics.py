import sys
import csv

class VisaStats:
    def __init__(self, input_file, output_file1, output_file2):
        """
        Initializes of objects of the class
        """
        self.certified_count = 0
        self.visa_status, self.case_number = '',''
        self.soc_occupation, self.work_state,= '',''
        self.state_dict = {}
        self.occ_dict = {}
        self.unique_case_numbers = set()
        self.inputfile = input_file
        self.occ_file = output_file1
        self.state_file = output_file2

    def parse_file(self, input_csv):
        reader = csv.DictReader(open(input_csv))
        # todo : Missing data
        for row in reader:
            try:
                # Non-repetitive case numbers
                if row[self.case_number] not in self.unique_case_numbers and row[self.visa_status] == 'CERTIFIED':
                    self.unique_case_numbers.add(row[self.case_number])
                    self.certified_count += 1
                    if row[self.work_state] != '':
                        if row[self.work_state] not in self.state_dict:
                            self.state_dict[row[self.work_state]] = 0
                        self.state_dict[row[self.work_state]] += 1
                    if row[self.soc_occupation] != '':
                        if row[self.soc_occupation] not in self.occ_dict:
                            self.occ_dict[row[self.soc_occupation]] = 0
                        self.occ_dict[row[self.soc_occupation]] += 1
            except:
                pass

    def filter_columns(self):
        with open(self.inputfile) as file:
            header = file.readline().split(',')
            print(header)
            for name in header:
                try:
                    if 'STATUS' in name:
                        self.visa_status = name
                    elif 'CASE' in name and 'NUMBER' in name:
                        self.case_number = name
                    elif 'SOC' in name and 'NAME' in name:
                        self.soc_occupation = name
                    elif 'WORK' in name and 'STATE' in name:
                        self.work_state = name
                except:
                    pass
        self.parse_file(self.inputfile)

    def find_occupation(self):
        sorted_d = sorted((-value, key) for (key, value) in self.occ_dict.items())[:10]
        print(sorted_d)
        with open(self.occ_file, 'w') as file:
            file.write('TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'+'\n')
            for item in sorted_d:
                try:
                    percentage = round((abs(item[0])/self.certified_count)*100,1)
                    output = item[1] + ";" + str(abs(item[0])) + ";" + str(percentage) + "%"
                    file.write(output + '\n')
                except:
                    pass

    def find_states(self):
        sorted_d = sorted((-value, key) for (key, value) in self.state_dict.items())[:10]
        print(sorted_d)
        print(self.state_dict)
        with open(self.state_file, 'w') as file:
            file.write('TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'+'\n')
            for item in sorted_d:
                try:
                    percentage = round((abs(item[0])/self.certified_count)*100,1)
                    output = item[1] + ";" + str(abs(item[0])) + ";" + str(percentage) + "%"
                    file.write(output + '\n')
                except:
                    pass

def main(input_file,output_file1,output_file2):
    visa_stats = VisaStats(input_file,output_file1, output_file2)
    visa_stats.filter_columns()
    visa_stats.find_occupation()
    visa_stats.find_states()

if __name__ == "__main__":
    # sys.argv[1] = "./input/h1b_input.csv"
    main("../input/h1b_input.csv","../output/top_10_occupations.txt","../output/top_10_states.txt")