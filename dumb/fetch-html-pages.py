#!/usr/bin/python

import json
import requests
import sys
import os

if not os.path.exists('pages'):
  os.mkdir('pages')

data = json.loads(open(sys.argv[1]).read())
for key in data['products']:
  url = data['products'][key]['pip_url']
  print(url)

  outputFilename = f'pages/{key}.html'
  if os.path.exists(outputFilename) and os.path.getsize(outputFilename) > 100:
    print('already have %s, skipping' %s key)

  r = requests.get(url)
  f = open(outputFilename, 'w')
  f.write(r.text)
  f.close()

