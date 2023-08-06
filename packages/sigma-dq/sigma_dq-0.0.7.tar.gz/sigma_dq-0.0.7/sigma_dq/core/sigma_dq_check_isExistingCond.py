from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


# sigma_dq_check_isExistingCond('VENDOR_ACCOUNT_NO','jde_vendor.Global_Vendor_Number','purchase_order.SOURCE_NM="JDE"','edap_transform.purchase_order')
def sigma_dq_check_isExistingCond(target_column,api_response,api_response2,target_table,Execution_Type='',rule_id:int=0,from_date=0,to_date=0,meta={}):
  column = target_column
  dq_rule = 'isExistingCond'
  target_table_for_join = target_table.split('.')
  modified_target_column = target_table+"."+target_column
  modifiedapi_response =''
  modifiedapi_responseSplit = api_response.split('.')
  modifiedapi_leftJoinresponse2 = ''
  schema = target_table_for_join[0]

  # pass count
  if api_response.__contains__("%OR%"):
    table_list = api_response.split("%OR%")
    sub_query = ''
    for single_table in table_list:
      left_join_table = schema+'.'+single_table.split('.')[0]
      left_join_column = single_table.split('.')[1]
      if table_list.index(single_table) > 0:
        sub_query += ' OR '
      sub_query += f"{target_column} in (select distinct {left_join_column} from {left_join_table}) "

  elif api_response.__contains__("#AND#"):
    table_list = api_response.split("#AND#")
    sub_query = ''
    for single_table in table_list:
      left_join_table = schema+'.'+single_table.split('.')[0]
      left_join_column = single_table.split('.')[1]
      if table_list.index(single_table) > 0:
        sub_query += ' AND '
      sub_query += f"{target_column} in (select distinct {left_join_column} from {left_join_table}) "

  elif not api_response.__contains__("%OR%") and not api_response.__contains__("#AND#") and api_response != '':
    single_table = api_response
    left_join_table = schema+'.'+single_table.split('.')[0]
    left_join_column = single_table.split('.')[1]
    sub_query = f"{target_column} in (select distinct {left_join_column} from {left_join_table}) "

  else:
    return "Error please check the input dqRule:sigma_dq_check_isExisting"

  subquery2 = ''
  if api_response2 != '':
    subquery2 = api_response2.replace("#AND#", " AND ").replace("%OR%", " OR ")
    sub_query = f" ({sub_query}) AND ({subquery2}) "

  if Execution_Type == 'Incremental':
    sub_query = f" ({sub_query}) and UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from {target_table}) "
  elif Execution_Type == 'date_range':
    from_timestamp = datetime.fromtimestamp(from_date)
    from_date_str = from_timestamp.strftime( "%Y-%m-%d")
    to_timestamp = datetime.fromtimestamp(to_date)
    to_date_str = to_timestamp.strftime( "%Y-%m-%d")
    between_condition = f' cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
    sub_query = f" ({sub_query}) and {between_condition} "

  pass_count_query = f"select {modified_target_column} from {target_table} "
  if sub_query != '':
    pass_count_query += f"where {sub_query}"

  # Total count query
  total_count_query = f"select {modified_target_column} from {target_table} "
  total_count_subquery = ''

  if Execution_Type == 'Incremental':
    total_count_subquery += " UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+") "
  elif Execution_Type == 'date_range':
    from_timestamp = datetime.fromtimestamp(from_date)
    from_date_str = from_timestamp.strftime( "%Y-%m-%d")
    to_timestamp = datetime.fromtimestamp(to_date)
    to_date_str = to_timestamp.strftime( "%Y-%m-%d")
    between_condition = f' cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
    total_count_subquery += between_condition

  if total_count_subquery != '':
    total_count_query += " WHERE " + total_count_subquery

  # query for failed values
  StrSQl = ''
  if(api_response.__contains__("%OR%")):
    modifiedApiOR_Res = api_response.split('%OR%')
    modifiedORFinal=''
    modifiedORLeftjoin = ''
    left_join_singleTable = ''
    for singleTable in modifiedApiOR_Res:
      left_join_singleTable = singleTable.split('.') 
      index = modifiedApiOR_Res.index(singleTable)
      if(index >= 1):
        modifiedORFinal += " OR "+modified_target_column +" == " +singleTable #operator goes here
        modifiedORLeftjoin += " left join "+target_table_for_join[0]+"."+left_join_singleTable[0]+" on "+modified_target_column +" = " +singleTable 
      else:
        modifiedORFinal += modified_target_column +" == " +singleTable   #operator goes here
        modifiedORLeftjoin = " left join "+target_table_for_join[0]+"."+left_join_singleTable[0]+" on "+modified_target_column +" = " +singleTable       

    StrSQl = "select distinct "+modified_target_column+", CASE WHEN " +modifiedORFinal+ \
             "THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +target_table + " " + modifiedORLeftjoin

  elif(api_response.__contains__("#AND#")):
    modifiedApiAND_Res = api_response.split('#AND#')
    modifiedANDFinal=''
    modifiedANDLeftjoin = ''
    left_join_singleTable = ''
    for singleTable in modifiedApiAND_Res:
      left_join_singleTable = singleTable.split('.') 
      index = modifiedApiAND_Res.index(singleTable)
      if(index >= 1):
        modifiedANDFinal += " AND "+modified_target_column +" == " +singleTable #operator goes here
        modifiedANDLeftjoin += " left join "+target_table_for_join[0]+"."+left_join_singleTable[0]+" on "+modified_target_column +" = " +singleTable 
      else:
        modifiedANDFinal += modified_target_column +" == " +singleTable  #operator goes here
        modifiedANDLeftjoin = " left join "+target_table_for_join[0]+"."+left_join_singleTable[0]+" on "+modified_target_column +" = " +singleTable

    StrSQl = "select distinct "+modified_target_column+", CASE WHEN " +modifiedANDFinal+ \
          " THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +target_table + " " + modifiedANDLeftjoin

  else: # When my api_response    = 'JDE_VENDOR.global_vendor_number
    modifiedapi_response += modified_target_column +" == " +api_response   #operator goes here
    modifiedORLeftjoin = " left join "+target_table_for_join[0]+"."+modifiedapi_responseSplit[0]+" on "+modified_target_column +" = " +api_response       
    StrSQl = "select distinct "+modified_target_column+", CASE WHEN " +modifiedapi_response+ \
             " THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +target_table + modifiedORLeftjoin

  if(api_response2 != ''):
    lsmodifiedApliResponse = ''
    if(not api_response2.__contains__("#AND#") and api_response2.__contains__("%OR%")):
      lsmodifiedApliResponse = target_table_for_join[0]+"."+api_response2.replace("%OR%", " OR "+target_table_for_join[0]+".")
    elif(not api_response2.__contains__("%OR%") and api_response2.__contains__("#AND#")):
      lsmodifiedApliResponse =target_table_for_join[0]+"."+api_response2.replace("#AND#", " AND "+target_table_for_join[0]+".")
    elif(api_response2.__contains__("%OR%") and api_response2.__contains__("#AND#")):
      lsmodifiedApliResponse  = target_table_for_join[0]+"."+api_response2.replace("#AND#", "AND "+target_table_for_join[0]+".").replace("%OR%", " OR " + target_table_for_join[0]+".")
    else:
      lsmodifiedApliResponse = target_table_for_join[0]+"."+api_response2
    StrSQl += " WHERE " +lsmodifiedApliResponse

  else:
    print("Invalid Input")

  if Execution_Type == 'Incremental':
    StrSQl += " AND "+target_table+".UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+") "
  elif Execution_Type == 'date_range':
    from_timestamp = datetime.fromtimestamp(from_date)
    from_date_str = from_timestamp.strftime( "%Y-%m-%d")
    to_timestamp = datetime.fromtimestamp(to_date)
    to_date_str = to_timestamp.strftime( "%Y-%m-%d")
    between_condition = f' cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
    StrSQl += f" AND {between_condition}"

  dq_apply_column_data = spark.sql(StrSQl)
  total_count = spark.sql(total_count_query).count()
  pass_count = spark.sql(pass_count_query).count()
  dq_report = sigma_dq_generate_dq_report_for_joins(dq_apply_column_data,column,dq_rule,total_count,pass_count,meta={})
  dq_report["meta"]["rule_id"] = rule_id
  return dq_report
