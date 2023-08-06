from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


def sigma_dq_check_fieldCompare_with_field(target_column,api_response,target_table,Execution_Type='',from_date=0,to_date=0,meta={}):
  column = target_column
  dq_rule = 'fieldCompare_with_field'
  source_table_with_column = target_table+'.'+target_column
  source_table = target_table

  if(api_response.__contains__("%>=%")):#Greater than eqaul to
    compare_table_with_column = api_response.split('%>=%')[-1]
    compare_table = '.'.join(compare_table_with_column.split('.')[:-1])
    operator = '>='
    if source_table == compare_table:
      StrSQl = "select "+source_table_with_column+",case when "+source_table_with_column+" "+operator+" "+compare_table_with_column+" then 'PASS' else 'FAIL' end as DQ_Status from "+source_table+"  "
    else:
      StrSQl = "select "+source_table_with_column+",case when "+source_table_with_column+" "+operator+" "+compare_table_with_column+" then 'PASS' else 'FAIL' end as DQ_Status from "+source_table+" left join "+compare_table+" on "+source_table_with_column+" = "+compare_table_with_column + " "

  elif(api_response.__contains__("%>%")):#Greater Than
    compare_table_with_column = api_response.split('%>%')[-1]
    compare_table = '.'.join(compare_table_with_column.split('.')[:-1])
    operator = '>'
    if source_table == compare_table:
      StrSQl = "select "+source_table_with_column+",case when "+source_table_with_column+" "+operator+" "+compare_table_with_column+" then 'PASS' else 'FAIL' end as DQ_Status from "+source_table+"  "
    else:
      StrSQl = "select "+source_table_with_column+",case when "+source_table_with_column+" "+operator+" "+compare_table_with_column+" then 'PASS' else 'FAIL' end as DQ_Status from "+source_table+" left join "+compare_table+" on "+source_table_with_column+" = "+compare_table_with_column + "  "

  elif(api_response.__contains__("%<=%")):#Less than equal to 
    compare_table_with_column = api_response.split('%<=%')[-1]
    compare_table = '.'.join(compare_table_with_column.split('.')[:-1])
    operator = '<='
    if source_table == compare_table:
      StrSQl = "select "+source_table_with_column+",case when "+source_table_with_column+" "+operator+" "+compare_table_with_column+" then 'PASS' else 'FAIL' end as DQ_Status from "+source_table+"  "
    else:
      StrSQl = "select "+source_table_with_column+",case when "+source_table_with_column+" "+operator+" "+compare_table_with_column+" then 'PASS' else 'FAIL' end as DQ_Status from "+source_table+" left join "+compare_table+" on "+source_table_with_column+" = "+compare_table_with_column+" "

  elif(api_response.__contains__("%<%")):#Less than
    compare_table_with_column = api_response.split('%<%')[-1]
    compare_table = '.'.join(compare_table_with_column.split('.')[:-1])
    operator = '<'
    if source_table == compare_table:
      StrSQl = "select "+source_table_with_column+",case when "+source_table_with_column+" "+operator+" "+compare_table_with_column+" then 'PASS' else 'FAIL' end as DQ_Status from "+source_table+"  "
    else:    
      StrSQl = "select "+source_table_with_column+",case when "+source_table_with_column+" "+operator+" "+compare_table_with_column+" then 'PASS' else 'FAIL' end as DQ_Status from "+source_table+" left join "+compare_table+" on "+source_table_with_column+" = "+compare_table_with_column + "  "

  elif(api_response.__contains__("%=%")):#equalTo
    compare_table_with_column = api_response.split('%=%')[-1]
    compare_table = '.'.join(compare_table_with_column.split('.')[:-1])
    operator = '='
    if source_table == compare_table:
      StrSQl = "select "+source_table_with_column+",case when "+source_table_with_column+" "+operator+" "+compare_table_with_column+" then 'PASS' else 'FAIL' end as DQ_Status from "+source_table+"  "
    else:
      StrSQl = "select "+source_table_with_column+",case when "+source_table_with_column+" "+operator+" "+compare_table_with_column+" then 'PASS' else 'FAIL' end as DQ_Status from "+source_table+" left join "+compare_table+" on "+source_table_with_column+" = "+compare_table_with_column + " "

  elif(api_response.__contains__("%<>%")):#NotEqualTo
    compare_table_with_column = api_response.split('%<>%')[-1]
    compare_table = '.'.join(compare_table_with_column.split('.')[:-1])
    operator = '!='
    if source_table == compare_table:
      StrSQl = "select "+source_table_with_column+",case when "+source_table_with_column+" "+operator+" "+compare_table_with_column+" then 'PASS' else 'FAIL' end as DQ_Status from "+source_table+"  "
    else:    
      StrSQl = "select "+source_table_with_column+",case when "+source_table_with_column+" "+operator+" "+compare_table_with_column+" then 'PASS' else 'FAIL' end as DQ_Status from "+source_table+" left join "+compare_table+" on "+source_table_with_column+" = "+compare_table_with_column + " "

  else:
    return " Error please check the input dqRule : fieldCompare_with_field"
 
  if Execution_Type == 'Incremental': 
    StrSQl += " where UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+") OR dqAction = 'NA'"
  
  elif Execution_Type == "date_range":
    from_timestamp = datetime.fromtimestamp(from_date)
    from_date_str = from_timestamp.strftime( "%Y-%m-%d")
    to_timestamp = datetime.fromtimestamp(to_date)
    to_date_str = to_timestamp.strftime( "%Y-%m-%d")
    between_condition = f' WHERE cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
    StrSQL += between_condition
  
  dq_apply_column_data = spark.sql(StrSQl)
  dq_report = sigma_dq_generate_dq_report(dq_apply_column_data,column,dq_rule)
  
  return dq_report
