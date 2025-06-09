
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
