import json, requests

class Search:

  def __init__(self, index):
    self.index = index

  def search(self, params = {}):
    basic_search = self.__import_dict('data/requests/basic_search.json')
    if params['query']:
      basic_search['query'] = params['query']
    
    basic_search['size'] = params['size']
    basic_search['from'] = params['from']

    return self.__get(basic_search)

  def __get(self, dict):
    query = self.__format(dict)
    print('/GET')
    print(query)

    results = requests.get(self.index + '/_search', headers={'content-type': 'application/json'}, data=query)
    
    print('/Response: ' + str(results.status_code))
    
    results = json.loads(results.content)
    print(self.__format(results))

    return results

  def __format(self, data):
    return json.dumps(data, indent=2, sort_keys=True)

  def __import_dict(self, filename):
    file_data = open(filename).read()
    return json.loads(file_data)

  def __import_json(self, filename):
    json_data = self.__import_dict(filename)
    return json.dumps(json_data, indent=2, sort_keys=True) # Make it pretty!