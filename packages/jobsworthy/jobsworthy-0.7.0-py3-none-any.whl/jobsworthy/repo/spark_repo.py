from typing import Union, Optional
from pyspark.sql import functions as F

from . import spark_db, readers, writers, repo_messages
from jobsworthy.util import secrets, fn

ReaderType = Union[readers.DeltaFileReader, readers.DeltaTableReader, readers.HiveTableReader]
StreamReaderType = Union[readers.CosmosStreamReader, readers.DeltaStreamReader]
StreamWriterType = Union[writers.StreamFileWriter, writers.StreamHiveWriter]


class SparkRepo:
    schema = None

    def __init__(self,
                 db: spark_db.Db,
                 reader: Optional[ReaderType] = None,
                 delta_table_reader: Optional[ReaderType] = None,
                 stream_reader: Optional[StreamReaderType] = None,
                 stream_writer: Optional[StreamWriterType] = None,
                 stream_awaiter: Optional[writers.StreamAwaiter] = None,
                 secrets_provider: Optional[secrets.Secrets] = None):
        self.db = db
        self.reader = reader if reader else readers.HiveTableReader
        self.delta_table_reader = delta_table_reader if delta_table_reader else readers.DeltaTableReader
        self.stream_reader = stream_reader
        self.stream_writer = stream_writer
        self.stream_awaiter = stream_awaiter if stream_awaiter else writers.StreamAwaiter
        self.secrets_provider = secrets_provider

    def has_specified_schema(self):
        return hasattr(self, "schema_as_dict") or self.__class__.schema

    def _struct_schema(self):
        return self.__class__.schema if self.__class__.schema else None

    def determine_schema_to_use_for_df(self, schema_from_argument=None):
        if schema_from_argument:
            return schema_from_argument

        if not self.has_specified_schema():
            raise repo_messages.no_schema_provided_on_create_df()

        return self.schema_as_struct()

    def schema_as_struct(self):
        if not self.has_specified_schema():
            return None
        return self._struct_schema() if self._struct_schema() else F.StructType().fromJson(self.schema_as_dict())

    def after_initialise(self):
        ...

    def after_append(self):
        ...

    def after_upsert(self):
        ...

    def after_stream_write_via_delta_upsert(self):
        ...
