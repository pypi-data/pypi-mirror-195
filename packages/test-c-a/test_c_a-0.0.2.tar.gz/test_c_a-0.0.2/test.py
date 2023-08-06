from time import strftime
def methodA():
	printf("tested method")
	string="testtest"
	filenmae="/tmp/test.txt"
	f= open(filenmae, "w")
	f.write("testé")
	f.close()
	