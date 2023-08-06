from sigma_dq.core.common import spark

def sigma_dq_helper_reset_dqAction_dqMessage(target_table, execution_type=''):
    StrSQl_update = f"update {target_table} set dqAction = 'NA' , dqMessage = ''"
    if execution_type == 'Incremental':
      StrSQl_update += " where "+target_table+".UPDATE_RUN_TS = (select MAX("+target_table+".UPDATE_RUN_TS) from "+target_table+") "
      
    try:
        spark.sql(StrSQl_update)
        status_ =  f"All dqAction and dqMessage is reset to default values for table {target_table}"
    except Exception as e:
          status_ = f"Reset of DQ_Action and DQ_Message for {target_table}  failed with error : {str(e)} " 
    
    return status_