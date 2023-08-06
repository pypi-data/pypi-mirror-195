from sigma_dq.helper.sigma_dq_helper_unique_elements_in_list import sigma_dq_helper_unique_elements_in_list

def sigma_dq_generate_dq_report_for_joins(dq_apply_column_data,column,dq_rule,total_count,pass_count,meta={}):
  dq_report = {}
  dq_report['column'] = column
  dq_report['rule'] = dq_rule
  #print("check total rows")
  print(f"column: {column}, RuleName: {dq_rule}")
  dq_report['total_rows_checked'] = total_count
  #print("check pass rows")
  total_DQ_Pass_count = pass_count
  #print("check failed rows")
  dq_report['total_rows_failed'] = total_count - pass_count
  
  if dq_report['total_rows_failed'] > 0:
    print("inside failed")
    dq_report['success'] = False
    dq_report['failed_percent'] = (dq_report['total_rows_failed']/dq_report['total_rows_checked'])*100
    raw_fail_list = dq_apply_column_data.select(dq_apply_column_data[column]
                                                              ).filter(dq_apply_column_data.DQ_Status == 'FAIL'
                                                                      ).rdd.flatMap(lambda x: x).collect()
    
    raw_fail_list_ = sigma_dq_helper_unique_elements_in_list(raw_fail_list)
    dq_report['failed_values'] = raw_fail_list_
  elif dq_report['total_rows_checked'] < 1:
    dq_report['success'] = False
    dq_report['successResult'] = 'Table is empty'
    dq_report['passed_percent'] = []
    dq_report['failed_values'] = []
    dq_report['failed_percent'] = []
    
  elif dq_report['total_rows_failed'] == dq_report['total_rows_checked']:
    dq_report['success'] = False
    dq_report['failed_values'] = []
    dq_report['failed_percent'] = []

  elif dq_report['total_rows_failed'] == dq_report['total_rows_checked']:
    #print("when all failed")
    dq_report['success'] = False
    dq_report['failed_percent'] = (dq_report['total_rows_failed']/dq_report['total_rows_checked'])*100
    dq_report['failed_values'] = []
  else:
    dq_report['success'] = True
    dq_report['passed_percent'] = (total_DQ_Pass_count/dq_report['total_rows_checked'])*100



  dq_report['meta'] = meta
  return dq_report