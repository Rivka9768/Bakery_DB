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
הנתונים מקובצים לפי שם העובד (e.name), ומחושב סך הכולל של ההפקה (SUM(pl.quantity)) עבור כל עובד.
בסופו של תהליך, התוצאות ממוינות בסדר יורד לפי ערך ההפקה הכוללת, כך שהעובדים עם ההפקה הגבוהה ביותר מוצגים קודם.

*שאילתא:*
```sql
SELECT e.name, SUM(pl.quantity) AS totalProduction
FROM Employee e
NATURAL JOIN ProductionLine pl
WHERE EXTRACT(YEAR FROM pl.productionDate) = 2024
GROUP BY e.name
ORDER BY totalProduction DESC;
```
*הרצה:*

![image](https://github.com/user-attachments/assets/6433d313-6eb6-454d-9cd3-2c95c230a05b)
*תוצאה:*

![image](https://github.com/user-attachments/assets/db134df5-9f50-48fd-ae13-a63edf61053f)


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









































