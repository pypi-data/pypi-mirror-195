from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


#target_table = 'edap_transform.Purchase_Requisition'
#api_response = '%>%0'
#api_response2 = 'COMPONENT_QUANTITY >=0 #AND# COMPONENT_QUANTITY < 0 %OR% COMPONENT_QUANTITY < 0  '
#sigma_dq_check_fieldCompare_with_value_condition('POSOSWO_LINE_NO',api_response,api_response2,target_table,meta={'dq_master_id' : 3})
def sigma_dq_check_fieldCompareWithCondition(target_column,api_response,api_response2,target_table,Execution_Type='',meta={}):
    column = target_column
    dq_rule = 'fieldCompareWithCondition'
    source_table_with_column = target_table+'.'+target_column
    source_table = target_table
    operator = ''.join(api_response.split('%')[1:-1])
    value = ''.join(api_response.split('%')[::-3])

    try:
        value = float(value)
    except:
        return("Insert valid number")
    else:
        value = float(value)

    if(operator == '>'):#Greater than 0
        operator = '> ' + str(value)
        StrSQl = "select "+source_table_with_column+", CASE WHEN " +source_table_with_column+" "+operator+" THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +source_table+"  "

    elif(operator == '>'):#Greater than equal to 0
        operator = '> '+ str(value)
        StrSQl = "select "+source_table_with_column+", CASE WHEN " +source_table_with_column+" "+operator+" THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +source_table+"  "

    elif(operator == '<'):#Less than 0
        operator = '< '+ str(value)
        StrSQl = "select "+source_table_with_column+", CASE WHEN " +source_table_with_column+" "+operator+" THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +source_table+"  "

    elif(operator == '<='):#Less than equal to 0
        operator = '<= '+ str(value)
        StrSQl = "select "+source_table_with_column+", CASE WHEN " +source_table_with_column+" "+operator+" THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +source_table+"  "

    elif(operator == '<>'):#Not equal to 0
        operator = '<> '+ str(value)
        StrSQl = "select "+source_table_with_column+", CASE WHEN " +source_table_with_column+" "+operator+" THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +source_table+"  "

    elif(operator == '='):#Not equal to 0
        operator = '= '+ str(value)
        StrSQl = "select "+source_table_with_column+", CASE WHEN " +source_table_with_column+" "+operator+" THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +source_table+"  "

    else:
        return "Error please check the input"
    
    api_response_conditon = api_response2.replace('#AND#', 'AND' ).replace('%OR%','OR') 
    StrSQl += " WHERE " +api_response_conditon

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
    dq_report = sigma_dq_generate_dq_report(dq_apply_column_data,column,dq_rule)

    return dq_report
