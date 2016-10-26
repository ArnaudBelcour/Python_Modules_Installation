#coding: utf-8
from moduleInstallation import ModuleInstallation
import sys

moduleInstall = ModuleInstallation("nltk", ['punkt', 'averaged_perceptron_tagger'])

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

import nltk
from nltk import word_tokenize
from nltk import pos_tag
from xml.dom import minidom

def xmlAbstractExtraction(fileName):
	print ("Parsing and extracting abstracts from corpus")
	xmldoc = minidom.parse(fileName)
	l_abstracts = xmldoc.getElementsByTagName('AbstractText')

	l_abstractsExtracted = []

	for abstractDOM in l_abstracts:
		l_abstractsExtracted.append(abstractDOM.firstChild.nodeValue.decode('utf-8'))

	return l_abstractsExtracted

def tokenizationAndTagging(l_abstract)
	for line in l_abstract:
		#creates tokens of a string
		tokens = word_tokenize(line.decode('utf-8'))

		#tags tokens with their PoS
		taggedTokens = pos_tag(tokens)
		print(str(taggedTokens))
