import csv

dwdata = []

with open('whitehouse_darkmarket_torrez.csv', 'r') as data:
    reader = csv.reader(data)
    for row in reader:
        dwdata.append(row)

torrez_values = []
for entry in dwdata:
    try:
        if '(' in entry[6]:
            torrez_values.append(entry[6]) 
    except:
        pass


positives = []
negatives = []
neutrals = []
for rating in torrez_values:
    rating = rating.replace('(', '')
    rating = rating.replace(')', '')
    positives.append(int(rating.split('/')[0]))
    negatives.append(int(rating.split('/')[1]))
    neutrals.append(int(rating.split('/')[2]))

print(positives)
print(negatives)
print(neutrals)

print(sum(positives) / len(positives))
print(sum(negatives) / len(negatives))
print(sum(neutrals) / len(neutrals))