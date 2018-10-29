"""
    @author: Deepthi Devaraj
    @version: v1.0

    INSIGHT DATA ENGINEERING CODING CHALLENGE

    Challenge:
    Given immigration data of H1B visa application processing, this
    program identifies the top 10 states and top 10 occupations with most
    number of approved H1B visas.

    Result:
    Data is parsed and missing values are added, the program outputs two
    files - top_10_occupations.txt and top_10_states.txt that contains the top
    10 values of occupations and states respectively.
"""

import sys
import csv


class VisaStats:
    """
    VisaStats class implements the core modules required to parse the file, add
    missing data and outputs the required data
    """
    def __init__(self, input_file, output_file1, output_file2):
        """
        Initializes objects of class
        :param input_file: input path of the csv file
        :param output_file1: output top_10_occupations.txt file path
        :param output_file2: output top_10_states.txt file path
        """
        self.certified_count = 0
        self.visa_status, self.case_number = '', ''
        self.soc_occupation, self.work_state = '', ''
        self.employer_state = ''
        self.state_dict = {}
        self.occ_dict = {}
        self.unique_case_numbers = set()
        self.inputfile = input_file
        self.occ_file = output_file1
        self.state_file = output_file2

    def add_missing_values(self, row):
        """
        Adds employer_state as the user working_state if working_state is
        missing
        :param row: individual row of csv file that has missing working_state
        :return: dict of state as key and its occurrence number as value
        """
        if row[self.employer_state] != '':
            if row[self.employer_state] not in self.state_dict:
                self.state_dict[row[self.employer_state]] = 0
            self.state_dict[row[self.employer_state]] += 1

    def parse_file(self, input_csv):
        """
        Parses the input file to get the required details
        :param input_csv: input csv file
        :return: creates occupation and state dict for book-keeping values
        """
        reader = csv.DictReader(open(input_csv,'r', encoding='utf-8'),
                                delimiter=';')

        for row in reader:
            try:
                # Non-repetitive case numbers
                if row[self.case_number] not in self.unique_case_numbers and \
                                row[self.visa_status] == 'CERTIFIED':
                    self.unique_case_numbers.add(row[self.case_number])
                    self.certified_count += 1
                    if row[self.work_state] != '':
                        if row[self.work_state] not in self.state_dict:
                            self.state_dict[row[self.work_state]] = 0
                        self.state_dict[row[self.work_state]] += 1
                    # else:
                    #     # if work_state value is missing, add employer_state
                    #     self.add_missing_values(row)
                    if row[self.soc_occupation] != '':
                        if row[self.soc_occupation] not in self.occ_dict:
                            self.occ_dict[row[self.soc_occupation]] = 0
                        self.occ_dict[row[self.soc_occupation]] += 1
            except (IndexError, ValueError, TypeError):
                pass

    def filter_columns(self):
        """
        Filter columns based on the required column headings(as column headings
        can change depending on the input csv file.
        eg: LCA_CASE_NUMBER and CASE_NUMBER
        :return: required column headers
        """
        with open(self.inputfile, 'r', encoding='utf-8') as file:
            header = next(csv.reader(file, delimiter=';'))
            soc_occupation = []
            work_state = []
            employer_state = []
            print(header)
            for name in header:
                try:
                    if 'STATUS' in name:
                        self.visa_status = name
                    elif 'CASE' in name and 'NUMBER' in name:
                        self.case_number = name
                    elif 'SOC' in name and 'NAME' in name:
                        soc_occupation.append(name)
                    elif 'WORK' in name and 'STATE' in name:
                        work_state.append(name)
                    elif 'EMPLOYER' in name and 'STATE' in name:
                        employer_state.append(name)
                except (IndexError, ValueError, TypeError):
                    pass
        self.soc_occupation = soc_occupation[0]
        self.work_state = work_state[0]
        self.employer_state = employer_state[0]
        print(self.visa_status, self.case_number, self.soc_occupation, self.work_state, self.employer_state)
        self.parse_file(self.inputfile)

    def find_top_ten(self, req_dict, output_file, out_str):
        """
        Finds the top 10 occupations of H1B certified applications
        :param req_dict: occupation or state dict required to parse
        :param output_file: output file path
        :param out_str: required out operation to be performed
        :return: output file with top 10 occupations, number of certified
        applications and its percentage
        """
        write_str = ''
        # Sort dictionary based on value and key and retrieve the first 10
        # ascending order sort of negative value to obtain top 10
        sorted_d = sorted((-value, key) for (key, value) in
                          req_dict.items())[:10]
        if out_str == 'OCCUPATIONS':
            write_str = "TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;" \
                        "PERCENTAGE" + '\n'
        elif out_str == 'STATES':
            write_str ="TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;" \
                       "PERCENTAGE" + '\n'
        with open(output_file, 'w') as file:
            file.write(write_str)
            for item in sorted_d:
                try:
                    percentage = round((abs(item[0])/
                                        self.certified_count)*100,1)
                    output = item[1] + ";" + str(abs(item[0])) + ";" + \
                             str(percentage) + "%"
                    file.write(output + '\n')
                except (IndexError, ValueError, TypeError):
                    pass

    def write_output(self):
        """
        Calls function find_top_ten to generate the required output files
        :return: returns nothing
        """
        self.find_top_ten(self.occ_dict, self.occ_file, "OCCUPATIONS")
        self.find_top_ten(self.state_dict, self.state_file, "STATES")

    # def find_occupation(self):
    #     """
    #     Finds the top 10 occupations of H1B certified applications
    #     :return: Output file with top 10 occupations, number of certified
    #     applications and its percentage
    #     """
    #     # Sort dictionary based on value and key and retrieve the first 10
    #     # ascending order sort of negative value to obtain top 10
    #     sorted_d = sorted((-value, key) for (key, value) in
    #                       self.occ_dict.items())[:10]
    #     with open(self.occ_file, 'w') as file:
    #         file.write('TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;'
    #                    'PERCENTAGE'+'\n')
    #         for item in sorted_d:
    #             try:
    #                 percentage = round((abs(item[0])/
    #                                     self.certified_count)*100,1)
    #                 output = item[1] + ";" + str(abs(item[0])) + ";" + \
    #                          str(percentage) + "%"
    #                 file.write(output + '\n')
    #             except (IndexError, ValueError, TypeError):
    #                 pass
    #
    # def find_states(self):
    #     """
    #     Finds the top 10 states of H1B certified applications
    #     :return: Output file with top 10 states, number of certified applications
    #     and its percentage
    #     """
    #     sorted_d = sorted((-value, key) for (key, value) in
    #                       self.state_dict.items())[:10]
    #     print(sorted_d)
    #     print(self.state_dict)
    #     with open(self.state_file, 'w') as file:
    #         file.write('TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE')
    #         file.write('\n')
    #         for item in sorted_d:
    #             try:
    #                 percentage = round((abs(item[0])/
    #                                     self.certified_count)*100,1)
    #                 output = item[1] + ";" + str(abs(item[0])) + ";" + \
    #                          str(percentage) + "%"
    #                 file.write(output + '\n')
    #             except (IndexError, ValueError, TypeError):
    #                 pass


def main(input_file,output_file1,output_file2):
    """
    Main function that identifies the columns, top 10 occupations and states
    :param input_file: path of input h1b_input.csv file
    :param output_file1: path of output top_10_occupations.txt file
    :param output_file2: path of output top_10_states.txt file
    :return: returns nothing
    """
    visa_stats = VisaStats(input_file,output_file1, output_file2)
    visa_stats.filter_columns()
    visa_stats.write_output()
    # visa_stats.find_occupation()
    # visa_stats.find_states()



if __name__ == "__main__":
    # main("../input/H1B_FY_2014.csv", "../output/occ.txt", "../output/stat.txt")
    main(sys.argv[1], sys.argv[2], sys.argv[3])