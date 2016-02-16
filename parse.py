import urllib2
import urllib
from bs4 import BeautifulSoup

def get_next_sol_site(sol):
	#8 tries.
	for i in range (1, 8):
		try:
			url = "http://mars.nasa.gov/mer/gallery/all/opportunity_p{}_text.html".format(sol)
			page = urllib2.urlopen(url)
			return page, sol
		except urllib2.HTTPError: # 404 -error
			print "Sol:{}, 404-Error".format(sol)
		sol +=1
	#No page found. Terminating.
	return False, False

def download_image(url):
	try:
		filename = "latest_image.jpg"
		urllib.urlretrieve (url, filename)
		return True
	except NameError:
		print "No such url to download from:{}".format(url)
		return False

def get_sol_from_url(url):
	sol = url[:-10]
	sol = sol[-4:]
	return sol

def find_image_urls_from_soup(soup, fast_seek):

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

def main():

	current_sol = 4287

	fast_seek = True

	while True:

		site, current_sol = get_next_sol_site( current_sol) #Find page with no 404 error

		if site == False: #No page found. Terminating.
			print "No valid sol address found. Terminating."
			break

		# Create soup instance.
		soup = 	BeautifulSoup(site.read())
			
		# List images found in site
		list_of_image_paths = find_image_urls_from_soup(soup, fast_seek)

		# Append root folder to image paths and print them.
		full_paths = []
		print "Paths found from sol: {}".format(current_sol)
		for a in list_of_image_paths:
			full_paths.append('http://mars.nasa.gov/mer/gallery/all/{}'.format(a['href']))
			print full_paths[-1]

		#Pick the first url found. It's the image we're looking for.
		try:
			first_url_found = full_paths[0]
		except IndexError: # No images found. Restart process.
			print "No paths found."
			current_sol+=1
			continue

		download_image(first_url_found)

		print "Download successfull"

		break

if __name__ == '__main__':
	main()

