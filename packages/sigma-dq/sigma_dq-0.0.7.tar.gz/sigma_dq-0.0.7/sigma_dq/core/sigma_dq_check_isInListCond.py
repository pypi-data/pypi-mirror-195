from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


# sigma_dq_check_isInListCond(target_column,list_of_values,api_response,target_table,meta={})
def sigma_dq_check_isInListCond(target_column,list_of_values,api_response,target_table,Execution_Type='',from_date=0,to_date=0,meta={}):
  column = target_column
  dq_rule = 'isInListWithCondition'
  dq_apply_column_data = None
  database_name = target_table.split('.')[0]
  
  # total count query
  total_rows_query = "select * from " + target_table + " "
  if Execution_Type == 'Incremental':
    total_rows_query += f" WHERE UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from {target_table})"
  elif Execution_Type == "date_range":
    from_timestamp = datetime.fromtimestamp(from_date)
    from_date_str = from_timestamp.strftime( "%Y-%m-%d")
    to_timestamp = datetime.fromtimestamp(to_date)
    to_date_str = to_timestamp.strftime( "%Y-%m-%d")
    between_condition = f' WHERE cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
    StrSQL += between_condition
  
  # pass count query
  pass_count_query = "select " + target_column + " from " + target_table + " where " + target_column + " in ('" +"','".join(list_of_values) + "') "
  if(api_response != ''):
    pass_count_query += " and " + api_response.replace("#AND#", " AND ").replace("%OR%", " OR ")
 
  if Execution_Type == 'Incremental':
    pass_count_query += f" and UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from {target_table})"  
  elif Execution_Type == "date_range":
    from_timestamp = datetime.fromtimestamp(from_date)
    from_date_str = from_timestamp.strftime( "%Y-%m-%d")
    to_timestamp = datetime.fromtimestamp(to_date)
    to_date_str = to_timestamp.strftime( "%Y-%m-%d")
    between_condition = f' and cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
    StrSQL += between_condition
  
  StrSQl = "Select " + target_column + ", case when " + target_column + " in ('" +"','".join(list_of_values) + "') then 'PASS' else 'FAIL' end as DQ_Status from " + target_table + " "
  
  if api_response != '':
    lsmodifiedApliResponse = ''
    if(not api_response.__contains__("#AND#") and api_response.__contains__("%OR%")):
      lsmodifiedApliResponse = database_name+"."+api_response.replace("%OR%", " OR "+database_name+".")
    elif(not api_response.__contains__("%OR%") and api_response.__contains__("#AND#")):
      lsmodifiedApliResponse =database_name+"."+api_response.replace("#AND#", " AND "+database_name+".")
    elif(api_response.__contains__("%OR%") and api_response.__contains__("#AND#")):
      lsmodifiedApliResponse  = database_name+"."+api_response.replace("#AND#", "AND "+database_name+".").replace("%OR%", " OR "+database_name+".")
    else:
      lsmodifiedApliResponse = database_name+"."+api_response

    StrSQl += " WHERE " +lsmodifiedApliResponse

    if Execution_Type == 'Incremental':
      StrSQl += " and UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+") "
    
    elif Execution_Type == "date_range":
      from_timestamp = datetime.fromtimestamp(from_date)
      from_date_str = from_timestamp.strftime( "%Y-%m-%d")
      to_timestamp = datetime.fromtimestamp(to_date)
      to_date_str = to_timestamp.strftime( "%Y-%m-%d")
      between_condition = f' and cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
      StrSQL += between_condition

  dq_apply_column_data = spark.sql(StrSQl)
  
  total_count = spark.sql(total_rows_query).count()
  pass_count = spark.sql(pass_count_query).count()
  dq_apply_column_data.show()
  print(pass_count_query)
  print(total_count, "-", pass_count)
  dq_report = sigma_dq_generate_dq_report_for_joins(dq_apply_column_data,column,dq_rule,total_count,pass_count,meta={})
  
  return dq_report
