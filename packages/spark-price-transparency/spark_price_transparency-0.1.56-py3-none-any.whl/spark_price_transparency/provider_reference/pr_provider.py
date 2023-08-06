from ..pt_ingest_table import IngestTable
from pyspark.sql.types import StringType, LongType, StructType, StructField, ArrayType


class Pr_provider(IngestTable):

    header_key = 'provider_groups'

    provider_group = StructType([StructField("npi", ArrayType(StringType()), True),
                                 StructField("tin", StructType([
                                     StructField("type", StringType(), True),
                                     StructField("value", StringType(), True)]), True)])

    definition = [("file_name",       StringType(),   False, "Negotiated Price Provider Details"),
                  ("batch_id",        LongType(),     True,  "Streaming ingest batchId"),
                  ("provider_groups", provider_group, True, "Negotiated Price Provider Details")]
