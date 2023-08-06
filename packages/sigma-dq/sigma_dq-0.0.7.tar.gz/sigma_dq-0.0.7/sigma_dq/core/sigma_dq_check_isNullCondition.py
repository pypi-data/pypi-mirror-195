from datetime import datetime
from sigma_dq.core.common import spark
from sigma_dq.helper.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


# sigma_dq_check_isNullCondition('PURCHASE_DOCUMENT_CATEGORY','JDE_Material_Master.Brand_BU_Map_Custom = "HEALTH"',target_table)
def sigma_dq_check_isNullCondition(target_column:str, api_response:str,target_table:str,Execution_Type='',from_date=0,to_date=0,meta={}):
    conditions = api_response.split('#and#')
    case_list = []
    column = target_column
    dq_rule = 'isNullCond'

    for condition in conditions:
        case = ""
        if condition.__contains__("="):
            case = condition.replace("=", "==")
        elif condition.__contains__("is null"):
            case = condition  # TODO
        elif condition.__contains__("is not null"):
            case = condition  # TODO
        elif condition.__contains__("not like"):
            clause = condition.split("not like")
            pattern = clause[1].strip().replace("'", "").replace('"', '')
            case = f"{clause[0].strip()} not like '%{pattern}%'"
        elif condition.__contains__("like"):
            clause = condition.split("like")
            pattern = clause[1].strip().replace("'", "").replace('"', '')
            case = f"{clause[0].strip()} like '%{pattern}%'"
        elif condition.__contains__("not in"):
            case = condition  # TODO
        elif condition.__contains__("in"):
            case = condition  # TODO
        case_list.append(case)

    sql_case_when = ""
    common_condition = f"({target_column} is not null and trim({target_column}) <> '') then 'PASS'"
    if len(case_list) > 0:
        for case in case_list:
            if case_list.index(case) == 0:
                sql_case_when += " case"
            sql_case_when += f" when {case} and {common_condition}"
    else:
        sql_case_when = f" case when {common_condition}"

    sql_case_when += f" else 'FAIL' end as DQ_Status"

    if(Execution_Type == 'Incremental'):
       StrSQl = f"select {target_column},{sql_case_when} from {target_table}  where UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+") "

    elif Execution_Type == "date_range":
        from_timestamp = datetime.fromtimestamp(from_date)
        from_date_str = from_timestamp.strftime( "%Y-%m-%d")
        to_timestamp = datetime.fromtimestamp(to_date)
        to_date_str = to_timestamp.strftime( "%Y-%m-%d")
        between_condition = f' WHERE cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
        StrSQL = f"select {target_column},{sql_case_when} from {target_table}" + between_condition

    else:
        StrSQl = f"select {target_column},{sql_case_when} from {target_table} "

    dq_apply_column_data = spark.sql(StrSQl)
    dq_report = sigma_dq_generate_dq_report(dq_apply_column_data,column,dq_rule)

    return dq_report
