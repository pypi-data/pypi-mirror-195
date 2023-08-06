import requests

def sigma_dq_helper_get_tables_by_layer(url,target_layer,tables=[],datasets=[],categories=[],primary_domains=[],sec_domains=[],sub_domains=[]):
  #http://10.49.13.203:8000/
  url_ = 'v1/table/get_tables_by_layer'
  url = url + url_
  payload = {}
  payload['layer'] = target_layer
  payload['tables'] = tables
  payload['datasets'] = datasets
  payload['categories'] = categories
  payload['primary_domains'] = primary_domains
  payload['secondary_domains'] = sec_domains
  payload['sub_domains'] = sub_domains
  
  x = requests.post(url, json = payload)
  return x.json()