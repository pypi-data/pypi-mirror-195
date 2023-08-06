from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


#GrossMargin should be equal to (TotalNetrevenue3rdparties - TotalCOGS3rdparties)
#target_table = 'rgm_src.fusion_pnl'
#target_column = 'GrossMargin'
#api_response = 'TotalNetrevenue3rdparties - TotalCOGS3rdparties'
#sigma_dq_check_mathematicalCalculations(target_column,api_response,target_table,'Incremental',meta={'dq_master_id' : 3})
def sigma_dq_check_fieldCompareWithMathematicalOperations(target_column,api_response,target_table,Execution_Type = '',meta={}): 
    column = target_column
    dq_rule = 'fieldCompareWithMathematicalOperations'  
    StrSQl = f"select {target_column}, case when {target_column} = {api_response} then 'PASS' else 'FAIL' from {target_table} "
    
    if Execution_Type == 'Incremental':
        StrSQl += " Where UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+") "

    elif Execution_Type == "date_range":
        from_timestamp = datetime.fromtimestamp(from_date)
        from_date_str = from_timestamp.strftime( "%Y-%m-%d")
        to_timestamp = datetime.fromtimestamp(to_date)
        to_date_str = to_timestamp.strftime( "%Y-%m-%d")
        between_condition = f' WHERE cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
        StrSQL = f"select {target_column}, case when {target_column} = {api_response} then 'PASS' else 'FAIL' from {target_table}" + between_condition
      
    dq_apply_column_data = spark.sql(StrSQl)
    dq_report = sigma_dq_generate_dq_report(dq_apply_column_data,column,dq_rule)

    return dq_report
    