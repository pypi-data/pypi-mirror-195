from ..pt_ingest_table import IngestTable
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, LongType


class Toc_reporting(IngestTable):

    header_key: str = "reporting_structure"

    reporting_plans = ArrayType(StructType([
                          StructField("plan_name",        StringType(), True),
                          StructField("plan_id_type",     StringType(), True),
                          StructField("plan_id",          StringType(), True),
                          StructField("plan_market_type", StringType(), True)]))

    file_location = StructType([
                          StructField("description", StringType(), True),
                          StructField("location",    StringType(), True)])

    in_network_files = ArrayType(file_location)

    definition = [("file_name",             StringType(),     False, "File name of table of contents json"),
                  ("batch_id",              LongType(),       True,  "Streaming ingest batchId"),
                  ("reporting_plans",       reporting_plans,  True,  "Legal name of the entity publishing"),
                  ("in_network_files",      in_network_files, True,  "Type of the legal entity"),
                  ("allowed_amount_file",   file_location,    True,  "The plan name and plan sponsor/company.")]
