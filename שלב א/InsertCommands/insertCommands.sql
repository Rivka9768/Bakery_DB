-- Insert into Branches
INSERT INTO Branches (branchId, location, minAmountOfWorkers) VALUES
(1, 'Tel Aviv', 10),
(2, 'Jerusalem', 8),
(3, 'Haifa', 7),
(4, 'Eilat', 5),
(5, 'Beer Sheva', 6),
(6, 'Netanya', 7),
(7, 'Ashdod', 9),
(8, 'Rishon Lezion', 8),
(9, 'Holon', 7),
(10, 'Petah Tikva', 6);

-- Insert into Categories
INSERT INTO Categories (CategoryId, name, description, pricePerWeight) VALUES
(1, 'Bread', 'Various types of bread', 10.5),
(2, 'Pastry', 'Sweet and savory pastries', 15.0),
(3, 'Cake', 'Different kinds of cakes', 20.0),
(4, 'Cookies', 'Assorted cookies', 12.0),
(5, 'Muffins', 'Soft and fluffy muffins', 14.0),
(6, 'Doughnuts', 'Fried or baked doughnuts', 18.0),
(7, 'Pies', 'Sweet and savory pies', 22.0),
(8, 'Gluten-Free', 'Baked goods without gluten', 25.0),
(9, 'Vegan', 'Baked goods with no animal products', 27.0),
(10, 'Specialty', 'Unique or seasonal baked goods', 30.0);

-- Insert into BakedGoods
INSERT INTO BakedGoods (bakedGoodsId, name, lifetime, allergenInfo, CategoryId) VALUES
(1, 'Baguette', 3, 'Gluten', 1),
(2, 'Croissant', 2, 'Gluten, Butter', 2),
(3, 'Chocolate Cake', 5, 'Eggs, Dairy', 3),
(4, 'Whole Wheat Bread', 4, 'Gluten', 1),
(5, 'Danish Pastry', 3, 'Gluten, Butter', 2),
(6, 'Cheesecake', 6, 'Dairy, Eggs', 3),
(7, 'Pita', 3, 'Gluten', 1),
(8, 'Apple Pie', 5, 'Eggs, Gluten', 7),
(9, 'Rye Bread', 4, 'Gluten', 1),
(10, 'Cinnamon Roll', 3, 'Gluten, Butter', 2),
(11, 'Chocolate Chip Cookies', 7, 'Gluten, Dairy', 4),
(12, 'Blueberry Muffin', 5, 'Gluten, Eggs', 5),
(13, 'Vanilla Doughnut', 3, 'Gluten, Dairy', 6),
(14, 'Pumpkin Pie', 6, 'Eggs, Dairy', 7),
(15, 'Gluten-Free Brownie', 5, 'Dairy, Eggs', 8),
(16, 'Vegan Banana Bread', 6, 'None', 9),
(17, 'Specialty Matcha Cake', 7, 'Dairy, Eggs', 10),
(18, 'French Baguette', 3, 'Gluten', 1),
(19, 'Almond Croissant', 2, 'Gluten, Nuts, Dairy', 2),
(20, 'Red Velvet Cake', 5, 'Eggs, Dairy', 3);

-- Insert into RawMaterials
INSERT INTO RawMaterials (RawMaterialsId, name, unitOfMeasurement, quantity, branchId) VALUES
(1, 'Flour', 'kg', 100, 1),
(2, 'Sugar', 'kg', 50, 2),
(3, 'Butter', 'kg', 30, 3),
(4, 'Eggs', 'units', 200, 4),
(5, 'Milk', 'liters', 150, 5),
(6, 'Yeast', 'kg', 20, 6),
(7, 'Salt', 'kg', 25, 7),
(8, 'Chocolate', 'kg', 40, 8),
(9, 'Vanilla', 'liters', 10, 9),
(10, 'Cinnamon', 'kg', 15, 10),
(11, 'Baking Powder', 'kg', 12, 1),
(12, 'Honey', 'liters', 18, 2),
(13, 'Coconut Oil', 'liters', 22, 3),
(14, 'Oats', 'kg', 35, 4),
(15, 'Almond Flour', 'kg', 20, 5),
(16, 'Raisins', 'kg', 10, 6),
(17, 'Walnuts', 'kg', 12, 7),
(18, 'Pecans', 'kg', 14, 8),
(19, 'Maple Syrup', 'liters', 16, 9),
(20, 'Cornstarch', 'kg', 10, 10),
(21, 'Molasses', 'liters', 8, 1),
(22, 'Cocoa Powder', 'kg', 25, 2),
(23, 'Brown Sugar', 'kg', 30, 3),
(24, 'Soy Milk', 'liters', 12, 4),
(25, 'Rice Flour', 'kg', 18, 5),
(26, 'Hazelnuts', 'kg', 10, 6),
(27, 'Sunflower Seeds', 'kg', 8, 7),
(28, 'Pumpkin Seeds', 'kg', 6, 8),
(29, 'Chia Seeds', 'kg', 5, 9),
(30, 'Sesame Seeds', 'kg', 7, 10),
(31, 'Peanut Butter', 'kg', 15, 1),
(32, 'Cashews', 'kg', 12, 2),
(33, 'Dried Cranberries', 'kg', 9, 3),
(34, 'Coconut Flakes', 'kg', 14, 4),
(35, 'Tapioca Starch', 'kg', 10, 5),
(36, 'Agave Syrup', 'liters', 13, 6),
(37, 'Quinoa Flour', 'kg', 11, 7),
(38, 'Pistachios', 'kg', 10, 8),
(39, 'Date Syrup', 'liters', 9, 9),
(40, 'Carob Powder', 'kg', 8, 10);

-- Insert into Roles
INSERT INTO Roles (roleId, name, description) VALUES
(1, 'Baker', 'Responsible for baking goods'),
(2, 'Cashier', 'Handles customer transactions'),
(3, 'Manager', 'Oversees branch operations'),
(4, 'Cleaner', 'Maintains cleanliness in the bakery'),
(5, 'Delivery', 'Responsible for delivering orders');

-- Insert into Recipe
INSERT INTO Recipe (materialQuantity, bakeGoodsId, RawMaterialsId) VALUES
(3, 1, 1),  -- Flour for Baguette
(2, 1, 2),  -- Sugar for Baguette
(1, 1, 5),  -- Milk for Baguette
(2, 2, 1),  -- Flour for Croissant
(3, 2, 3),  -- Butter for Croissant
(1, 2, 4),  -- Eggs for Croissant
(3, 3, 1),  -- Flour for Chocolate Cake
(4, 3, 3),  -- Butter for Chocolate Cake
(2, 3, 8),  -- Chocolate for Chocolate Cake
(1, 4, 1),  -- Flour for Whole Wheat Bread
(2, 4, 7),  -- Salt for Whole Wheat Bread
(1, 5, 5),  -- Milk for Danish Pastry
(3, 5, 3),  -- Butter for Danish Pastry
(2, 6, 1),  -- Flour for Cheesecake
(4, 6, 5),  -- Milk for Cheesecake
(1, 6, 4),  -- Eggs for Cheesecake
(3, 7, 7),  -- Salt for Pita
(2, 7, 1),  -- Flour for Pita
(1, 8, 4),  -- Eggs for Apple Pie
(2, 8, 9),  -- Vanilla for Apple Pie
(3, 9, 1),  -- Flour for Rye Bread
(1, 9, 7),  -- Salt for Rye Bread
(2, 10, 3),  -- Butter for Cinnamon Roll
(3, 10, 1),  -- Flour for Cinnamon Roll
(1, 10, 7),  -- Salt for Cinnamon Roll
(1, 11, 1),  -- Flour for Chocolate Chip Cookies
(3, 11, 8),  -- Chocolate for Chocolate Chip Cookies
(2, 12, 1),  -- Flour for Blueberry Muffin
(3, 12, 4),  -- Eggs for Blueberry Muffin
(2, 13, 3),  -- Butter for Vanilla Doughnut
(1, 13, 5),  -- Milk for Vanilla Doughnut
(4, 14, 1),  -- Flour for Pumpkin Pie
(2, 14, 4),  -- Eggs for Pumpkin Pie
(1, 15, 6),  -- Yeast for Gluten-Free Brownie
(2, 15, 8),  -- Coconut for Gluten-Free Brownie
(3, 16, 1),  -- Flour for Vegan Banana Bread
(1, 16, 5),  -- Milk for Vegan Banana Bread
(2, 17, 3),  -- Butter for Specialty Matcha Cake
(3, 17, 5),  -- Milk for Specialty Matcha Cake
(1, 18, 1),  -- Flour for French Baguette
(2, 19, 2),  -- Sugar for Almond Croissant
(1, 19, 3),  -- Butter for Almond Croissant
(3, 20, 1),  -- Flour for Red Velvet Cake
(4, 20, 5),  -- Milk for Red Velvet Cake
(1, 21, 7),  -- Salt for Oatmeal Cookie
(3, 21, 1),  -- Flour for Oatmeal Cookie
(2, 22, 1),  -- Flour for Lemon Tart
(3, 22, 4),  -- Eggs for Lemon Tart
(1, 23, 5),  -- Milk for Coconut Macaroon
(2, 23, 8),  -- Coconut for Coconut Macaroon
(3, 24, 1),  -- Flour for Strawberry Shortcake
(1, 24, 5),  -- Milk for Strawberry Shortcake
(3, 25, 1),  -- Flour for Chocolate Muffin
(4, 25, 8),  -- Chocolate for Chocolate Muffin
(2, 26, 1),  -- Flour for Glazed Doughnut
(1, 26, 5),  -- Milk for Glazed Doughnut
(3, 27, 1),  -- Flour for Cherry Pie
(2, 27, 9),  -- Vanilla for Cherry Pie
(3, 28, 8),  -- Chocolate for Vegan Chocolate Cake
(1, 28, 3),  -- Butter for Vegan Chocolate Cake
(2, 29, 5),  -- Milk for Specialty Honey Cake
(3, 30, 1);  -- Flour for Ciabatta



-- Insert into NutritionFacts
INSERT INTO NutritionFacts (nutritionFactId, bakedGoodsId, calories, carbs, protein, fat, sugar) VALUES
(1, 1, 250, 50, 7, 2, 1),
(2, 2, 350, 45, 6, 20, 10),
(3, 3, 500, 60, 8, 25, 30),
(4, 4, 270, 52, 8, 3, 2),
(5, 5, 400, 48, 7, 22, 12),
(6, 6, 550, 65, 9, 30, 35),
(7, 7, 220, 45, 6, 1, 1),
(8, 8, 480, 55, 8, 27, 25),
(9, 9, 260, 50, 7, 2, 1),
(10, 10, 420, 46, 7, 21, 15),
(11, 11, 300, 45, 5, 12, 18),
(12, 12, 330, 55, 6, 15, 20),
(13, 13, 320, 50, 5, 14, 16),
(14, 14, 390, 60, 7, 19, 22),
(15, 15, 280, 40, 4, 9, 10),
(16, 16, 310, 45, 5, 11, 12),
(17, 17, 380, 55, 7, 20, 23),
(18, 18, 270, 50, 6, 3, 2),
(19, 19, 350, 50, 6, 18, 15),
(20, 20, 500, 60, 8, 26, 28),
(21, 21, 300, 50, 6, 14, 16),
(22, 22, 330, 45, 5, 18, 20),
(23, 23, 250, 40, 4, 10, 12),
(24, 24, 400, 55, 6, 22, 25),
(25, 25, 350, 50, 6, 18, 20),
(26, 26, 310, 45, 5, 14, 18),
(27, 27, 370, 50, 7, 18, 22),
(28, 28, 450, 60, 8, 20, 24),
(29, 29, 380, 55, 7, 19, 21),
(30, 30, 290, 50, 6, 10, 8),
(31, 31, 350, 50, 6, 18, 15),
(32, 32, 420, 55, 7, 22, 20),
(33, 33, 300, 40, 5, 16, 14),
(34, 34, 330, 45, 6, 17, 19),
(35, 35, 360, 50, 7, 18, 25),
(36, 36, 410, 55, 8, 24, 28),
(37, 37, 250, 45, 5, 9, 12),
(38, 38, 330, 50, 6, 15, 18),
(39, 39, 460, 60, 8, 20, 23),
(40, 40, 280, 50, 6, 11, 15);


-- Insert into Employee ???
INSERT INTO employee (employeeid, name, phone, email, dob, branchid, roleid) 
VALUES 
(144, 'David Cohen', '054-1234567', 'david.cohen@example.com', '1990-05-15', 1, 2),
(145, 'Maya Levi', '052-7654321', 'maya.levi@example.com', '1995-09-20', 2, 3),
(146, 'Avi Shimon', '050-1122334', 'avi.shimon@example.com', '1988-12-10', 1, 1);

-- Insert into ProductionLine ???
INSERT INTO productionLine (productionlineid, productiondate, quantity, bakegoodsid, employeeid) 
VALUES 
(201, '2025-03-29', 150, 10, 144),
(202, '2025-03-29', 200, 12, 145),
(203, '2025-03-29', 180, 11, 146);
