# from collections import Counter

# counter = Counter()

# with open("health.log") as file:
#     for line in file:

#         if "INFO" in line:
#             counter["INFO"] +=1

#         elif "WARNING" in line:
#             counter["WARN"] +=1

#         elif "ERROR" in line:
#             counter["ERROR"] +=1
# print(counter)


import re

with open("process.log") as file:
    text = file.read()

matches = re.findall(r"\d+\.\d+\.\d+\.\d+", text)

print(matches)