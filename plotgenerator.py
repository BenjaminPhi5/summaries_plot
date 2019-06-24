import math
import itertools
import matplotlib.pyplot as plt
import numpy as np
import csv
import matplotlib.font_manager
print(matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))

"""
I have a number of plots that I want to make, these include: 

1) total attempts for the 2019 topics
2) medians for the 2019 topics
3) mean medians for until medians began
6) how the subjects on the last two papers from last year vary over time, for median
7) attempts over time how they've changed

TODO: need to order them by highest to lowest on the graphs
TODO: make the graphs look pretty, not default and ugly. also change font to something nicer

"""

"""
------------------------------------------------------------------------------------------------------------------------
----- OPENING FILES AND AUXILLARY METHODS ------------------------------------------------------------------------------
"""

# open the 4 files
csv_attempts = open("csvs/attempts.csv", 'r')
csv_mins = open("csvs/mins.csv", 'r')
csv_maxes = open("csvs/maxes.csv", 'r')
csv_medians = open("csvs/medians.csv", 'r')

# setup the csv readers
attempts_reader = csv.reader(csv_attempts, delimiter=',')
mins_reader = csv.reader(csv_mins, delimiter=',')
maxes_reader = csv.reader(csv_maxes, delimiter=',')
medians_reader = csv.reader(csv_medians, delimiter=',')

# put the csvs into arrays
attempts_list = [row for row in attempts_reader][2:]    # remove file header and column names
mins_list = [row for row in mins_reader][2:]
maxes_list = [row for row in maxes_reader][2:]
medians_list = [row for row in medians_reader][2:]

# number of columns
no_cols = len(attempts_list[1])


# convert to float -- assumes given an float or integer as a string or the empty string
def convert(string):
    if string == "":
        return 0
    else:
        return float(string)


# calculates a mean of a list of values
def calc_mean(list_values):
    # we don't include zeroes here
    total = 0
    length = 0
    for values in list_values:
        total += values
        if values != 0:
            length += 1
    if length == 0:
        return 0
    else:
        return total/length


"""
------------------------------------------------------------------------------------------------------------------------
----- STYLING THE PLOTS ------------------------------------------------------------------------------------------------

general aesthetic setting applied to all plots
"""

# dark background styling
def dark_style(plt):
    # general plot style
    plt.style.use('dark_background')

    # set axis colour to dark grey and reduce their width, get rid of the box effect
    plt.rcParams['axes.edgecolor'] = '#F4ECF7'  # set axis to grey
    plt.rcParams['axes.linewidth'] = 0.8        # set axis width
    plt.rcParams['xtick.color'] = '#F4ECF7'     # set the tick colours to grey like the bars
    plt.rcParams['ytick.color'] = '#F4ECF7'

    # font - set the family and then font
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Khmer Sangam MN'


# light style
def light_style(plt):
    # general plot style
    plt.style.use('default')

    # set axis colour to dark grey and reduce their width, get rid of the box effect
    plt.rcParams['axes.edgecolor'] = '#333F4B'  # set axis to grey
    plt.rcParams['axes.linewidth'] = 0.8  # set axis width
    plt.rcParams['xtick.color'] = '#333F4B'  # set the tick colours to grey like the bars
    plt.rcParams['ytick.color'] = '#333F4B'

    # font - set the family and then font
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Khmer Sangam MN'


# Style the spines to remove top and right spines, and remove the box effect by making them only
# span the range they need
def style_ax(ax_obj):
    ax_obj.spines['top'].set_color('none')
    ax_obj.spines['right'].set_color('none')
    ax_obj.spines['left'].set_smart_bounds(True)
    ax_obj.spines['bottom'].set_smart_bounds(True)


# instead of plotting a bar graph, with plot a series of horizontal lines on a standard plot,
# the rest of the styling is in the plots themselves...


"""
------------------------------------------------------------------------------------------------------------------------
----- GRAPH 1 - TOTAL ATTEMPTS FOR THE 2019 TOPICS ---------------------------------------------------------------------

here if there are two questions, show two bar lines per topic

"""

# select topics from attempts where there were attempts in 2019
topics = [row[0]
          for row in attempts_list
          if row[no_cols-1] != ""       # the last two columns are the two potential 2019 questions
          or row[no_cols-2] != ""]

# question 1 selection
q1 = [convert(row[no_cols-2]) for row in attempts_list if row[no_cols-1] != "" or row[no_cols-2] != ""]


# question 2 selection
q2 = [convert(row[no_cols-1]) for row in attempts_list if row[no_cols-1] != "" or row[no_cols-2] != ""]


########################################################################################################################

ind = np.arange(len(q1))  # the x locations for the groups
width = 0.35  # the width of the bars

# figure 1
plt.figure(1)

fig, ax = plt.subplots()  # fetch the subplot, can add size parameters here

# the two bar lines
rects1 = ax.barh(ind - width/2, q1, width,
                label='Question 1', color='#F1C40F', alpha=0.9, linewidth=5)
rects2 = ax.barh(ind + width/2, q2, width,
                label='Question 2', color='#58D68D', alpha=0.9, linewidth=5)

# style the axes
style_ax(ax)

# style the plot - by doing it here it only does the legend, cool
dark_style(plt)

# Add text for labels, title and x-axis tick labels, etc.
ax.set_xlabel('Attempts')
ax.set_title('2019 Question Attempts by Topic')
ax.set_yticks(ind)
ax.set_yticklabels(topics)
ax.legend()

# automatically adjusts subplot params so that the subplot(s) fits in to the figure area
# useful for getting the plot to look neat without having to do too much fiddling around
# but doesn't always work, so sometimes have to disable
fig.tight_layout()

# display the plot
plt.show()



"""
------------------------------------------------------------------------------------------------------------------------
----- GRAPH 2 - MEDIANS FOR THE 2019 TOPICS ----------------------------------------------------------------------------

here the topics are the same as before
"""
topics = topics

# question 1 selection
q1 = [convert(row[no_cols-2]) for row in medians_list if row[no_cols-1] != "" or row[no_cols-2] != ""]

# the convert method above gets the numerical value from the string data

# question 2 selection
q2 = [convert(row[no_cols-1]) for row in medians_list if row[no_cols-1] != "" or row[no_cols-2] != ""]

########################################################################################################################


ind = np.arange(len(q1))  # the x locations for the groups
width = 0.35  # the width of the bars

plt.figure(2)
fig, ax = plt.subplots()  # fetch from subplots the fig and axes to modify..? not quite sure

rects1 = ax.barh(ind - width/2, q1, width,
                label='Question 1')
rects2 = ax.barh(ind + width/2, q2, width,
                label='Question 2')

# style the axes
style_ax(ax)

# Add text for labels, title and x-axis tick labels, etc.
ax.set_xlabel('Medians')
ax.set_title('2019 Question Medians by Topic')
ax.set_yticks(ind)
ax.set_yticklabels(topics)
ax.legend()

# change where the legend appears on the graph, to be top left hand corner instead
plt.legend(bbox_to_anchor=(0.22, 1),
           bbox_transform=plt.gcf().transFigure)

fig.tight_layout()

# display the plot
plt.show()



"""
------------------------------------------------------------------------------------------------------------------------
----- GRAPH 3 - MEDIANS FOR THE 2019 TOPICS ---------------------------------------------------------------------

the mean medians per each topics since medians began...
medians began in 2012, so only include topics since 2012
"""

# just fetch all topics
topics = [row[0] for row in medians_list]

# mean medians get the medians for each row, in a list, and calculate the mean of that list
means = [calc_mean([convert(median) for median in row[1:]]) for row in medians_list]
print("means")
print(means)
print(len(q1))

# now create a new topics and means lists where we only include non zero values
new_topics = []
new_means = []
for index in range(0, len(means)):
    if means[index] != 0:
        new_topics.append(topics[index])
        new_means.append(means[index])

topics = new_topics
means = new_means
print(len(topics))
print((len(means)))
print(topics)
print(means)

########################################################################################################################

ind = np.arange(len(means)+1)  # the x locations for the groups
width = 0.25  # the width of the bars

plt.figure(3)
# style the plot
light_style(plt)


# now plot the means on the graph in the same way as the first two....
fig, ax = plt.subplots(figsize=(7, 7))  # fetch from subplots the fig and axes to modify..? not quite sure

my_range = list(range(1,len(topics)+1))

#rects3 = ax3.barh(ind - width/2, means, width)

# plot the straight lines
plt.hlines(y=my_range, xmin=0, xmax=means, color='#007acc', alpha=0.2, linewidth=3)

# plot the dots on the ends
plt.plot(means, my_range, "o", markersize=5, color='#007ACC', alpha=0.6)

# style the axis
style_ax(ax)

# setting a light green background
# fig.patch.set_facecolor('#E9F7EF')
# ax.set_facecolor('#E9F7EF')

# Add text for labels, title and x-axis tick labels, etc.
ax.set_xlabel('Means of medians', fontsize=13, fontweight='black', color='#333F4B')
ax.tick_params(axis='both', which='major', labelsize=10)
ax.set_title('Mean medians per topic 2012-2019', fontsize=15, fontweight='bold', color='#333F4B')
ax.set_yticks(my_range)
ax.set_yticklabels(topics)

fig.tight_layout()

# display the plot
plt.show()




"""
------------------------------------------------------------------------------------------------------------------------
----- GRAPH 4 HOW THE RELEVANT CURRENT TOPICS HAVE VARIED OVER TIME (IN TERMS OF MEDIANS) ------------------------------


for this I need for each topic, how its median varies over time.
will use a dictionary, which will store a set of coordinates, xs being years, ys being median.
if there are two questions, will plot two medians
"""

# vetted topics from paper 7
paper_7_vet = ['Prolog', 'Economics, Law & Ethics', 'HCI', 'Further HCI', 'Concepts in Programming Languages',
               'Formal Models of Language']


# check if a topic has relevant data from the last two years and does not include any of the vetted paper 7 topics
def use_topic(topic_row):
    if topic_row[0] not in paper_7_vet and topic_row[-4:] != ['', '', '', '']:
        return True
    else:
        return False


# get topics that will be used for this data
topics = [row[0] for row in medians_list if use_topic(row)]

# get medians for each topic as a list of lists  (use -16 for 2012 to 2019)
medians_list_list = [[convert(median) for median in row[-16:]] for row in medians_list if use_topic(row)]


# This converts a list of medians into coordinates with the year
coords = [
    [
        (2012 + math.floor(index /2), medians_list[index])      # include the year with the median
        for index in range(0, len(medians_list))                # for each median for that topic
        if medians_list[index] != 0                             # don't include years where there was no value
    ]
    for medians_list in medians_list_list]                      # for each topic's list of medians

# now convert those medians into a set of points to be plotted:

print("-------\n\n")
print(topics)
print(medians_list_list)
print(coords)

########################################################################################################################

# first get number of subplots on this plot
total = len(topics)
numrows = 4
numcols = math.ceil(total / numrows)

# set next figure
plt.figure(4)

fig, ax = plt.subplots(figsize=(30, 10))

# set background colour and title
fig.patch.set_facecolor('xkcd:black')

# get the y axis values
x_range = np.arange(2012, 2021, 1)
y_range = np.arange(5, 22, 2)

# setup the colours for my plots
colors = itertools.cycle(["lime", "salmon", "orange", "magenta", "lightblue", "red", "gold", "lightgreen" ,"violet"])

# unzip the coords for each pair (inefficient I know, could have got the data structure right in the first place)
# and plot each subplot using it
index = 1
for coord_list in coords:
    # style the plot
    dark_style(plt)

    # define current subplot
    ax = plt.subplot(numrows, numcols, index)

    # set title
    plt.title(topics[index-1])

    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    # ticks
    plt.xticks(x_range)
    plt.xlim(2011)
    plt.yticks(y_range)
    plt.ylim(5)

    # plot points
    x, y = zip(*coord_list)
    plt.scatter(x, y, color='xkcd:'+next(colors), s=25)

    index += 1


plt.show()




