from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


def sigma_dq_check_isExisting_v1(target_column,api_response,target_table,Execution_Type='',meta = {}):

    and_logic = '#and#'
    or_logic = '%OR%'
    userinput = '>0'
    column = target_column
    dq_rule = 'isExisting'


    #target_table_for_join = target_table.split('.')
    target_table_for_join = '_'.join(str(a)for a in target_table.split('_')[:2])
    modified_target_column = target_table+"."+target_column 


    if(api_response.__contains__("%OR%")):
        modifiedApiOR_Res = api_response.split('%OR%')
        modifiedORFinal=''
        modifiedORLeftjoin = ''
        left_join_singleTable = ''
        #print(len(modifiedApiOR_Res))
        for singleTable in modifiedApiOR_Res:
            left_join_singleTable = singleTable.split('.') 
            index = modifiedApiOR_Res.index(singleTable)
            if(index >= 1):
                modifiedORFinal += " OR "+modified_target_column +" == " +singleTable #operator goes here
                modifiedORLeftjoin += " left join "+target_table_for_join+"."+left_join_singleTable[0]+" on "+modified_target_column +" = " +singleTable  #Appendlogicneedstobe impleted
            else:
                modifiedORFinal += modified_target_column +" == " +singleTable   #operator goes here
                modifiedORLeftjoin = " left join "+target_table_for_join+"."+left_join_singleTable[0]+" on "+modified_target_column +" = " +singleTable
            StrSQl = "select "+modified_target_column+", CASE WHEN " +modifiedORFinal+" \
                THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +target_table+" \
                " +modifiedORLeftjoin+"  "


    elif(api_response.__contains__("#and#")):
        modifiedApiAND_Res = api_response.split('#and#')
        modifiedANDFinal=''
        modifiedANDLeftjoin = ''
        left_join_singleTable = ''
        # print(len(modifiedApiAND_Res))
        for singleTable in modifiedApiAND_Res:
            left_join_singleTable = singleTable.split('.') 
            index = modifiedApiAND_Res.index(singleTable)
            if(index >= 1):
                modifiedANDFinal += " AND "+modified_target_column +" == " +singleTable #operator goes here
                modifiedANDLeftjoin += " left join "+target_table_for_join+"."+left_join_singleTable[0]+" on "+modified_target_column +" = " +singleTable  #Appendlogicneedstobe impleted
            else:
                modifiedANDFinal += modified_target_column +" == " +singleTable  #operator goes here
                modifiedANDLeftjoin = " left join "+target_table_for_join+"."+left_join_singleTable[0]+" on "+modified_target_column +" = " +singleTable
            StrSQl = "select "+modified_target_column+", CASE WHEN " +modifiedANDFinal+" \
            THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " +target_table+" \
            " +modifiedANDLeftjoin+"  "

    #if(api_response.__contains__("#or#") and api_response.__contains__("#and#") ):
        #for singleTable in api_response:
    
    else:
        return "Error please check the input"
    #print(StrSQl)
    if(Execution_Type == 'Incremental'):
      StrSQl += " WHERE "+target_table+"."+"dqAction = 'NA'"
    dq_apply_column_data = spark.sql(StrSQl)
    
    dq_report = sigma_dq_generate_dq_report(dq_apply_column_data,column,dq_rule)
  
    return dq_report
