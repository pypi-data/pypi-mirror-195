import requests

def sigma_dq_helper_save_results_to_backend(url,save_result):
  #http://10.49.13.203:8000/
  url_ = 'v1/table_result/'
  url = url + url_
  x = requests.post(url, json = save_result)
  return x