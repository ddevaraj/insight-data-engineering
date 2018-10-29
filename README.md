# H1B Statistics

Insight Data Engineering Coding Challenge

## Table of Contents
1. [Challenge Summary](README.md#challenge-summary)
2. [Approach](README.md#approach)
3. [Run Instructions](README.md#run-instructions)

### Challenge Summary
A task to find trends in the immigration data of H1B visa application processing over the years. This task analyzes the past years data and calculates two metrics - Top 10 Occupations and Top 10S States for certified visa applications.

The data is downloaded from the [Office of Foreign Labor Certification Performance Data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis) and converted into a semicolon(;) separated CSV file. 

### Approach
The task analyzes the data sent as h1b_input.csv and created a simple dictionary to store the values (book-keeping). 
Language - Python3

#### Data
The semicolon separated CSV file is read by the program and only the essential column headers are identified. Since each year can have different data/column headers, the column headers are initially read and generalized. The columns headers that are required are: 
* CASE_NUMBER - To uniquely identify the visa application
> CSV file can have duplicates of the case_number, and this data is avoided. A set is created to store the unique case numbers that were encountered.
* STATUS - Status of the visa application to be CERTIFIED
* SOC_NAME - Standard Occupational Classification name that denotes the occupation of the visa applicant
* WORKSITE_STATE - State in which the user is intended to work 

#### Implementation
The required columns are identified, the script parses through each row of the file to extract data. If the visa status is certified, a dictionary is created to store the worksite_state. The state becomes the key of the dictionary and its occurrence is the key. The occupation dictionary is also created the same way (only for soc_name field not being empty).
The dictionaries are sorted and the top 10 occupations and states are identified.

#### Directory Structure 
The directory structure of the repo looks like:
```
      ├── README.md 
      ├── run.sh
      ├── src
      │   └──h1b_analytics.py
      ├── input
      │   └──h1b_input.csv
      ├── output
      |   └── top_10_occupations.txt
      |   └── top_10_states.txt
      ├── insight_testsuite
          └── run_tests.sh
          └── tests
              └── test_1
              |   ├── input
              |   │   └── h1b_input.csv
              |   |__ output
              |   |   └── top_10_occupations.txt
              |   |   └── top_10_states.txt
              ├── test_2
                  ├── input
                  │   └── h1b_input.csv
                  |── output
                  |   |   └── top_10_occupations.txt
                  |   |   └── top_10_states.txt
```

#### Result
The top 10 occupations and top 10 states of certified visa applications is written into *top_10_occupations.txt* and *top_10_states.txt* respectively. 

The format of the result files are:

`./output/top_10_occupations.txt`:
```
TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
SOFTWARE DEVELOPERS, APPLICATIONS;6;60.0%
ACCOUNTANTS AND AUDITORS;1;10.0%
COMPUTER OCCUPATIONS, ALL OTHER;1;10.0% 
COMPUTER SYSTEMS ANALYST;1;10.0%
DATABASE ADMINISTRATORS;1;10.0%
```
`./output/top_10_states.txt`:
```
TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
FL;2;20.0%
AL;1;10.0%
CA;1;10.0%
DE;1;10.0%
GA;1;10.0%
MD;1;10.0%
NJ;1;10.0%
TX;1;10.0%
WA;1;10.0%
``` 
### Run Instructions
To run the h1b-analytics.py, the run.sh file is invoked. 
> run.sh contains command to run the python script with the input and output file paths as arguments

```
python3 ./src/h1b-analytics.py ./input/h1b_input.csv ./output/top_10_occupations.txt ./output/top_10_states.txt
```
