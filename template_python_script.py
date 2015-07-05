import sys, getopt

'''
This is a template script focused on reading arguments
from the command line and caling functions.
'''

def main(argv):
	inputfile = ""
	outputfile = ""
	try:
		opts, args = getopt.getopt(argv,"i:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'Error: run file in correct format'	
		print 'template_python_script.py -i <inputfile> -o <outputfile>'
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		else :
			print 'test.py -i <inputfile> -o <outputfile>'
			sys.exit()

	print 'Input file is "', inputfile
	print 'Output file is "', outputfile


if __name__ == '__main__':
	main(sys.argv[1:])
	print "Finished"
	