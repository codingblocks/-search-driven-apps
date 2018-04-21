from flask import Flask, render_template, request
from logger import Logger
from importer import Importer
import json, requests

app = Flask(__name__)

@app.route('/')
def index():
  query = import_json('data/basic_search.json', get_query_from_params())
  Logger.info(query)
  search_results = requests.get('http://elasticsearch:9200/games/_search', headers={'content-type': 'application/json'}, data=query)
  results = json.loads(search_results.content) # deserialize the content so we can access things via python
  paging = {
    'showPaging': True,
    'currentPage': 1,
    'startPage': 1,
    'endPage': 10,
    'totalPages': 100
  }
  return render_template("index.j2", hits=results['hits'], aggregations=results['aggregations'], paging=paging)

@app.route('/reset')
def reset():
  i = Importer()
  games_converted = i.convert_json_to_elastic('data/games.json','data/games-formatted.import')
  game_conversion_success = games_converted > 0
  responses = {
    'delete': requests.delete('http://elasticsearch:9200/games', headers={'content-type': 'application/json'}),
    'put': requests.put('http://elasticsearch:9200/games', headers={'content-type': 'application/json'}, data=import_json('data/mapping_config.json')),
    'post': requests.post('http://elasticsearch:9200/games/doc/_bulk', headers={'content-type': 'application/x-ndjson'}, data=open('data/games-formatted.txt').read())
  }
  return render_template("reset.j2", game_conversion_success=game_conversion_success, responses=responses)

def import_json(filename, query={}):
  file_data = open(filename).read()
  json_data = json.loads(file_data)
  if query:
    json_data['query'] = query
  return json.dumps(json_data, indent=2, sort_keys=True) # Make it pretty!

def get_query_from_params():
  wants_to_play = request.args.getlist('wants_to_play')
  mechanics = request.args.getlist('mechanics')
  Logger.info(wants_to_play)
  Logger.info(mechanics)
  data = {}
  
  if wants_to_play or mechanics:
    data['bool'] = { 'filter': [] }

  if wants_to_play:
    for p in wants_to_play:
      data['bool']['filter'].append({ 'term': { 'wantsToPlay' : p } })

  if mechanics:
    for m in mechanics:
      data['bool']['filter'].append({ 'term': { 'mechanics' : m } })

  return data

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')