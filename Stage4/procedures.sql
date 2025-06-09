--1

CREATE OR REPLACE PROCEDURE assign_employees_to_shift(
  p_branchId NUMERIC,
  p_shiftDate DATE,
  p_shiftTime VARCHAR
)
LANGUAGE plpgsql
AS
$$
DECLARE
  emp_cursor CURSOR FOR
    SELECT e.employeeId
    FROM Employee e
    WHERE e.branchId = p_branchId
      AND NOT EXISTS (
        SELECT 1
        FROM EmployeeShifts es
        JOIN Shifts s ON es.shiftId = s.shiftId
        WHERE es.employeeId = e.employeeId
          AND s.shiftDate = p_shiftDate
          AND s.shiftTime = p_shiftTime
      );

  emp RECORD;
  v_required INT;
  v_count INT := 0;
  v_shiftId INT;
BEGIN
  SELECT minAmountOfWorkers INTO v_required FROM Branches WHERE branchId = p_branchId;

  INSERT INTO Shifts(branchId, shiftDate, shiftTime)
  VALUES (p_branchId, p_shiftDate, p_shiftTime)
  RETURNING shiftId INTO v_shiftId;

  OPEN emp_cursor;
  LOOP
    FETCH emp_cursor INTO emp;
    EXIT WHEN NOT FOUND;

    INSERT INTO EmployeeShifts(employeeId, shiftId)
    VALUES (emp.employeeId, v_shiftId);

    v_count := v_count + 1;
    EXIT WHEN v_count >= v_required;
  END LOOP;
  CLOSE emp_cursor;

  IF v_count < v_required THEN
    RAISE NOTICE 'Only % employees assigned, but % required', v_count, v_required;
  ELSE
    RAISE NOTICE 'Shift % successfully filled with % employees.', v_shiftId, v_count;
  END IF;
EXCEPTION
  WHEN OTHERS THEN
    RAISE WARNING 'Shift assignment failed: %', SQLERRM;
END;
$$;
