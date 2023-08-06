"""
In coverage is an analytic table form of in network rate data containing coverage details

"""


from ..pt_analytic_table import AnalyticTable
from pyspark.sql.types import StringType, IntegerType, StructType, StructField, ArrayType
from pyspark.sql.functions import first, broadcast, hash, split, col, lit, struct, array, when, slice, concat_ws

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

class In_coverage(AnalyticTable):

    planType = StructType([StructField("name", StringType(), True),
                           StructField("id", StringType(), True),
                           StructField("id_type", StringType(), True),
                           StructField("market_type", StringType(), True)])

    billingCodeType = StructType([StructField("code", StringType(), True),
                                  StructField("type", StringType(), True),
                                  StructField("version", StringType(), True)])

    billingCodesType = ArrayType(billingCodeType)

    definition = \
        [("inr_file_name",         StringType(),     True,  "Coverage source in-network-rate file"),
         ("reporting_entity_name", StringType(),     True,  "Legal name of the entity publishing"),
         ("reporting_entity_type", StringType(),     True,  "Type of the legal entity"),
         ("plan",                  planType,         True,  "Plan details from in-network-rate file"),
         ("sk_date",               StringType(),     True,  "SK of date"),
         ("sk_coverage",           IntegerType(),    True,  "SK of coverage details and primary key for in_coverage"),
         ("arrangement",           StringType(),     True,  "ffs, bundle, or capitation"),
         ("name",                  StringType(),     True,  "This is name of the item/service that is offered"),
         ("issuer_billing_code",   billingCodeType,  True,  "Issuer billing code details"),
         ("billing_codes",         billingCodesType, True,  "Array of billing code details")]

    def run_file_analytic_merge(self, file_name):
        header = self.spark.table('pt_stage.inr_header').filter(col('file_name') == lit(file_name)) \
                           .groupBy(col('file_name').alias('inr_file_name')) \
                           .agg(first(col('reporting_entity_name'), ignorenulls=True).alias('reporting_entity_name'),
                                first(col('reporting_entity_type'), ignorenulls=True).alias('reporting_entity_type'),
                                first(col('plan_name'), ignorenulls=True).alias('name'),
                                first(col('plan_id'), ignorenulls=True).alias('id'),
                                first(col('plan_id_type'), ignorenulls=True).alias('id_type'),
                                first(col('plan_market_type'), ignorenulls=True).alias('market_type'),
                                first(col('last_updated_on'), ignorenulls=True).alias('last_updated_on')) \
                           .select(col('inr_file_name'),
                                   col('reporting_entity_name'),
                                   col('reporting_entity_type'),
                                   struct(col('name'),
                                          col('id'),
                                          col('id_type'),
                                          col('market_type')).alias('plan'),
                                   col_sk_date()).alias('header')

        coverage = self.spark.table('pt_stage.inr_network').filter(col('file_name') == lit(file_name)) \
                       .withColumn('arrangement', cols_arrangement()) \
                       .select(col('file_name').alias('inr_file_name'),
                               col_sk_coverage(),
                               col('arrangement.*'))

        src = broadcast(header).join(coverage, 'inr_file_name', 'left')

        self.get_table().merge(src, "1 != 1") \
            .whenNotMatchedInsertAll() \
            .execute()
