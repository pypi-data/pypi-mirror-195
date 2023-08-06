from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


# sigma_dq_check_isDate(target_column,api_response,target_table)
def sigma_dq_check_isDate(target_column,api_response,target_table,Execution_Type='',from_date=0,to_date=0,meta={}):
  column = target_column
  dq_rule = 'isDate'
  StrSQl  = ''

  if api_response == 'dd.mm.YYYY' or api_response == 'dd/mm/YYYY' or api_response == 'dd-mm-YYYY':
    StrSQl = "select "+target_column+", CASE WHEN " +target_column+" REGEXP '^([0]?[1-9]|[1|2][0-9]|[3][0|1])[.\/-]([0]?[1-9]|[1][0-2])[.\/-]([0-9]{4}|[0-9]{2})$' THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +target_table+ "  "

  elif api_response == 'mm.dd.YYYY' or api_response == 'mm/dd/YYYY' or api_response == 'mm-dd-YYYY':
    StrSQl = "select "+target_column+", CASE WHEN " +target_column+" REGEXP '^([0]?[1-9]|[1][0-2])[.\/-]([0]?[1-9]|[1|2][0-9]|[3][0|1])[.\/-]([0-9]{4}|[0-9]{2})$' THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +target_table+ " "

  elif api_response == 'YYYY.mm.dd' or api_response == 'YYYY/mm/dd' or api_response == 'YYYY-mm-dd':
    StrSQl = "select "+target_column+", CASE WHEN " +target_column+" REGEXP '^([0-9]{4}|[0-9]{2})[.\/-]([0]?[1-9]|[1][0-2])[.\/-]([0]?[1-9]|[1|2][0-9]|[3][0|1])$' THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +target_table+ "  "

  elif api_response == 'YYYYmmdd':
    StrSQl = "select "+target_column+", CASE WHEN " +target_column+" REGEXP '^([0-9]{4}|[0-9]{2})([0]?[1-9]|[1][0-2])([0]?[1-9]|[1|2][0-9]|[3][0|1])$' THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +target_table+ "  "

  elif api_response == 'ddmmYYYY':
    StrSQl = "select "+target_column+", CASE WHEN " +target_column+" REGEXP '^([0]?[1-9]|[1|2][0-9]|[3][0|1])([0]?[1-9]|[1][0-2])([0-9]{4}|[0-9]{2})$' THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +target_table+ "  "

  elif api_response == 'mmddYYYY':
    StrSQl = "select "+target_column+", CASE WHEN " +target_column+" REGEXP '^([0]?[1-9]|[1][0-2])([0]?[1-9]|[1|2][0-9]|[3][0|1])([0-9]{4}|[0-9]{2})$' THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +target_table+ "  "

  else:
    print('Incorrect/Unsupported Format Selected')

  if Execution_Type == 'Incremental': 
     StrSQl += " where UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+") "

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
