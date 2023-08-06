from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


def sigma_dq_check_isExisting(target_column,api_response,target_table,Execution_Type='',from_date=0,to_date=0,meta = {}):
  and_logic = '#and#'
  or_logic = '%OR%'
  userinput = '>0'
  column = target_column
  dq_rule = 'isExisting'

  target_table_for_join = target_table.split('.')
  schema = target_table_for_join[0]
  modified_target_column = target_table+"."+target_column 

  # get correct pass count
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

  if Execution_Type == 'Incremental':
    if api_response == '':
      sub_query += " UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+") "
    else:
      sub_query = "( " + sub_query + " ) and UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+") "
  
  elif Execution_Type == "date_range":
    from_timestamp = datetime.fromtimestamp(from_date)
    from_date_str = from_timestamp.strftime( "%Y-%m-%d")
    to_timestamp = datetime.fromtimestamp(to_date)
    to_date_str = to_timestamp.strftime( "%Y-%m-%d")
    between_condition = f' cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
    if api_response == '':
      sub_query += f" {between_condition} "
    else:
      sub_query = "( " + sub_query + " ) and " + between_condition
  
  pass_count_query = f"select {modified_target_column} from {target_table} "
  if sub_query != '':
    pass_count_query += f"where {sub_query}"
  
  total_count_query = f"select {modified_target_column} from {target_table} "
  if Execution_Type == 'Incremental':
    total_count_query += " WHERE UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+") "
  elif Execution_Type == "date_range":
    from_timestamp = datetime.fromtimestamp(from_date)
    from_date_str = from_timestamp.strftime( "%Y-%m-%d")
    to_timestamp = datetime.fromtimestamp(to_date)
    to_date_str = to_timestamp.strftime( "%Y-%m-%d")
    between_condition = f' WHERE cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
    total_count_query += f" {between_condition} "  
  
  # get failed values                
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
        if(modifiedORLeftjoin.__contains__(left_join_singleTable[0])):
          modifiedORLeftjoin += " AND "+modified_target_column +" = " +singleTable
        else:
          modifiedORLeftjoin += " left join "+target_table_for_join[0]+"."+left_join_singleTable[0]+" on "+modified_target_column +" = " +singleTable 
      else:
        modifiedORFinal += modified_target_column +" == " +singleTable   #operator goes here
        modifiedORLeftjoin = " left join "+target_table_for_join[0]+"."+left_join_singleTable[0]+" on "+modified_target_column +" = " +singleTable
      StrSQl = "select distinct "+modified_target_column+", CASE WHEN " +modifiedORFinal+" \
          THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +target_table+" " +modifiedORLeftjoin

  elif(api_response.__contains__("#and#")):
    modifiedApiAND_Res = api_response.split('#and#')
    modifiedANDFinal=''
    modifiedANDLeftjoin = ''
    left_join_singleTable = ''
    for singleTable in modifiedApiAND_Res:
      left_join_singleTable = singleTable.split('.') 
      index = modifiedApiAND_Res.index(singleTable)
      if(index >= 1):
        modifiedANDFinal += " AND "+modified_target_column +" == " +singleTable #operator goes here
        if(modifiedANDLeftjoin.__contains__(left_join_singleTable[0])):
          modifiedANDLeftjoin += " AND "+modified_target_column +" = " +singleTable
        else:   
          modifiedANDLeftjoin += " left join "+target_table_for_join[0]+"."+left_join_singleTable[0]+" on "+modified_target_column +" = " +singleTable
      else:
        modifiedANDFinal += modified_target_column +" == " +singleTable  #operator goes here
        modifiedANDLeftjoin = " left join "+target_table_for_join[0]+"."+left_join_singleTable[0]+" on "+modified_target_column +" = " +singleTable
      StrSQl = "select distinct "+modified_target_column+", CASE WHEN " +modifiedANDFinal+" \
      THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +target_table+" " +modifiedANDLeftjoin 

  elif (not api_response.__contains__("%OR%") and not api_response.__contains__("#AND#") and api_response != ''):
    modifiedAPIResponsefirnotcontain = api_response
    modifiedORFinal = ''
    left_join_singleTable = modifiedAPIResponsefirnotcontain.split('.')
    modifiedORFinal += modified_target_column + " == " + api_response  # operator goes here
    modifiedORLeftjoin = " left join " + target_table_for_join[0] + "." + left_join_singleTable[0] + \
                         " on " + modified_target_column + " = " + api_response
    StrSQl = "select distinct " + modified_target_column + ", CASE WHEN " + modifiedORFinal + " \
        THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " + target_table + " " + modifiedORLeftjoin

  else:
    return "Error please check the input dqRule:sigma_dq_check_isExisting"

  if Execution_Type == 'Incremental':
    StrSQl += " WHERE "+target_table+".UPDATE_RUN_TS = (select MAX("+target_table+".UPDATE_RUN_TS) from "+target_table+") "
  elif Execution_Type == 'date_range':
    from_timestamp = datetime.fromtimestamp(from_date)
    from_date_str = from_timestamp.strftime( "%Y-%m-%d")
    to_timestamp = datetime.fromtimestamp(to_date)
    to_date_str = to_timestamp.strftime( "%Y-%m-%d")
    between_condition = f' WHERE cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
    StrSQl += between_condition

  dq_apply_column_data = spark.sql(StrSQl)
  total_count = spark.sql(total_count_query).count()
  pass_count = spark.sql(pass_count_query).count()
  dq_report = sigma_dq_generate_dq_report_for_joins(dq_apply_column_data,column,dq_rule,total_count,pass_count,meta={})
  return dq_report
