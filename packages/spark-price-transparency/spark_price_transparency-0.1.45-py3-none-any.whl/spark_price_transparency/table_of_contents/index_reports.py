"""
Index reports is the analytic form for table of contents data
It is necessary since it will have all of the files that need to be ingested for any given payer
"""

from ..pt_analytic_table import AnalyticTable
from pyspark.sql.functions import col, lit, first
from pyspark.sql.functions import explode, array, when
from pyspark.sql.functions import broadcast
from pyspark.sql.types import ArrayType, StructType, StructField, StringType


class Index_reports(AnalyticTable):

    reporting_plans = ArrayType(StructType([
                                StructField("plan_name", StringType(), True),
                                StructField("plan_id", StringType(), True),
                                StructField("plan_id_type", StringType(), True),
                                StructField("plan_market_type", StringType(), True)]))

    definition = \
        [("toc_file_name",         StringType(),    True, "Table of Contents file name"),
         ("reporting_entity_name", StringType(),    True, "Entity Name of the TOC reporting entity"),
         ("reporting_entity_type", StringType(),    True, "Entity Type of the TOC reporting entity"),
         ("file_type",             StringType(),    True, "File Type; 'in-network-rates' or 'allowed-amounts'"),
         ("location",              StringType(),    True, "URL of file"),
         ("reporting_plans",       reporting_plans, True, "Location file plans detail")]

    def run_file_analytic_merge(self, file_name):
        header = self.spark.table('pt_stage.toc_header').filter(col('file_name') == lit(file_name)) \
            .groupBy(col('file_name').alias('toc_file_name')) \
            .agg(first(col('reporting_entity_name'), ignorenulls=True).alias('reporting_entity_name'),
                 first(col('reporting_entity_type'), ignorenulls=True).alias('reporting_entity_type')) \
            .alias('header')

        reporting = self.spark.table('pt_stage.toc_reporting').filter(col('file_name') == lit(file_name)) \
            .withColumn('file_type', explode(array(lit('in-network-rates'), lit('allowed-amounts')))) \
            .withColumn('file_detail',
                        explode(when(col('file_type') == lit('in-network-rates'), col('in_network_files'))
                                .otherwise(array(col('allowed_amount_file'))))) \
            .select(col('file_name').alias('toc_file_name'),
                    col('file_type'),
                    col('file_detail.location').alias('location'),
                    col('reporting_plans')) \
            .alias('reporting')

        src = broadcast(header).join(reporting, 'toc_file_name', 'left')

        self.get_table().merge(src, "1 != 1") \
            .whenNotMatchedInsertAll() \
            .execute()
