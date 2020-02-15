# Python3 util to grep one csv/file for contents from another file.

bldgs = open('file1', 'r').readlines()  # contents of first file
wmcs = open('file2.csv', 'r').readlines()  # Second csv file.

match = {}
for bldg in bldgs:  # Loop over both files looking for the match.
  for wmc in wmcs:
    if bldg.lower().strip('\n') in wmc.lower().split(',')[2]:
      match[bldg.lower().strip('\n')] = wmc.lower().split(',')[1]

for k,v in sorted(match.items()):
  print(k + ',' + v)  # Print results in CSV format.
