import argparse
import time
from word2number import w2n

parser = argparse.ArgumentParser(description='set a timer for')
parser.add_argument('--prompt')
args = parser.parse_args()
prompt = args.prompt
number_words = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen","seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred"}
tokenized = prompt.split()
hours = list()
minutes = list()
seconds = list()

if 'hours' in tokenized or 'hour' in tokenized or 'our' in tokenized or 'ours' in tokenized:
    for i in tokenized:
        if i == 'hours' or i == 'hour':
            lastdex = tokenized.index(i)
            tokenized = tokenized[lastdex::]
            break
        else:
            hours.append(i)
else:
    pass

if 'minutes' in tokenized or 'minute' in tokenized:    
    for i in tokenized:
        if i == 'minutes' or i =='minute':
            lastdex = tokenized.index(i)
            tokenized = tokenized[lastdex::]
            break
        else:
            minutes.append(i)
else:
    pass

   
if 'seconds' in tokenized or 'second' in tokenized:
    for i in tokenized:
        if i == 'seconds' or i =='second':
            lastdex = tokenized.index(i)
            tokenized = tokenized[lastdex::]
            break
        else:
            seconds.append(i)
else:
    pass

try:
    hours = w2n.word_to_num(' '.join(hours))
except:
    hours = 0

try:
    minutes = w2n.word_to_num(' '.join(minutes))
except:
    minutes = 0

try:
    seconds = w2n.word_to_num(' '.join(seconds))
except:
    seconds = 0

timer = seconds + (minutes * 60) + (hours * 60 * 60)
print(f'setting a timer for {hours} hours, {minutes} minutes, and {seconds} seconds')
time.sleep(timer)
