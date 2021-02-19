import datetime
import pandas as pd
import argparse


parser = argparse.ArgumentParser(description='Convert WhatsApp chat file to CSV')
parser.add_argument('-i', required=True, type=str, metavar='input', help='whatsapp chat filename')
parser.add_argument('-o', required=True, type=str, metavar='ouput', help='name of file to be output')
args = parser.parse_args()

def read_file(file):
  x = open(file, 'r', encoding = 'utf-8')
  y = x.read()
  content = y.splitlines()
  return content

chat = read_file(args.i)

for i in range(len(chat)):
  try:
    datetime.datetime.strptime(chat[i].split(',')[0], '%m/%d/%y') 
  except ValueError:  
    chat[i-1] = chat[i-1] + ' ' + chat[i] 
    chat[i] = "NA" 
    
#Handle more than double-line texting
for i in range(len(chat)):
  if chat[i].split(' ')[0] == 'NA':
    chat[i] = 'NA'
# print(chat)
while True:
  try:
    chat.remove("NA")
  except ValueError:
    break
        
date = [chat[i].split(',')[0] for i in range(len(chat))]

time = [chat[i].split(',')[1].split('-')[0] for i in range(len(chat))]
time = [s.strip(' ') for s in time] # Remove spacing  

name = [chat[i].split('-')[1].split(':')[0] for i in range(len(chat))]

content = []
for i in range(len(chat)):
  try:
    content.append(chat[i].split(':')[2])
  except IndexError:
    content.append('Missing Text')


df = pd.DataFrame(list(zip(date, time, name, content)), columns = ['Date', 'Time', 'Name', 'Content'])
if '.csv' in args.o:
  df.to_csv(args.o)
else:
  df.to_csv(args.o + '.csv')