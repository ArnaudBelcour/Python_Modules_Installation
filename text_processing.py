#coding: utf-8
from moduleInstallation import ModuleInstallation
moduleInstall = ModuleInstallation("nltk", ['punkt', 'averaged_perceptron_tagger'])

def nltkCheckAndInstallation():

	#Check and, if not present, instal nltk and needed packages
	choiceSentence =  "Do you want to check " + moduleInstall.module + " and his packages to see if they are up-to-date for our script : \n\t" + moduleInstall.module +" version " + moduleInstall.moduleVersionUsed

	for package in moduleInstall.packages :
		choiceSentence += "\n\tpackage " + package
	choiceSentence += "\nProceed(y/n)?"

	if moduleInstall.pythonVersion < (3,0,0):
		choice = raw_input(choiceSentence).lower()
	elif moduleInstall.pythonVersion > (3,0,0):
		choice = input(choiceSentence).lower()

	if choice  in moduleInstall.answersYN[0] :
		moduleInstall.checkModuleInstallation()
	if choice in moduleInstall.answersYN[1] :
				pass

def xmlAbstractExtraction(fileName):
	from xml.dom import minidom

	fileName = fileName + ".xml"
	print ("Parsing and extracting abstracts from corpus")
	xmldoc = minidom.parse(fileName)
	l_abstracts = xmldoc.getElementsByTagName('AbstractText')

	l_abstractsExtracted = []

	for abstractDOM in l_abstracts:
		if moduleInstall.pythonVersion > (3,0,0):
			l_abstractsExtracted.append(abstractDOM.firstChild.nodeValue)
		if moduleInstall.pythonVersion < (3,0,0):
			l_abstractsExtracted.append([i.encode('utf-8') for i in abstractDOM.firstChild.nodeValue])

	return l_abstractsExtracted

def tokenizationAndTagging(l_abstract):
	import nltk
	from nltk import word_tokenize
	from nltk import pos_tag

	for line in l_abstract:
		#creates tokens of a string
		tokens = word_tokenize(line)
		#tags tokens with their PoS
		taggedTokens = pos_tag(tokens)
		print(str(taggedTokens))

def main():
	nltkCheckAndInstallation()
	l_abstract = xmlAbstractExtraction("bioninformatic_gene_solanacea")
	tokenizationAndTagging(l_abstract)

main()