import requests

def sigma_dq_helper_get_validation_suite(url,target_table_):
  
  validation_suite_path = 'v1/table/validation_suite'
  validation_suite_url = url+validation_suite_path
  table_payload = {'name': target_table_}
  api_call = requests.post(validation_suite_url, json = table_payload)
  api_response_vs = api_call.json()
  return api_response_vs