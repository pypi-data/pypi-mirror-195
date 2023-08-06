import requests

def sigma_dq_helper_get_pipeline_table_id(url,target_table):
  
  pipeline_table_id_path = 'v1/table/get_table_id'
  pipeline_table_id_url = url + pipeline_table_id_path
  table_components = target_table.split(".")
  payload = {}
  payload['primary_data_domain'] = table_components[0]
  payload['secondary_data_domain'] = table_components[1]
  payload['sub_data_domain'] = table_components[2]
  payload['dataset_name'] = table_components[3]
  payload['catalog_name'] = table_components[4]
  payload['schema_name'] = table_components[5]
  payload['table_name'] = table_components[6]

  api_call_ = requests.post(pipeline_table_id_url, json=payload)
  pipeline_table_id = api_call_.json()['id']
  return pipeline_table_id