import time
import os
import sys
import shutil
import math
import uuid
import requests
import io


print('\nThis program retrieves historical winning numbers for Westlotto. Years list file:')
filename = input()
if not os.path.isfile(filename):
    print('File not found. Exiting...')
    time.sleep(1)
    sys.exit()


uid_str = str(uuid.uuid1())
foldname = os.getcwd()+ '\\' + uid_str
os.mkdir(foldname)


url_base = 'https://www.westlotto.de/lotto-6aus49/gewinnzahlen/gewinnzahlen.html?year='



years_list = open(filename, "r")
years_list_line = years_list.readline()

dates_list = open(foldname + '\\' + 'DATES_LIST.txt', "x")
print('\nGetting dates list.')
while years_list_line != '':
    print('Collecting dates for ' + years_list_line[:4] + '...')
    temp_url_file = requests.get(url_base + str(years_list_line[0:4]))
    response = io.BytesIO(temp_url_file.content)
    inmem = io.TextIOWrapper(response, encoding=None)
    inmem_line = inmem.readline()
    while inmem_line != '':
        if inmem_line == '\u003Cselect name=\u0022date\u0022 \u003E\n':
            inmem_line =  inmem.readline()
            while (inmem_line != '\u003C\u002Fselect\u003E\n') and (inmem_line != ''):
                dates_list.write(inmem_line[15:25] + '\n')
                inmem_line =  inmem.readline()
        else: inmem_line =  inmem.readline()
    response.close()
    inmem.close()
    years_list_line = years_list.readline()
years_list.close()
dates_list.close()







print('\nGetting winning numbers.')
winning_list = open(os.getcwd() + '\\' + 'WINNING-' + uid_str + '.csv', "x")
winning_list.write('Date,1,2,3,4,5,6,,,,Extra draw,,SuperZahl\n')

dates_list = open(foldname + '\\' + 'DATES_LIST.txt', "r")
dates_list_line = dates_list.readline()
url_base = 'https://www.westlotto.de/lotto-6aus49/gewinnzahlen/gewinnzahlen.html?date='

buff_year = '0000'
while dates_list_line != '':
    temp_url_file = requests.get(url_base + str(dates_list_line[0:10]))
    response = io.BytesIO(temp_url_file.content)
    inmem = io.TextIOWrapper(response, encoding=None)
    inmem_line = inmem.readline()
    if buff_year not in dates_list_line:
        buff_year = str(dates_list_line[6:10])
        print('Parsing pages for ' + buff_year + '...')
    spcount = 0
    winning_list.write(dates_list_line[0:10] + ',')
    while inmem_line != '':
# Parsing out main winning 6 numbers
        if ('<span class="polygon polygon-big polygon-outlined">' in inmem_line):
            inmem_line =  inmem.readline()
            winning_list.write(inmem_line[28])
            if str(inmem_line[29]) in '0123456789':
                winning_list.write(inmem_line[29] + ',')
            else: winning_list.write(',')
#            count += 1
            inmem_line =  inmem.readline()
# Parsing out additional winning number drawn from main 49 numbers pool ("7th ball")
        elif ('<span class="polygon polygon-big">' in inmem_line):
            inmem_line =  inmem.readline()
            winning_list.write(',,,' + inmem_line[28])
            if (str(inmem_line[29]) in '0123456789'):
                winning_list.write(inmem_line[29])
            spcount += 1
# Parsing out so called "Superzahl" - one number out of separate pool.
        elif ('<p class="heading-h5">Superzahl</p>' in inmem_line):
            inmem_line =  inmem.readline()
            inmem_line =  inmem.readline()
            if spcount == 1: winning_list.write(',,' + inmem_line[22])
            else: winning_list.write(',,,,,' + inmem_line[22])
            if (str(inmem_line[23]) in '0123456789'):
                winning_list.write(inmem_line[29])
        else:
            inmem_line =  inmem.readline()
        if inmem_line == '':
            winning_list.write('\n')
    response.close()
    inmem.close()
    dates_list_line = dates_list.readline()



dates_list.close()
winning_list.close()
print("Parsing is complete. Removing temporary folder.")
shutil.rmtree(foldname + '\\')
print('Cleaning space is complete. See WINNING-' + uid_str + '.csv for the data gathered.')

time.sleep(1)