CREATE TABLE Branches
(
  branchId NUMERIC NOT NULL,
  location VARCHAR NOT NULL,
  minAmountOfWorkers NUMERIC NOT NULL,
  PRIMARY KEY (branchId)
);

CREATE TABLE Categories
(
  CategoryId NUMERIC NOT NULL,
  name VARCHAR NOT NULL,
  description VARCHAR,
  pricePerWeight NUMERIC NOT NULL,
  PRIMARY KEY (CategoryId)
);

CREATE TABLE BakedGoods
(
  bakedGoodsId NUMERIC NOT NULL,
  name VARCHAR NOT NULL,
  lifetime NUMERIC NOT NULL,
  allergenInfo VARCHAR NOT NULL,
  categoryId NUMERIC NOT NULL,
  PRIMARY KEY (bakedGoodsId),
  FOREIGN KEY (categoryId) REFERENCES Categories(categoryId)
);

CREATE TABLE RawMaterials
(
  rawMaterialsId NUMERIC NOT NULL,
  name VARCHAR NOT NULL,
  unitOfMeasurement VARCHAR NOT NULL,
  quantity NUMERIC NOT NULL,
  branchId NUMERIC NOT NULL,
  PRIMARY KEY (rawMaterialsId),
  FOREIGN KEY (branchId) REFERENCES Branches(branchId)
);

CREATE TABLE NutritionFacts
(
  nutritionFactId NUMERIC NOT NULL,
  bakedGoodsId NUMERIC NOT NULL,
  calories NUMERIC NOT NULL,
  carbs NUMERIC NOT NULL,
  protein NUMERIC NOT NULL,
  fat NUMERIC NOT NULL,
  sugar NUMERIC NOT NULL,
  PRIMARY KEY (nutritionFactId, bakedGoodsId),
  FOREIGN KEY (bakedGoodsId) REFERENCES BakedGoods(bakedGoodsId)
);

CREATE TABLE Roles
(
  roleId NUMERIC NOT NULL,
  name VARCHAR NOT NULL,
  description VARCHAR NOT NULL,
  PRIMARY KEY (roleId)
);

CREATE TABLE Recipe
(
  bakeGoodsId NUMERIC NOT NULL,
  rawMaterialsId NUMERIC NOT NULL,
  materialQuantity NUMERIC NOT NULL,
  PRIMARY KEY (bakeGoodsId, rawMaterialsId),
  FOREIGN KEY (bakeGoodsId) REFERENCES BakedGoods(bakedGoodsId),
  FOREIGN KEY (rawMaterialsId) REFERENCES RawMaterials(rawMaterialsId)
);

CREATE TABLE Employee
(
  employeeId NUMERIC NOT NULL,
  name VARCHAR NOT NULL,
  phone VARCHAR NOT NULL,
  email VARCHAR NOT NULL,
  dob DATE NOT NULL,
  branchId NUMERIC NOT NULL,
  roleId NUMERIC NOT NULL,
  PRIMARY KEY (employeeId),
  FOREIGN KEY (branchId) REFERENCES Branches(branchId),
  FOREIGN KEY (roleId) REFERENCES Roles(roleId)
);

CREATE TABLE ProductionLine
(
  productionLineId NUMERIC NOT NULL,
  productionDate DATE NOT NULL,
  quantity NUMERIC NOT NULL,
  bakeGoodsId NUMERIC NOT NULL,
  employeeId NUMERIC NOT NULL,
  PRIMARY KEY (productionLineId),
  FOREIGN KEY (bakeGoodsId) REFERENCES BakedGoods(bakedGoodsId),
  FOREIGN KEY (employeeId) REFERENCES Employee(employeeId)
);