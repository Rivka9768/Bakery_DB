CREATE OR REPLACE PROCEDURE produce_batch(
    p_baked_id INT,
    p_quantity INT,
    p_employee_id INT,
    p_branch_id INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;
    needed NUMERIC;
    available NUMERIC;
BEGIN
    -- בדיקת זמינות חומרי גלם
    FOR rec IN SELECT * FROM Recipe WHERE bakeGoodsId = p_baked_id LOOP
        needed := rec.materialQuantity * p_quantity;

        SELECT quantity INTO available
        FROM RawMaterials
        WHERE RawMaterialsId = rec.RawMaterialsId;

        IF available IS NULL THEN
            RAISE EXCEPTION 'Raw material % not found.', rec.RawMaterialsId;
        ELSIF available < needed THEN
            RAISE EXCEPTION 'Not enough material %: needed %, available %',
                rec.RawMaterialsId, needed, available;
        END IF;
    END LOOP;

    -- עדכון מלאי חומרי גלם
    FOR rec IN SELECT * FROM Recipe WHERE bakeGoodsId = p_baked_id LOOP
        UPDATE RawMaterials
        SET quantity = quantity - (rec.materialQuantity * p_quantity)
        WHERE RawMaterialsId = rec.RawMaterialsId;
    END LOOP;

    -- הכנסת רשומה ל-ProductionLine
    INSERT INTO ProductionLine (bakeGoodsId, quantity, employeeId, productionDate)
    VALUES (p_baked_id, p_quantity, p_employee_id, CURRENT_DATE);

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Production failed: %', SQLERRM;
END;
$$;



UPDATE RawMaterials
SET quantity = 100
WHERE RawMaterialsId = 23;




SELECT * FROM productionline
CALL produce_batch(
    p_baked_id := 1,         -- מזהה מוצר אפייה (קיים בטבלת BakedGoods)
    p_quantity := 5,         -- כמות יחידות שרוצים לייצר
    p_employee_id := 2,      -- מזהה עובד (קיים בטבלת Employee)
    p_branch_id := 1         -- מזהה סניף (קיים בטבלת Branches)
);


ALTER TABLE ProductionLine
DROP COLUMN productionLineId;
ALTER TABLE ProductionLine
ADD COLUMN productionLineId SERIAL PRIMARY KEY;


SELECT rm.RawMaterialsId, rm.name, rm.quantity AS before_quantity
FROM Recipe r
JOIN RawMaterials rm ON r.RawMaterialsId = rm.RawMaterialsId
WHERE r.bakeGoodsId = 1;