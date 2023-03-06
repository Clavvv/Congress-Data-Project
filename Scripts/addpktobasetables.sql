DO $$
DECLARE row RECORD;
BEGIN
  FOR row IN 
    SELECT tab.table_schema, tab.table_name
    FROM information_schema.tables tab
    LEFT JOIN information_schema.table_constraints tco 
          ON tab.table_schema = tco.table_schema
          AND tab.table_name = tco.table_name 
          AND tco.constraint_type = 'PRIMARY KEY'
    WHERE tab.table_type = 'BASE TABLE'
          AND tab.table_schema not in ('pg_catalog', 'information_schema')
          AND tco.constraint_name is null
    ORDER BY table_schema, table_name 
    LOOP 
        EXECUTE 'ALTER TABLE "' || row.table_schema || '"."' || row.table_name  || '" ADD COLUMN p_id SERIAL PRIMARY KEY';
    END LOOP;  
END;
$$;
