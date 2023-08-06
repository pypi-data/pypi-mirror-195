from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


# test_sigma_dq_check_startsWith('MATERIAL_NO',"dls",'edap_transform.Production_order')
def sigma_dq_check_startsWith(target_column,string_check,target_table,Execution_Type='',from_date=0,to_date=0,meta = {}):
  column = target_column
  dq_rule = 'startsWith'

  if Execution_Type == 'Incremental':
    StrSQl = "select "+target_column+",case when "+target_column+" like '"+string_check+"%' then 'PASS' else 'FAIL' end as DQ_Status from  "+target_table+" where UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+") "
  
  elif Execution_Type == "date_range":
    from_timestamp = datetime.fromtimestamp(from_date)
    from_date_str = from_timestamp.strftime( "%Y-%m-%d")
    to_timestamp = datetime.fromtimestamp(to_date)
    to_date_str = to_timestamp.strftime( "%Y-%m-%d")
    between_condition = f' WHERE cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
    StrSQL = "select "+target_column+",case when "+target_column+" like '"+string_check+"%' then 'PASS' else 'FAIL' end as DQ_Status from  " +target_table + between_condition
      
  else:
    StrSQl = "select "+target_column+",case when "+target_column+" like '"+string_check+"%' then 'PASS' else 'FAIL' end as DQ_Status from  "+target_table+" "

  dq_apply_column_data = spark.sql(StrSQl)
  dq_report = sigma_dq_generate_dq_report(dq_apply_column_data,column,dq_rule)

  return dq_report
