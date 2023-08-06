from datetime import datetime

def sigma_dq_helper_generate_created_at():
  return datetime.now().strftime('%s')