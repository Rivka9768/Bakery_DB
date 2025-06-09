--1

CREATE OR REPLACE FUNCTION get_unassigned_employees(
  p_branchId NUMERIC,
  p_roleName VARCHAR,
  p_shiftDate DATE,
  p_shiftTime VARCHAR
)
RETURNS REFCURSOR AS
$$
DECLARE
  emp_cursor REFCURSOR;
BEGIN
  OPEN emp_cursor FOR
    SELECT e.*
    FROM Employee e
    JOIN Roles r ON e.roleId = r.roleId
    WHERE e.branchId = p_branchId
      AND r.name = p_roleName
      AND NOT EXISTS (
        SELECT 1
        FROM EmployeeShifts es
        JOIN Shifts s ON es.shiftId = s.shiftId
        WHERE es.employeeId = e.employeeId
          AND s.shiftDate = p_shiftDate
          AND s.shiftTime = p_shiftTime
      );
  RETURN emp_cursor;
END;
$$ LANGUAGE plpgsql;


--2

CREATE OR REPLACE FUNCTION log_changes_function()
RETURNS TRIGGER AS
$$
BEGIN
  INSERT INTO LogChanges (
    tableName,
    operation,
    changedBy,
    changeTime,
    oldData,
    newData
  )
  VALUES (
    TG_TABLE_NAME,
    TG_OP,
    CURRENT_USER,
    CURRENT_TIMESTAMP,
    CASE WHEN TG_OP = 'INSERT' THEN NULL ELSE to_jsonb(OLD) END,
    CASE WHEN TG_OP = 'DELETE' THEN NULL ELSE to_jsonb(NEW) END
  );

  RETURN NULL; -- For AFTER triggers
END;
$$ LANGUAGE plpgsql;
