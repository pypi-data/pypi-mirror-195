"""
The Schema Class is logically tied to the price transparency guide schemas
It is intended to provide a standard class that will contain
all table stream target tables and analytic tables

It will also
"""

from .pt_table import Pt_table
from .pt_analytic_table import AnalyticTable
from .pt_ingest_table import IngestTable
from pyspark.sql.session import SparkSession

from typing import Callable

import time

class Pt_schema:

    spark: SparkSession
    ingest_tables: {str: IngestTable}
    analytic_tables: {str: AnalyticTable}

    def __init__(self, spark=None):
        self.spark = spark if spark is not None else SparkSession.builder.getOrCreate()
        self.set_tables()

    def set_tables(self):
        """
        Method is intended to be overwritten for each specific pt_schema subclass
        :return: None
        """
        self.analytic_tables = {}
        self.ingest_tables = {}
        return None

    def get_tables(self) -> [Pt_table]:
        return list(self.ingest_tables.values()) + list(self.analytic_tables.values())

    def create_tables(self):
        # TODO: parallelize table create
        for t in self.get_tables():
            t.create_table()

    def drop_tables(self):
        # TODO: parallelize drop table
        for t in self.get_tables():
            t.drop_table()

    def create_views(self) -> None:
        # TODO: parallelize create views
        for t in self.get_tables():
            t.create_view()

    def purge_tables(self) -> None:
        # TODO: parallelize purge tables
        for t in self.get_tables():
            t.purge_table()

    def get_insertIntoIngestTables(self):
        batch_merge_functions: [Callable] = [t.get_batch_merge_function() for t in list(self.ingest_tables.values())]

        def insertIntoIngestTables(microBatchOutputDF, batchId):
            # This approach feels expensive, will need to compare vs persist & filter
            microBatchOutputDF.persist()
            for batch_merge in batch_merge_functions:
                batch_merge(microBatchOutputDF, batchId)
            microBatchOutputDF.unpersist()
        return insertIntoIngestTables

    def file_ingest_query(self, ingest_file_path):
        # TODO: make queryName include payer description from file name
        # TODO: derive checkpoint location from raw file location
        source_cp = 'dbfs:/tmp/inr/_checkpoint'
        return self.spark.readStream.option("buffersize", 67108864).format("payer-mrf") \
                   .option("payloadAsArray", "true").load(ingest_file_path) \
                   .writeStream.queryName("payer-mrf") \
                   .option("checkpointLocation", source_cp) \
                   .foreachBatch(self.get_insertIntoIngestTables()).start()

    def run_file_ingest(self, ingest_file_path):
        # Method for single file ingest stop stream on complete
        def stop_on_file_complete(query, wait_time=10):
            while query.isActive:
                msg, is_data_available, is_trigger_active = query.status.values()
                if not is_data_available and not is_trigger_active and msg != "Initializing sources":
                    query.stop()
                time.sleep(5)
            query.awaitTermination(wait_time)
        stop_on_file_complete(self.file_ingest_query(ingest_file_path), wait_time=10)

    def run_file_analytic_merge(self, file_name):
        # This method is intended to be overwritten in subclasses
        pass
