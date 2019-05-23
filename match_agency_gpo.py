###LOWERCASE EVERYTHING

import unicodecsv as csv
import itertools
import json
import sys

csv.field_size_limit(sys.maxsize)

abbreviations_dict = {}

def insert_initial(arr, initial_word):
    arr_inserted = []
    for a in arr:
        arr_inserted.append([initial_word] + a if initial_word is not None else a)
    return arr_inserted


def find_comb(sent_array, initial_word=None):

    # base case
    if len(sent_array) == 1:
        combs = [[sent_array[0]]]
        try:
            word_reps = abbreviations_dict[sent_array[0]]
            for r in word_reps:
                combs.append([r])
        except KeyError:
            pass
        return insert_initial(combs, initial_word)

    combs = find_comb(sent_array[1:], sent_array[0])
    try:
        word_reps = abbreviations_dict[sent_array[0]]
        for r in word_reps:
            combs.extend(find_comb(sent_array[1:], r))
    except KeyError:
        pass
    return insert_initial(combs, initial_word)


def start(sent):
    sent_arrays = find_comb(sent.split())
    sents = [" ".join(s) for s in sent_arrays]
    return sents



#finds al alternatives of the agency name
# inefficient, use the recursive method instead
def find_all_alternatives(original, substitution_dict):
	all_words = []
	agency_name_words = original.split()
	for word in agency_name_words:
		all_words.append(word)
		if word in substitution_dict:
			all_words.extend(substitution_dict[word])

	all_combinations = itertools.permutations(all_words, len(agency_name_words))

	final_options = []

	#prune all_combinations
	for possible_combination in all_combinations:
		possible = True
		for i, word in enumerate(possible_combination):
			options_at_index_i = [agency_name_words[i]]
			if word in substitution_dict:
				options_at_index_i.extend(substitution_dict[word])

			if word not in options_at_index_i:
				possible = False
				break

		if possible:
			final_options.append(" ".join(possible_combination))

	return final_options


### FOR ENSURING MATCH IS NOT A STATE AGENCY
state_abbreviations = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", \
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", \
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", \
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", \
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
state_abbreviations_lower = [s.lower() for s in state_abbreviations]

states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado', \
         'Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho', \
         'Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana', \
         'Maine' 'Maryland','Massachusetts','Michigan','Minnesota', \
         'Mississippi', 'Missouri','Montana','Nebraska','Nevada', \
         'New Hampshire','New Jersey','New Mexico','New York', \
         'North Carolina','North Dakota','Ohio', 'Oklahoma', \
         'Oregon','Pennsylvania','Rhode Island', 'South  Carolina', \
         'South Dakota','Tennessee','Texas','Utah', 'Vermont', \
         'Virginia','Washington','West Virginia', 'Wisconsin','Wyoming']
states_lower = [s.lower() for s in states]


all_state_matches = set()
#all words before matches are states/state abreviations
def is_state_match(text, matched_string):
    match = 0
    text = "filler " + text # in case the matches happen at the beginning
    words_before_matches = []

    #print matched_string
    #print text
    strings = text.lower().split(matched_string.lower())[:-1]
    for s in strings:
        try:
            words_before_matches.append(s.strip().split()[-1])
        except:
            continue
    for word in words_before_matches:
        if word in state_abbreviations_lower or word in states_lower:
            match += 1
    if match == len(words_before_matches):
        all_state_matches.add(tuple([matched_string, text]))
        #state_writer.writerow([matched_string, text])
        return True
    return False


#open file
abbreviations_dict = {}

abbreviations_file = csv.reader(open("data/agency_name_data/Abbreviations for Master agencies list_Oct. 2018.csv", 'rU'), delimiter=',', quotechar='"')
abbreviations_file.next()
for row in abbreviations_file:
	word = row[0].lower()
	synonyms = [item.lower() for item in row[1:] if item]
	print row

	abbreviations_dict[word] = synonyms
	print word, abbreviations_dict[word]

	#for synonym in synonyms:
	#	if synonym in abbreviations_dict:
	#		print synonym
	#		raise "Wwewewe"
	#	abbreviations_dict[synonym] = synonyms
	#	print abbreviations_dict[synonym]



#read in all abreviations, save dict of each word: list of all abreviations (others in that row)
#check if key already in dictionary



#master agency list file
master_agency_file = csv.reader(open("data/agency_name_data/Master agencies list_Oct.2018.csv", 'rU'), delimiter=',', quotechar='"')
master_agency_file.next()

agency_name_to_code = {}
agency_acronym_to_code = {}

for row in master_agency_file:
	code = row[0]
	agency_names = [item.lower() for item in row[1:8] + row[12:] if item]
	agency_acronym = row[11].lower()
	agency_acronym_to_code[agency_acronym] = code
	#print agency_names

	for name in agency_names:
		if name.lower() == "va":
			agency_acronym_to_code["va"] = code
			continue
		agency_name_to_code[name] = code

		#all_alternatives = find_all_alternatives(name, abbreviations_dict)
		sents = start(name)

		for sent in sents:
			if "united states" in sent:
				#need to handle the case where the word we're replacing is two words (ie united states)
				agency_name_to_code[sent.replace("united states", "us")] = code
				agency_name_to_code[sent.replace("united states", "u.s.")] = code
			agency_name_to_code[sent] = code

		
		#if len(sents) > 1:
		#	print "orig", name
		#	print "alternatives", sents


		#agency_name_words = name.split()
		

		"""count = 0
		for abreviation in abbreviations_dict:
			if abreviation in agency_name_words:
				count += 1
				continue

				##sometimes three times (I think not more)
				## also need to take into account multi word things, ie US (United States is only case)
				for abreviation_synonym in abbreviations_dict[abreviation]:
					new_name = " ".join([abreviation_synonym if x==abreviation else x for x in name.split()])
					#new_name = "".join(name.split().replace(abreviation, abreviation_synonym))
					print new_name
					agency_name_to_code[new_name] = code

					for abreviation_2 in abbreviations_dict:
						if abreviation_2 == abreviation: #don't replace the same synonym
							continue
						if abreviation_2 in agency_name_words:
							for abreviation_synonym_2 in abbreviations_dict[abreviation_2]:
								new_name_2 = " ".join([abreviation_synonym_2 if x==abreviation_2 else x for x in new_name.split()])
								#new_name = "".join(name.split().replace(abreviation, abreviation_synonym))
								print new_name_2
								agency_name_to_code[new_name_2] = code"""


print len(agency_name_to_code)

#for each entry in columns 2->x
#save that in dict of that: column 1
#when adding, check if any of those in dict, if so save all versions of that


#this will give me a list of phrases to lauren's agency index


#then for each line in the master csv, open the respective text file, open it check for each of the phrases in text
#check for each phrase in title
#were those the only two??
#write my id number in a new column



#convert all json (in results/) to csv (in results_csvs/)
"""from os import listdir
from os.path import isfile, join

inpath = "results/"
onlyfiles = [f for f in listdir(inpath) if isfile(join(inpath, f)) and f.endswith(".txt")]

for f in onlyfiles:
	hearing_text_json = json.loads(open(inpath + f).read())

	outfile_writer = csv.writer(open("results_csvs/" + f.replace(".txt", ".csv"), 'w'), delimiter=',', quotechar='"')
	#header = hearing_text_json[1].keys()
	header = ["committees","raw_comittees","hearing_chamber","name_raw","congress","name_full","member_id",\
	          "jacket","majority","state","leadership","person_chamber","cleaned","date","party","party_seniority"]

	outfile_writer.writerow(header)

	for row in hearing_text_json:
		to_write = []
		for key in header:
			#### need to remove newlines
			if type(row[key]) == list:
				#print row[key]
				to_write.append("".join(row[key]))
				#if len(row[key]) > 1:
				#	to_write.append("".join(row[key]))
				#else:
			elif type(row[key]) == int:
				to_write.append(row[key])
			elif type(row[key]) == str:
				to_write.append(row[key].replace('\n', ' ').replace('\r', ''))
			else:
				to_write.append(row[key])

		outfile_writer.writerow(to_write)
"""

metadata_file = csv.reader(open("metadata_results.csv", 'rU'), delimiter=',', quotechar='"')
header = metadata_file.next() + ["lauren's code (in title)", "lauren's code (in transcript)"]

metadata_file_writer = csv.writer(open("metadata_results_with_code.csv", 'w'), delimiter=',', quotechar='"')
metadata_file_writer.writerow(header)

count = 0
for row in metadata_file:
	count += 1
	if count % 10 == 0:
		print count, "total", 30227
	agency_codes_title = set()
	agency_codes_transcript = set()

	hearing_title = row[3]

	hearing_filename = row[5]

	try:
		#not all transcripts exist
		hearing_text_csv = csv.reader(open("results_csvs/" + hearing_filename + ".csv", 'r'))
		hearing_text_csv.next()
	except:
		hearing_text_csv = []


	for agency_acronym in agency_acronym_to_code:
		agency_acronym_with_periods = "".join([letter + "." for letter in agency_acronym])
		#check in title
		if agency_acronym in hearing_title.lower().split():
			if not is_state_match(hearing_title, agency_acronym):
				#print "agency_acronym", agency_acronym
				agency_codes_title.add(agency_acronym_to_code[agency_acronym])
		if agency_acronym_with_periods in hearing_title.lower().split():
			if not is_state_match(hearing_title, agency_acronym_with_periods):
				#print "agency_acronym_with_periods", agency_acronym_with_periods
				agency_codes_title.add(agency_acronym_to_code[agency_acronym])

	#check in hearing transcript
	for hearing_csv_row in hearing_text_csv:
		for agency_acronym in agency_acronym_to_code:
			transcript = " ".join(hearing_csv_row[12].lower().split())
			if agency_acronym in transcript.split():
				if not is_state_match(transcript, agency_acronym):
					#print "agency_acronym", agency_acronym
					agency_codes_transcript.add(agency_acronym_to_code[agency_acronym])
			if agency_acronym_with_periods in transcript.split():
				if not is_state_match(transcript, agency_acronym_with_periods):
					#print "agency_acronym_with_periods", agency_acronym_with_periods
					agency_codes_transcript.add(agency_acronym_to_code[agency_acronym])


	try:
		#not all transcripts exist
		hearing_text_csv = csv.reader(open("results_csvs/" + hearing_filename + ".csv", 'r'))
		hearing_text_csv.next()
	except:
		hearing_text_csv = []


	for agency_name in agency_name_to_code:
		if agency_name in hearing_title.lower():
			if not is_state_match(hearing_title, agency_name):
				#print "agency_name", agency_name
				agency_codes_title.add(agency_name_to_code[agency_name])

	#check in hearing transcript
	for hearing_csv_row in hearing_text_csv:
		for agency_name in agency_name_to_code:
			transcript = " ".join(hearing_csv_row[12].lower().split())
			if agency_name in transcript:
				if not is_state_match(transcript, agency_name):
					#print "agency_name", agency_name
					agency_codes_transcript.add(agency_name_to_code[agency_name])

	#if agency_codes_title:
	#	print "TITLE MATCH!!"
	#	print agency_codes_title
	#	print hearing_title
	#if agency_codes_transcript:
	#	print "TRANSCRIPT MATCH~!!!"
	#	print agency_codes_transcript


	metadata_file_writer.writerow(row + [",".join(sorted(agency_codes_title, key=int)), ",".join(sorted(agency_codes_transcript, key=int))])




##### NEED TO DEAL WITH UNITED STATES replacements
### separate handling of the acronyms, needs to deal with apostrophe after (eg FIMA's)


#### issues:
#why the acronyms with periods never match in title




#fixed:
#why is just VA matching:
#HOUSE HEARING, 115TH CONGRESS - POWERING AMERICA: REEVALUATING PURPA'S OBJECTIVES AND ITS EFFECTS ON TODAY'S CONSUMERS







