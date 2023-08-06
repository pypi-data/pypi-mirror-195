from datetime import datetime

def sigma_dq_helper_generate_run_id():
  return datetime.now().strftime('%Y%m%d%H%M%S')