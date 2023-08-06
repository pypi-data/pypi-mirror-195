from sigma_dq.helper.sigma_dq_helper_generate_run_id import sigma_dq_helper_generate_run_id
from sigma_dq.helper.sigma_dq_helper_generate_update_condition import sigma_dq_helper_generate_update_condition
from sigma_dq.core.common import spark


def sigma_dq_helper_update_dqaction_dqmessage(results_final,target_table_cleaned,Execution_type = ''):
  max_batch_limit = 5000
  #target_table = 'edap_transform.purchase_order'
  #target_table_cleaned = 'edap_transform.purchase_order'
  run_id = str(sigma_dq_helper_generate_run_id())
  w_cond = sigma_dq_helper_generate_update_condition(results_final)
  w_cond_count = (len(w_cond))
  use_batch_update_flag = 0
  for a in w_cond:
      if len(a['failed_values']) > max_batch_limit:
          use_batch_update_flag += 1

  if use_batch_update_flag == 0:
      #print(x)
      #print()
      for a in w_cond:
          if a['rule'] in ["mathematicalOperationsWithColumn","isDuplicate"]:
            continue
          stmnt_list = []
          dqaction_cond = ' '
          dqmessage_cond = ' '
          print("applying rule: ", a['column'], a['rule'])
#           for a in w_cond :
          if w_cond_count > 1:

              dqaction_cond += a['column']+ " in (\'"+ "','".join(str(x) for x in a['failed_values']) + '\') OR '
              dqmessage_cond += 'When '+a['column']+" in (\'"+ "','".join(str(x) for x in a['failed_values'])+ "\') then concat(dqMessage,'" + a['column']+ " for rule " + a['rule'] + " Failed, ') "

              if None in a['failed_values']:
                  dqaction_cond += a['column']+ " is null OR "
                  dqmessage_cond += 'When '+a['column']+" is null then concat(dqMessage,'" + a['column']+ " for rule " + a['rule'] + " Failed, ') "

              dqaction_cond__ = dqaction_cond[:-3]
             
              x = "update " + target_table_cleaned + " set dqAction = case When " +  dqaction_cond__ + " then 'FAIL' When dqAction = 'FAIL' then 'FAIL' else 'PASS' end,      dqMessage = case " + dqmessage_cond + " else dqMessage end " #AG
              if(Execution_type == 'Incremental'):
                 x += " WHERE UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table_cleaned+") OR dqAction = 'NA'" 

          else:
              if None in a['failed_values']:
                  dqaction_cond += a['column']+ " is null "

              else:
                  dqaction_cond += a['column']+ " in (\'"+ "','".join(str(x) for x in a['failed_values']) + '\') '
                  #dqaction_cond += a['column']+ ' in ("'+ '","'.join(x for x in x__[0]['failed_values']) + '") '
                  #dqaction_cond += dqaction_cond  

              if None in a['failed_values']:
                  dqmessage_cond += 'When '+a['column']+" is null then concat(dqMessage,'" + a['column']+ " for rule " + a['rule'] + " Failed, ') "
              else:
                  dqmessage_cond += 'When '+a['column']+" in (\'"+ "','".join(str(x) for x in a['failed_values'])+ "\') then concat(dqMessage,'" + a['column']+ " for rule " + a['rule'] + " Failed, ') "
                  #dqmessage_cond += 'When '+a['column']+' in ("'+ '","'.join(str(x) for x in a['failed_values'])+ '") then concat(dqMessage,'  + a['column']+ " for rule " + a['rule'] + " Failed, ') "
                  #dqmessage_cond_ += dqmessage_cond

              x = "update " + target_table_cleaned + " set dqAction = case When " +  dqaction_cond + " then 'FAIL' When dqAction = 'FAIL' then 'FAIL' else 'PASS' end, dqMessage = case " + dqmessage_cond + " else dqMessage end " #Changes by AG , PC(061222)
              if(Execution_type == 'Incremental'):
                 x += " WHERE UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table_cleaned+") OR dqAction = 'NA'" 


          try:
            spark.sql(x)
            status_ = "Writing DQ_Action and DQ_Message into " + target_table_cleaned +" completed "
          except Exception as e:
                status_ = "Writing DQ_Action and DQ_Message into " + target_table_cleaned +" failed\n" + str(e)        
  else:
      dqaction_cond = ' '
      dqmessage_cond = ' '
      for a in w_cond:
          if a['rule'] in ["mathematicalOperationsWithColumn","isDuplicate"]:
            continue
          failed_values_len= len(a['failed_values'])
          print("applying rule: ", a['column'], a['rule'])
          i = 0
          n = 5000

          if failed_values_len > n:
              while i < failed_values_len:

                  dqaction_cond = a['column']+ " in (\'"+ "','".join(str(x) for x in a['failed_values'][i:i+n]) + '\') '
                  dqmessage_cond = 'When '+a['column']+" in (\'"+ "','".join(str(x) for x in a['failed_values'][i:i+n])+ "\') then concat(dqMessage,'" + a['column']+ " for rule " + a['rule'] + " Failed, ') "
                #dqaction_cond += a['column']+ ' in ("'+ '","'.join(x for x in x__[0]['failed_values']) + '") '
                  #dqaction_cond += dqaction_cond  
                  if None in a['failed_values']:
                      dqaction_cond += "OR " + a['column']+ " is null"
                      dqmessage_cond += 'When '+a['column']+" is null then concat(dqMessage,'" + a['column']+ " for rule " + a['rule'] + " Failed, ') "

                  x = "update " + target_table_cleaned + " set dqAction = case When " +  dqaction_cond + " then 'FAIL' When dqAction = 'FAIL' then 'FAIL' else 'PASS' end, dqMessage = case " + dqmessage_cond + " else dqMessage end "
                  if(Execution_type == 'Incremental'):
                    x += " WHERE UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table_cleaned+") OR dqAction = 'NA'"

                  try:
                    spark.sql(x)
                    status_ = "Writing DQ_Action and DQ_Message into " + target_table_cleaned +" completed "
                  except Exception as e:
                    status_ = "Writing DQ_Action and DQ_Message into " + target_table_cleaned +" failed\n" + str(e)
                  #print(a['column'])
                  #print(i)
                  #print(dqaction_cond)
                  #print(dqmessage_cond)
                  #print()
                  i = i + n
          else:

              dqaction_cond = a['column']+ " in (\'"+ "','".join(str(x) for x in a['failed_values']) + '\') '
              dqmessage_cond = 'When '+a['column']+" in (\'"+ "','".join(str(x) for x in a['failed_values'])+ "\') then concat(dqMessage,'" + a['column']+ " for rule " + a['rule'] + " Failed, ') "

              if None in a['failed_values']:
                  dqaction_cond += "OR " + a['column']+ " is null "
                  dqmessage_cond += 'When '+a['column']+" is null then concat(dqMessage,'" + a['column']+ " for rule " + a['rule'] + " Failed, ') "



              x = "update " + target_table_cleaned + " set dqAction = case When " +  dqaction_cond + " then 'FAIL' When dqAction = 'FAIL' then 'FAIL' else 'PASS' end, dqMessage = case " + dqmessage_cond + " else dqMessage end "
              if(Execution_type == 'Incremental'):
                 x += " WHERE UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table_cleaned+") OR dqAction = 'NA'"

              try:
                spark.sql(x)
                status_ = "Writing DQ_Action and DQ_Message into " + target_table_cleaned +" completed "
              except Exception as e:
                status_ = "Writing DQ_Action and DQ_Message into " + target_table_cleaned +" failed\n" + str(e)

              i = i + n
             