import urllib2
import urllib
from bs4 import BeautifulSoup

def main():
	url = "http://mars.nasa.gov/mer/gallery/all/opportunity_p4286_text.html"
	data = urllib2.urlopen(url).read()
	soup = BeautifulSoup(data)

	sol = url[:-10]
	sol = sol[-4:]
	print sol

	trs = soup.find_all('tr')

	list_of_image_paths = []

	for tr in trs:
		try:
			if tr['class']:
				list_of_image_paths.append(tr.a)
		except KeyError:
			pass

	full_paths = []

	# Print all the paths
	print "Paths found from sol: {}".format(sol)
	for a in list_of_image_paths:
		full_paths.append('http://mars.nasa.gov/mer/gallery/all/{}'.format(a['href']))
		print full_paths[-1]

	# Pick the first url.
	try:
		urllib.urlretrieve (full_paths[0], "latest_image.jpg")
	except NameError:
		print "Url not found."

if __name__ == '__main__':
	main()