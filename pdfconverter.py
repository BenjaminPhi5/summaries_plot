from tika import parser
import os

# Will extract the text from each pdf, and store it as a series of text files.
# Get list of all the summary pdfs.
file_handles = os.listdir('pdfs/')
s = "summary.pdf"

length = str(len(file_handles))
count = 1

# print length of file handles
print('status: 0/' + length)

# extract the data from each file, only extracting the b files:
for file in file_handles:

    if file[-5] == 'b':

        # extract text
        raw = parser.from_file('pdfs/' + file)
    
        # write text from pdf to a txt file
        open("text_files/" + file[0:-4] + '.txt', 'w').write(raw['content'])

    # print index
    print('status: ' + str(count) + '/' + length)
    count += 1
    

print('done!')
