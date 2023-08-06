from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


def sigma_dq_check_isDuplicate(target_column, list_of_columns,target_table,Execution_Type = '',from_date=0,to_date=0,meta={}):
  dq_rule = 'isDuplicate'
  columns = ','.join(list_of_columns)
  column = columns
  
  if Execution_Type == 'Incremental':
    StrSQl = f"select {columns}, count(1), case when count(1) > 1 then 'FAIL' else 'PASS' end as DQ_Status from " \
             f"{target_table} where UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+ ") " \
             f"group by {columns} ORDER BY {len(list_of_columns) + 1} DESC "
  
  elif Execution_Type == "date_range":
    from_timestamp = datetime.fromtimestamp(from_date)
    from_date_str = from_timestamp.strftime( "%Y-%m-%d")
    to_timestamp = datetime.fromtimestamp(to_date)
    to_date_str = to_timestamp.strftime( "%Y-%m-%d")
    between_condition = f' WHERE cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}" group by {columns} ORDER BY {len(list_of_columns) + 1} DESC '
    StrSQL = f"select {columns}, count(1), case when count(1) > 1 then 'FAIL' else 'PASS' end as DQ_Status from " \
            f"{target_table}" + between_condition
      
  else:
    StrSQl = f"select {columns}, count(1), case when count(1) > 1 then 'FAIL' else 'PASS' end as DQ_Status from " \
             f"{target_table} group by {columns} ORDER BY {len(list_of_columns) + 1} DESC "
  
  dq_apply_column_data = spark.sql(StrSQl)
  
  ## additional handling required for list of columns as main argument
  failed_values_dict = {}
  dq_report = {}
  dq_report['column'] = target_column
  dq_report['rule'] = dq_rule
  dq_report['total_rows_checked'] = dq_apply_column_data.count()
  total_DQ_Pass_count = dq_apply_column_data.filter(dq_apply_column_data.DQ_Status == 'PASS').count()
  dq_report['total_rows_failed'] = dq_apply_column_data.filter(dq_apply_column_data.DQ_Status == 'FAIL').count()
  if dq_report['total_rows_failed'] > 0:
    dq_report['success'] = False
    dq_report['failed_percent'] = (dq_report['total_rows_failed']/dq_report['total_rows_checked'])*100
    raw_fail_list = dq_apply_column_data.select([c for c in dq_apply_column_data.columns if c in list_of_columns]
                                                              ).filter(dq_apply_column_data.DQ_Status == 'FAIL'
                                                                      ).rdd.flatMap(lambda x: x).collect()
    dq_apply_column_data_ = dq_apply_column_data.filter(dq_apply_column_data.DQ_Status == 'FAIL').toPandas()
    failed_values_dict = dq_apply_column_data_.to_dict(orient='list')
    for i in dq_apply_column_data.columns:
      if i not in list_of_columns:
        del failed_values_dict[i]
        
    raw_fail_list_ = failed_values_dict     
    #raw_fail_list_ = sigma_dq_helper_unique_elements_in_list(raw_fail_list)
    dq_report['failed_values'] = raw_fail_list_
  elif dq_report['total_rows_failed'] == dq_report['total_rows_checked']:
    dq_report['success'] = False
    try:
      dq_report['failed_percent'] = (dq_report['total_rows_failed']/dq_report['total_rows_checked'])*100
    except:
      dq_report['failed_percent'] = 0
    dq_report['failed_values'] = []
  else:
    dq_report['success'] = True
    try:
      dq_report['passed_percent'] = (total_DQ_Pass_count/dq_report['total_rows_checked'])*100
    except:
      dq_report['passed_percent'] = 0

  dq_report['meta'] = meta
  dq_report_parent ={}
  dq_report_parent[0]= dq_report
  
  dq_message = sigma_dq_helper_generate_dq_message(dq_report_parent)
  dq_action = sigma_dq_helper_generate_dq_action(dq_message)
  
  dq_apply_column_data.createOrReplaceTempView('results_out') 
  COALESCE_target = ' '
  COALESCE_results_out = ' '

  for cols in list_of_columns:
    COALESCE_target += f"COALESCE({target_table}.{cols}, '') ,"
  COALESCE_target = COALESCE_target[:-1]

  for cols in list_of_columns:
    COALESCE_results_out += f"COALESCE(results_out.{cols}, '') ,"
  COALESCE_results_out = COALESCE_results_out[:-1]
  
  StrSQl_update = f"merge into  {target_table} using results_out on CONCAT({COALESCE_target}) = CONCAT({COALESCE_results_out}) WHEN MATCHED and results_out.DQ_Status = 'FAIL' THEN UPDATE SET dqAction = '{dq_action}', dqMessage = Concat(dqMessage, ' ,{dq_message[0]['column_name']} for rule {dq_message[0]['rule']} failed , ')"
  
  try:
    spark.sql(StrSQl_update)
    status_ = "Writing DQ_Action and DQ_Message into " + target_table +" completed "
  except Exception as e:
    status_ = "Writing DQ_Action and DQ_Message into " + target_table +" failed\n" + str(e) 

  print(status_)
  return dq_report
