--1

CREATE OR REPLACE FUNCTION trg_notify_employee_assigned()
RETURNS TRIGGER AS
$$
DECLARE
  empName VARCHAR;
BEGIN
  SELECT name INTO empName FROM Employee WHERE employeeId = NEW.employeeId;
  RAISE NOTICE 'Employee % assigned to shift %', empName, NEW.shiftId;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER notify_employee_assigned
AFTER INSERT ON EmployeeShifts
FOR EACH ROW
EXECUTE FUNCTION trg_notify_employee_assigned();

--2

-- Branches
CREATE TRIGGER log_branches_trigger
AFTER INSERT OR UPDATE OR DELETE ON Branches
FOR EACH ROW EXECUTE FUNCTION log_changes_function();



-- Categories
CREATE TRIGGER log_categories_trigger
AFTER INSERT OR UPDATE OR DELETE ON Categories
FOR EACH ROW EXECUTE FUNCTION log_changes_function();



-- BakedGoods
CREATE TRIGGER log_bakedgoods_trigger
AFTER INSERT OR UPDATE OR DELETE ON BakedGoods
FOR EACH ROW EXECUTE FUNCTION log_changes_function();



-- RawMaterials
CREATE TRIGGER log_rawmaterials_trigger
AFTER INSERT OR UPDATE OR DELETE ON RawMaterials
FOR EACH ROW EXECUTE FUNCTION log_changes_function();



-- NutritionFacts
CREATE TRIGGER log_nutritionfacts_trigger
AFTER INSERT OR UPDATE OR DELETE ON NutritionFacts
FOR EACH ROW EXECUTE FUNCTION log_changes_function();



-- Roles
CREATE TRIGGER log_roles_trigger
AFTER INSERT OR UPDATE OR DELETE ON Roles
FOR EACH ROW EXECUTE FUNCTION log_changes_function();



-- Recipe
CREATE TRIGGER log_recipe_trigger
AFTER INSERT OR UPDATE OR DELETE ON Recipe
FOR EACH ROW EXECUTE FUNCTION log_changes_function();



-- Employee
CREATE TRIGGER log_employee_trigger
AFTER INSERT OR UPDATE OR DELETE ON Employee
FOR EACH ROW EXECUTE FUNCTION log_changes_function();


-- ProductionLine
CREATE TRIGGER log_productionline_trigger
AFTER INSERT OR UPDATE OR DELETE ON ProductionLine
FOR EACH ROW EXECUTE FUNCTION log_changes_function();

-- Shifts 
CREATE TRIGGER log_shifts_trigger
AFTER INSERT OR UPDATE OR DELETE ON Shifts
FOR EACH ROW EXECUTE FUNCTION log_changes_function();



-- employeeShifts 
CREATE TRIGGER log_employeeshifts_trigger
AFTER INSERT OR UPDATE OR DELETE ON Employeeshifts
FOR EACH ROW EXECUTE FUNCTION log_changes_function();
