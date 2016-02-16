import urllib2
import urllib
from bs4 import BeautifulSoup

def get_last_sol_site(sol, url_var):
	site = None
	while True:
		site, sol = get_next_sol_site(sol, url_var)
		if site == False:
			return last_usable_site, last_usable_sol
		else:
			last_usable_site, last_usable_sol = site, sol
			print "Found sol:{} searching for next one.".format(sol)
			sol +=1
	print "Fatal error in getting last sol"

def get_next_sol_site(sol, url_var):
	#30 tries.
	for i in range (1, 30):
		try:
			url = "http://mars.nasa.gov/mer/gallery/all/opportunity_{}{}_text.html".format(url_var, sol)
			page = urllib2.urlopen(url)
			return page, sol
		except urllib2.HTTPError: # 404 -error
			print "Sol:{}, 404-Error".format(sol)
		sol +=1
	#No page found. Terminating.
	return False, False

def download_image(url, url_var):
	try:
		filename = "latest_image{}.jpg".format(url_var)
		urllib.urlretrieve (url, filename)
		return True
	except NameError:
		print "No such url to download from:{}".format(url)
		return False

def get_sol_from_url(url):
	sol = url[:-10]
	sol = sol[-4:]
	return sol

def find_image_urls_from_soup(soup, fast_seek, alternative_search):

	if alternative_search == False:

		if fast_seek == True:	
			soup = soup.body.table.tr.td.table.tr.td.next_sibling
			soup = soup.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
			soup = soup.table.next_sibling.next_sibling.next_sibling.next_sibling
	
		list_of_tables = soup.find_all('tr')

		list_of_image_paths = []

		for table in list_of_tables:
			try:
				if table['class']: # Only the images have this: <tr class="galleryImageNew">
					list_of_image_paths.append(table.a)
			except KeyError:
				pass
	
		return list_of_image_paths

	elif alternative_search == True:
		returns = soup.body.table.tr.td.table.tr.td.next_sibling.next_sibling
		returns = returns.next_sibling.next_sibling.next_sibling.next_sibling
		returns = returns.table.next_sibling.next_sibling.next_sibling.next_sibling
		returns = returns.find_all('a')[1:] # Get all links without the first
		return [str(x)[9:-37] for x in returns] # Tidyup the links


def do_the_magic(url_var, starting_sol):

	current_sol = starting_sol


	fast_seek = True
	alternative_search = True

	site = None
	while True:

		site, current_sol = get_last_sol_site(current_sol, url_var)
		#site, current_sol = get_next_sol_site( current_sol) #Find page with no 404 error

		if site == False: #No page found. Falling back to last sol found.
			alternative_search = True
			site = last_usable_site
			sol = last_usable_sol

		# Create soup instance.
		soup = 	BeautifulSoup(site.read())
			
		# List images found in site
		list_of_image_paths = find_image_urls_from_soup(soup, fast_seek, alternative_search)

		if list_of_image_paths == False:
			print "No valid sol address found. Terminating."
			break

		# Append root folder to image paths and print them.
		full_paths = []
		print "Paths found from sol: {}".format(current_sol)
		for a in list_of_image_paths: # A is either str, or dictionary
			try:
				full_paths.append('http://mars.nasa.gov/mer/gallery/all/{}'.format(a['href']))
			except TypeError:
				full_paths.append('http://mars.nasa.gov/mer/gallery/all/{}'.format(a))
			print full_paths[-1]

		#Pick the first url found. It's the image we're looking for.
		try:
			first_url_found = full_paths[0]
		except IndexError: # No images found. Restart process.
			print "No paths found."
			current_sol+=1
			continue

		download_image(first_url_found, url_var)

		print "Download successfull"

		return current_sol

def main():

	try:
		with open('parser.conf') as f:
			content = [int(x.strip('\n')) for x in f.readlines()]
	except IOError:
		content = [4250 for x in range (1,6)]

		

	m = do_the_magic('m', content[0])
	p = do_the_magic('p', content[1])
	f = do_the_magic('f', content[2])
	r = do_the_magic('r', content[3])
	n = do_the_magic('n', content[4])

	with open('parser.conf', 'w') as ff:
		ff.write('{}\n'.format(m))
		ff.write('{}\n'.format(p))
		ff.write('{}\n'.format(f))
		ff.write('{}\n'.format(r))
		ff.write('{}\n'.format(n))

	print "Config updated"

	

if __name__ == '__main__':
	main()

