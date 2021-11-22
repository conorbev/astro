from typing import Callable, Optional

from airflow.decorators.base import task_decorator_factory

from astro.sql.operators.dataframe_to_sql import DataframeToSqlOperator
from astro.sql.operators.sql_to_dataframe import SqlToDataframeOperator


def from_sql(
    python_callable: Optional[Callable] = None,
    multiple_outputs: Optional[bool] = None,
    conn_id: str = "",
    database: Optional[str] = None,
    schema: Optional[str] = None,
    warehouse: Optional[str] = None,
):
    return task_decorator_factory(
        python_callable=python_callable,
        multiple_outputs=multiple_outputs,
        decorated_operator_class=SqlToDataframeOperator,
        **{
            "conn_id": conn_id,
            "database": database,
            "schema": schema,
            "warehouse": warehouse,
        }
    )


def to_sql(
    python_callable: Optional[Callable] = None,
    multiple_outputs: Optional[bool] = None,
    conn_id: str = "",
    database: Optional[str] = None,
    schema: Optional[str] = None,
    warehouse: Optional[str] = None,
    output_table_name: str = "",
):
    return task_decorator_factory(
        python_callable=python_callable,
        multiple_outputs=multiple_outputs,
        decorated_operator_class=DataframeToSqlOperator,
        conn_id=conn_id,
        database=database,
        schema=schema,
        warehouse=warehouse,
        output_table_name=output_table_name,
    )