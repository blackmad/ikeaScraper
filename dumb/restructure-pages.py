#!/usr/bin/python

import os
import sys
import json

from bs4 import BeautifulSoup

def tagAndAttrFilter(tagName, attrName, attrValue):
	return lambda tag: tag and \
		    tag.name and \
		    tag.has_attr(attrName) and \
		    tag.name == tagName and \
		    tag.attrs[attrName] == attrValue


def meta_description(tag):
    return tag and \
	    tag.name and \
	    tag.has_attr('property') and \
	    tag.name == 'meta' and \
	    tag.attrs['property'] == 'og:description'

products = []

originalData = json.loads(open('data.json').read())['products']


def process_file(file):
	print(file)
	soup = BeautifulSoup(open(file).read(), 'html5lib')

	def images():
		return [div.find('img').attrs['src'] for div in soup.find_all("div", {"class": 'range-carousel__image'})]

	def tagValue(tagName, attrName, attrValue, contentAttrName):
		return soup.find_all(tagAndAttrFilter(tagName, attrName, attrValue))[0].attrs[contentAttrName]

	pid = soup.find('div', {'itemtype': "http://schema.org/Product"}).attrs['data-product-id']

	product = {
		'description': tagValue('meta', 'property', 'og:description', 'content'),
		'price': tagValue('meta', 'itemprop', 'price', 'content'),
		# <meta name="keywords" content="VIPPÄRT, Chair pad" /
		'keywords': tagValue('meta', 'name', 'keywords', 'content').split(', '),
		'title': tagValue('meta', 'property', 'og:title', 'content').replace(' - IKEA', ''),
		'images': images(),
		'id': pid
	}

	product.update(originalData.get(pid.lower(), {}))

	products.append(product)



files = os.listdir(sys.argv[1])
for f in files:
	process_file(sys.argv[1] + '/' + f)

f = open(f'combined-data.json', 'w')
f.write(json.dumps({'products': products}))
f.close()

f = open(f'combined-data.js', 'w')
f.write('const ikeaProducts = ' + json.dumps(products) + ';')
f.close()