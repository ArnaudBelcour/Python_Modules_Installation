from xml.dom import minidom

def xmlAbstractExtraction(fileName):
	print ("Parsing and extracting abstracts from corpus")
	xmldoc = minidom.parse(fileName)
	l_abstracts = xmldoc.getElementsByTagName('AbstractText')

	l_abstractsExtracted = []

	for abstractDOM in l_abstracts:
		l_abstractsExtracted.append(abstractDOM.firstChild.nodeValue.decode('utf-8'))
		
	print(l_abstractsExtracted)

xmlAbstractExtraction('abstract_ethology_animal.xml')
