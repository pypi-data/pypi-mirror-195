## generate dq message
def sigma_dq_helper_generate_dq_message(results_final):
    dq_message = []
    dq = {}
    for a in results_final:
        dq = {}
        dq['column_name'] = results_final[a]['column']
        dq['rule'] = results_final[a]['rule']
        dq['success'] = results_final[a]['success']
        dq_message.append(dq)

    return dq_message
