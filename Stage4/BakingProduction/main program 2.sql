DO $$
DECLARE
    ref refcursor;
    rec RECORD;
BEGIN
    RAISE NOTICE '--- בדיקת זמינות חומרי גלם למוצר 1 ---';

    -- שלב 1: קריאה לפונקציה שמחזירה RefCursor
    ref := get_materials_summary_for_product(1);

    LOOP
        FETCH ref INTO rec;
        EXIT WHEN NOT FOUND;
        RAISE NOTICE 'חומר: %, נדרש: %, קיים: %, סטטוס: %',
            rec.name, rec.required, rec.available, rec.status;
    END LOOP;

    CLOSE ref;

    RAISE NOTICE '--- הרצת ייצור אצווה של מוצר 1 בכמות 5 ---';

    -- שלב 2: קריאה לפרוצדורה לייצור אצווה
    CALL produce_batch(
        p_baked_id := 1,
        p_quantity := 5,
        p_employee_id := 2,
        p_branch_id := 1
    );

    RAISE NOTICE '✅ ההפקה הושלמה בהצלחה';

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE '❌ שגיאה בתהליך: %', SQLERRM;
END;
$$;
