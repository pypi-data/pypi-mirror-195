from typing import Dict, Any
from pyspark.sql import Row


class GoogleAnalytics4EventBuilder:
    def build(self, row: Row) -> Dict[str, Any]:
        all_columns = row.asDict().keys()
        id_columns = {"client_id", "user_id"}
        attribute_columns = all_columns - id_columns

        return {
            "client_id": str(row.client_id),
            "user_id": str(row.user_id) if hasattr(row, "user_id") else None,
            "events": [{"name": "odap_export"}],
            "user_properties": {attr: {"value": getattr(row, attr, None)} for attr in attribute_columns},
        }
