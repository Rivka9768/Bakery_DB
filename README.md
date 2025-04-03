# BAKERY - Project Report

## Table of Contents
1. [Cover Page](#cover-page)
2. [Introduction](#introduction)
3. [ERD and DSD Diagrams](#erd-and-dsd-diagrams)
4. [Data Entry Methods](#data-entry-methods)
5. [Backup and Restore](#backup-and-restore)

---

## Cover Page
**Project Name:** Bakery_DB  
**Submitted by:** **Gila Kassab 330080821 &
                    Rivka Sorscher 567153394**


---
# Bakery Management Database

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

