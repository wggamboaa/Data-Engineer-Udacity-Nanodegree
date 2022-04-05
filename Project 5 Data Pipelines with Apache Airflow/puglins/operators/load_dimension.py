from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#33CEFF'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 sql_query = "",
                 delete_load = False,
                 table_name = "",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql_query = sql_query
        self.table_name = table_name
        self.delete_load = delete_load

    def execute(self, context):
        redshift_hook = PostgresHook(postgres_conn_id = self.redshift_conn_id)
        if self.delete_load:
            self.log.info('------------------------------------------------------------------------------')
            self.log.info(f"Remove load from process if true. Execute delete statement on table {self.table_name}")
            redshift_hook.run(f"DELETE FROM {self.table_name}")
        
        self.log.info('------------------------------------------------------------------------------')
        self.log.info(f"Running ETL for the Dimension Table {self.table_name}")
        redshift_hook.run(self.sql_query)
        self.log.info('------------------------------------------------------------------------------')
        self.log.info(f"Dimension Table {self.table_name} loaded.")
