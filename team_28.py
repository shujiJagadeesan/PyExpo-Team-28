from tika import parser
import re

file=r"sampleResumePDF.pdf"

data = parser.from_file(file)
text = data['content']

print("THE CONTENT OF THE PDF FILE IS,\n")
print(text)


phone_numbers= re.findall('[0-9]{10}',text)
emails = re.findall('\S+@\S+',text)

print("PRINTING EMAIL AND THE PHONE NUMBER,\n")



for i in range(len(emails)):
    print(f"EMAIL {i+1} :",emails[i])
    print(f"PHONE NUMBER {i+1} :",phone_numbers[i])
    print("-" * 100)
