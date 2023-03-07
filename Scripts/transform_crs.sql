DO $$  
DECLARE
    table_name text;
    column_name text;
    sql text; 
BEGIN
    FOR table_name, column_name IN  
        SELECT c.table_name, c.column_name
        FROM information_schema.columns c
        JOIN geometry_columns g
            ON c.table_name = g.f_table_name AND c.column_name = g.f_geometry_column
        WHERE g.srid = 4269
        LOOP
            EXECUTE format('ALTER TABLE %I ALTER COLUMN geometry TYPE geometry(MultiPolygon, 4269) USING ST_Multi(%I);', table_name, column_name);
            sql := format('ALTER TABLE %I ALTER COLUMN geometry TYPE geometry(MultiPolygon, 102003) USING ST_Transform(%I, 102003);', table_name, column_name); 
            EXECUTE sql;
        END LOOP;
END;
$$ LANGUAGE plpgsql;
