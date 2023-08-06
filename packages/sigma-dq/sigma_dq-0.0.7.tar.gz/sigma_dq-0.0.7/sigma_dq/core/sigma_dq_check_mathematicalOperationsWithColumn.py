from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


# mapping of sigma_dq_check_columnOperations (above method) in backend is under this name, 
# hence copying same method with different name
def sigma_dq_check_mathematicalOperationsWithColumn(target_column,target_column_operation,target_table,Execution_Type='',from_date=0,to_date=0,meta={}):
    
    # split based on comparator
    columns = []
    if target_column_operation.__contains__("=="):
        columns.extend(target_column_operation.split("=="))
    elif target_column_operation.__contains__(">"):
        columns.extend(target_column_operation.split(">"))
    elif target_column_operation.__contains__("<"):
        columns.extend(target_column_operation.split("<"))
    elif target_column_operation.__contains__(">="):
        columns.extend(target_column_operation.split(">="))
    elif target_column_operation.__contains__("<="):
        columns.extend(target_column_operation.split("<="))
    else:
      raise Exception("target_column_operation is invalid or incorrect") 
    columns = [columns[0]]
    
    dq_rule = 'mathematicalOperationsWithColumn'
    
    # split based on operators
    addition = []
    if target_column_operation.__contains__("#+#"):
        for c in columns:
            addition.extend(c.split("#+#"))
        columns = addition
    subtraction = []
    if target_column_operation.__contains__("#-#"):
        for a in columns:
            subtraction.extend(a.split("#-#"))
        columns = subtraction
    division = []
    if target_column_operation.__contains__("#/#"):
        for s in columns:
            division.extend(s.split("#/#"))
        columns = division
    multiply = []
    if target_column_operation.__contains__("#*#"):
        for d in columns:
            multiply.extend(d.split("#*#"))
        columns = multiply
    query_columns = ", ".join([x.strip() for x in columns])
    column_operation = target_column_operation.replace("#+#", "+").replace("#-#", "-"). \
        replace("#/#", "/").replace("#*#", "*")

    str_sql = f"select distinct {query_columns}, case when {column_operation} then 'PASS' else 'FAIL' end as DQ_Status" \
              f" from {target_table} "
    #return print(str_sql)
    if(Execution_Type == 'Incremental'):
      str_sql += ' WHERE "+UPDATE_RUN_TS+" = (select MAX("+UPDATE_RUN_TS+") from '+target_table+') '
    elif Execution_Type == "date_range":
      from_timestamp = datetime.fromtimestamp(from_date)
      from_date_str = from_timestamp.strftime( "%Y-%m-%d")
      to_timestamp = datetime.fromtimestamp(to_date)
      to_date_str = to_timestamp.strftime( "%Y-%m-%d")
      between_condition = f' WHERE cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
      str_sql += between_condition
    
    list_of_columns = []
    for c in columns:
      list_of_columns.append(c.strip())
    print(list_of_columns)
    
    ## additional handling required for list of columns as main argument
    failed_values_dict = {}
    dq_apply_column_data = spark.sql(str_sql)
    dq_report = {}
    dq_report['column'] = target_column
    dq_report['rule'] = dq_rule
    dq_report['total_rows_checked'] = dq_apply_column_data.count()
    total_DQ_Pass_count = dq_apply_column_data.filter(dq_apply_column_data.DQ_Status == 'PASS').count()
    dq_report['total_rows_failed'] = dq_apply_column_data.filter(dq_apply_column_data.DQ_Status == 'FAIL').count()
    if dq_report['total_rows_failed'] > 0:
      dq_report['success'] = False
      dq_report['failed_percent'] = (dq_report['total_rows_failed']/dq_report['total_rows_checked'])*100
      raw_fail_list = dq_apply_column_data.select([c for c in dq_apply_column_data.columns if c in list_of_columns]
                                                                 ).filter(dq_apply_column_data.DQ_Status == 'FAIL'
                                                                         ).rdd.flatMap(lambda x: x).collect()
      dq_apply_column_data_ = dq_apply_column_data.filter(dq_apply_column_data.DQ_Status == 'FAIL').toPandas()
      failed_values_dict = dq_apply_column_data_.to_dict(orient='list')
      for i in dq_apply_column_data.columns:
        if i not in list_of_columns:
          del failed_values_dict[i]

      raw_fail_list_ = failed_values_dict     
      #raw_fail_list_ = sigma_dq_helper_unique_elements_in_list(raw_fail_list)
      dq_report['failed_values'] = raw_fail_list_
    elif dq_report['total_rows_failed'] == dq_report['total_rows_checked']:
      dq_report['success'] = False
      dq_report['failed_percent'] = (dq_report['total_rows_failed']/dq_report['total_rows_checked'])*100
      dq_report['failed_values'] = []
    else:
      dq_report['success'] = True
      dq_report['passed_percent'] = (total_DQ_Pass_count/dq_report['total_rows_checked'])*100

    dq_report['meta'] = meta
    dq_report_parent ={}
    dq_report_parent[0]= dq_report

    dq_message = sigma_dq_helper_generate_dq_message(dq_report_parent)
    dq_action = sigma_dq_helper_generate_dq_action(dq_message)

    dq_apply_column_data.createOrReplaceTempView('results_out')

    COALESCE_target = ' '
    COALESCE_results_out = ' '

    for cols in list_of_columns:
        COALESCE_target += f"COALESCE({target_table}.{cols}, '') ,"
    COALESCE_target = COALESCE_target[:-1]
    
    for cols in list_of_columns:
        COALESCE_results_out += f"COALESCE(results_out.{cols}, '') ,"

    COALESCE_results_out = COALESCE_results_out[:-1]
    StrSQl_update = f"merge into  {target_table} using results_out on CONCAT({COALESCE_target}) = CONCAT({COALESCE_results_out}) WHEN MATCHED and results_out.DQ_Status = 'FAIL' THEN UPDATE SET dqAction = '{dq_action}', dqMessage = Concat(dqMessage, '( ,{','.join(dq_message[0]['column_name'])} )for rule {dq_message[0]['rule']} failed , ')"

    try:
      spark.sql(StrSQl_update)
      status_ = "Writing DQ_Action and DQ_Message into " + target_table +" completed "
    except Exception as e:
      status_ = "Writing DQ_Action and DQ_Message into " + target_table +" failed\n" + str(e) 
    print(status_)
    
    return dq_report
  