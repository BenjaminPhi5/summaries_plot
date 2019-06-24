import os
import re
import csv

"""
# now generate a big csv for the extracted data.

# I will have 4 csvs, one for each of attempts, min, max, median - assume each subject has two questions
# and so two values per column (some topics only have 1)

# so we have topic name 2019 min1 min2 2018 min1 min2 etc for each topic
"""

# get txt file handles
file_handles = os.listdir('text_files/')
print(file_handles)

# regex to detect that it starts with a number
# the earlier records don't have a median, so have to match at most 1 extra number columns followed by a space
regex = "[0-9][0-9]? [0-9][0-9]? [0-9][0-9]? ([0-9][0-9]? )?[A-Z][A-z]*"

# get regex
pattern = re.compile(regex)

# dictionary of results
results = {}


new_lines = []  # formatted lines will be stored in this temp array


# apply formatting to lines, where some \n characters have not been inserted
def format_line(line_f):
    index = 0
    start = 0
    count = 0
    on_num = False
    on_char = False
    selected_line = ''
    for c in line_f:

        # on digits
        if c.isdigit():
            on_num = True
            # if also on char found misplaced line
            if on_char:
                selected_line = line_f[start:index-1] + '\n'
                new_lines.append(line_f[start:index-1] + '\n')
                count += 1
                on_char = False
                start = index

        if count == 2:
            selected_line = line_f[start:]
            new_lines.append(line_f[start:])
            break

        # on chars
        elif c.isalpha():
            on_char = True
            if on_num:
                on_num = False

        # increment index
        index += 1
    # put in lines that were fine, and weve got to the end of them
    new_lines.append(line_f[start:])


# extract the attempts, min, max, median and the
def extract(current_line):
    values = ["", "", "", ""]
    index = 0
    topic = ""
    line_index = 0

    for c in current_line:
        # extract numerical values
        if c.isdigit() or c == '.':
            values[index] += c
        # move on to next value
        elif c == ' ':
            index += 1
        # extract topic
        elif c.isalpha:
            topic = line[line_index::]
            break

        # increment index into line (for extracting topic)
        line_index += 1

    # remove newline from topic
    topic = topic[:-1]

    return values[0], values[1], values[2], values[3], topic


# insert new values into the dictionary of results
def insert_data(attempts_d, min_d, max_d, median_d, topic_d, year_d):

    if topic_d == 'Prolog for Artificial Intelligence':
        print("hi")

    # first check if the topic is currently present at all or not
    if topic_d in results:
        # if present next check if the year is present
        if year_d in results[topic_d]:
            # update the year entry to include the next question's data for that year
            results[topic_d][year][0].append(attempts_d)
            results[topic_d][year][1].append(min_d)
            results[topic_d][year][2].append(max_d)
            results[topic_d][year][3].append(median_d)

        else:
            # add the new year information as per below
            results[topic_d][year_d] = [[attempts_d], [min_d], [max_d], [median_d]]
    else:
        # add new topic to results, using an inner dictionary for the year, storing a list of lists for each value
        # since there may have been more than one question per the topic that year
        results[topic_d] = {year_d: [[attempts_d], [min_d], [max_d], [median_d]]}


# for replacing alias topic names (where they don't always use the exact same name for a course) with the original name.
def switch_alias_topic(topic_a):
    switcher = {
        'AI II': 'Artificial Intelligence II',
        'Comp. Syst. Mod.': 'Comp. Sys. Modelling',
        'Computer System Modelling': 'Computer Systems Modelling',
        'Comparative Programming Languages': 'Concepts in Programming Languages',
        'Denotational Sem.': 'Denotational Semantics',
        'DSP': 'Digital Signal Processing',
        'Hoare Logic': 'Hoare Logic & Model Checking',
        'Hoare Logic ': 'Hoare Logic & Model Checking',
        'Hoare Logic & Model checking': 'Hoare Logic & Model Checking',
        'Human–Computer Interaction': 'HCI',
        'Human-Computer Interaction': 'HCI',
        'Info. Retrieval': 'Information Retrieval',
        'Information Theory and Coding': 'Information Theory',
        'NLP': 'Natural Language Processing',
        'Principles of Comm.': 'Principles of Communications',
        'System-on-Chip Design': 'System on-Chip Design',
        'System on-Chip-Design': 'System on-Chip Design',
        'Temporal Logic & Model Checking': 'Hoare Logic & Model Checking',
        'Topics in Concurrency ': 'Topics in Concurrency'

    }
    if topic_a in switcher:
        return switcher[topic_a]
    else:
        return topic_a


# some first and second year courses have slipped into later papers due to their diploma
# thingy from a few years ago.. bah bad this messes me up a bit
# so instead I will vet a list of topics I do not care about - this is getting woefully inefficient now
# but it doesn't matter since it is just data prep, once its done its done.
dont_cares = ['Compiler Construction', 'Complexity Theory', 'Computation Theory', 'Computer Design',
              'Continuous Mathematics', 'Database Theory', 'Databases', 'Digital Communication',
              'Digital Communication II', 'Digital Electronics', 'Distributed Systems', 'Floating-Point Computation',
              'Foundations of Programming', 'Introduction to Func. Programming', 'Introduction to Security',
              'Numerical Analysis I', 'Numerical Analysis II', 'Operating System Foundations',
              'Operating System Functions', 'Programming in C and C++', 'Security', 'Software Engineering I',
              'Software Engineering II', 'Software Engineering and Design']

# I care about results where the paper > 6 and the paper name does not include IB
for file_h in file_handles:

    # reset new lines
    new_lines = []

    # get year of record
    year = file_h[7:11]

    # first open the file and get lines
    lines = open('text_files/' + file_h, 'r').readlines()

    # find the lines of the file I care about
    count = 0
    for line in lines:
        if 'paper 7' in line.lower() and 'ib' not in line.lower():
            break
        else:
            count += 1

    # remove leading lines before relevant paper
    lines = lines[count::]

    # generate new lines list that is correctly formatted
    for line in lines:
        format_line(line)
    lines = new_lines

    # if line matches, extract data and put it in dictionary
    for line in lines:
        if re.findall(pattern, line):
            # extract data
            attempts_l, min_l, max_l, median_l, topic_l = extract(line)
            print("LINE: " + year + ": " + line)

            # switch out an alias topic for its original:
            topic_l = switch_alias_topic(topic_l)

            # put data in dictionary, if the topic is relevant
            if topic_l not in dont_cares:
                insert_data(attempts_l, min_l, max_l, median_l, topic_l, year)

# now the results have been collected into a dictionary, I will write this dictionary to csvs
print(results)

"""
------------------------------------------------------------------------------------------------------------------------
------------ DATA HAS BEEN EXTRACTED, NOW WRITE IT TO CSV --------------------------------------------------------------
"""


# Create a csv file for each in the csvs folder
csv_attempts_file = open('csvs/attempts.csv', 'w')
csv_mins_file = open('csvs/mins.csv', 'w')
csv_maxes_file = open('csvs/maxes.csv', 'w')
csv_medians_file = open('csvs/medians.csv', 'w')

# get csv writer objects
writer_attempts = csv.writer(csv_attempts_file)
writer_mins = csv.writer(csv_mins_file)
writer_maxes = csv.writer(csv_maxes_file)
writer_medians = csv.writer(csv_medians_file)

# Create an array of the correct format for the csv header
csv_headings_contents = [['topic'] + [item
                                      for sublist in
                                      [[str(year) + ' a', str(year) + ' b'] for year in range(2000, 2020)]
                                      for item in sublist]
                         ]

csv_attempts_contents = [['attempts']] + csv_headings_contents
csv_mins_contents = [['mins']] + csv_headings_contents
csv_maxes_contents = [['maxes']] + csv_headings_contents
csv_medians_contents = [['medians']] + csv_headings_contents

# generate the contents from the dictionary, sorting by topic
for topic in sorted(results):
    print(topic)
    row_attempt = [topic]
    row_min = [topic]
    row_max = [topic]
    row_median = [topic]
    for year_s in range(2000, 2020):
        if str(year_s) in results[topic]:
            values_list = results[topic][str(year_s)]
            if len(values_list[0]) == 2:
                row_attempt += [values_list[0][0], values_list[0][1]]
                row_min += [values_list[1][0], values_list[1][1]]
                row_max += [values_list[2][0], values_list[2][1]]
                row_median += [values_list[3][0], values_list[3][1]]
            else:
                # only one question for that topic that year
                row_attempt += [values_list[0][0], ""]
                row_min += [values_list[1][0], ""]
                row_max += [values_list[2][0], ""]
                row_median += [values_list[3][0], ""]

        else:
            # values not present, so fill the csvs with nothing:
            row_attempt += ["", ""]
            row_min += ["", ""]
            row_max += ["", ""]
            row_median += ["", ""]

    # add rows to csv columns
    csv_attempts_contents += [row_attempt]
    csv_mins_contents += [row_min]
    csv_maxes_contents += [row_max]
    csv_medians_contents += [row_median]


# data added to csv tables now

# Write the contents:
writer_attempts.writerows(csv_attempts_contents)
writer_mins.writerows(csv_mins_contents)
writer_maxes.writerows(csv_maxes_contents)
writer_medians.writerows(csv_medians_contents)

# close csv files
csv_attempts_file.close()
csv_mins_file.close()
csv_maxes_file.close()
csv_medians_file.close()

print('done!')
