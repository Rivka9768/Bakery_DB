CREATE OR REPLACE FUNCTION log_allergen_warning()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.allergenInfo IS NOT NULL AND length(trim(NEW.allergenInfo)) > 0 THEN
        INSERT INTO AllergenLog(bakedGoodsId, allergenInfo, note)
        VALUES (
            NEW.bakedGoodsId,
            NEW.allergenInfo,
            'Product contains allergen information'
        );
    END IF;

    RETURN NEW;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Failed to log allergen info for product %: %', NEW.bakedGoodsId, SQLERRM;
        RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_allergen
AFTER INSERT ON BakedGoods
FOR EACH ROW
EXECUTE FUNCTION log_allergen_warning();




