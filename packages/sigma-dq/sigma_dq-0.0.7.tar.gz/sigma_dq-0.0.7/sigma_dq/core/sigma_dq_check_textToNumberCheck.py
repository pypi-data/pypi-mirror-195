from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


# sigma_dq_check_textToNumberCheck(target_column,target_table)
def sigma_dq_check_textToNumberCheck(target_column,target_table,Execution_Type='',from_date=0,to_date=0,meta={}):
    column = target_column
    dq_rule = 'textToNumberCheck'

    if Execution_Type == 'Incremental': 
        StrSQl = f"select {target_column}, case when cast(replace(replace({target_column}, ',', ''), ' ', '') as INT) > 0" \
                 f" and {target_column}%1 == 0 then 'PASS' else 'FAIL' end as DQ_Status from {target_table}" \
                 f" where UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+") "
    
    elif Execution_Type == "date_range":
        from_timestamp = datetime.fromtimestamp(from_date)
        from_date_str = from_timestamp.strftime( "%Y-%m-%d")
        to_timestamp = datetime.fromtimestamp(to_date)
        to_date_str = to_timestamp.strftime( "%Y-%m-%d")
        between_condition = f' WHERE cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
        StrSQL = f"select {target_column}, case when cast(replace(replace({target_column}, ',', ''), ' ', ') as INT) > 0" \
                 f" and {target_column}%1 == 0 then 'PASS' else 'FAIL' end as DQ_Status from {target_table}" + between_condition
    
    else:
        StrSQl = f"select {target_column}, case when cast(replace(replace({target_column}, ',', ''), ' ', '') as INT) > 0" \
                 f" and {target_column}%1 == 0 then 'PASS' else 'FAIL' end as DQ_Status from {target_table} " 
      
    dq_apply_column_data = spark.sql(StrSQl)
    dq_report = sigma_dq_generate_dq_report(dq_apply_column_data,column,dq_rule)
  
    return dq_report
