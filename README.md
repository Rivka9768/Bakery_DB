# BAKERY - Project Report

## Table of Contents
[Phase 1](#phase-1)
1. [Cover Page](#cover-page)
2. [Introduction](#introduction)
3. [ERD and DSD Diagrams](#erd-and-dsd-diagrams)
4. [Data Entry Methods](#data-entry-methods)
5. [Backup and Restore](#backup-and-restore)

[Phase 2 - Integration](#phase-2-integration)

---

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

### Phase 2 - Integration
**SELECT QUERIES:**
**1. Average calorie count per baked goods category, ordered from highest to lowest**

השאילתה מאגדת נתונים משלוש טבלאות (Categories, BakedGoods ו-NutritionFacts) לצורך חישוב ממוצע הקלוריות עבור כל קטגוריית מוצרי מאפה.
היא מבצעת חיבורים בין הטבלאות באמצעות מפתחות זרים (categoryId ו-bakedGoodsId), מחשבת את ממוצע הקלוריות לכל קטגוריה (מעוגל לשני מקומות אחרי הנקודה), מקבצת את התוצאות לפי שם הקטגוריה (c.name), וממיינת את הפלט בסדר יורד לפי ערך ממוצע הקלוריות.



![image](https://github.com/user-attachments/assets/4a61776c-59a8-49b3-a4dc-02843670fd68)
![image](https://github.com/user-attachments/assets/c5904ff9-fa9c-4275-96a4-8e3e1e1e87bd)


**2. Total Production per Employee in 2024, Ordered by Output**
השאילתה מחברת את טבלאות Employee ו-ProductionLine באמצעות NATURAL JOIN כדי לחשב את מספר היחידות הכולל שהופק על ידי כל עובד במהלך שנת 2024.
הנתונים מקובצים לפי שם העובד (e.name), ומחושב סך הכולל של ההפקה (SUM(pl.quantity)) עבור כל עובד.
בסופו של תהליך, התוצאות ממוינות בסדר יורד לפי ערך ההפקה הכוללת, כך שהעובדים עם ההפקה הגבוהה ביותר מוצגים קודם.

![image](https://github.com/user-attachments/assets/6433d313-6eb6-454d-9cd3-2c95c230a05b)
![image](https://github.com/user-attachments/assets/db134df5-9f50-48fd-ae13-a63edf61053f)


**3. High-Fat or High-Sugar Baked Goods, Ordered by Fat and Sugar Content**

השאילתה מחזירה את שם מוצר המאפה, כמות השומן וכמות הסוכר שלו, על ידי ביצוע חיבור (JOIN) בין הטבלאות BakedGoods ו-NutritionFacts על בסיס bakedGoodsId.
התוצאות מסוננות כך שיוצגו רק מוצרי מאפה שבהם כמות השומן גדולה מ-20 גרם או כמות הסוכר גדולה מ-10 גרם.
בסיום, הנתונים ממוינים תחילה לפי כמות השומן בסדר יורד, ולאחר מכן לפי כמות הסוכר בסדר יורד.


![image](https://github.com/user-attachments/assets/7cc98e1f-05b7-47c7-9659-676f490cdc89)
![image](https://github.com/user-attachments/assets/f1d96095-1cb3-4744-90b5-6df6516d053e)

**4. Branch Production Efficiency: Total Output, Number of Employees, and Average Production per Employee**
השאילתה מאחדת נתונים מהטבלאות Branches, Employee, ו-ProductionLine באמצעות NATURAL JOIN,
ומחזירה עבור כל סניף את המזהה (branchId), המיקום (location), סך כל יחידות הייצור (totalProduction), מספר העובדים הייחודיים (numEmployees), ואת ממוצע יחידות הייצור לעובד (productionPerEmployee).
התוצאות כוללות רק סניפים שבהם יש לפחות עובד אחד (באמצעות תנאי HAVING).
לבסוף, התוצאות ממוינות לפי ממוצע הייצור לעובד בסדר עולה (מהפחות יעילים ליותר יעילים).


![image](https://github.com/user-attachments/assets/0e3c6c6a-2415-4be5-b719-49fc1fd9eb36)
![image](https://github.com/user-attachments/assets/a7b1617f-c6c4-4497-b89d-8259ca254075)

**5. Baked Goods Priced Above Average per Weight, Ordered by Price**
השאילתה מאחדת נתונים מהטבלאות BakedGoods ו-Categories באמצעות JOIN, ומחזירה שמות ייחודיים של מוצרי מאפה (bg.name) ואת מחירם ליחידת משקל (c.priceperweight).
מוצרי המאפה שנבחרים הם רק אלו שמחירם ליחידת משקל גבוה מהממוצע המחושב לכלל מוצרי המאפה במערכת.
בסיום, התוצאות ממוינות בסדר יורד לפי מחיר ליחידת משקל, כך שהמוצרים היקרים יותר מוצגים ראשונים.
![image](https://github.com/user-attachments/assets/92b8df4d-0d12-403b-8870-c3f8276a7c78)
![image](https://github.com/user-attachments/assets/7ecb98a6-23b2-404e-a380-905eb7f7a54a)

**6. Total Baked Goods Produced Per Month in 2024, Ordered by Month**

השאילתה מחזירה את שם החודש (month_name) וסך כל יחידות הייצור של מוצרי המאפה (total_baked_goods) עבור כל חודש בשנת 2024, מתוך טבלת ProductionLine.
הנתונים מקובצים לפי חודש (כאשר החודש מנותב על פי הפורמט של TO_CHAR) וממוינים לפי סדר החודשים בשנה.
השאילתה מבטיחה שהתוצאות יכללו רק את השנה 2024 (באמצעות EXTRACT(YEAR FROM productionDate)).

![image](https://github.com/user-attachments/assets/191cbb5b-a901-40bb-b54f-d8c0c5e701f9)
![image](https://github.com/user-attachments/assets/1c9c65db-2601-43dd-ab62-615afb4fe99a)

**7. Employee Count by Branch Location, Ordered by Employee Count**

השאילתה מחזירה את המיקום של כל סניף (branch_location) ואת מספר העובדים בכל סניף (employee_count).
הנתונים נאספים בעזרת חיבור מסוג LEFT JOIN בין טבלאות Branches ו-Employee, כך שגם סניפים ללא עובדים ייכללו בתוצאה עם ערך של 0 לעובדים.
התוצאות ממוינות לפי מספר העובדים בסדר יורד, כך שסניפים עם יותר עובדים יופיעו קודם.


![image](https://github.com/user-attachments/assets/be14daba-25d6-4872-b2e0-95eca932f6d2)
![image](https://github.com/user-attachments/assets/2f0ec9f5-194b-49cd-9f50-3b76f30fe73d)

**8. Expired Baked Goods: Production Line ID and Expiration Date**

השאילתה מחזירה את מזהה קו הייצור (productionLineId) ואת תאריך התפוגה של מוצרי המאפה, שמחושב על ידי הוספת זמן חיי המוצר (לפי lifetime בטבלת BakedGoods) לתאריך הייצור (productionDate) מתוך טבלת ProductionLine.
השאילתה מסננת את התוצאות כך שמופיעים רק המוצרים שתאריך התפוגה שלהם עבר את התאריך הנוכחי (CURRENT_DATE).
התוצאות ממוינות בסדר יורד לפי תאריך התפוגה, כך שמוצרים שתוקפם פג קודם יופיעו ראשונים.
![image](https://github.com/user-attachments/assets/ed6278e3-3bc9-4087-8c5a-e1c3d16f306c)
![image](https://github.com/user-attachments/assets/df4caab3-91be-4c8a-bab8-9ab9486a0443)

**UPDATE QUERIES:**
**1. Update Recipe and Nutrition Facts for Baked Goods**
העסקה הזאת מבצעת עדכונים בשתי טבלאות:
עדכון מתכון: כמות הסוכר במתכון עבור מוצר מאפה ספציפי (עם bakedGoodsId = 52) מתעדכנת ב-200 גרם (0.20 ק"ג). הסוכר מזוהה לפי RawMaterialsId, שנלקח מטבלת ה-RawMaterials.
עדכון נתוני תזונה: כמות הסוכר מתעדכנת ב-0.20 ק"ג, והקלוריות מתעדכנות ב-774 עבור אותו מוצר מאפה (עם bakedGoodsId = 52) בטבלת NutritionFacts.
העסקה מבטיחה עדכון מתואם של המתכון ונתוני התזונה, לשמירה על עקביות בין הטבלאות הקשורות.


![image](https://github.com/user-attachments/assets/7b56c832-2dcf-474e-8d58-f1c56aabc1d7)

Before:
![image](https://github.com/user-attachments/assets/47e014f9-8fe3-4764-b5a9-ac39cf925ce6)

After:
![image](https://github.com/user-attachments/assets/e555c0bc-d2d2-4aa6-a912-d13e33107d88)

**2. Update Category Price Based on VAT Increase**

השאילתה מבצעת עדכון במחיר לכל קילוגרם של כל קטגוריה, בהתאם לשינוי במע"מ מ-17% ל-18%. מחירי הקטגוריות מעודכנים על ידי חישוב תוספת של המע"מ החדש (1.18) בהשוואה למע"מ הקודם (1.17), ומחיר לכל קילוגרם מוגדל לפי היחס בין 1.18 ל-1.17, כאשר התוצאה מעוגלת לשני מקומות אחרי הנקודה.


![image](https://github.com/user-attachments/assets/e06d7e4c-4ae6-4601-bf0b-818e69db7b41)

Before:
![image](https://github.com/user-attachments/assets/c7b442e2-3537-4bd4-b285-a5c8596cb272)

After:
![image](https://github.com/user-attachments/assets/54cbf789-e0e4-46d6-840b-149c33c18bab)

**3.**






















