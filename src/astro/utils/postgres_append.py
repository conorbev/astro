from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2 import sql


def postgres_append_func(main_table, columns, casted_columns, append_table, conn_id):
    if columns or casted_columns:
        statement = "INSERT INTO {main_table} ({main_cols}{sep}{main_casted_cols})(SELECT {fields}{sep}{casted_fields} FROM {append_table})"
    else:
        statement = "INSERT INTO {main_table} (SELECT * FROM {append_table})"

    column_names = [sql.Identifier(c) for c in columns]
    casted_column_names = [sql.Identifier(k) for k in casted_columns.keys()]
    fields = [sql.Identifier(append_table, c) for c in columns]
    casted_fields = [
        sql.SQL("CAST({k} AS {v})").format(k=sql.Identifier(k), v=sql.SQL(v))
        for k, v in casted_columns.items()
    ]

    query = sql.SQL(statement).format(
        main_cols=sql.SQL(",").join(column_names),
        main_casted_cols=sql.SQL(",").join(casted_column_names),
        main_table=sql.Identifier(main_table),
        fields=sql.SQL(",").join(fields),
        sep=sql.SQL(",") if columns and casted_columns else sql.SQL(""),
        casted_fields=sql.SQL(",").join(casted_fields),
        append_table=sql.Identifier(append_table),
    )

    hook = PostgresHook(postgres_conn_id=conn_id)
    return query.as_string(hook.get_conn())