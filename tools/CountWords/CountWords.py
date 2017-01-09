import argparse
import xml.etree.cElementTree as etree
from os import listdir
from os.path import isfile, join

def processMedlineFolder(medlineFolder,outFolder):
	"""Basic function that iterates through abstracts in a medline file, do a basic word count and save to a file

	Args:
		medlineFolder (folder): Medline XML folder containing abstracts
		outFolder (folder): Folder to save output data to
	Returns:
		Nothing

	"""
	abstractCount = 0

	# List of all files in the directory
	files = [f for f in listdir(medlineFolder) if isfile(join(medlineFolder, f)) and ".DS_Store" not in f]

	# Iterate over all files
	for f in files:
		# Iterate through the XML file and stop on each MedlineCitation
		for event, elem in etree.iterparse(medlineFolder+f, events=('start', 'end', 'start-ns', 'end-ns')):
			if (event=='end' and elem.tag=='MedlineCitation'):

				# Let's get the PMID and Abstract elements from the XML
				pmidElements = elem.findall('./PMID')
				abstractElements = elem.findall('./Article/Abstract/AbstractText')

				if len(pmidElements) != 1 or len(abstractElements) != 1:
					continue

				# Pull the values of the PMID and abstract elements
				pmid = pmidElements[0].text
				abstract = abstractElements[0].text

				# Do a very basic word count
				wordCount = len(abstract.split())

				# Prepare and save output to file
				line = "%s\t%d\n" % (pmid,wordCount)
				with open(outFolder+"countWords.txt", "a") as result:
					result.write(line)

				abstractCount += 1

	print "%d abstracts processed" % abstractCount

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Little toy example to "process" a Medline abstract file and gives naive word counts for each abstract')
	parser.add_argument('-i',required=True,help='Medline folder to process')
	parser.add_argument('-o',required=True,help='Output folder for word-counts')

	args = parser.parse_args()

	processMedlineFolder(args.i,args.o)
