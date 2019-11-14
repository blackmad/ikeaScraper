#!/usr/bin/python
import requests
import json

products = {}
queries = ['ikea', 'kitchen', 'home', 'chair', 'office', 'desk', 'table', 'kids', 'children', 'christmas', 'food', 'couch', 'closet', 'work', 'play']

def run_query(q):
  print(f'running query {q}, had {len(products)} products')
  for i in range(0, 200):
    url = f'https://sik.search.blue.cdtapps.com/us/en/search-result-page/more-products?sessionId=969dc501-18be-4f58-b328-ed8a254a4aa4&q={q}&start={i*48}&end={(i+1)*48}&sort=RELEVANCE'
    #print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    if 'moreProducts' in data and 'productWindow' in data['moreProducts'] and len(data['moreProducts']['productWindow']) > 0:
      print(f'got products on page {i}')
      productResults = data['moreProducts']['productWindow']
      for product in productResults:
        products[product['id']] = product
    else:
      break
  print(f'done running query {q}, had {len(products)} products')

for query in queries:
  run_query(query)


f = open(f'data.json', 'w')
f.write(json.dumps({'products': products}))
f.close()

