from sigma_dq.core.common import spark

def column_operations_new(target_table: str, target_column_operation: str):
    target_column_operation = target_column_operation.replace("=", "==")

    # split based on comparator
    columns = []
    if target_column_operation.__contains__("=="):
        columns.extend(target_column_operation.split("=="))
    if target_column_operation.__contains__(">"):
        columns.extend(target_column_operation.split(">"))
    if target_column_operation.__contains__("<"):
        columns.extend(target_column_operation.split("<"))

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

    str_sql = f"select {query_columns}, case when {column_operation} then 'PASS' else 'FAIL' end \
        as DQ_Status from {target_table} limit 100 "
    print(str_sql)

    dq_apply_column_data = spark.sql(str_sql)
    dq_report = {'column': query_columns, 'rule': 'columnOperation',
                 'total_rows_checked': dq_apply_column_data.count()}
    total_dq_pass_count = dq_apply_column_data.filter(dq_apply_column_data.DQ_Status == 'PASS').count()
    dq_report['total_rows_failed'] = dq_apply_column_data.filter(dq_apply_column_data.DQ_Status == 'FAIL').count()

    if dq_report['total_rows_failed'] > 0:
        dq_report['success'] = False
        dq_report['failed_percent'] = (dq_report['total_rows_failed'] / dq_report['total_rows_checked']) * 100
        dq_report['failed_values'] = set(dq_apply_column_data.select(dq_apply_column_data[columns[0]]
                                                                     ).filter(dq_apply_column_data.DQ_Status == 'FAIL'
                                                                              ).rdd.flatMap(lambda x: x).collect())
    else:
        dq_report['success'] = True
        dq_report['passed_percent'] = (total_dq_pass_count / dq_report['total_rows_checked']) * 100

    return dq_report
