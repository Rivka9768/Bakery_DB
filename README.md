# BAKERY - Project Report

## Table of Contents
[Phase 1](#phase-1)
1. [Cover Page](#cover-page)
2. [Introduction](#introduction)
3. [ERD and DSD Diagrams](#erd-and-dsd-diagrams)
4. [Data Entry Methods](#data-entry-methods)
5. [Backup and Restore](#backup-and-restore)

[Phase 2 - Queries](#phase-2-queries)
- [Select queries](#select-queries)
- [Update queries](#update-queries)
- [Delete queries](#delete-queries)
- [Rollback](#rollback)
- [Commit](#commit)
- [Constraints](#constraints)

[Phase 3](#phase-3)

[Phase 4](#phase-4)



## Cover Page
**Project Name:** Bakery_DB  
**Submitted by:** **Gila Kassab 330080821 &
                    Rivka Sorscher 567153394**


---
# Bakery Management Database
## **PHASE 1**
## Introduction
The **Bakery Management Database** is designed to efficiently manage information related to bakery branches, employees, baked goods, ingredients, and production processes. This system ensures smooth organization and tracking of essential details such as inventory management, employee roles, recipe ingredients, and daily production records.

## Purpose of the Database
This database serves as a structured and reliable solution for bakeries to:

- **Manage multiple branches**, including their locations and minimum required staff.
- **Track employee details**, linking them to specific roles and branches.
- **Store and categorize baked goods**, including nutritional information and allergen details.
- **Organize recipes**, mapping ingredients to baked goods with precise quantities.
- **Monitor inventory levels**, tracking raw materials and their distribution across branches.
- **Log daily production data**, recording what is produced, in what quantity, and by whom.

## Potential Use Cases
- **Bakery Managers** can monitor production levels, manage employees, and ensure ingredient availability.
- **Employees** can track their assigned tasks and manage production processes efficiently.
- **Suppliers** can check inventory levels to deliver raw materials as needed.
- **Customers** can receive accurate nutritional information and allergen warnings for baked goods.
- **Business Owners** can use the system for reporting, analysis, and decision-making to improve efficiency and reduce waste.

This structured database helps streamline bakery operations, ensuring efficient inventory management, optimized production, and smooth coordination between branches, employees, and suppliers. 🍞🥐


---

## ERD and DSD Diagrams
### Entity-Relationship Diagram (ERD)
![image](https://github.com/gilakassab/Bakery_0821_6010/blob/main/Stage%201/ERD(erd.plus).png?raw=true)


### Data Structure Diagram (DSD)
![image](https://github.com/gilakassab/Bakery_0821_6010/blob/main/Stage%201/DSD.png?raw=true)

---

## Data Entry Methods
The project includes foure different data entry methods to populate the database efficiently:

1. **Using Mockaroo for Data Generation**  
   - We utilized [Mockaroo](https://www.mockaroo.com/) to generate realistic sample data for our tables.  
   - The generated data was exported into a CSV file, which was later imported into the database.  
   - This method allowed us to quickly create large datasets that resemble real-world data.
**📸 Screenshots:**  
![Mockaroo Data Generation_Employee](https://github.com/gilakassab/Bakery_0821_6010/blob/main/Stage%201/MockarooFiles/EmployeeMacroo.png)
![Mockaroo Data Generation_ProductionLine](https://github.com/gilakassab/Bakery_0821_6010/blob/main/Stage%201/MockarooFiles/productionLineMacroo.png) 

2. **Writing SQL `INSERT` Commands**  
   - We manually wrote `INSERT` statements to add records to the database.  
   - This method ensured precise control over the data values and structure.  
   - It was particularly useful for inserting predefined records, such as employee roles and branch details.
**📸 Screenshot:**  
![SQL Insert Statements](https://github.com/gilakassab/Bakery_0821_6010/blob/main/Stage%201/InsertCommands/exampleOutput.png)

3. **CSV File Imports**  
   - Data was prepared in CSV format and imported into PostgreSQL.  
   - This method enabled bulk data insertion quickly and efficiently.  
   - We used PostgreSQL’s import feature within **pgAdmin** to load structured data into the tables.
**📸 Screenshot:**  
![CSV File Import](https://github.com/gilakassab/Bakery_0821_6010/blob/main/Stage%201/DataImportFiles/importScreenshot.png))  

4. **Python Script for Data Generation**  
   - We wrote a Python script to generate structured data and export it into a CSV file.  
   - The script created realistic values for the recipe table.  
   - This method allowed for automation and customization of the data generation process.
**📸 Screenshot:**  
![Python Script Data Generation](https://github.com/gilakassab/Bakery_0821_6010/blob/main/Stage%201/Programing/pythonScriptScreenshot.png)
     

Each method played a crucial role in ensuring that our database was populated efficiently and with meaningful data.

---

## Backup and Restore

### Backup Process
To ensure data safety, we performed a backup of our database using **pgAdmin**'s built-in backup functionality.  
The steps we followed:  
1. Right-clicked on the `BAKERY_DB` database in **pgAdmin**.  
2. Selected **Backup** from the context menu.  
3. Chose a file location and format (`.backup` file).  
4. Clicked **OK** to initiate the backup.  

#### Screenshot of Backup Process  
![Backup Screenshot](https://github.com/gilakassab/Bakery_0821_6010/blob/main/Stage%201/backup%26restore/backupScreenshot.png)  

---

### Restore Process
To restore the database, we used **pgAdmin**'s restore functionality:  
1. Right-clicked on `Databases` and selected **Create > Database** to create an empty `BAKERY_DB`.  
2. Right-clicked on the newly created `BAKERY_DB` and selected **Restore**.  
3. Selected the previously created `.backup` file.  
4. Clicked **Restore** to complete the process.  

#### Screenshot of Restore Process  
![Restore Screenshot](https://github.com/gilakassab/Bakery_0821_6010/blob/main/Stage%201/backup%26restore/restoreScreenshot.png) 

---

### Phase 2 Queries
### **SELECT QUERIES:**
**1. Average calorie count per baked goods category, ordered from highest to lowest**

השאילתה מאגדת נתונים משלוש טבלאות (Categories, BakedGoods ו-NutritionFacts) לצורך חישוב ממוצע הקלוריות עבור כל קטגוריית מוצרי מאפה.
היא מבצעת חיבורים בין הטבלאות באמצעות מפתחות זרים (categoryId ו-bakedGoodsId), מחשבת את ממוצע הקלוריות לכל קטגוריה (מעוגל לשני מקומות אחרי הנקודה), מקבצת את התוצאות לפי שם הקטגוריה (c.name), וממיינת את הפלט בסדר יורד לפי ערך ממוצע הקלוריות.

*שאילתא:*
```sql
SELECT c.name AS categoryName, ROUND(AVG(nf.calories), 2) AS avgCalories
FROM Categories c
JOIN BakedGoods bg ON c.categoryId = bg.categoryId
JOIN NutritionFacts nf ON bg.bakedGoodsId = nf.bakedGoodsId
GROUP BY c.name
ORDER BY avgCalories DESC;
```
*הרצה:*

![image](https://github.com/user-attachments/assets/4a61776c-59a8-49b3-a4dc-02843670fd68)
*תוצאה:*

![image](https://github.com/user-attachments/assets/c5904ff9-fa9c-4275-96a4-8e3e1e1e87bd)


**2. Total Production per Employee in 2024, Ordered by Output**

השאילתה מחברת את טבלאות Employee ו-ProductionLine באמצעות NATURAL JOIN כדי לחשב את מספר היחידות הכולל שהופק על ידי כל עובד במהלך שנת 2024.
הנתונים מקובצים לפי זהות העובד (e.EmployeeId), ומחושב סך הכולל של ההפקה (SUM(pl.quantity)) עבור כל עובד.
בסופו של תהליך, התוצאות ממוינות בסדר יורד לפי ערך ההפקה הכוללת, כך שהעובדים עם ההפקה הגבוהה ביותר מוצגים קודם.

*שאילתא:*
```sql
SELECT e.name, SUM(pl.quantity) AS totalProduction
FROM Employee e
NATURAL JOIN ProductionLine pl
WHERE EXTRACT(YEAR FROM pl.productionDate) = 2024
GROUP BY e.EmployeeId
ORDER BY totalProduction DESC;
```
*הרצה:*

![image](https://github.com/user-attachments/assets/a6868195-735e-4572-9464-89facbe3186b)

*תוצאה:*

![image](https://github.com/user-attachments/assets/0ca49e57-8108-412b-b671-eed34e1af8bc)


**3. High-Fat or High-Sugar Baked Goods, Ordered by Fat and Sugar Content**

השאילתה מחזירה את שם מוצר המאפה, כמות השומן וכמות הסוכר שלו, על ידי ביצוע חיבור (JOIN) בין הטבלאות BakedGoods ו-NutritionFacts על בסיס bakedGoodsId.
התוצאות מסוננות כך שיוצגו רק מוצרי מאפה שבהם כמות השומן גדולה מ-20 גרם או כמות הסוכר גדולה מ-10 גרם.
בסיום, הנתונים ממוינים תחילה לפי כמות השומן בסדר יורד, ולאחר מכן לפי כמות הסוכר בסדר יורד.

*שאילתא:*
```sql
SELECT bg.name, nf.fat, nf.sugar
FROM BakedGoods bg
JOIN NutritionFacts nf ON bg.bakedGoodsId = nf.bakedGoodsId
WHERE nf.fat > 20 OR nf.sugar > 10
ORDER BY nf.fat DESC, nf.sugar DESC;
```
*הרצה:*

![image](https://github.com/user-attachments/assets/7cc98e1f-05b7-47c7-9659-676f490cdc89)
*תוצאה:*

![image](https://github.com/user-attachments/assets/f1d96095-1cb3-4744-90b5-6df6516d053e)

**4. Branch Production Efficiency: Total Output, Number of Employees, and Average Production per Employee**

השאילתה מאחדת נתונים מהטבלאות Branches, Employee, ו-ProductionLine באמצעות NATURAL JOIN,
ומחזירה עבור כל סניף את המזהה (branchId), המיקום (location), סך כל יחידות הייצור (totalProduction), מספר העובדים הייחודיים (numEmployees), ואת ממוצע יחידות הייצור לעובד (productionPerEmployee).
התוצאות כוללות רק סניפים שבהם יש לפחות עובד אחד (באמצעות תנאי HAVING).
לבסוף, התוצאות ממוינות לפי ממוצע הייצור לעובד בסדר עולה (מהפחות יעילים ליותר יעילים).

*שאילתא:*
```sql
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
```
*הרצה:*

![image](https://github.com/user-attachments/assets/0e3c6c6a-2415-4be5-b719-49fc1fd9eb36)
*תוצאה:*

![image](https://github.com/user-attachments/assets/a7b1617f-c6c4-4497-b89d-8259ca254075)


**5. Baked Goods Priced Above Average per Weight, Ordered by Price**

השאילתה מאחדת נתונים מהטבלאות BakedGoods ו-Categories באמצעות JOIN, ומחזירה שמות ייחודיים של מוצרי מאפה (bg.name) ואת מחירם ליחידת משקל (c.priceperweight).
מוצרי המאפה שנבחרים הם רק אלו שמחירם ליחידת משקל גבוה מהממוצע המחושב לכלל מוצרי המאפה במערכת.
בסיום, התוצאות ממוינות בסדר יורד לפי מחיר ליחידת משקל, כך שהמוצרים היקרים יותר מוצגים ראשונים.

*שאילתא:*
```sql
SELECT distinct bg.name, c.priceperweight
FROM BakedGoods bg
JOIN Categories c ON bg.categoryId = c.categoryId
WHERE c.priceperweight > (
	SELECT AVG(priceperweight)
	FROM BakedGoods bg2
	JOIN Categories c2 ON bg2.categoryId = c2.categoryId)
ORDER BY c.priceperweight DESC;
```
*הרצה:*

![image](https://github.com/user-attachments/assets/92b8df4d-0d12-403b-8870-c3f8276a7c78)
*תוצאה:*

![image](https://github.com/user-attachments/assets/7ecb98a6-23b2-404e-a380-905eb7f7a54a)


**6. Total Baked Goods Produced Per Month in 2024, Ordered by Month**

השאילתה מחזירה את שם החודש (month_name) וסך כל יחידות הייצור של מוצרי המאפה (total_baked_goods) עבור כל חודש בשנת 2024, מתוך טבלת ProductionLine.
הנתונים מקובצים לפי חודש (כאשר החודש מנותב על פי הפורמט של TO_CHAR) וממוינים לפי סדר החודשים בשנה.
השאילתה מבטיחה שהתוצאות יכללו רק את השנה 2024 (באמצעות EXTRACT(YEAR FROM productionDate)).

*שאילתא:*

```sql
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
```
*הרצה:*

![image](https://github.com/user-attachments/assets/191cbb5b-a901-40bb-b54f-d8c0c5e701f9)

*תוצאה:*

![image](https://github.com/user-attachments/assets/1c9c65db-2601-43dd-ab62-615afb4fe99a)

**7. Employee Count by Branch Location, Ordered by Employee Count**


השאילתה מחזירה את המיקום של כל סניף (branch_location) ואת מספר העובדים בכל סניף (employee_count).
הנתונים נאספים בעזרת חיבור מסוג LEFT JOIN בין טבלאות Branches ו-Employee, כך שגם סניפים ללא עובדים ייכללו בתוצאה עם ערך של 0 לעובדים.
התוצאות ממוינות לפי מספר העובדים בסדר יורד, כך שסניפים עם יותר עובדים יופיעו קודם.

*שאילתא:*

```sql
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
```
*הרצה:*

![image](https://github.com/user-attachments/assets/be14daba-25d6-4872-b2e0-95eca932f6d2)

*תוצאה:*

![image](https://github.com/user-attachments/assets/2f0ec9f5-194b-49cd-9f50-3b76f30fe73d)

**8. Expired Baked Goods: Production Line ID and Expiration Date**

השאילתה מחזירה את מזהה קו הייצור (productionLineId) ואת תאריך התפוגה של מוצרי המאפה, שמחושב על ידי הוספת זמן חיי המוצר (לפי lifetime בטבלת BakedGoods) לתאריך הייצור (productionDate) מתוך טבלת ProductionLine.
השאילתה מסננת את התוצאות כך שמופיעים רק המוצרים שתאריך התפוגה שלהם עבר את התאריך הנוכחי (CURRENT_DATE).
התוצאות ממוינות בסדר יורד לפי תאריך התפוגה, כך שמוצרים שתוקפם פג קודם יופיעו ראשונים.

*שאילתא:*
```sql
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
```
*הרצה:*

![image](https://github.com/user-attachments/assets/ed6278e3-3bc9-4087-8c5a-e1c3d16f306c)
*תוצאה:*

![image](https://github.com/user-attachments/assets/df4caab3-91be-4c8a-bab8-9ab9486a0443)

### **UPDATE QUERIES:**

**1. Update Recipe and Nutrition Facts for Baked Goods**


הטרנזקציה הזאת מבצעת עדכונים בשתי טבלאות:
עדכון מתכון: כמות הסוכר במתכון עבור מוצר מאפה ספציפי (עם bakedGoodsId = 52) מתעדכנת ב-200 גרם (0.20 ק"ג). הסוכר מזוהה לפי RawMaterialsId, שנלקח מטבלת ה-RawMaterials.
עדכון ערך תזונתי: כמות הסוכר מתעדכנת ב-0.20 ק"ג, והקלוריות מתעדכנות ב-774 עבור אותו מוצר מאפה (עם bakedGoodsId = 52) בטבלת NutritionFacts.
הטרנזקציה מבטיחה עדכון מתואם של המתכון וערך תזונתי, לשמירה על עקביות בין הטבלאות הקשורות.

*שאילתא:*
```sql
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
```
*לפני העדכון:*

![image](https://github.com/user-attachments/assets/47e014f9-8fe3-4764-b5a9-ac39cf925ce6)

*הרצה:*

![image](https://github.com/user-attachments/assets/7b56c832-2dcf-474e-8d58-f1c56aabc1d7)

*תוצאה:*

![image](https://github.com/user-attachments/assets/e555c0bc-d2d2-4aa6-a912-d13e33107d88)


**2. Update Category Price Based on VAT Increase**

השאילתה מבצעת עדכון במחיר לכל קילוגרם של כל קטגוריה, בהתאם לשינוי במע"מ מ-17% ל-18%. מחירי הקטגוריות מעודכנים על ידי חישוב תוספת של המע"מ החדש (1.18) בהשוואה למע"מ הקודם (1.17), ומחיר לכל קילוגרם מוגדל לפי היחס בין 1.18 ל-1.17, כאשר התוצאה מעוגלת לשני מקומות אחרי הנקודה.

*שאילתא:*
```sql
UPDATE Categories
SET pricePerWeight = pricePerWeight * ROUND((1.18 / 1.17),2);
```
*לפני העדכון:*

![image](https://github.com/user-attachments/assets/c7b442e2-3537-4bd4-b285-a5c8596cb272)

*הרצה:*

![image](https://github.com/user-attachments/assets/e06d7e4c-4ae6-4601-bf0b-818e69db7b41)

*תוצאה:*

![image](https://github.com/user-attachments/assets/54cbf789-e0e4-46d6-840b-149c33c18bab)


**3. Update Bakers to Senior Bakers in Bnei Brak Branch Due to Staff Shortage**

השאילתה מעדכנת את כל העובדים בעלי תפקיד "אופה" בסניף בני ברק, והופכת אותם ל"סופר אופים" (Senior Bakers), זאת מאחר שמספר העובדים בסניף נמוך מהמינימום הנדרש (פחות מ-4 עובדים). הפעולה מתבצעת במסגרת טרנזקציה כדי להבטיח עקביות הנתונים.

*שאילתא:*
```sql
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
```
*לפני העדכון:*

![image](https://github.com/user-attachments/assets/3da82602-95d4-40f3-b84b-ad3d9bfad1c6)
![image](https://github.com/user-attachments/assets/ffe0ac05-c384-4667-bb51-1e208de890e4)



*הרצה:*

![image](https://github.com/user-attachments/assets/eac14fbd-c003-42c7-a79a-3f8ac6301626)

*תוצאה:*

![image](https://github.com/user-attachments/assets/4bcb4f20-f117-4053-b09c-9eb11601c7f6)


### **DELETE QUERIES:**

**1. Deleting old records from the production line**

שאילתה זו מוחקת רשומות מטבלת ProductionLine שבהן תאריך הייצור (productionDate) הוא לפני יותר משלוש שנים מהתאריך הנוכחי.
המטרה היא לנקות מידע ישן ולא רלוונטי ולשמור על גודל נתונים סביר.

*שאילתא:*
```sql
DELETE FROM productionLine
WHERE productionDate < CURRENT_DATE - INTERVAL '3 years';
```
*לפני המחיקה:*

![image](https://github.com/user-attachments/assets/38f83b81-7cbb-43cd-8e49-97fcc5771b8c)

*הרצה:*

![image](https://github.com/user-attachments/assets/e5b01f51-1f94-4be8-a7cc-518f344f3b58)

*תוצאה:*

![image](https://github.com/user-attachments/assets/a9bc3d15-bfbc-4d03-a722-2239b8b3e8b2)


**2. Delete Unlinked Baked Goods**

השאילתה מוחקת רשומות מטבלת bakedGoods שאין להן התאמה בטבלת productionLine, כלומר מוצרי מאפה שלא משויכים לאף קו ייצור.

*שאילתא:*
```sql
DELETE FROM bakedGoods
WHERE bakedGoodsId IN (
    SELECT b.bakedGoodsId
    FROM bakedGoods b
    LEFT JOIN productionLine p ON p.bakeGoodsId = b.bakedGoodsId
    WHERE p.productionLineId IS NULL
);
```
*לפני המחיקה:*

![image](https://github.com/user-attachments/assets/884852c6-ce44-4f8b-b2ff-d2b03cb3bbdb)

*הרצה:*

![image](https://github.com/user-attachments/assets/c466019b-5d0a-4c92-9b18-95b293961665)

*תוצאה:*

![image](https://github.com/user-attachments/assets/e16daba7-a3e5-4ab0-bdaa-7c2623b16f52)


**3. Deleting Raw Materials Not Used in Any Recipe**

שאילתה זו מוחקת את כל הרשומות מטבלת RawMaterials שחומר הגלם שלהן (RawMaterialsId) אינו מופיע בטבלת recipe. כלומר, נשמרים רק חומרי גלם שמקושרים לפחות למתכון אחד. השאילתה מתחשבת גם בכך שחומרי גלם עם ערך NULL לא ייכללו בבדיקה.

*שאילתא:*
```sql
DELETE FROM RawMaterials
WHERE RawMaterialsId NOT IN (
  SELECT r.RawMaterialsId
  FROM recipe r
  WHERE r.RawMaterialsId IS NOT NULL  -- Exclude NULLs
)
```
*לפני המחיקה:*

![image](https://github.com/user-attachments/assets/c809dd0f-21a6-419f-82d7-aa93f3fb8aba)

*הרצה:*

![image](https://github.com/user-attachments/assets/7a1d8ea6-bedc-4a47-923f-2ba8a10ba1f5)

*תוצאה:*

![image](https://github.com/user-attachments/assets/e9826edd-3151-4c10-9fec-c32126894bd0)


### Commit
פקודת INSERT כדי לבצע עדכון לבסיס הנתונים
*עדכון מסד הנתונים:*
```sql
BEGIN;

UPDATE employee
SET name = 'Rivka Sorscher'
WHERE employeeid = 1;
```

![image](https://github.com/user-attachments/assets/6219c3d4-4706-46e6-acde-372cccdf275c)

בדיקת הרשומה לפני COMMIT בטאב חדש שום דבר לא השתנה
```sql
SELECT * FROM employee WHERE employeeid = 1;
```
![image](https://github.com/user-attachments/assets/bf465871-c884-4b05-9e5f-285d96646773)

*ביצוע COMMIT:*
```sql
COMMIT;
```
![image](https://github.com/user-attachments/assets/088d05d5-76f8-4230-bbfd-4de13569278c)

בדיקה אחרי COMMIT גם בטאב אחר כדי לבדוק אם באמת נשמר לבסיס הנתונים
```sql
SELECT * FROM employee WHERE employeeid = 1;
```
![image](https://github.com/user-attachments/assets/710e0b0a-947b-4000-8b8b-1fbe15ebf80a)

אכן פעולת הCOMMIT עבדה ומסד הנתונים התעדכן!


### Rollback

פקודת SELECT על מנת לבדוק את מצב הנתונים - יש לנו 403 עובדים
```sql
SELECT * FROM Employee;
```
![image](https://github.com/user-attachments/assets/2fae84b4-5f98-4e41-892b-60fdf3411ddb)

פקודת INSERT כדי לבצע עדכון לבסיס הנתונים
*עדכון מסד הנתונים:*
```sql
BEGIN;

INSERT INTO employee (employeeid, name, phone, email, dob, branchid, roleid)
VALUES
(404, 'Gila Kassab', '054-1234567', 'Gila.Kassab@gmail.com', '2003-05-15', 1, 2);
```
![image](https://github.com/user-attachments/assets/c81a6f9e-134d-4473-b229-bfcafce61ff8)

טבלת העובדים לאחר ההכנסה של עובד נוסף
```sql
SELECT * FROM Employee;
```
![image](https://github.com/user-attachments/assets/4c38c621-97d1-4ba9-bee9-646ea2b24e1c)

*ביצוע הrollback:*
```sql
rollback;
```
![image](https://github.com/user-attachments/assets/4861464a-b95d-461b-8075-08396713226e)

הנתונים אכן חזרו לקדמותם - פקודת הrollback אכן עבדה!
```sql
SELECT * FROM Employee;
```
![image](https://github.com/user-attachments/assets/b706ca4e-09ca-4c6d-a172-ae5542f41074)


### **Constraints:**

**1. Ensures no two employees share the same email (employee.email)**

*אילוץ:*

```sql
ALTER TABLE employee
ADD CONSTRAINT unique_employee_email UNIQUE (email);
```
*הרצה:*

![image](https://github.com/user-attachments/assets/3f5e756e-b3b8-4a84-b6b9-27ab34a2ba95)

*פקודה הסותרת את האילוץ:*
```sql
INSERT INTO employee (employeeid, name, phone, email, dob, branchid, roleid)
VALUES
(404, 'Maria Sharon', '054-1234567', 'david.cohen@example.com', '1990-05-15', 1, 2);
```

*תוצאת הרצת פקודה הסותרת את האילוץ:*

![image](https://github.com/user-attachments/assets/94c88d18-8c67-4b0b-a2f7-f148fcf3300a)



**2. Enforces that every category’s price per weight (Categories.pricePerWeight) is greater than 0**

*אילוץ:*

```sql
ALTER TABLE Categories
ADD CONSTRAINT chk_valid_price CHECK (pricePerWeight > 0);
```
*הרצה:*

![image](https://github.com/user-attachments/assets/77cec9de-4ba9-4657-81fe-1e20b119b0f3)

*פקודה הסותרת את האילוץ:*
```sql
INSERT INTO Categories (CategoryId, name, description, pricePerWeight) VALUES
(11, 'Drinks', 'Ices and drinks', -1);
```
*תוצאת הרצת פקודה הסותרת את האילוץ:*

![image](https://github.com/user-attachments/assets/6c55498e-357d-4ff1-8cde-d7e434018e86)


**3. makes the production line’s date (productionLine.productionDate) default to the current date if none is provided**

*אילוץ:*

```sql
ALTER TABLE productionLine
ALTER COLUMN productionDate SET DEFAULT CURRENT_DATE;
```
*הרצה:*

![image](https://github.com/user-attachments/assets/4cbae51a-307a-4e8e-a045-0008ecd4e900)

*פקודת INSERT:*
```sql
INSERT INTO productionLine (productionlineid, quantity, bakegoodsid, employeeid) 
VALUES 
(404, 150, 10, 144);
```
*תוצאת פקודת הINSERT העובדת עם האילוץ:*

![image](https://github.com/user-attachments/assets/57804ec3-33c7-46b3-9250-b83f0740aa50)

# PHASE 3

## INTEGRATION WITH CLOTHING STORE DATABASE

בשלב זה של הפרויקט ביצענו מיזוג בין שני בסיסי נתונים קיימים:

1. בסיס נתונים של המאפייה
2. בסיס נתונים של חנות הבגדים

---

### שלבים שביצענו

* קיבלנו קובץ גיבוי (Backup) של בסיס הנתונים של חנות בגדים בפורמט SQL.
* על סמך פקודות יצירת הטבלאות (CREATE TABLE) ופקודות מפתחות זרים (FOREIGN KEY) יצרנו ב erdPlus דיאגרמת DSD.

*דיאגרמת הDSD:*

![image (34)](https://github.com/user-attachments/assets/162b0c73-7778-4bbc-989e-b430ff893f86)

* מתוך דיאגרמת ה-DSD יצרנו דיאגרמת ERD לפי הקשרים שהוגדרו באמצעות מפתחות זרים.

  
*דיאגרמת הERD:*
![image (35)](https://github.com/user-attachments/assets/cccb92f7-860c-46a2-a048-cc39b0c2f6ba)

בהמשך:

* מיזגנו את שתי הדיאגרמות על מנת ליצור בסיס נתונים מאוחד.
* הוספנו שתי ישויות חדשות:
  * ישות Department – לסיווג בין מחלקת מוצרי מאפייה למחלקת בגדים.
  * ישות Product – לשילוב בין הישויות GARMENT ו-BAKEDGOODS.
* מיזגנו בין טבלת העובדים Employee של שתי המערכות.
  
*דיאגרמת הERD המשולבת:*

 ![image (38)](https://github.com/user-attachments/assets/032f2491-8a20-46ba-b632-3e75fae6fb36)
 
* כעת מתוך הERD פלוס המרנו את הERD המשולב לטבלת DSD.

*דיאגרמת הDSD המשולבת:*

![image (39)](https://github.com/user-attachments/assets/5b22b5b1-cd43-4244-9e5a-482228e9ed71)


יצרנו בסיס נתונים חדש בשם INTEGRATION: 
* טענו לתוכו את הגיבוי של המאפייה.
* טענו קובץ SQL נוסף של חנות הבגדים לאחר שינוי שם הטבלה `EMPLOYEE` ל-`EMPLOYEE_1` כדי למנוע התנגשות עם טבלה קיימת.

  ![image](https://github.com/user-attachments/assets/b868272f-1763-42eb-b1c6-269c71513364)

פקודת הטעינה:

```bash
psql --host=localhost --port=5432 --username=postgres --dbname=CLOTHES_DB --file="C:\Users\RIVKA\Downloads\dress_Backup#29.3.25.sql"
```

### יצירת טבלאות חדשות
* טבלת עזר לסיווג עובדים ומוצרים: DEPARTMENT
* טבלת מוצרים מאוחדת: PRODUCTS

### מיזוג נתוני עובדים
* הוספת עמודת department\_id לטבלאות העובדים:

```sql
ALTER TABLE employee
ADD COLUMN department_id NUMERIC 
```

![image (20) (1)](https://github.com/user-attachments/assets/e517c1c2-f438-46c1-bca8-0d413deb269c)


```sql
ALTER TABLE employee_1
ADD COLUMN department_id NUMERIC 
```

![image (19) (1)](https://github.com/user-attachments/assets/06d88eb8-dba8-492e-8b9d-6a704629242f)

* עדכון ערכים בעמודת department\_id:

```sql
UPDATE employee
SET department_id = 1;
```

![image (18) (1)](https://github.com/user-attachments/assets/436f79c5-e926-4bb4-aef0-e9a06ba1ec53)


```sql
UPDATE employee_1
SET department_id = 2;
```

* התאמת מבנה הטבלאות:

```sql
ALTER TABLE employee
ADD COLUMN date_join DATE NULL,
ADD COLUMN salary NUMERIC NULL;
```

![image (21) (1)](https://github.com/user-attachments/assets/a569ec2e-c6da-476e-b9d3-c26ab94592cf)

* הסרת הגדרות NOT NULL מעמודות קיימות בטבלת employee.

לפני:

![image (15) (1)](https://github.com/user-attachments/assets/975b4800-16d5-45b5-897b-231a106ad3cb)
אחרי:


![image](https://github.com/user-attachments/assets/8a8860b5-2c58-4aa5-b928-92b22ddca2cc)

* עדכון מזהי עובדים בטבלה employee\_1:

```sql
UPDATE employee_1
SET employee_id = employee_id + 403
```

![image (14) (1)](https://github.com/user-attachments/assets/f59e223b-a37a-45bd-aedc-9a20e5cd1d9f)

* עדכון מזהי עובדים בטבלה customer\_order כיוון שזה מפתח זר לטבלת העובדים ( המפתח הזר בוטל לפני השינויים שנעשו בטבלת employee\_1 ):

```sql
UPDATE customer_order
SET employee_id = employee_id + 403
```

![image](https://github.com/user-attachments/assets/7679ef72-88b9-44a8-86f6-a9b15a76ede6)

* מיזוג הנתונים בפועל:

```sql
INSERT INTO employee (employeeid, name, email ,date_join, salary,department_id)
SELECT employee_id, employee_name, employee_mail, date_join, salary, department_id FROM employee_1;
```

![image (13) (1)](https://github.com/user-attachments/assets/103ca777-76a8-484f-a281-75119d9efb8d)


קיבלנו טבלה משולבת עם 803 שורות – פי שניים מהנתונים המקוריים.

![image (12) (1)](https://github.com/user-attachments/assets/69f822f3-ff53-44e3-811e-32aa465bcfc2)

* עדכון ה foreign key בטבלת ה costomer_order להיות מקושר לטבלת employee:

![image](https://github.com/user-attachments/assets/a85614bc-2d30-4cf5-b08f-4e66dc6c3da8)

* מחיקת הטבלה employee\_1 לאחר סיום המיזוג.

### מיזוג טבלאות המוצרים – GARMENT ו-BAKEDGOODS

* יצירת טבלה PRODUCTS חדשה הכוללת את השדות משתי הטבלאות.
* הגדרת מזהה מוצר רץ (SERIAL):

```sql
ALTER TABLE products
ADD COLUMN productid SERIAL PRIMARY KEY;
```

![image (11) (1)](https://github.com/user-attachments/assets/85ee3638-1361-455d-8831-b9f52e682960)

* הוספת עמודת department\_id לשתי הטבלאות המקוריות:

```sql
ALTER TABLE bakedgoods
ADD COLUMN department_id NUMERIC;
```

![image (10) (1)](https://github.com/user-attachments/assets/91229cf1-2f89-4bba-986a-7d9560836690)


```sql
ALTER TABLE garment
ADD COLUMN department_id NUMERIC;
```

![image (9) (1)](https://github.com/user-attachments/assets/930b4a7a-d7e3-439b-b996-072cae1d4bad)

* עדכון ערכי department\_id:

```sql
UPDATE bakedgoods
SET department_id = 1;
```

![image (8) (1)](https://github.com/user-attachments/assets/e73e59a0-2ee4-4d0b-930d-e396af746a59)


```sql
UPDATE garment
SET department_id = 2;
```

![image (7) (1)](https://github.com/user-attachments/assets/c257e9d3-72ca-4f2f-b1ad-a1b66a76434e)

* הכנסת נתונים ל-`PRODUCTS`:

```sql
INSERT INTO products (bakedgoodsid, bakedgoods_name, bakedgoods_lifetime , bakedgoods_allergeninfo, bakedgoods_categ_id, department_id)
SELECT *
FROM bakedgoods;
```

![image (4) (1)](https://github.com/user-attachments/assets/d5945b91-1efe-4e1e-99d2-11506addf3bb)

```sql
INSERT INTO products (garment_name, garment_quantity_in_stock, garment_price , garment_id, garment_supplierID, garment_categoryId, department_id)
SELECT *
FROM garment;
```

![image (5) (1)](https://github.com/user-attachments/assets/58ad4dc3-cb04-4411-81bd-860e8811485d)

תוצאת הכנסת הנתונים:
![image (2) (2)](https://github.com/user-attachments/assets/643ccc8d-44b7-4f8f-b8e4-4dec18969a77)


* עדכון קשרים (Foreign Keys):

  * הגדרת bakedgoodsid ו-garmentid כ-UNIQUE.על מנת שיוכלו להיות FOREIGN KEY לטבלאות שונות.
    
![{9AEC67A2-D412-47D0-A1DA-FCE24C7777CF}](https://github.com/user-attachments/assets/88cb607a-550e-4da8-b154-761db3476616)

  * עדכון טבלאות להפניה אל/מ products במקום אל/מ הטבלאות המקוריות.

![{3145935F-1669-4041-9540-45673DE18E88}](https://github.com/user-attachments/assets/0b387a0d-e5de-467f-a537-a7a71917e68c)
    
![{55B17870-8949-4A30-BFE3-FE5E22420C7A}](https://github.com/user-attachments/assets/77064df6-02a9-47fd-a058-b5ddc331c2f4)

![{34F57986-D695-416F-956B-F3357B10843E}](https://github.com/user-attachments/assets/67ae54a2-2c6c-4061-a132-a464a18af0a9)

![image](https://github.com/user-attachments/assets/4b7a048c-8fa0-4bf4-8208-307d298324e6)

![{A58CB85D-EC8D-42B4-B19D-46C951EAE437}](https://github.com/user-attachments/assets/99831e76-b547-4184-9025-08bcb273cdf7)

* מחיקת הטבלאות הישנות לאחר אימות הקשרים והנתונים.

### Views – מבטים

* מבט על חנות הבגדים:

```sql
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
```

![image](https://github.com/user-attachments/assets/51d407dd-6b50-4c52-8b3b-c1460a1671b4)

* שליפת נתונים מהמבט:
  
```sql
select * from View_ClothingCustomersOrders;
```
![{7C2132E2-0DBF-4102-AF30-06085236C1C8}](https://github.com/user-attachments/assets/dcdf5509-15b6-45c8-b02a-adeee0119ba4)

* שאילתות על המבט:

  *שאילתא 1 -  מאפשרת ניתוח של אילו פריטים הוזמנו על ידי כל לקוח (לפי מזהה), וכמה מכל פריט.*
  
```sql
SELECT 
    customer_id,
    garment_name,
    SUM(amount) AS total_amount_ordered
FROM View_ClothingCustomersOrders
GROUP BY customer_id, garment_name;
```

![{FAC56667-BCF2-4C43-9B1B-3B4D54DABC8B}](https://github.com/user-attachments/assets/534a0fc8-5c75-4394-a54e-599e41136487)

  *שאילתא 2 - מציגה את ההזמנה האחרונה של כל לקוח – ניתוח חשוב לעדכניות ההתקשרות עם הלקוח, או למשל כדי להחליט מתי לפנות אליו שוב.*

  
```sql
SELECT v.*
FROM View_ClothingCustomersOrders v
WHERE order_date = (
    SELECT MAX(order_date)
    FROM View_ClothingCustomersOrders v2
    WHERE v2.customer_id = v.customer_id
);
```

![{3B23E034-F1ED-4BF2-9456-893A4E6A7EF5}](https://github.com/user-attachments/assets/c130318d-3c02-4a4b-9846-d0099590aafb)

* מבט על המאפייה:

```sql
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
```

![{75CB1307-1558-4960-9B4C-EA38AA628BDD}](https://github.com/user-attachments/assets/dc831894-8d48-44e2-9260-9379c9332fbf)

* שליפת נתונים מהמבט:

```sql
select * from View_BakeryEmployeeProduction;
```

![{2DCD1694-8860-4154-B243-E054CFA58082}](https://github.com/user-attachments/assets/bc7c2998-add4-4196-86d8-2cf2a2b507bb)

* שאילתות על המבט:

  *שאילתא 1 - מזהה את העובדים היצרניים ביותר – כלי להערכת עובדים או לתמרוץ.*

```sql
SELECT 
    employeeId,
    employee_name,
    SUM(quantity) AS total_produced
FROM View_BakeryEmployeeProduction
where quantity is not null
GROUP BY employeeId, employee_name
ORDER BY total_produced DESC;
```
![{5A44BAB2-0323-4F5A-852A-77A9CC0AFFFA}](https://github.com/user-attachments/assets/bfe317d2-42a0-49c1-80de-be0e11cceb60)


  *שאילתא 2 - כמה עוגות יוצרו בכל סניף - מאפשר לראות איזה סניף מייצר יותר (מועיל לתכנון לוגיסטי, ניהול מלאי והחלטות על תגבור).*

  ```sql
SELECT 
    branch_location,
    SUM(quantity) AS total_quantity
FROM View_BakeryEmployeeProduction
where quantity is not null
GROUP BY branch_location;
```
![image](https://github.com/user-attachments/assets/830c92f0-c7cf-4444-92ff-60cd7fe4d020)

  
---
# PHASE 4


# שלב 4 – חזרה לעבודה עם בסיס הנתונים של המאפייה

בשלב זה אנו חוזרים לעבוד עם בסיס הנתונים המקורי של **המאפייה**, ומתמקדים בתכנות מתקדם באמצעות **PL/pgSQL**.

מטרת שלב זה היא לתרגל וליישם תכנות ב־PL/pgSQL, כולל שימוש בפונקציות, פרוצדורות, טריגרים, לולאות, תנאים וחריגות.

המערכת נבנית בשלושה חלקים עיקריים:

- **ניהול משמרות** – כולל יצירת טבלאות רלוונטיות, טריגרים, פונקציות, פרוצדורות ותוכנית ראשית.
- **לוגים על פעולות CRUD** – מנגנון כללי לרישום שינויים בכל טבלה.

## תוכן העניינים

### ⚙️ [ניהול משמרות](#ניהול-משמרות)
- [1. יצירת טבלת Shifts](#1-יצירת-טבלת-shifts)
- [2. יצירת טבלת EmployeeShifts](#2-טבלת-employeeshifts)
- [3. פונקציה get_unassigned_employees](#3-פונקציה-get_unassigned_employees)
- [4. טריגר: הודעה על שיבוץ עובד](#4-טריגר-הודעה-על-שיבוץ-עובד)
- [5. פרוצדורה assign_employees_to_shift](#5-פרוצדורה-assign_employees_to_shift)
- [6. תוכנית ראשית](#6-תוכנית-ראשית)

### 📝 [לוגים על פעולות CRUD](#לוגים-על-פעולות-crud)
- [7. יצירת טבלת לוג כללית LogChanges](#7-יצירת-טבלת-לוג-כללית-logchanges)
- [8. פונקציית טריגר log_changes_function](#8-פונקציית-טריגר-log_changes_function)
- [9. טריגרים לכל טבלה](#9-טריגרים-לכל-טבלה)
- [10. בדיקה: הכנסת עובד חדש](#10-בדיקה-הכנסת-עובד-חדש)

- 

- ### 📝 [ניהול ייצור של מאפים וטריגר](#ניהול_מאפים)
- [12. פונקציה get_materials_summary_for_product](#12- פונקציה get_materials_summary_for_product)
- [13.פרוצדורה produce_batch](#8-פונקציית-טריגר-log_changes_function)
- [14.טריגר log_allergen_warning](#9-טריגרים-לכל-טבלה)
- [15. תוכנית ראשית](#10-בדיקה-הכנסת-עובד-חדש)

# ניהול משמרות

## 1. יצירת טבלת Shifts

### תיאור:

יצירת טבלה חדשה בשם `Shifts` הכוללת מזהה משמרת, מזהה סניף, תאריך וזמן (בוקר / ערב), עם קשר זר לטבלת Branches.

```sql
CREATE TABLE Shifts (
  shiftId SERIAL PRIMARY KEY,
  branchId NUMERIC NOT NULL,
  shiftDate DATE NOT NULL,
  shiftTime VARCHAR NOT NULL CHECK (shiftTime IN ('morning', ‘evening’)),
  FOREIGN KEY (branchId) REFERENCES Branches(branchId)
);
```

### תמונת מסך של הרצת פקודת הCREATE:

![unnamed](https://github.com/user-attachments/assets/f48a8609-5b7e-4023-9a3a-b2010f470afc)

---

## 2.יצירת טבלת EmployeeShifts

### תיאור:

טבלת קישור בין עובדים למשמרות. כל רשומה מייצגת שיבוץ של עובד למשמרת מסוימת.

```sql
CREATE TABLE EmployeeShifts (
  employeeId NUMERIC NOT NULL,
  shiftId NUMERIC NOT NULL,
  PRIMARY KEY (employeeId, shiftId),
  FOREIGN KEY (employeeId) REFERENCES Employee(employeeId),
  FOREIGN KEY (shiftId) REFERENCES Shifts(shiftId)
);
```

### תמונת מסך של הרצת פקודת הCREATE:


<img width="550" alt="unnamed" src="https://github.com/user-attachments/assets/7c114f55-b50e-40d0-a578-bf66b9552eca" />

---

## 3. פונקציה get\_unassigned\_employees

### תיאור:

מאחזרת עובדים שעדיין לא שובצו למשמרת בסניף, תאריך ושעה מסוימים לפי תפקיד.

```sql
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
```

### תמונת מסך של הרצת הפונקציה:


![unnamed](https://github.com/user-attachments/assets/f8d96786-f1c1-4fa0-8081-f1b0a492cf36)

---

## 4. טריגר: הודעה על שיבוץ עובד

### תיאור:

טריגר שמפעיל הודעת מערכת (RAISE NOTICE) כאשר עובד שובץ למשמרת.

```sql
CREATE OR REPLACE FUNCTION trg_notify_employee_assigned()
RETURNS TRIGGER AS
$$
DECLARE
  empName VARCHAR;
BEGIN
  SELECT name INTO empName FROM Employee WHERE employeeId = NEW.employeeId;
  RAISE NOTICE 'Employee % assigned to shift %', empName, NEW.shiftId;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER notify_employee_assigned
AFTER INSERT ON EmployeeShifts
FOR EACH ROW
EXECUTE FUNCTION trg_notify_employee_assigned();
```

### תמונת מסך של הרצת הטריגר:


![unnamed](https://github.com/user-attachments/assets/5e5b3ca6-e233-417e-9153-b574d3ca9c93)

---

## 5. פרוצדורה assign\_employees\_to\_shift

### תיאור:

פרוצדורה אשר יוצרת משמרת ומשבצת לה את כמות העובדים המינימלית הנדרשת לפי הגדרות הסניף.

```sql
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
```

### תמונת מסך של הרצת הפרוצדורה:


![unnamed](https://github.com/user-attachments/assets/6d839dfa-9364-4972-9ab4-3edb48e57ac9)

---

## 6. תוכנית ראשית

### תיאור:

תכנית ראשית המשתמשת ב DO block שמדגים שימוש בפונקציה ובפרוצדורה ומציג עובדים זמינים, ואז משבץ אותם למשמרת חדשה.

```sql
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
```

### תמונת מסך של הרצת התוכנית הראשית:


![unnamed](https://github.com/user-attachments/assets/367b4329-a3a7-445e-998c-eea69c7e6ea4)


### תמונות מסך של תוצאות התוכנית - הפרוצדורה והפונקציה:

<img width="331" alt="unnamed" src="https://github.com/user-attachments/assets/ad038cd6-c136-4179-8e1b-d978f27ca997" />

<img width="223" alt="unnamed" src="https://github.com/user-attachments/assets/12d2d7d9-fa16-4d55-bde1-ebfd8d86866e" />

התוכנית זרקה חריגה מהפרוצדורה:

<img width="614" alt="image" src="https://github.com/user-attachments/assets/59c4b45f-980b-486e-b706-140458835438" />


---
# לוגים על פעולות CRUD

רישום אוטומטי של שינויים במסד הנתונים חשוב לשמירה על עקבות דיגיטליים – ניתן לדעת מי ביצע שינוי, מתי ומה בדיוק השתנה. לוגים מאפשרים לאתר תקלות ולשחזר מידע במקרה של שגיאה, ותורמים לעמידה בדרישות אבטחת מידע וביקורת.



## 7. יצירת טבלת לוג כללית LogChanges

### תיאור:

טבלה אשר רושמת שינויים (INSERT/UPDATE/DELETE) בכל טבלה באמצעות טריגרים.

```sql
CREATE TABLE LogChanges (
  logId SERIAL PRIMARY KEY,
  tableName VARCHAR NOT NULL,
  operation VARCHAR NOT NULL, -- INSERT, UPDATE, DELETE
  changedBy VARCHAR DEFAULT CURRENT_USER,
  changeTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  oldData JSONB,
  newData JSONB
);
```

### תמונת מסך של הרצת פקודת הCREATE:

<img width="548" alt="unnamed" src="https://github.com/user-attachments/assets/79cb03f9-7d9d-4460-9e89-e68476787df3" />

---

## 8. פונקציית טריגר log\_changes\_function

### תיאור:

פונקציה הנקראת מטריגר, המכניסה את נתוני השינוי לטבלת LogChanges בפורמט JSON.

```sql
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
```

### תמונת מסך של הרצת פונקציית הטריגר:

<img width="473" alt="unnamed" src="https://github.com/user-attachments/assets/10e0c429-802a-48af-a414-2fcd4b4cad55" />

---

## 9. טריגרים לכל טבלה

### תיאור:

כל טבלה מקבלת טריגר אשר מפעיל את `log_changes_function` על פעולות INSERT/UPDATE/DELETE.

```sql
-- Branches
CREATE TRIGGER log_branches_trigger
AFTER INSERT OR UPDATE OR DELETE ON Branches
FOR EACH ROW EXECUTE FUNCTION log_changes_function();
```
<img width="438" alt="unnamed" src="https://github.com/user-attachments/assets/df029a23-69fa-44bc-85c2-687b170a7070" />


```sql
-- Categories
CREATE TRIGGER log_categories_trigger
AFTER INSERT OR UPDATE OR DELETE ON Categories
FOR EACH ROW EXECUTE FUNCTION log_changes_function();
```
<img width="456" alt="unnamed" src="https://github.com/user-attachments/assets/845a56a3-9b89-4aeb-9948-6c0e9b55c2c5" />


```sql
-- BakedGoods
CREATE TRIGGER log_bakedgoods_trigger
AFTER INSERT OR UPDATE OR DELETE ON BakedGoods
FOR EACH ROW EXECUTE FUNCTION log_changes_function();
```
<img width="459" alt="unnamed" src="https://github.com/user-attachments/assets/1103d6de-7aeb-46fb-85bf-b6064f8fe131" />


```sql
-- RawMaterials
CREATE TRIGGER log_rawmaterials_trigger
AFTER INSERT OR UPDATE OR DELETE ON RawMaterials
FOR EACH ROW EXECUTE FUNCTION log_changes_function();
```
<img width="439" alt="unnamed" src="https://github.com/user-attachments/assets/0de237b7-f9de-459f-8e18-4914cf0d777b" />


```sql
-- NutritionFacts
CREATE TRIGGER log_nutritionfacts_trigger
AFTER INSERT OR UPDATE OR DELETE ON NutritionFacts
FOR EACH ROW EXECUTE FUNCTION log_changes_function();
```
<img width="473" alt="unnamed" src="https://github.com/user-attachments/assets/d83764f1-8362-4754-8c2c-62cc7d188309" />



```sql
-- Roles
CREATE TRIGGER log_roles_trigger
AFTER INSERT OR UPDATE OR DELETE ON Roles
FOR EACH ROW EXECUTE FUNCTION log_changes_function();
```
<img width="440" alt="unnamed" src="https://github.com/user-attachments/assets/594a81ef-0ead-4631-9e4c-d5e36d682b90" />



```sql
-- Recipe
CREATE TRIGGER log_recipe_trigger
AFTER INSERT OR UPDATE OR DELETE ON Recipe
FOR EACH ROW EXECUTE FUNCTION log_changes_function();
```
<img width="475" alt="unnamed" src="https://github.com/user-attachments/assets/77a0ab4d-45f3-4189-be9d-651db70c6eed" />


```sql
-- Employee
CREATE TRIGGER log_employee_trigger
AFTER INSERT OR UPDATE OR DELETE ON Employee
FOR EACH ROW EXECUTE FUNCTION log_changes_function();
```
<img width="375" alt="unnamed" src="https://github.com/user-attachments/assets/f521ca7c-cda1-4ff7-b13b-8c8181af4025" />


```sql
-- ProductionLine
CREATE TRIGGER log_productionline_trigger
AFTER INSERT OR UPDATE OR DELETE ON ProductionLine
FOR EACH ROW EXECUTE FUNCTION log_changes_function();
```
<img width="456" alt="image" src="https://github.com/user-attachments/assets/75efebd0-94ce-4e89-a937-26edaee81baf" />


```sql
-- Shifts 
CREATE TRIGGER log_shifts_trigger
AFTER INSERT OR UPDATE OR DELETE ON Shifts
FOR EACH ROW EXECUTE FUNCTION log_changes_function();
```
<img width="387" alt="unnamed" src="https://github.com/user-attachments/assets/b2d514cd-9f9c-4f10-9bfe-2a4acbf9337b" />


```sql
-- employeeShifts 
CREATE TRIGGER log_employeeshifts_trigger
AFTER INSERT OR UPDATE OR DELETE ON Employeeshifts
FOR EACH ROW EXECUTE FUNCTION log_changes_function();
```
<img width="400" alt="unnamed" src="https://github.com/user-attachments/assets/580b6886-2356-416b-bf24-085bbaaa1250" />

---

## 11. בדיקה: הכנסת עובד חדש

### תיאור:

נבדקה פעולת INSERT בטבלת Employee עם מעקב אחרי יצירת שורת לוג.

```sql
INSERT INTO Employee (employeeId, name, phone, email, dob, branchId, roleId)
VALUES (500, 'Test Tester', '050-0000000', 'test@example.com', '1995-01-01', 1, 2);
```

### תמונות מסך של ההרצה והתוצאה:

<img width="572" alt="unnamed" src="https://github.com/user-attachments/assets/76cc2611-3d82-4f32-96af-b9c5e4d45cd9" />

<img width="778" alt="unnamed" src="https://github.com/user-attachments/assets/28bd1764-68e2-4066-a301-dd3b92b29829" />

### 12 - פונקציה get_materials_summary_for_product
הפונקציה נועדה להחזיר דו"ח על מצב חומרי הגלם הדרושים לייצור מוצר אפוי מסוים, לפי מזהה (baked_id). היא בודקת האם יש מספיק מלאי זמין לכל חומר גלם שנדרש לפי המתכון, ומחזירה טבלה זמנית הכוללת את שמות החומרים, הכמות הנדרשת, הכמות הזמינה, ומצבם ("OK" אם יש מספיק, "LOW" אם חסר).

### קוד הפונקציה:
```sql
CREATE OR REPLACE FUNCTION get_materials_summary_for_product(baked_id INT)
RETURNS refcursor AS $$
DECLARE
    ref refcursor;
    rec RECORD;
    available_qty NUMERIC;
    temp_table TEXT := 'temp_material_status';
BEGIN
    
    EXECUTE format('DROP TABLE IF EXISTS %I', temp_table);
    EXECUTE format('CREATE TEMP TABLE %I (name TEXT, required NUMERIC, available NUMERIC, status TEXT)', temp_table);

    FOR rec IN
        SELECT rm.name, r.materialQuantity AS required, rm.quantity AS available
        FROM Recipe r
        JOIN RawMaterials rm ON r.RawMaterialsId = rm.RawMaterialsId
        WHERE r.bakeGoodsId = baked_id
    LOOP
        INSERT INTO temp_material_status(name, required, available, status)
        VALUES (
            rec.name,
            rec.required,
            rec.available,
            CASE
                WHEN rec.available >= rec.required THEN 'OK'
                ELSE 'LOW'
            END
        );
    END LOOP;

    OPEN ref FOR EXECUTE format('SELECT * FROM %I', temp_table);
    RETURN ref;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error: %', SQLERRM;
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;
```

### יצירת פונקציה:

![image](https://github.com/user-attachments/assets/097f26b3-9c40-44b2-b3ef-a37c601f1f3e)

### הרצה:

![image](https://github.com/user-attachments/assets/914618ab-4091-40aa-9e59-454823fd89fe)


### דוגמא להרצה שנכשלה:

![image](https://github.com/user-attachments/assets/6280a1a4-48e2-4781-ba59-9562e2df690a)



### 13 - פרוצדורה produce_batch :

הפרוצדורה מבצעת הפקה של סדרת ייצור (Batch) של מוצר אפוי בכמות מסוימת. היא בודקת האם יש מספיק חומרי גלם לפי המתכון, מעדכנת את המלאי, ורושמת את הפעולה בטבלת הייצור (ProductionLine). אם אין מספיק חומרי גלם – היא זורקת חריגה.

### קוד:

```sql
CREATE OR REPLACE PROCEDURE produce_batch(
    p_baked_id INT,
    p_quantity INT,
    p_employee_id INT,
    p_branch_id INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;
    needed NUMERIC;
    available NUMERIC;
BEGIN
    FOR rec IN SELECT * FROM Recipe WHERE bakeGoodsId = p_baked_id LOOP
        needed := rec.materialQuantity * p_quantity;

        SELECT quantity INTO available
        FROM RawMaterials
        WHERE RawMaterialsId = rec.RawMaterialsId;

        IF available IS NULL THEN
            RAISE EXCEPTION 'Raw material % not found.', rec.RawMaterialsId;
        ELSIF available < needed THEN
            RAISE EXCEPTION 'Not enough material %: needed %, available %',
                rec.RawMaterialsId, needed, available;
        END IF;
    END LOOP;


    FOR rec IN SELECT * FROM Recipe WHERE bakeGoodsId = p_baked_id LOOP
        UPDATE RawMaterials
        SET quantity = quantity - (rec.materialQuantity * p_quantity)
        WHERE RawMaterialsId = rec.RawMaterialsId;
    END LOOP;

   
    INSERT INTO ProductionLine (bakeGoodsId, quantity, employeeId, productionDate)
    VALUES (p_baked_id, p_quantity, p_employee_id, CURRENT_DATE);

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Production failed: %', SQLERRM;
END;
$$;
```


 ### יצירת הפרוצדורה:

 
 ![image](https://github.com/user-attachments/assets/50335e9f-df3c-48a3-966a-531867d68177)

### הרצה:


![image](https://github.com/user-attachments/assets/1c684da6-aa94-4513-a927-dfbe0c326ab4)



### הטבלה Recipe לפני:


![image](https://github.com/user-attachments/assets/f90dd914-c7b6-400d-a161-06ab976adffb)



### הטבלה Recipe אחרי: 


![image](https://github.com/user-attachments/assets/2e87d94a-b969-473e-a1b3-bdc48d5f1374)


### דוגמא להרצה שנכשלה:


![image](https://github.com/user-attachments/assets/b9bddbea-5eab-4f39-b6db-55ef7789ccfe)


### 14 - טריגר log_allergen_warning :

מעקב אחר מוצרים חדשים המכילים מידע על אלרגנים. בכל פעם שנוסף מוצר חדש לטבלת BakedGoods, אם יש בו מידע על אלרגנים, נשמרת על כך רשומה בטבלת AllergenLog.

### הוספת טבלת AllergenLog:
#### קוד:
```sql
CREATE TABLE IF NOT EXISTS AllergenLog (
    log_id SERIAL PRIMARY KEY,
    bakedGoodsId INT,
    allergenInfo TEXT,
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    note TEXT
);
```

### קוד הטריגר: 


```sql
CREATE OR REPLACE FUNCTION log_allergen_warning()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.allergenInfo IS NOT NULL AND length(trim(NEW.allergenInfo)) > 0 THEN
        INSERT INTO AllergenLog(bakedGoodsId, allergenInfo, note)
        VALUES (
            NEW.bakedGoodsId,
            NEW.allergenInfo,
            'Product contains allergen information'
        );
    END IF;

    RETURN NEW;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Failed to log allergen info for product %: %', NEW.bakedGoodsId, SQLERRM;
        RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_allergen
AFTER INSERT ON BakedGoods
FOR EACH ROW
EXECUTE FUNCTION log_allergen_warning();

```



### יצירת הטריגר:

![image](https://github.com/user-attachments/assets/4ee1480d-1121-436b-98fd-519ab7972b8f)


### הרצה:


![image](https://github.com/user-attachments/assets/230f7069-b00f-4393-93e6-f776fdb7b44b)


### 15 - תוכנית ראשית :

בלוק DO שמבצע הרצת תהליך מלא של:

בדיקת זמינות חומרי גלם עבור מוצר מסוים (באמצעות פונקציה שמחזירה refcursor)

הדפסת המידע של כל חומר גלם (כמות נדרשת, זמינה, סטטוס)

קריאה לפרוצדורת ייצור (הפקת אצווה של מוצר)

הדפסת הודעת הצלחה או שגיאה בהתאם - מפורט בפונקציה ובפרוצדורה בנפרד.

### 🔧 בדיקה והרצה של תהליך ייצור מלא

הקוד הבא מבצע תהליך מלא הכולל בדיקת זמינות חומרי גלם והרצת ייצור בפועל. נועד לצורכי בדיקות ושימוש תפעולי.

#### קוד:
```sql
DO $$
DECLARE
    ref refcursor;
    rec RECORD;
BEGIN
    RAISE NOTICE '--- בדיקת זמינות חומרי גלם למוצר 1 ---';

    -- שלב 1: קריאה לפונקציה שמחזירה RefCursor
    ref := get_materials_summary_for_product(1);

    LOOP
        FETCH ref INTO rec;
        EXIT WHEN NOT FOUND;
        RAISE NOTICE 'חומר: %, נדרש: %, קיים: %, סטטוס: %',
            rec.name, rec.required, rec.available, rec.status;
    END LOOP;

    CLOSE ref;

    RAISE NOTICE '--- הרצת ייצור אצווה של מוצר 1 בכמות 5 ---';

    -- שלב 2: קריאה לפרוצדורה לייצור אצווה
    CALL produce_batch(
        p_baked_id := 1,
        p_quantity := 5,
        p_employee_id := 2,
        p_branch_id := 1
    );

    RAISE NOTICE '✅ ההפקה הושלמה בהצלחה';

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE '❌ שגיאה בתהליך: %', SQLERRM;
END;
$$;
```


### הרצה:

![image](https://github.com/user-attachments/assets/8a8b6913-2914-4014-b80e-d4acb89a7cbe)










---






































