from __future__ import print_function, unicode_literals
import csv

from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint


style = style_from_dict({
    Token.Separator: '#CEA00F',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#CEA00F',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

questions = [
    {
        'type': 'checkbox',
        'message': 'Select Members You Want Contacts For',
        'name': 'VCards',
        'choices': [
            Separator('= BBS Members Fall 2019 ='),
        ],
        'validate': lambda answer: 'You must choose at least one member.' \
            if len(answer) == 0 else True
    }
]

master = ["BEGIN:VCARD", "VERSION:4.0", "N:", "FN:", "EMAIL:", "TEL:", "END:VCARD"]
contacts = {}

with open('Contact Info.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	for row in csv_reader:
		full_name = row[0].split(" ")
		first_name = full_name[0]
		last_name = full_name[1]

		cur = {}
		cur["name"] = first_name + " " + last_name

		questions[0]["choices"].append(cur)


		contacts[cur["name"]] = {
			"first_name": first_name,
			"last_name": last_name,
			"email": row[1],
			"phone_number": row[2]
		}

answers = prompt(questions, style=style)

mfile = open("BBS_FA19_Contacts.vcf", "w")

for member in answers["VCards"]:

	cur = contacts[member]

	#file_name = cur["first_name"] + "_" + cur["last_name"] + ".vcf"
	#file = open(file_name, "w")
	current = ["", "", cur["last_name"] + ";" + cur["first_name"] + ";", cur["first_name"] + " " + cur["last_name"], cur["email"], cur["phone_number"], ""]
	for i in range(7):
		mfile.write(master[i] + current[i] + "\n")
	line_count += 1
	mfile.write("\n")
	#file.close()
mfile.close()
