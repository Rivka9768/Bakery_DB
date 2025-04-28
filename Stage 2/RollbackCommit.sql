-- rollback:

BEGIN;

INSERT INTO employee (employeeid, name, phone, email, dob, branchid, roleid)
VALUES
(404, 'Gila Kassab', '054-1234567', 'Gila.Kassab@gmail.com', '2003-05-15', 1, 2);

rollback;


-- commit:


BEGIN;

UPDATE employee
SET name = 'Rivka Sorscher'
WHERE employeeid = 1;


COMMIT;

SELECT * FROM employee WHERE employeeid = 1;