#coding: utf-8
from moduleInstallation import ModuleInstallation

#Check and, if not present, instal nltk and needed packages
def moduleCheckAndInstallation(moduleInstallationInstance):

	if moduleInstallationInstance.getModuleVersionUsed() is None:
		choiceSentence =  "Do you want to check " + moduleInstallationInstance.getModule() + " installation (y/n)? "
	if moduleInstallationInstance.getModuleVersionUsed() is not None:
		choiceSentence =  "Do you want to check " +moduleInstallationInstance.getModule() + \
		" and his packages to see if they are up-to-date for our script : \n\t" + \
		moduleInstallationInstance.getModule() + " version " + moduleInstallationInstance.getModuleVersionUsed()

	if moduleInstallationInstance.getPackages() is not None:
		for package in moduleInstallationInstance.getPackages() :
			choiceSentence += "\n\tpackage " + package
		choiceSentence += "\nProceed(y/n)? "

	if moduleInstallationInstance.getPythonVersion() < (3,0,0):
		choice = raw_input(choiceSentence).lower()
	elif moduleInstallationInstance.getPythonVersion() > (3,0,0):
		choice = input(choiceSentence).lower()

	if choice  in moduleInstallationInstance.getAnswersYN()[0] :
		moduleInstallationInstance.checkModuleInstallation()
	elif choice in moduleInstallationInstance.getAnswersYN()[1] :
				pass
	elif choice not in moduleInstallationInstance.getAnswersYN():
		print("\n Uncorrect answer, please rewrite it.\n")
		moduleCheckAndInstallation(nltkInstall)

def python2Utf8Encoding():
	import sys
	reload(sys)
	sys.setdefaultencoding('utf8')

def terminalUtf8Encoding(nltkInstall):
	import os
	import sys
	print("\nCheck if the terminal is compatible with utf-8 encoding : ")
	try:
		print("'\u03bb'")
		print("\nThe terminal is compatible.\n")
	except:
		print("\nThe terminal isn't compatible.\n")
		print("The script will change some variables to adapt this.")
		if nltkInstall.getNameOS() == "nt":
			os.system("chcp 65001")
			print("Modification have been made.")
			os.execv(sys.executable, ['python'] + sys.argv)
		else:
			os.system("export LC_ALL=en_US.UTF-8")
			os.system("export LANG=en_US.UTF-8")
			os.system("export LANGUAGE=en_US.UTF-8")
			print("Modification have been made.\n")

def progressInstallation(nltkInstall):
	#Check if progress is installed to show progression bar
	#And import basic data from nltkInstall Instance to ease installation
	progressInstall = ModuleInstallation("progress")

	progressInstall.setPipVerification(nltkInstall.getPipVerification())

	moduleCheckAndInstallation(progressInstall)

#Extract abstract fom xml downloaded from Pubmed.
def xmlAbstractExtraction(fileName, nltkInstall):
	from xml.dom import minidom
	from nltk import sent_tokenize

	progressInstallation(nltkInstall)

	from progress.bar import Bar

	fileName = fileName + ".xml"

	xmldoc = minidom.parse(fileName)
	l_abstracts = xmldoc.getElementsByTagName('AbstractText')

	d_abstractsSentencesExtracted = {}

	print ("\nParsing and extracting abstracts from corpus")
	bar = Bar('Processing', max=len(l_abstracts))

	for abstractDOM in l_abstracts:
		if nltkInstall.getPythonVersion() < (3,0,0):
			python2Utf8Encoding()
			abstract = abstractDOM.firstChild.nodeValue.encode('utf-8')
			d_abstractsSentencesExtracted[l_abstracts.index(abstractDOM)] = sent_tokenize(abstract.strip())
			bar.next()

		if nltkInstall.getPythonVersion() > (3,0,0):
			d_abstractsSentencesExtracted[l_abstracts.index(abstractDOM)] = sent_tokenize(abstractDOM.firstChild.nodeValue.strip())
			bar.next()

	bar.finish()

	print("Abstracts extracted!")
	return d_abstractsSentencesExtracted

def sentenceCheck(d_abstracts):
	from progress.bar import Bar

	sentencesNumber = sum([len(value) for value in d_abstracts.values()])

	countSentencesChange = 0

	print("\nSentences Consistency check.")
	bar = Bar('Processing', max= sentencesNumber)

	for abstract in d_abstracts:
		for sentence in d_abstracts[abstract]:
			if d_abstracts[abstract][sentence.index(sentence)][-2:] == ".)":
				d_abstracts[abstract][sentence.index(sentence):sentence.index(sentence)+2] = [' '.join(d_abstracts[abstract][sentence.index(sentence):sentence.index(sentence)+2])]
				bar.next()
				countSentencesChange += 1
			bar.next()

	bar.finish()

	print("Sentences consistency check finished!")
	print(str(countSentencesChange) + " sentences have been modified.")

	return d_abstracts

#Tokenize and tag abstract.
def tokenizationAndTagging(d_abstracts):
	from nltk import word_tokenize
	from nltk import pos_tag
	from progress.bar import Bar

	d_abstracts_text_lines = {}

	numberOfAbstracts = 1

	sentencesNumber = sum([len(value) for value in d_abstracts.values()])

	print ("\nAbstract tokenization and tagging")
	bar = Bar('Processing', max = len(d_abstracts))

	for index, abstract in d_abstracts.items():
		numberOfSentence = 1
		d_sentencePerAbstracts = {}

		for line in abstract:
			#creates tokens of a string
			tokens = word_tokenize(line)
			#tags tokens with their PoS
			taggedTokens = pos_tag(tokens)
			numberOfSentence += 1
			d_sentencePerAbstracts[numberOfSentence] = taggedTokens

		d_abstracts_text_lines[numberOfAbstracts] = d_sentencePerAbstracts
		numberOfAbstracts += 1
		bar.next()

	bar.finish()

	print("Abstracts tokenized and tagged.")
	return d_abstracts_text_lines

def nouns_and_verbs_by_sentences(token_pos_text):
	#translate all sentence in a dictionnary with two keys V and N for two lists a verb list and a noun list.

	from progress.bar import Bar

	nltk_verbs = ['VB','VBD','VBG','VBN','VBP','VBZ'] #verb PoS with nltk tagger
	nltk_nouns = ['NN','NNS','NNP','NNPS'] #noun PoS with nltk tagger

	d_abstracts_sentences_NandV = {}
	numberOfAbstracts = 1

	print("\nNouns and verbs in abstracts extraction.")
	bar = Bar('Processing', max = len(token_pos_text))

	for abstractIndex, abstract in token_pos_text.items():
		d_sentencePerAbstracts = {}
		numberOfsentence = 0

		for sentenceIndex, sentence in abstract.items():
			verbs = []
			nouns = []

			for token in sentence:
				NandV = {}
				pos = token[1]
				if (pos in nltk_nouns) and (pos not in nouns):
					nouns.append(token[0].lower())
				elif (pos in nltk_verbs) and (pos not in verbs):
					verbs.append(token[0].lower())

			NandV = {'N':nouns,'V':verbs}  #each key is a line number start at 0, the first sentence is the 0 key, the second 1 ect...
			d_sentencePerAbstracts[numberOfsentence] = NandV
			numberOfsentence += 1

		d_abstracts_sentences_NandV[numberOfAbstracts] = d_sentencePerAbstracts
		numberOfAbstracts += 1
		bar.next()

	bar.finish()

	print("Nouns and verbs in abstracts extracted.")
	return d_abstracts_sentences_NandV

def check_couple_in_sentences(d_abstracts_sentences_NandV, window):
#this function use a text translated in a NadnV text and check all couples (verb/nouns) and their occurence.
	from progress.bar import Bar

	d_abstracts_sentences_couples_checked = {}
	numberOfAbstracts = 1

	print("\nChecking couples in sentences in abstracts.")
	bar = Bar('Processing', max = len(d_abstracts_sentences_NandV))

	for abstractIndex, abstract in d_abstracts_sentences_NandV.items():

		numlines = len(abstract.values())
		d_abstracts_sentences_couples = {}
		for lines in range(window, numlines-window):
			d_abstract_couple_numbers = {}
			if lines == window: #at the beginning
				nouns = []
				verbs = []
				for i in range (lines-window, lines+window):
					sentence = abstract[i]
					nouns = nouns + sentence['N']
					verbs = verbs + sentence['V']
				V_len = len(verbs)
				N_len = len(nouns)
				if V_len >= N_len:
					for i in range (0,V_len):
						for j in range(0, N_len):
							couple = verbs[i] + '\\' + nouns[j]
							if couple not in d_abstract_couple_numbers.keys():
								d_abstract_couple_numbers[couple] = 1
							else:
								d_abstract_couple_numbers[couple] = d_abstract_couple_numbers[couple] + 1
				elif V_len < N_len:
					for i in range (0,N_len):
						for j in range(0, V_len):
							couple = verbs[j] + '\\' + nouns[i]
							if couple not in d_abstract_couple_numbers.keys():
								d_abstract_couple_numbers[couple] = 1
							else:
								d_abstract_couple_numbers[couple] = d_abstract_couple_numbers[couple] + 1

			elif lines > window and lines < (numlines - window - 1) : #during the analysis
				last_sentence = abstract[lines + window]
				for i in range (lines - window, lines + window - 1): #parcour les phrases precedent la nouvelle phrase lors du glissement de la fenêtre.
					sentence = abstract[i]
					nouns = sentence['N'] + last_sentence['N']
					verbs = sentence['V'] + last_sentence['V']
					V_len = len(verbs)
					N_len = len(nouns)
					if V_len >= N_len:
						for i in range (0,V_len):
							for j in range(0, N_len):
								couple = verbs[i] + '\\' + nouns[j]
								if couple not in d_abstract_couple_numbers.keys():
									d_abstract_couple_numbers[couple] = 1
								else:
									d_abstract_couple_numbers[couple] = d_abstract_couple_numbers[couple] + 1
					elif V_len < N_len:
						for i in range (0,N_len):
							for j in range(0, V_len):
								couple = verbs[j] + '\\' + nouns[i]
								if couple not in d_abstract_couple_numbers.keys():
									d_abstract_couple_numbers[couple] = 1
								else:
									d_abstract_couple_numbers[couple] = d_abstract_couple_numbers[couple] + 1

			elif lines == (numlines - window - 1): #at the end
				nouns = abstract[lines]['N']
				verbs = abstract[lines]['V']
				for i in range (lines + 1, numlines):
					sentence = abstract[i]
					nouns = nouns + sentence['N']
					verbs = verbs + sentence['V']
				for i in range (lines - window,lines):
					sentence = abstract[i]
					for a_noun in sentence['N']:
						for a_verb in verbs:
							couple = a_verb + '\\' + a_noun
							if couple not in d_abstract_couple_numbers.keys():
								d_abstract_couple_numbers[couple] = 1
							else:
								d_abstract_couple_numbers[couple] = d_abstract_couple_numbers[couple] + 1
					for a_noun in nouns:
						for a_verb in sentence['V']:
							couple = a_verb + '\\' + a_noun
							if couple not in d_abstract_couple_numbers.keys():
								d_abstract_couple_numbers[couple] = 1
							else:
								d_abstract_couple_numbers[couple] = d_abstract_couple_numbers[couple] + 1
				for a_noun in nouns:
					for a_verb in verbs:
						couple = a_verb + '\\' + a_noun
						if couple not in d_abstract_couple_numbers.keys():
							d_abstract_couple_numbers[couple] = 1
						else:
							d_abstract_couple_numbers[couple] = d_abstract_couple_numbers[couple] + 1

		d_abstracts_sentences_couples_checked[numberOfAbstracts] = d_abstract_couple_numbers
		numberOfAbstracts += 1
		bar.next()

	bar.finish()

	print("Couples in sentences in abstracts checked.")
	return d_abstracts_sentences_couples_checked

def merge_couplesNV_from_all_abstracts(d_abstract_couple_numbers):
	from progress.bar import Bar

	d_couplesNV_corpus = {}

	print("\nMerging couples NV in corpus.")
	bar = Bar('Processing', max = len(d_abstract_couple_numbers))

	for abstractIndex, abstract in d_abstract_couple_numbers.items():
		for coupleNV, occurenceNV in abstract.items():
			if coupleNV not in d_couplesNV_corpus:
				d_couplesNV_corpus[coupleNV] = occurenceNV
			elif coupleNV in d_couplesNV_corpus:
				d_couplesNV_corpus[coupleNV] += occurenceNV

		bar.next()

	bar.finish()

	print("Couples NV in corpus merged.")
	return d_couplesNV_corpus

def couplesNV_selection_with_cut_off(d_couplesNV_corpus, cutOff):
	from progress.bar import Bar

	d_couplesNV_cutOff_corpus = {}

	print("\nChecking couples NV in corpus, which exceed the cut-off.")
	bar = Bar('Processing', max = len(d_couplesNV_corpus))

	for couplesNV, occurenceNV in d_couplesNV_corpus.items():
		if occurenceNV >= cutOff:
			if couplesNV not in d_couplesNV_cutOff_corpus:
				d_couplesNV_cutOff_corpus[couplesNV] = occurenceNV
			elif couplesNV in d_couplesNV_cutOff_corpus:
				d_couplesNV_cutOff_corpus[couplesNV] += occurenceNV

		bar.next()

	bar.finish()

	print("Couples NV in corpus, which exceed the cut-off checked.")
	print("From " + str(len(d_couplesNV_corpus)) + " couples in corpus, " + str(len(d_couplesNV_cutOff_corpus)) + " have been selectionned.")
	return d_couplesNV_cutOff_corpus

def create_file_with_couple(d_couplesNV_cutOff_corpus):
	from progress.bar import Bar
	import csv

	outputfile  = open('couplesNV_corpus.tsv', "wt")
	writer = csv.writer(outputfile, delimiter='\t')

	writer.writerow(["Verbs", "Nouns", "Occurences"])

	print("\nWriting couples into a tsv file named : couplesNV_corpus.tsv.")
	bar = Bar('Processing', max = len(d_couplesNV_cutOff_corpus))

	for couplesNV, occurenceNV in d_couplesNV_cutOff_corpus.items():
		l_couplesNV = couplesNV.split("\\")
		l_couplesNV.append(occurenceNV)
		writer.writerow(l_couplesNV)
		bar.next()

	bar.finish()

	outputfile.close()
	print("Couples writed, file created.")

def choice_input_number(variableName, nltkInstall):
	sentenceChocie = "\nSelect value of " + variableName + ": "
	if nltkInstall.getPythonVersion() < (3,0,0):
		choice = int(raw_input(sentenceChocie).lower())
	elif nltkInstall.getPythonVersion() > (3,0,0):
		choice = int(input(sentenceChocie))

	return choice

def count_noun_in_couple(d_couplesNV_cutOff_corpus):
	from progress.bar import Bar

	d_nouns_occurrence = {}

	print("\nRetrieving all nouns and their occurrence in the couples.")
	bar = Bar('Processing', max = len(d_couplesNV_cutOff_corpus))

	for couplesNV, occurrenceNV in d_couplesNV_cutOff_corpus.items():
		nounsFromCouplesNV = couplesNV.split("\\")[1]
		if nounsFromCouplesNV not in d_nouns_occurrence:
			d_nouns_occurrence[nounsFromCouplesNV] = occurrenceNV
		if nounsFromCouplesNV in d_nouns_occurrence:
			d_nouns_occurrence[nounsFromCouplesNV] += occurrenceNV
		bar.next()

	bar.finish()

	print("Nouns and their occurrence in the couples retrieved.")

	return d_nouns_occurrence

def occurrence_distribution(d_nouns_occurrence, window_distribution):
	from progress.bar import Bar

	d_nouns_occurrence_distribution = {}

	print("\nProcessing occurrence distribution for all couples.")
	bar = Bar('Processing', max = len(d_nouns_occurrence))

	for nouns, occurrenceOfNoun in d_nouns_occurrence.items():
		l_distribution = []
		for nouns_comparison, occurrenceOfNoun_comparison in d_nouns_occurrence.items():
			if occurrenceOfNoun == occurrenceOfNoun_comparison:
				l_distribution.append(nouns_comparison)
			for number_distribution in range(window_distribution):
				number_distribution = number_distribution + 1
				occurrenceNV_comparison_more = occurrenceOfNoun_comparison + number_distribution
				occurrenceNV_comparison_minus = occurrenceOfNoun_comparison - number_distribution
				if occurrenceNV_comparison_more == occurrenceOfNoun:
					l_distribution.append(nouns_comparison)
				if occurrenceNV_comparison_minus == occurrenceOfNoun:
					l_distribution.append(nouns_comparison)
		d_nouns_occurrence_distribution[occurrenceOfNoun] = l_distribution
		bar.next()

	bar.finish()

	print("Occurrence distribution processed.")

	return d_nouns_occurrence_distribution

def main():
	nltkInstall = ModuleInstallation("nltk", ['punkt', 'averaged_perceptron_tagger'], "3.2.1")
	moduleCheckAndInstallation(nltkInstall)
	terminalUtf8Encoding(nltkInstall)
	d_abstractWithSentences = xmlAbstractExtraction("predator-prey[Title]", nltkInstall)
	d_abstractWithSentencesModified = sentenceCheck(d_abstractWithSentences)
	d_abstracts_text_lines = tokenizationAndTagging(d_abstractWithSentencesModified)
	d_abstracts_sentences_NandV = nouns_and_verbs_by_sentences(d_abstracts_text_lines)
	windowLengthChoice =  choice_input_number("window_Length", nltkInstall)
	d_abstract_couple_numbers = check_couple_in_sentences(d_abstracts_sentences_NandV , windowLengthChoice)
	d_couplesNV_corpus = merge_couplesNV_from_all_abstracts(d_abstract_couple_numbers)
	cutOffChoice =  choice_input_number("cut_off", nltkInstall)
	d_couplesNV_cutOff_corpus = couplesNV_selection_with_cut_off(d_couplesNV_corpus, cutOffChoice)
	create_file_with_couple(d_couplesNV_cutOff_corpus)
	d_nouns_occurrence = count_noun_in_couple(d_couplesNV_cutOff_corpus)
	windowDistribution =  choice_input_number("window_distribution", nltkInstall)
	d_nouns_occurrence_distribution = occurrence_distribution(d_nouns_occurrence, windowDistribution)
	print(d_nouns_occurrence_distribution)

main()