from sigma_dq.helper.sigma_dq_helper_generate_run_id import sigma_dq_helper_generate_run_id
from sigma_dq.helper.sigma_dq_helper_generate_update_condition import sigma_dq_helper_generate_update_condition
from sigma_dq.core.common import spark

def sigma_dq_helper_update_dqaction_dqmessage_old(results_final,target_table_cleaned,dq_action,dq_message):
  run_id = str(sigma_dq_helper_generate_run_id())
  w_cond = sigma_dq_helper_generate_update_condition(results_final)
  w_cond_count = (len(w_cond))
  stmnt_list = []
  dqaction_cond = ' '
  dqmessage_cond = ' '
  for a in w_cond :
    if w_cond_count > 1:
      
      if None in a['failed_values']:
        dqaction_cond += a['column']+ " is null OR "
      else:
        dqaction_cond += a['column']+ " in (\'"+ "','".join(str(x) for x in a['failed_values']) + '\') OR '
      #dqaction_cond += dqaction_cond  
      dqaction_cond__ = dqaction_cond[:-3]
      
      if None in a['failed_values']:
        dqmessage_cond += 'When '+a['column']+" is null then concat(dqMessage,', " + a['column']+ " for rule " + a['rule'] + " Failed, ') "
      else:
        dqmessage_cond += 'When '+a['column']+" in (\'"+ "','".join(str(x) for x in a['failed_values'])+ "\') then concat(dqMessage,', " + a['column']+ " for rule " + a['rule'] + " Failed, ') "
      #dqmessage_cond_ += dqmessage_cond

      x = "update " + target_table_cleaned + " set dqAction = case When " +  dqaction_cond__ + " then 'FAIL' else 'PASS' end, dqMessage = case " + dqmessage_cond + " else '' end "

    else:
      if None in a['failed_values']:
        dqaction_cond += a['column']+ " is null "
      else:
        dqaction_cond += a['column']+ " in (\'"+ "','".join(str(x) for x in a['failed_values']) + '\') '
        #dqaction_cond += a['column']+ ' in ("'+ '","'.join(x for x in x__[0]['failed_values']) + '") '
      #dqaction_cond += dqaction_cond  
      
      if None in a['failed_values']:
        dqmessage_cond += 'When '+a['column']+" is null then concat(dqMessage,', " + a['column']+ " for rule " + a['rule'] + " Failed, ') "
      else:
        dqmessage_cond += 'When '+a['column']+" in (\'"+ "','".join(str(x) for x in a['failed_values'])+ "\') then concat(dqMessage,', " + a['column']+ " for rule " + a['rule'] + " Failed, ') "
        #dqmessage_cond += 'When '+a['column']+' in ("'+ '","'.join(str(x) for x in a['failed_values'])+ '") then concat(dqMessage,'  + a['column']+ " for rule " + a['rule'] + " Failed, ') "
      #dqmessage_cond_ += dqmessage_cond

      x = "update " + target_table_cleaned + " set dqAction = case When " +  dqaction_cond + " then 'FAIL' else 'PASS' end, dqMessage = case " + dqmessage_cond + " else 'NA' end "


  
  try:
    spark.sql(x)
    status_ = "Writing DQ_Action and DQ_Message into " + target_table_cleaned +" completed "
  except Exception as e:
    status_ = "Writing DQ_Action and DQ_Message into " + target_table_cleaned +" failed\n" + str(e)
    
  return(status_)
  