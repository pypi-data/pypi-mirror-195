
from pyspark.sql.session import SparkSession
from .in_network_rates.schema import In_network_rates_schema


class PTStage:

    name: str = "pt_stage"

    def __init__(self, spark=None):
        self.spark = spark if spark is not None else SparkSession.builder.getOrCreate()
        self.in_network_rates = In_network_rates_schema(self.spark)

    def create_stage_database(self):
        # TODO: check if database already exists
        self.spark.sql(f'CREATE DATABASE IF NOT EXISTS {self.name}')

    def initialize_pt_stage(self):
        self.create_stage_database()
        self.in_network_rates.create_tables()
