INSERT into Department(department_id, department_name)
values (1,'bakery'),(2,'dress store');

SELECT count(*) FROM employee;
SELECT * FROM employee_1;

ALTER TABLE employee_1
ADD COLUMN department_id NUMERIC 

UPDATE employee_1
SET department_id = 2;

ALTER TABLE employee
ADD COLUMN date_join DATE NULL,
ADD COLUMN salary NUMERIC NULL;

INSERT INTO employee (employeeid, name, email ,date_join, salary,department_id)
SELECT employee_id, employee_name, employee_mail, date_join, salary, department_id
FROM employee_1;

UPDATE employee_1
SET employee_id = employee_id + 403


ALTER TABLE products
ADD COLUMN garment_categoryId character varying;


INSERT INTO products (garment_name, garment_quantity_in_stock, garment_price , garment_id, garment_supplierID, garment_categoryId, department_id)
SELECT *
FROM garment;


INSERT INTO products (bakedgoodsid, bakedgoods_name, bakedgoods_lifetime , bakedgoods_allergeninfo, bakedgoods_categ_id, department_id)
SELECT *
FROM bakedgoods;

-- נא לשים לב שהרבה מפעולות האינטגרציה נעשו לפי הממשק של PG-ADMIN לפי שמתואר בreadMe.



