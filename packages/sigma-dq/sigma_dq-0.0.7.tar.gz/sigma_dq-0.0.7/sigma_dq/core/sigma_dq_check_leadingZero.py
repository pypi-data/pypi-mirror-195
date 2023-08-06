from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


# sigma_dq_check_leadingZero('MATERIAL_NO',2,target_table)
def sigma_dq_check_leadingZero(target_column,minimum_zeros, target_table,Execution_Type='',from_date=0,to_date=0,meta = {}):
  leading_zeros = ''
  column = target_column
  dq_rule = 'leadingZero'

  for i in range(minimum_zeros):
      leading_zeros += '0'
  leading_zeros += '%'

  if(Execution_Type == 'Incremental'):
    StrSQl = f"select {column}, case when cast({target_column} as int) is not null " \
            f"and {target_column} like '{leading_zeros}' then 'PASS' else 'FAIL' end as DQ_Status " + \
            f"from {target_table} " + " where UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+") "
  
  elif Execution_Type == "date_range":
    from_timestamp = datetime.fromtimestamp(from_date)
    from_date_str = from_timestamp.strftime( "%Y-%m-%d")
    to_timestamp = datetime.fromtimestamp(to_date)
    to_date_str = to_timestamp.strftime( "%Y-%m-%d")
    between_condition = f' WHERE cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'

    StrSQL = f"select {column}, case when cast({target_column} as int) is not null " \
              f"and {target_column} like '{leading_zeros}' then 'PASS' else 'FAIL' end as DQ_Status " + \
              f"from {target_table} " + between_condition
    
  else:
    StrSQl = f"select {column}, case when cast({target_column} as int) is not null " \
            f"and {target_column} like '{leading_zeros}' then 'PASS' else 'FAIL' end as DQ_Status " + \
            f"from {target_table} "

  dq_apply_column_data = spark.sql(StrSQl)
  dq_report = sigma_dq_generate_dq_report(dq_apply_column_data,column,dq_rule)

  return dq_report
