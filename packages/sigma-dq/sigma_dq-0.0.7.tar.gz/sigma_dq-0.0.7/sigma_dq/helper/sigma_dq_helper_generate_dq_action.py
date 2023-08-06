def sigma_dq_helper_generate_dq_action(dq_message):
    dq_action = 'Fail'
    for a in range(0,len(dq_message)):
        if dq_message[a]['success'] == False:
            dq_action = 'Fail'
            break
        
        else:
            dq_action = 'Pass'
    return dq_action
  