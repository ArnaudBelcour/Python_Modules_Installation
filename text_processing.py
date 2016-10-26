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

with open("abstract_ethology_animal.txt", "r") as corpus:
	for line in corpus:
		#creates tokens of a string
		tokens = word_tokenize(line.decode('utf-8'))

		#tags tokens with their PoS
		taggedTokens = pos_tag(tokens)
		print(str(taggedTokens))
