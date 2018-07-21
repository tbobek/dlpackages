from bs4 import BeautifulSoup
import requests
import sys
import re

dependent_packages = set()
debug_level = 1

def printdebug(*args): 
	'''
	produce debug output depending on levels
	@param 1 : first parameter is the debug level as integer. 0 = no debug, >0 more verbose, <0 not used
	@param 2..: argument for the print command
	@return nothing
	'''
	global debug_level
	if len(args)<2: 
		return
	level = 99
	try: 
		level = int(args[0])
	except ValueError: 
		return 
	if debug_level >= level: 
		print("DEBUG: ", args[1:])

def getPackageUrl(packagename, arch = 'amd64'): 
	'''
	retrieves the download url of a package. Right now, only amd64 architecture and bionic is tested
	@param packagename: the name of the package
	@return url to download the package
	'''
	url = 'https://packages.ubuntu.com/bionic/' + arch + '/' + str(packagename) + '/download'
	printdebug(1, 'getPackageUrl: url = ', url)
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	try: 
		result = soup.body.div.ul.li.a['href']
		return result
	except AttributeError: 
		printdebug(1, 'could not get package-url for %s' % packagename)
	except: 
		printdebug(1, 'no result for %s' % packagename)
    

def getDependentPackages(packagename): 
	'''
	returns the package names of the packages that the input package depends on. This is only the 
	first level of dependence. 
	@param packagename: the name of the package
	@return: list of strings naming the packages 
	'''
	url = 'https://packages.ubuntu.com/bionic/' + packagename
    
	printdebug(1, 'getDependentPackages: url=', url)
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	f = soup.find_all('dt')
	f2 = [a for a in f if str(a.text).find('de')>=0]
	#print(1, 'f2 = ', f2)
	packages = []
	for t in f2: 
		p = t.a.text
		#printdebug(1, 'p=', p)
		packages.append(p)
	return packages
    
def getRecursiveDepPackages(packagename, init=True):
	'''
	builds up a set of package names that include the packages the input package depends on. 
	The function @see getDependentPackages is as long called for the packages in the list, 
	as long there are new dependent packages appearing. 
	TODO: do not search in every round for the first entries, because they were already searched. 
	Only search in new entries
	'''
	all_packages = set([packagename])
	newFilesThere = True
	#start_index = 0
	#len_packages = 0
	while newFilesThere: 
		#search_packages = list(all_packages)[start_index:]
		# len_all_packages = len(all_packages)
		for p in list(all_packages): 
			packages = getDependentPackages(p)
			#len_packages = len_packages
			printdebug(1, 'getRecursiveDepPackages: packages = ', packages)
			newFilesThere = False
			for pp in packages: 
				if pp not in all_packages: 
					all_packages.add(pp)
					newFilesThere = True
	return list(all_packages)
    


    
def getUrlsOfPackages(packages): 
	urls = []
	for p in packages: 
		u = getPackageUrl(p)
		if u is not None: 
			urls.append(u)
	return urls

def outputWgetCommands(urls, filename = ''): 
	if filename != '': 
		f = open(filename, 'wt')
		f.write('#!/bin/bash -f \n')
		
	for u in urls: 
		if filename=='': 
			print('wget -c %s' % u)
		else: 
			f.write('wget -c %s\n' % u)
			
	if filename != '': 
		f.close()
			


def main():    
	url1 = getPackageUrl(sys.argv[1])
	# packages = getDependentPackages('apache2')
	packages = getRecursiveDepPackages('apache2')
	#printdebug(1, packages)
	urls = getUrlsOfPackages(packages)
	urls.append(url1)
	#printdebug(1, urls)
	outputWgetCommands(urls, sys.argv[1] + '_dl.sh')


if __name__ == '__main__':
	main()
