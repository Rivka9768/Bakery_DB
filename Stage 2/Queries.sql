-- 8 Select Queries:


--ממוצע קלוריות לפי קטגוריה של מוצרי מאפה, ממויין מהכי משמין 1
SELECT c.name AS categoryName, ROUND(AVG(nf.calories), 2) AS avgCalories
FROM Categories c
JOIN BakedGoods bg ON c.categoryId = bg.categoryId
JOIN NutritionFacts nf ON bg.bakedGoodsId = nf.bakedGoodsId
GROUP BY c.name
ORDER BY avgCalories DESC;


-- 2 עובדים שהפיקו את הכמות הכי גדולה של מאפים בשנה מסוימת
SELECT e.name, SUM(pl.quantity) AS totalProduction
FROM Employee e
NATURAL JOIN ProductionLine pl
WHERE EXTRACT(YEAR FROM pl.productionDate) = 2024
GROUP BY e.name
ORDER BY totalProduction DESC;


-- 3 כל מוצרי המאפה עם יותר מ־20 גרם שומן או יותר מ־10 גרם סוכר
SELECT bg.name, nf.fat, nf.sugar
FROM BakedGoods bg
JOIN NutritionFacts nf ON bg.bakedGoodsId = nf.bakedGoodsId
WHERE nf.fat > 20 OR nf.sugar > 10
ORDER BY nf.fat DESC, nf.sugar DESC;


-- 4 כמות המאפים שיוצאו לכל סניף יחסית למספר העובדים בו
SELECT 
    b.branchId,
    b.location,
    SUM(pl.quantity) AS totalProduction,
    COUNT(DISTINCT e.employeeId) AS numEmployees,
    ROUND(SUM(pl.quantity) * 1.0 / COUNT(DISTINCT e.employeeId), 2) AS productionPerEmployee
FROM Branches b
NATURAL JOIN Employee e 
NATURAL JOIN ProductionLine pl 
GROUP BY b.branchId
HAVING COUNT(DISTINCT e.employeeId) > 0
ORDER BY productionPerEmployee ASC;


-- 5 המאפים עם מחיר גבוה יותר מהממוצע הכללי של מחירי כל המאפים
SELECT distinct bg.name, c.priceperweight
FROM BakedGoods bg
JOIN Categories c ON bg.categoryId = c.categoryId
WHERE c.priceperweight > (
	SELECT AVG(priceperweight)
	FROM BakedGoods bg2
	JOIN Categories c2 ON bg2.categoryId = c2.categoryId)
ORDER BY c.priceperweight DESC;


-- 6  מספר המאפים שיוצרו בכל חודש של 2024
SELECT 
    TO_CHAR(productionDate, 'Month') AS month_name,
    SUM(quantity) AS total_baked_goods
FROM 
    ProductionLine
WHERE 
    EXTRACT(YEAR FROM productionDate) = 2024
GROUP BY 
    TO_CHAR(productionDate, 'Month'),
    EXTRACT(MONTH FROM productionDate)
ORDER BY 
    EXTRACT(MONTH FROM productionDate);

-- 7 כמות עובדים לפי סניפים
SELECT 
    b.location AS branch_location,
    COUNT(e.employeeId) AS employee_count
FROM 
    Branches b
LEFT JOIN 
    Employee e ON b.branchId = e.branchId
GROUP BY 
    b.location
ORDER BY 
    employee_count DESC;

-- 8  כל המוצרים שפג תוקפם
SELECT 
    pl.productionLineId,
    pl.productionDate + (bg.lifetime * INTERVAL '1 day') AS expirationDate
FROM 
    ProductionLine pl
JOIN 
    BakedGoods bg ON pl.bakeGoodsId = bg.bakedGoodsId
WHERE 
    pl.productionDate + (bg.lifetime * INTERVAL '1 day') < CURRENT_DATE
ORDER BY 
    expirationDate DESC;




-- 3 Update Queries:


-- 1 הטרנזקציה מוסיפה 200 גרם סוכר למתכון של המוצר עם מזהה 52, מעדכנת בהתאם גם את תכולת הסוכר והקלוריות בטבלת הערכים התזונתיים, ושומרת את השינויים בצורה אטומית ומבוקרת.
BEGIN TRANSACTION;

-- 1. Recipe: add 200 g (0.20 kg) sugar
UPDATE Recipe
SET materialQuantity = materialQuantity + 0.20
WHERE bakeGoodsId = 52
AND RawMaterialsId = (
    SELECT RawMaterialsId
    FROM RawMaterials
    WHERE name = 'Sugar'
);

-- 2. NutritionFacts: +200 g sugar, +774 kcal
UPDATE NutritionFacts
SET sugar    = sugar    + 0.20,   -- in kg
    calories = calories + 774
WHERE bakedGoodsId = 52;

COMMIT;

-- 2 מכפיל את כל הערכים ב־pricePerWeight במכפיל מע"מ מעוגל (1.18 ÷ 1.17 ≈ 1.01), כך שכל המחירים בטבלת הקטגוריות משקפים את השינוי במע"מ מ-17% ל-18%.
UPDATE Categories
SET pricePerWeight = pricePerWeight * ROUND((1.18 / 1.17),2);

-- 3 מעדכן את כל העובדים עם תפקיד “Baker” בסניפים שבהם מספר העובדים בפועל קטֵן מהמינימום הנדרש, ומשנה להם את ה-roleId לתפקיד “Senior Baker” בתוך טרנזקציה אטומית.

BEGIN TRANSACTION;

UPDATE Employee
SET roleId = (
    SELECT roleId
    FROM Roles
    WHERE name = 'Senior Baker'
)
WHERE roleId = (
    SELECT roleId
    FROM Roles
    WHERE name = 'Baker'
)
AND branchId IN (
    SELECT B.branchId
    FROM Branches B
    JOIN Employee E ON B.branchId = E.branchId
    GROUP BY B.branchId, B.minAmountOfWorkers
    HAVING COUNT(E.employeeId) < B.minAmountOfWorkers
);

COMMIT;



-- 3 Delete Queries:



-- 1 מוחק את כל השורות שבהן תאריך הייצור (productionDate) הוא פחות מ־3 שנים מהיום.
DELETE FROM productionLine
WHERE productionDate < CURRENT_DATE - INTERVAL '3 years';

-- 2 מוחק שורות מ־bakedGoods עבורם אין כלל רשומה מתאימה ב־productionLine (כלומר, מוצרים שמעולם לא יוצרו).
delete from bakedGoods
using bakedGoods as b
left join productionLine p on p.bakeGoodsId = b.bakedGoodsId
where p.productionLineId is null;

-- 3 מבצעת מחיקה של חומרי גלם (raw materials) שמופיעים בטבלת RawMaterials אך לא נמצאים בשום מתכון בטבלת recipe.
DELETE FROM RawMaterials
WHERE RawMaterialsId NOT IN (
  SELECT r.RawMaterialsId
  FROM recipe r
  WHERE r.RawMaterialsId IS NOT NULL  -- Exclude NULLs
)







