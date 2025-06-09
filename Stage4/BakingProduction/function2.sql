CREATE OR REPLACE FUNCTION get_materials_summary_for_product(baked_id INT)
RETURNS refcursor AS $$
DECLARE
    ref refcursor;
    rec RECORD;
    available_qty NUMERIC;
    temp_table TEXT := 'temp_material_status';
BEGIN
    -- יצירת טבלה זמנית לאחסון תוצאות
    EXECUTE format('DROP TABLE IF EXISTS %I', temp_table);
    EXECUTE format('CREATE TEMP TABLE %I (name TEXT, required NUMERIC, available NUMERIC, status TEXT)', temp_table);

    FOR rec IN
        SELECT rm.name, r.materialQuantity AS required, rm.quantity AS available
        FROM Recipe r
        JOIN RawMaterials rm ON r.RawMaterialsId = rm.RawMaterialsId
        WHERE r.bakeGoodsId = baked_id
    LOOP
        INSERT INTO temp_material_status(name, required, available, status)
        VALUES (
            rec.name,
            rec.required,
            rec.available,
            CASE
                WHEN rec.available >= rec.required THEN 'OK'
                ELSE 'LOW'
            END
        );
    END LOOP;

    OPEN ref FOR EXECUTE format('SELECT * FROM %I', temp_table);
    RETURN ref;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error: %', SQLERRM;
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;
