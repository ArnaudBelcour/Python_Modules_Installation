#coding: utf-8
from moduleInstallation import ModuleInstallation
nltkInstall = ModuleInstallation("nltk", ['punkt', 'averaged_perceptron_tagger'], "3.2.1")

#Check and, if not present, instal nltk and needed packages
def moduleCheckAndInstallation(moduleInstallationInstance):

	if moduleInstallationInstance.moduleVersionUsed is None:
		choiceSentence =  "Do you want to check " + moduleInstallationInstance.module + " installation (y/n)? "
	if moduleInstallationInstance.moduleVersionUsed is not None:
		choiceSentence =  "Do you want to check " +moduleInstallationInstance.module + \
		" and his packages to see if they are up-to-date for our script : \n\t" + \
		moduleInstallationInstance.module + " version " + moduleInstallationInstance.moduleVersionUsed

	if moduleInstallationInstance.packages is not None:
		for package in moduleInstallationInstance.packages :
			choiceSentence += "\n\tpackage " + package
		choiceSentence += "\nProceed(y/n)? "

	if moduleInstallationInstance.pythonVersion < (3,0,0):
		choice = raw_input(choiceSentence).lower()
	elif moduleInstallationInstance.pythonVersion > (3,0,0):
		choice = input(choiceSentence).lower()

	if choice  in moduleInstallationInstance.answersYN[0] :
		moduleInstallationInstance.checkModuleInstallation()
	elif choice in moduleInstallationInstance.answersYN[1] :
				pass
	elif choice not in moduleInstallationInstance.answersYN:
		print("\n Uncorrect answer, please rewrite it.\n")
		moduleCheckAndInstallation(nltkInstall)

def python2Utf8Encoding():
	import sys
	reload(sys)
	sys.setdefaultencoding('utf8')

def progressInstallation():
	#Check if progress is installed to show progression bar
	#And import basic data from nltkInstall Instance to ease installation
	progressInstall = ModuleInstallation("progress")

	progressInstall.pipVerification = nltkInstall.pipVerification
	progressInstall.pythonVersion = nltkInstall.pythonVersion
	progressInstall.nameOS = nltkInstall.nameOS

	moduleCheckAndInstallation(progressInstall)

#Extract abstract fom xml downloaded from Pubmed.
def xmlAbstractExtraction(fileName):
	from xml.dom import minidom
	from nltk import sent_tokenize

	progressInstallation()

	from progress.bar import Bar

	fileName = fileName + ".xml"

	print ("Parsing and extracting abstracts from corpus")
	xmldoc = minidom.parse(fileName)
	l_abstracts = xmldoc.getElementsByTagName('AbstractText')

	l_abstractsExtracted = []

	d_abstractsSentencesExtracted = {}

	bar = Bar('Processing', max=len(l_abstracts))

	for abstractDOM in l_abstracts:
		if nltkInstall.pythonVersion < (3,0,0):
			python2Utf8Encoding()
			abstract = abstractDOM.firstChild.nodeValue.encode('utf-8')
			l_abstractsExtracted.append(abstract)
			d_abstractsSentencesExtracted[l_abstracts.index(abstractDOM)] = sent_tokenize(abstract.strip())
			bar.next()

		if nltkInstall.pythonVersion > (3,0,0):
			l_abstractsExtracted.append(abstractDOM.firstChild.nodeValue)
			d_abstractsSentencesExtracted[l_abstracts.index(abstractDOM)] = sent_tokenize(abstractDOM.firstChild.nodeValue.strip())
			bar.next()

	bar.finish()

	print("Abstracts extracted!")
	return l_abstractsExtracted, d_abstractsSentencesExtracted

def sentenceCheck(d_abstracts):
	from progress.bar import Bar

	sentencesNumber = sum([len(value) for value in d_abstracts.values()])

	print("Sentences Consistency check.")
	bar = Bar('Processing', max= sentencesNumber)

	countSentencesChange = 0
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
def tokenizationAndTagging(l_abstract):
	from nltk import word_tokenize
	from nltk import pos_tag
	from progress.bar import Bar

	print ("Abstract tokenization and tagging")
	bar = Bar('Processing', max=len(l_abstract))

	for line in l_abstract:
		#creates tokens of a string
		tokens = word_tokenize(line)
		#tags tokens with their PoS
		taggedTokens = pos_tag(tokens)
		bar.next()

	bar.finish()

	print("Abstracts tokenized and tagged.")

def main():
	moduleCheckAndInstallation(nltkInstall)
	l_abstract, d_abstractWithSentences = xmlAbstractExtraction("predator-prey[Title]")
	d_abstractWithSentencesModified = sentenceCheck(d_abstractWithSentences)
	tokenizationAndTagging(l_abstract)
	print(d_abstractWithSentencesModified)

main()