from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


# sigma_dq_check_isExistingCondAdvanced('VENDOR_ACCOUNT_NO','purchase_order.MATERIAL_NO = bill_of_material.SOURCE_ITEM_CODE',
#    'entity_classification.supply_Entity_Class = "RB Factory"','entity_classification.supply_Entity','edap_transform.purchase_order')
def sigma_dq_check_isExistingCondAdvanced(target_column,api_response,api_response2,left_join_tables,target_table,Execution_Type='',meta={}):
    api_responseSecond = ""
    dq_rule = 'isExistingCondAdvanced'
    column = target_column
    target_table_for_join = target_table.split('.')
    modified_target_column = target_table + "." + target_column
    modifiedapi_response = ''
    modifiedapi_responseSplit = api_response.split('.')
    andClause = ""
    secondLeftJoin = ""
    schema = target_table.split(".")[0]
    
    # calculate pass count
    pass_count_query = ''   
    table_list = api_response.split("=")
    subquery_tables = []
    for table in table_list:
      subquery_tables.append(table.strip())
    for x in subquery_tables:
      if x.split(".")[0] in target_table:
        from_table = x
      else:
        to_table = x
    subquery = f" {from_table} in (select distinct {to_table} from {schema}.{to_table.split('.')[0]} ) "
    if api_response2.split(".")[0] in to_table:
      subquery = subquery.replace(")", f" where {api_response2.replace('%OR%', ' OR ').replace('#AND#', ' AND ')} ")
    
    if left_join_tables != '':
      subquery += f" and {target_column} in (select distinct {left_join_tables} from {schema}.{left_join_tables.split('.')[0]}  "
      if api_response2.split(".")[0] in left_join_tables:
        subquery += f" where {api_response2.replace('%OR%', ' OR ').replace('#AND#', ' AND ')} "
      subquery += " ) "
      
    if api_response2 != '':
      if api_response2.split(".")[0] in target_table:
        subquery += f" and {api_response2.replace('%OR%', ' OR ').replace('#AND#', ' AND ')} "
    
    if Execution_Type == 'Incremental':
      subquery = f" ({subquery}) and {target_table}.UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from {target_table}) "
    elif Execution_Type == 'date_range':
      from_timestamp = datetime.fromtimestamp(from_date)
      from_date_str = from_timestamp.strftime( "%Y-%m-%d")
      to_timestamp = datetime.fromtimestamp(to_date)
      to_date_str = to_timestamp.strftime( "%Y-%m-%d")
      between_condition = f' cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
      subquery = f" ({subquery}) and {between_condition} "
      
    pass_count_query = f" select {target_column} from {target_table}"
    if subquery != '':
      pass_count_query += f" where {subquery} "
      
    # calculate total count
    total_subquery = ''
    if Execution_Type == 'Incremental':
      total_subquery = f" {target_table}.UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from {target_table}) "
    elif Execution_Type == 'date_range':
      from_timestamp = datetime.fromtimestamp(from_date)
      from_date_str = from_timestamp.strftime( "%Y-%m-%d")
      to_timestamp = datetime.fromtimestamp(to_date)
      to_date_str = to_timestamp.strftime( "%Y-%m-%d")
      between_condition = f' cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
      total_subquery = between_condition
    
    total_count_query = f"select {target_column} from {target_table}"
    if total_subquery != '':
      total_count_query += f" where {total_subquery}"

    # calculate failed values
    StrSQl = ''
    targetTableAPI = target_table_for_join[1]+"."+target_column

    modifiedapi_responseSplit
    modifiedORLeftjoin = ''
    if (api_response.__contains__("=")):
        modifiedApiORR_Res = left_join_tables.split('#AND#')
        modifiedApiResForCaseWhen = api_response.replace("=", "==")
        modifiedAPIResponseForEqualTo = api_response.split('=')
        stripmodifiedAPIResponseForEqualTo = []         # stripping
        tableNameInApi_response = []

        for index in modifiedAPIResponseForEqualTo:
            stripmodifiedAPIResponseForEqualTo.append(index.strip())
            tableNameInApi_response.append(index.split(".")[0])

        modifiedAPIResponseForEqualToTemp = modifiedAPIResponseForEqualTo[1].strip()
        index = modifiedAPIResponseForEqualToTemp.index('.')
        modifiedAPIResponseForEqualToTemp = modifiedAPIResponseForEqualToTemp[:index]

        for singleTable in modifiedApiORR_Res:
            index = modifiedApiORR_Res.index(singleTable)
            api_responseSecond = targetTableAPI + " = "+left_join_tables
            api_response_added = api_response + " and " + api_responseSecond
            temp1 = modifiedApiORR_Res[0].split('.')


        if(left_join_tables.split(".")[0] in tableNameInApi_response):
            modifiedORLeftjoin = " left join " + target_table_for_join[0] + "." + temp1[0] + " on " + api_responseSecond
            andClause = " and "+api_response

        else:
            modifiedORLeftjoin = " left join " + target_table_for_join[0] + "." + modifiedAPIResponseForEqualToTemp + " on " + api_response
            secondLeftJoin = " left join "+ target_table_for_join[0] + "."+left_join_tables.split(".")[0]+ " on " + api_responseSecond+" "

        StrSQl = "select distinct " + modified_target_column + ", CASE WHEN " + api_response_added + " \
        THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " + target_table + " " + modifiedORLeftjoin + secondLeftJoin + andClause

    else:  # When my api_response    = 'JDE_VENDOR.global_vendor_number
        temp1 = left_join_tables.split('.')
        modifiedapi_response += modified_target_column + " == " + api_response  # operator goes here
        modifiedORLeftjoin = " left join " + target_table_for_join[0] + "." + modifiedapi_responseSplit[0] + " on " + modified_target_column + " = " + api_response
        modifiedORLeftjoin += " left join " + target_table_for_join[0] + "." + temp1[0]
        StrSQl = "select distinct " + modified_target_column + ", CASE WHEN " + modifiedapi_response + " \
                THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " + target_table + " " + modifiedORLeftjoin

    if (api_response2 != ''):
        lsmodifiedApliResponse = ''
        if (not api_response2.__contains__("#AND#") and api_response2.__contains__("%OR%")):
            lsmodifiedApliResponse = target_table_for_join[0] + "." + api_response2.replace("%OR%", " OR " + target_table_for_join[0] + ".")
        elif (not api_response2.__contains__("%OR%") and api_response2.__contains__("#AND#")):
            lsmodifiedApliResponse = target_table_for_join[0] + "." + api_response2.replace("#AND#", " AND " + target_table_for_join[0] + ".")
        elif (api_response2.__contains__("%OR%") and api_response2.__contains__("#AND#")):
            lsmodifiedApliResponse = target_table_for_join[0] + "." + api_response2.replace("#AND#", "AND " + target_table_for_join[0] + ".").replace("%OR%", " OR " + target_table_for_join[0] + ".")
        else:
            lsmodifiedApliResponse = target_table_for_join[0] + "." + api_response2
        StrSQl += " WHERE " + api_response2

    else:
        print("Invalid Input")
        
    if Execution_Type == 'Incremental':
        StrSQl += " AND "+target_table+".UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+") "
    elif Execution_Type == 'date_range':
        from_timestamp = datetime.fromtimestamp(from_date)
        from_date_str = from_timestamp.strftime( "%Y-%m-%d")
        to_timestamp = datetime.fromtimestamp(to_date)
        to_date_str = to_timestamp.strftime( "%Y-%m-%d")
        between_condition = f' cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
        StrSQl += f" AND {between_condition}"
        
    dq_apply_column_data = spark.sql(StrSQl)
    total_count = spark.sql(total_count_query).count()
    pass_count = spark.sql(pass_count_query).count()
    dq_report = sigma_dq_generate_dq_report_for_joins(dq_apply_column_data,column,dq_rule,total_count,pass_count,meta={})
  
    return dq_report
