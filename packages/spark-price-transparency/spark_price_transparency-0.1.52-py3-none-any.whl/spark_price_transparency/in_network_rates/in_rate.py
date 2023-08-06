"""
In rate is an analytic table form of in network rate data containing rate details

"""
from ..pt_analytic_table import AnalyticTable
from pyspark.sql.types import IntegerType, FloatType, DateType

from pyspark.sql.functions import explode, array_contains, when, coalesce, to_date, concat_ws, struct, array
from pyspark.sql.functions import first, broadcast, hash, split, slice, col, lit
from pyspark.sql.types import ArrayType, StructField, StructType, StringType

billing_codes_schema = ArrayType(StructType([
                        StructField("code", StringType(), False),
                        StructField("type", StringType(), False),
                        StructField("version", StringType(), False)]))

def cols_arrangement():
    return when(col('negotiation_arrangement') == lit('ffs'),
                struct(col('negotiation_arrangement').alias('arrangement'),
                       col('name'),
                       struct(col('billing_code').alias('code'),
                              col('billing_code_type').alias('type'),
                              col('billing_code_type_version').alias('version')).alias('issuer_billing_code'),
                       array(struct(col('billing_code').alias('code'),
                                    col('billing_code_type').alias('type'),
                                    col('billing_code_type_version').alias('version'))).alias('billing_codes'))) \
          .when(col('negotiation_arrangement') == lit('bundle'),
                struct(col('negotiation_arrangement').alias('arrangement'),
                       col('name'),
                       struct(col('billing_code').alias('code'),
                              col('billing_code_type').alias('type'),
                              col('billing_code_type_version').alias('version')).alias('issuer_billing_code'),
                       col('bundled_codes').cast(billing_codes_schema.simpleString()).alias('billing_codes'))) \
          .when(col('negotiation_arrangement') == lit('capitation'),
                struct(col('negotiation_arrangement').alias('arrangement'),
                       col('name'),
                       struct(col('billing_code').alias('code'),
                              col('billing_code_type').alias('type'),
                              col('billing_code_type_version').alias('version')).alias('issuer_billing_code'),
                       col('covered_services').cast(billing_codes_schema.simpleString()).alias('billing_codes')
                       )).alias('arrangement')

def col_sk_coverage():
    return hash(cols_arrangement()).alias('sk_coverage')

def col_sk_date():
    """ A surrogate key for assigning a date to each report"""
    return concat_ws('', slice(split(col('last_updated_on'), '-'), 1, 2)).alias('sk_date')

def col_sk_provider():
    """ A surrogate key is needed to provide ease of look up for report provider it requires:
     - provider_groups
     - location
    """
    return coalesce(when(col('provider_groups').isNotNull(), hash(col('provider_groups'))),
                    when(col('location').isNotNull(), hash(col('location')))).alias('sk_provider')

class In_rate(AnalyticTable):

    serviceCodeType = ArrayType(StringType())
    billCodeModifierType = ArrayType(StringType())

    definition = \
        [("sk_entity", IntegerType(), False, "SK of payer entity"),
         ("sk_date", StringType(), True, "SK of date"),
         ("sk_coverage", IntegerType(), True, "SK of coverage details"),
         ("sk_provider", IntegerType(), True, "SK of provider details"),
         ("negotiated_type", StringType(), True, "negotiated, derived, fee schedule, percentage, or per diem"),
         ("negotiated_rate", FloatType(), True, "Dollar or percentage based on the negotiation_type"),
         ("expiration_date", DateType(), True, "Date agreement for the negotiated_price ends"),
         ("service_code", serviceCodeType, True, "CMS two-digit code(s) placed on a professional claim"),
         ("billing_class", StringType(), True, "professional or institutional"),
         ("billing_code_modifier", billCodeModifierType, True, "Billing Code Modifiers")]

    def run_file_analytic_merge(self, file_name):
        header = self.spark.table('pt_stage.inr_header').filter(col('file_name') == lit(file_name)) \
            .groupBy(col('file_name')) \
            .agg(first(col('reporting_entity_name'), ignorenulls=True).alias('reporting_entity_name'),
                 first(col('last_updated_on'), ignorenulls=True).alias('last_updated_on')) \
            .select(col('file_name'),
                    col('reporting_entity_name'),
                    col_sk_date()) \
            .alias('header')

        provider = self.spark.table('pt_stage.inr_provider').filter(col('file_name') == lit(file_name)) \
            .select(col('file_name'),
                    col('provider_group_id'),
                    col_sk_provider()) \
            .distinct().alias('provider')

        src = self.spark.table('pt_stage.inr_network').filter(col('file_name') == lit(file_name)).alias('network') \
            .withColumn('sk_coverage', col_sk_coverage()) \
            .join(broadcast(header), 'file_name', 'left') \
            .withColumn('negotiated_rate', explode(col('negotiated_rates'))) \
            .join(provider,
                  [col('network.file_name') == col('provider.file_name'),
                   array_contains(col('negotiated_rate.provider_references'), col('provider.provider_group_id'))],
                  "left") \
            .withColumn('negotiated_price', explode(col('negotiated_rate.negotiated_prices'))) \
            .select(col('reporting_entity_name'),
                    col('sk_date'),
                    col('sk_coverage'),
                    col('sk_provider'),
                    col('negotiated_price.*')) \
            .withColumn('expiration_date', to_date(col('expiration_date'), "yyyy-MM-dd"))

        self.get_table().merge(src, "1 != 1") \
            .whenNotMatchedInsertAll() \
            .execute()
