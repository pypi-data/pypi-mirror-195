from ..pt_ingest_table import IngestTable
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, FloatType, LongType


class Aa_network(IngestTable):

    header_key: str = "out_of_network"

    providers = ArrayType(StructType([
        StructField("billed_charge", FloatType(), True),
        StructField("npi", ArrayType(StringType()), True)]))

    payments = ArrayType(StructType([
        StructField("allowed_amount", FloatType(), True),
        StructField("billing_code_modifier", ArrayType(StringType()), True),
        StructField("providers", providers, True)]))

    allowed_amounts = ArrayType(StructType([
        StructField("tin", StructType([
            StructField("type", StringType(), True),
            StructField("value", StringType(), True)
        ]), True),
        StructField("service_code", ArrayType(StringType()), True),
        StructField("billing_class", StringType(), True),
        StructField("payments", payments, True)]))

    definition = \
        [("file_name",                 StringType(),     False, "File name of in network rate json"),
         ("batch_id",                  LongType(),       True,  "Streaming ingest batchId"),
         ("name",                      StringType(),     True,  "Name of the item/service offered"),
         ("billing_code",              StringType(),     True,  "Plan or issuer code for in-network providers"),
         ("billing_code_type",         StringType(),     True,  "Common billing code types."),
         ("billing_code_type_version", StringType(),     True,  "Version of billing code or year of plan"),
         ("allowed_amounts",           allowed_amounts,  True,  "Array of allowed amounts")]
