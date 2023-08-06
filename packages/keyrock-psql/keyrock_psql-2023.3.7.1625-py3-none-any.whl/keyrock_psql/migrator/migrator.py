import json
import logging

from keyrock_core import json_util
from .. import psql

logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)


class Migrator():
    def __init__(self, db_config):
        self.db_config = db_config

    def update(self, target_schema):
        logger.info(f"Migrator.update")

        logger.info(f"wait for psql server: {self.db_config['host']}")
        psql.wait_for_server(self.db_config, timeout_sec=15)

        debug_db_name = f"{self.db_config['host']}:{self.db_config['db']}"
        if psql.database_exists(self.db_config):
            logger.info(f"database exists: {debug_db_name}")
        else:
            logger.info(f"database doesn't exist: {debug_db_name}")
            logger.info(f"creating database: {debug_db_name}")
            psql.create_database(self.db_config)

        conn = psql.Connection(self.db_config)
        current_schema = psql.get_structure(conn)

        structure_diff = psql.catalog_diff(current_schema, target_schema)
        if structure_diff['op'] is not None:
            logger.debug("changes applied:")
            logger.debug(json.dumps(json_util.strip_unchanged(structure_diff), indent=2))

        cmd_list = psql.diff_to_cmd_list(structure_diff)
        if len(cmd_list) > 0:
            logger.debug("command list:")
            logger.debug(json.dumps(cmd_list, indent=2))

        error_list = conn.exec_cmd_list(cmd_list)
        if len(error_list) > 0:
            logger.error("errors encountered:")
            logger.error(json.dumps(error_list, indent=2))

        #
        # Verify that the new structure matches the intended target
        #
        updated_schema = psql.get_structure(conn)
        verify_diff = psql.catalog_diff(updated_schema, target_schema)
        if verify_diff['op'] is not None:
            logger.error(f"target schema not completely applied:")
            logger.error(json.dumps(json_util.strip_unchanged(verify_diff), indent=2))

        cmd_list = psql.diff_to_cmd_list(verify_diff)
        if len(cmd_list) > 0:
            logger.error(f"delta command list is not empty:")
            logger.error(json.dumps(cmd_list, indent=2))
