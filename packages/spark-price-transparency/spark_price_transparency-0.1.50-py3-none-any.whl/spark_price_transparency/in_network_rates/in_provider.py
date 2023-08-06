"""
In provider is an analytic table form of in network rates data containing provider details

"""

from ..pt_analytic_table import AnalyticTable
from pyspark.sql.types import StringType, IntegerType, ArrayType, StructType, StructField
from pyspark.sql.functions import first, broadcast, col, lit, coalesce, when

def col_sk_provider():
    """ A surrogate key is needed to provide ease of look up for report provider it requires:
     - provider_groups
     - location
    """
    return coalesce(when(col('provider_groups').isNotNull(), hash(col('provider_groups'))),
                    when(col('location').isNotNull(), hash(col('location')))).alias('sk_provider')

class In_provider(AnalyticTable):

    provider_groups = ArrayType(StructType([
        StructField("npi", ArrayType(StringType()), True),
        StructField("tin", StructType([
            StructField("type", StringType(), True),
            StructField("value", StringType(), True)]), True)]))

    definition = \
        [("reporting_entity_name", StringType(), False, "Reporting Entity Name"),
         ("sk_provider", IntegerType(), False, "SK of provider details"),
         ("provider_groups", provider_groups, True, "Group of providers as organized by publisher"),
         ("location", StringType(), True, "URL of download if not provided in provider_groups")]

    def run_file_analytic_merge(self, file_name):
        header = self.spark.table('pt_stage.inr_header').filter(col('file_name') == lit(file_name)) \
            .groupBy(col('file_name').alias('inr_file_name')) \
            .agg(first(col('reporting_entity_name'), ignorenulls=True).alias('reporting_entity_name')) \
            .alias('header')

        provider = self.spark.table('pt_stage.inr_provider').filter(col('file_name') == lit(file_name)) \
            .select(col('file_name').alias('inr_file_name'),
                    col_sk_provider(),
                    col('provider_groups'),
                    col('location'))

        src = broadcast(header).join(provider, 'inr_file_name', 'left') \
            .drop('inr_file_name')

        self.get_table().merge(src, "1 != 1") \
            .whenNotMatchedInsertAll() \
            .execute()
