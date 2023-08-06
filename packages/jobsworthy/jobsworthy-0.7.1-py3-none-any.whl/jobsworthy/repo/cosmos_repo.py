from typing import Optional, Dict, List
from pyspark.sql import types as T, SparkSession

from . import spark_repo, writers, readers, spark_util, repo_messages

from jobsworthy.repo import spark_db
from jobsworthy.util import secrets, logger


class CosmosDb(spark_repo.SparkRepo):
    """
    Repository Class which wraps Cosmos Table functions.  Designed specifically to enable streaming reads.

    To create an object of this class:

    MyCosmosTable(db=db,
                  secrets_provider=secrets_provider,
                  stream_reader=repo.CosmosStreamReader)

    To create an instance for testing (where there is no access to a Cosmos table, use a mock Stream Reader

    Class Attributes
    ----------------

    `additional_spark_options`:  A List of repo.Option which is added to the default spark options.
        Common options to consider adding here are as follows:
        [
            repo.Option.COSMOS_INFER_SCHEMA,
            repo.Option.COSMOS_ITEM_OVERWRITE,
            repo.Option.COSMOS_READ_PARTITION_DEFAULT,
            repo.Option.COSMOS_CHANGE_FEED_INCREMENTAL
        ]
        If providing a schema the `spark.cosmos.read.inferSchema.enabled` option is not required.

    """

    additional_spark_options = None

    def __init__(self,
                 db: spark_db.Db,
                 reader: Optional[spark_repo.ReaderType] = None,
                 stream_reader: Optional[spark_repo.StreamReaderType] = None,
                 stream_writer: Optional[spark_repo.StreamWriterType] = None,
                 secrets_provider: Optional[secrets.Secrets] = None):
        super().__init__(db, reader, None, stream_reader, stream_writer, None, secrets_provider)

    def _extended_spark_options(self) -> Dict:
        if not self.__class__.additional_spark_options:
            return {}
        if isinstance(self.__class__.additional_spark_options, dict):
            raise repo_messages.cosmos_additional_spark_options_as_dict_no_longer_supported()
        return spark_util.SparkOption.function_based_options(self.__class__.additional_spark_options)

    # Stream Processing
    def read_stream(self, reader_options: Optional[List[readers.ReaderSwitch]] = None):
        return self.stream_reader().read(self, reader_options=reader_options)

    # Configuration
    def db_config(self):
        return self.db.config.cosmos_db

    def spark_config_options(self):
        # TODO: assumes the secret provider returns a Right
        return {**self.default_spark_options(), **self._extended_spark_options()}

    def default_spark_options(self) -> Dict:
        return {"spark.cosmos.accountEndpoint": self.db_config().endpoint,
                "spark.cosmos.accountKey": self._get_secret(),
                "spark.cosmos.database": self.db_config().db_name,
                "spark.cosmos.container": self.db_config().container_name}

    def _get_secret(self):
        account_key = self.secrets_provider.get_secret(self.db_config().account_key_name)
        if account_key.is_left():
            logger.info(f"Jobsworth: Failed to get account key for: {self.db_config().account_key_name}")
            return None
        return account_key.value
