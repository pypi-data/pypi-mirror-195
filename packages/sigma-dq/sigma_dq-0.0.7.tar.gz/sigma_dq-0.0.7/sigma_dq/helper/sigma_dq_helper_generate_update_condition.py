def sigma_dq_helper_generate_update_condition(results_final):
  listt = []
  i = 0
  for a in results_final:
    cond = {}
    if results_final[a]['success'] == False:
      
      cond['column'] = results_final[a]['column']
      cond['rule'] =  results_final[a]['rule']
      cond['failed_values'] = results_final[a]['failed_values']
      
      listt.append(cond)
      i = i + 1
  return listt