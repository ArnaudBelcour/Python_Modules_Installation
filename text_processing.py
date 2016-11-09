#coding: utf-8
from moduleInstallation import ModuleInstallation
nltkInstall = ModuleInstallation("nltk", ['punkt', 'averaged_perceptron_tagger'], "3.2.1")

#Check and, if not present, instal nltk and needed packages
def moduleCheckAndInstallation(moduleInstallationInstance):

	if moduleInstallationInstance.moduleVersionUsed is None:
		choiceSentence =  "Do you want to check " + moduleInstallationInstance.module + " installation?"
	if moduleInstallationInstance.moduleVersionUsed is not None:
		choiceSentence =  "Do you want to check " +moduleInstallationInstance.module + " and his packages to see if they are up-to-date for our script : \n\t" + moduleInstallationInstance.module +" version " + moduleInstallationInstance.moduleVersionUsed

	if moduleInstallationInstance.packages is not None:
		for package in moduleInstallationInstance.packages :
			choiceSentence += "\n\tpackage " + package
		choiceSentence += "\nProceed(y/n)?"

	if moduleInstallationInstance.pythonVersion < (3,0,0):
		choice = raw_input(choiceSentence).lower()
	elif moduleInstallationInstance.pythonVersion > (3,0,0):
		choice = input(choiceSentence).lower()

	if choice  in moduleInstallationInstance.answersYN[0] :
		moduleInstallationInstance.checkModuleInstallation()
	if choice in moduleInstallationInstance.answersYN[1] :
				pass

#Extract abstract fom xml downloaded from Pubmed.
def xmlAbstractExtraction(fileName):
	from xml.dom import minidom
	from nltk import sent_tokenize

	#Check if progress is installed to show progression bar
	progressInstall = ModuleInstallation("progress")
	moduleCheckAndInstallation(progressInstall)

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
			l_abstractsExtracted.append(abstractDOM.firstChild.nodeValue.encode('utf-8'))

		if nltkInstall.pythonVersion > (3,0,0):
			l_abstractsExtracted.append(abstractDOM.firstChild.nodeValue)
			d_abstractsSentencesExtracted[l_abstracts.index(abstractDOM)] = sent_tokenize(abstractDOM.firstChild.nodeValue.strip())
			bar.next()

	bar.finish()

	print("Abstracts extracted!")
	return l_abstractsExtracted, d_abstractsSentencesExtracted

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
	tokenizationAndTagging(l_abstract)

main()