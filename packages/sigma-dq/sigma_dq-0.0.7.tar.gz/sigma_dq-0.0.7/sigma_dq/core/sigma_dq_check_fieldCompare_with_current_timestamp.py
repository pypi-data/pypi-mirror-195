from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


def sigma_dq_check_fieldCompare_with_current_timestamp(target_column,api_response,target_table,Execution_Type='',from_date=0,to_date=0,meta={}):
    column = target_column
    dq_rule = 'fieldCompare_with_current_timestamp'
    source_table_with_column = target_table+'.'+target_column
    source_table = target_table
       
    if(api_response == '< current_timestamp'):#Less than Current date
        operator = ' < '
        StrSQl = "select "+source_table_with_column+", CASE WHEN to_timestamp(" +source_table_with_column+", 'yyyy-MM-dd HH:mm:ss.SSS') "+operator+" current_timestamp() THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +source_table+"  "

    elif(api_response == '> current_timestamp'):#Greater than Current date
        operator = ' > '
        StrSQl = "select "+source_table_with_column+", CASE WHEN to_timestamp(" +source_table_with_column+", 'yyyy-MM-dd HH:mm:ss.SSS') "+operator+" current_timestamp() THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +source_table+"  "
    
    elif(api_response == '<= current_timestamp'):#Greater than Current date
        operator = ' <= '
        StrSQl = "select "+source_table_with_column+", CASE WHEN to_timestamp(" +source_table_with_column+", 'yyyy-MM-dd HH:mm:ss.SSS') "+operator+" current_timestamp() THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +source_table+"  "
    
    elif(api_response == '>= current_timestamp'):#Greater than Current date
        operator = ' >= '
        StrSQl = "select "+source_table_with_column+", CASE WHEN to_timestamp(" +source_table_with_column+", 'yyyy-MM-dd HH:mm:ss.SSS') "+operator+" current_timestamp() THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +source_table+"  "
    
    elif(api_response == '= current_timestamp'):#Greater than Current date
        operator = ' = '
        StrSQl = "select "+source_table_with_column+", CASE WHEN to_timestamp(" +source_table_with_column+", 'yyyy-MM-dd HH:mm:ss.SSS') "+operator+" current_timestamp() THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +source_table+"  "
    
    elif(api_response == '<> current_timestamp'):#Greater than Current date
        operator = ' != '
        StrSQl = "select "+source_table_with_column+", CASE WHEN to_timestamp(" +source_table_with_column+", 'yyyy-MM-dd HH:mm:ss.SSS') "+operator+" current_timestamp() THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +source_table+"  "
    
    else:
        return "Error please check the input dqRule:sigma_dq_check_fieldCompare_with_current_timestamp"

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
  