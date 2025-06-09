
DO
$$
DECLARE
  emp_rec RECORD;
  emp_cursor REFCURSOR;
BEGIN
  emp_cursor := get_unassigned_employees(
    1::NUMERIC,
    'baker'::VARCHAR,
    (CURRENT_DATE + INTERVAL '1 day')::DATE,
    'morning'::VARCHAR
  );

  LOOP
    FETCH emp_cursor INTO emp_rec;
    EXIT WHEN NOT FOUND;
    RAISE NOTICE 'Employee available for a shift assignment: %', emp_rec.name;
  END LOOP;
  CLOSE emp_cursor;

  CALL assign_employees_to_shift(1, (CURRENT_DATE + INTERVAL '1 day')::DATE, 'morning');
END;
$$ LANGUAGE plpgsql;
