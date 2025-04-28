-- אילוץ ראשון: UNIQUE על שדה email בטבלת employee
ALTER TABLE employee
ADD CONSTRAINT unique_employee_email UNIQUE (email);

-- אילוץ שני: CHECK על טבלת Categories
ALTER TABLE Categories
ADD CONSTRAINT chk_valid_price CHECK (pricePerWeight > 0);

-- אילוץ שלישי: DEFAULT על טבלת BakedGoods
ALTER TABLE productionLine
ALTER COLUMN productionDate SET DEFAULT CURRENT_DATE;