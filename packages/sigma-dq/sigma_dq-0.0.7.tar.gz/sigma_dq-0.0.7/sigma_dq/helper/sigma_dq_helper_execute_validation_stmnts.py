from sigma_dq.helper.sigma_dq_helper_unique_elements_in_list import sigma_dq_helper_unique_elements_in_list

def sigma_dq_helper_execute_validation_stmnts(expectation_suite):
    columns_values_parent = {}
    i = 0
    DQ_action = 'Pass'
    for stmnt in expectation_suite:
        stmnt_ = eval(stmnt)
        columns_values_child = {}
       
        if stmnt.startswith('sigma_dq_check') == True or stmnt.startswith('sigma_dq_core') == True:
            columns_values_child['column'] = stmnt_['column']
            columns_values_child['rule'] = stmnt_['rule']
            columns_values_child['total_rows_checked'] = stmnt_['total_rows_checked']
            columns_values_child['total_rows_failed'] = stmnt_['total_rows_failed']
            columns_values_child['success'] = stmnt_['success']
            try:
                rule_id_loop = stmnt_['meta']['rule_id']
                columns_values_child['meta'] = {'rule_id': rule_id_loop}
            except:
                columns_values_child['meta'] = {}
            if stmnt_['success'] == False:
                columns_values_child['failed_percent'] = stmnt_['failed_percent']
                columns_values_child['failed_values'] = stmnt_['failed_values']
            else:
                columns_values_child['passed_percent'] = stmnt_['passed_percent']
            columns_values_parent[i] = columns_values_child
        else:
            column = stmnt_['expectation_config']['kwargs']['column']
            rule = stmnt_['expectation_config']['expectation_type']
            total_rows_checked = stmnt_['result']['element_count']
            total_rows_failed = stmnt_['result']['unexpected_count']
            columns_values_child['column'] = column
            columns_values_child['rule'] = rule
            columns_values_child['total_rows_checked'] = total_rows_checked
            columns_values_child['total_rows_failed'] = total_rows_failed
            # columns_values_child['meta'] = stmnt_['meta']
            try:
                rule_id_loop = stmnt_['meta']['rule_id']
                columns_values_child['meta'] = {'rule_id': rule_id_loop}
            except:
                columns_values_child['meta'] = {}
            if stmnt_['success'] == False:
                failed_percent = stmnt_['result']['unexpected_percent_total']
                raw_fail_list = stmnt_['result']['unexpected_list']
                raw_fail_list_ = sigma_dq_helper_unique_elements_in_list(raw_fail_list)
                columns_values_child['failed_percent'] = failed_percent
                columns_values_child['failed_values'] = raw_fail_list_
                columns_values_child['success'] = False
            else:
                try:
                    passed_percent = ((total_rows_checked - total_rows_failed) / total_rows_checked) * 100
                except:
                    passed_percent = 0
                columns_values_child['success'] = True
                columns_values_child['passed_percent'] = passed_percent
            columns_values_parent[i] = columns_values_child
        i = i + 1
#     columns_values_parent[i] = {'DQ_action':   DQ_action}
    return columns_values_parent