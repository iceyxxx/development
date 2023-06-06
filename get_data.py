import csv
import codecs
import re
import copy
storyline = []
storyline.append({})
with codecs.open('./story.csv', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f, skipinitialspace=True):
        row['JumptoNum'] = row['JumptoNum'].split('/')
        row['RestrainType'] = row['RestrainType'].split('/')
        row['RestrainNum'] = row['RestrainNum'].split('/')
        row['AddNum'] = row['AddNum'].split('/')
        storyline.append(row)
print(storyline)