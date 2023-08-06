
def sigma_dq_helper_get_GE_DF(target_table):
  sql = 'select *  from '+target_table+' '
  base_df = spark.sql(sql)
  ge_base_df = ge.dataset.SparkDFDataset(base_df)
  return base_df,ge_base_df