CREATE VIEW View_ClothingCustomersOrders AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.customer_mail,
    co.order_id,
    co.order_date,
    co.order_notes,
    p.garment_name, 
    pu.amount
FROM customer c
JOIN customer_order co ON c.customer_id = co.customer_id
JOIN purchase pu ON co.order_id = pu.order_id
JOIN Products p ON pu.garm_id = p.garment_id;



CREATE VIEW View_BakeryEmployeeProduction AS
SELECT 
    e.employeeId,
    e.name AS employee_name,
    e.email,
    e.phone,
    e.salary,
    r.name AS role_name,
    b.location AS branch_location,
    pl.productionLineId,
    pl.productionDate,
    pl.quantity,
    p.bakedgoods_name
FROM Employee e
JOIN Roles r ON e.roleId = r.roleId
JOIN Branches b ON e.branchId = b.branchId
LEFT JOIN ProductionLine pl ON e.employeeId = pl.employeeId
LEFT JOIN Products p ON pl.bakeGoodsId = p.bakedGoodsId;

SELECT 
    customer_id,
    garment_name,
    SUM(amount) AS total_amount_ordered
FROM View_ClothingCustomersOrders
GROUP BY customer_id, garment_name;

SELECT v.*
FROM View_ClothingCustomersOrders v
WHERE order_date = (
    SELECT MAX(order_date)
    FROM View_ClothingCustomersOrders v2
    WHERE v2.customer_id = v.customer_id
);

SELECT 
    employeeId,
    employee_name,
    SUM(quantity) AS total_produced
FROM View_BakeryEmployeeProduction
where quantity is not null
GROUP BY employeeId, employee_name
ORDER BY total_produced DESC;


SELECT 
    branch_location,
    SUM(quantity) AS total_quantity
FROM View_BakeryEmployeeProduction
where quantity is not null
GROUP BY branch_location;