## this function generates validation suite based on inputs and blank dataframe
def sigma_dq_helper_generate_validation_suite(inputs):
    
    number_of_columns = len(inputs['table_columns'])
    expectation_statement_list = []
    for i in range(0,number_of_columns):
        #print(inputs['table_columns'][i])
        column_name = "'" + inputs['table_columns'][i]['column_name'] + "'"
        for rules_raw in inputs['table_columns'][i]['rules']:
            rule_name_ui = rules_raw['name']
            #print(rule_name_ui)
            rule_name_dq = rules_raw['substitute']
            rules_params = rules_raw['params']
            rules_df_params = rules_raw['default_static_params']
            #print(rules_df_params)
            #print(rules_params)
            #print(rule_name_dq)
            #print(rule_name_ui)

            if rules_df_params == []:
                statement  = 'ge_base_df.'+rule_name_dq+'('+ ','.join(rules_params)+')'
                #print('TT'+str(rules_df_params))
                statement_ = statement.replace('column_name',column_name)
                #print ('YU'+str(rules_df_params))
            else:
                statement__ = 'ge_base_df.'+rule_name_dq+'('+ ','.join(rules_df_params)+')'
                statement_ = statement__.replace('column_name',column_name)

            #print(statement_)
            expectation_statement_list.append(statement_)

    return expectation_statement_list