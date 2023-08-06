from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


## sigma_dq_check_isDecimalCond(target_column,api_response,target_table)

def sigma_dq_core_isDecimalCond(target_column,api_response,target_table,Execution_Type='',meta={}):
  column = target_column
  dq_rule = 'isDecimalWithCondition'
  
  target_table_for_join = target_table.split('.')
  modified_target_column = target_table+"."+target_column

  
  StrSQl = "select "+target_column+",case when "+target_column+" like '%.%' then 'PASS' else 'FAIL' end as DQ_Status from "+target_table
  target_table_for_join = target_table.split('.')

  if(api_response != ''):
      lsmodifiedApliResponse = ''
      if(not api_response.__contains__("#AND#") and api_response.__contains__("%OR%")):
          lsmodifiedApliResponse = target_table_for_join[0]+"."+api_response.replace("%OR%", " OR "+target_table_for_join[0]+".")
      elif(not api_response.__contains__("%OR%") and api_response.__contains__("#AND#")):
         lsmodifiedApliResponse =target_table_for_join[0]+"."+api_response.replace("#AND#", " AND "+target_table_for_join[0]+".")
      elif(api_response.__contains__("%OR%") and api_response.__contains__("#AND#")):
         lsmodifiedApliResponse  = target_table_for_join[0]+"."+api_response.replace("#AND#", "AND "+target_table_for_join[0]+".").replace("%OR%", " OR "+target_table_for_join[0]+".")
      else:
          lsmodifiedApliResponse = target_table_for_join[0]+"."+api_response
      
      StrSQl += " WHERE " +lsmodifiedApliResponse
      
      if(Execution_Type == 'Incremental'):
        StrSQl += " and UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+") OR dqAction = 'NA'"
  
  dq_apply_column_data = spark.sql(StrSQl)
  dq_report = sigma_dq_generate_dq_report(dq_apply_column_data,column,dq_rule)
  
  return dq_report