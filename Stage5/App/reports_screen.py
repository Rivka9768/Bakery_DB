import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psycopg2
from datetime import datetime
from typing import Optional, List, Dict, Any

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'BAKERY_DB',
    'user': 'postgres',
    'password': 'pswd'
}

class TransactionManager:
    """Real transaction manager using database transactions"""
    
    def __init__(self):
        self.active_transaction = None
        self.connection = None
    
    def begin_transaction(self, description: str):
        """Begin a new database transaction"""
        if self.active_transaction:
            raise Exception("Transaction already active. Complete or rollback current transaction first.")
        
        try:
            self.connection = DatabaseManager.get_connection()
            self.connection.autocommit = False
            cursor = self.connection.cursor()
            cursor.execute("BEGIN TRANSACTION;")
            
            self.active_transaction = {
                'description': description,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'connection': self.connection
            }
            
            return cursor
            
        except Exception as e:
            if self.connection:
                self.connection.close()
            self.connection = None
            self.active_transaction = None
            raise Exception(f"Failed to begin transaction: {str(e)}")
    
    def commit_transaction(self):
        """Commit the active transaction"""
        if not self.active_transaction:
            raise Exception("No active transaction to commit")
        
        try:
            self.connection.commit()
            description = self.active_transaction['description']
            self.cleanup_transaction()
            return True, description
            
        except Exception as e:
            self.cleanup_transaction()
            raise Exception(f"Failed to commit transaction: {str(e)}")
    
    def rollback_transaction(self):
        """Rollback the active transaction"""
        if not self.active_transaction:
            raise Exception("No active transaction to rollback")
        
        try:
            self.connection.rollback()
            description = self.active_transaction['description']
            self.cleanup_transaction()
            return True, description
            
        except Exception as e:
            self.cleanup_transaction()
            raise Exception(f"Failed to rollback transaction: {str(e)}")
    
    def cleanup_transaction(self):
        """Clean up transaction resources"""
        if self.connection:
            self.connection.close()
        self.connection = None
        self.active_transaction = None
    
    def has_active_transaction(self):
        """Check if there's an active transaction"""
        return self.active_transaction is not None
    
    def get_active_transaction_info(self):
        """Get active transaction info"""
        return self.active_transaction

class DatabaseManager:
    """Handles all database operations"""
    @staticmethod
    def get_connection():
        """Create and return database connection"""
        try:
            return psycopg2.connect(**DB_CONFIG)
        except Exception as e:
            raise Exception(f"Database connection failed: {str(e)}")
    
    @staticmethod
    def execute_query(query: str, params: tuple = None, fetch: bool = False):
        """Execute a database query"""
        conn = None
        try:
            conn = DatabaseManager.get_connection()
            cur = conn.cursor()
            cur.execute(query, params)
            
            if fetch:
                result = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                cur.close()
                conn.close()
                return result, columns
            else:
                conn.commit()
                cur.close()
                conn.close()
                return True
                
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            raise Exception(f"Query execution failed: {str(e)}")
    
    @staticmethod
    def execute_in_transaction(cursor, query: str, params: tuple = None):
        """Execute query within an existing transaction"""
        try:
            cursor.execute(query, params)
        except Exception as e:
            raise Exception(f"Query execution in transaction failed: {str(e)}")

class BakeryReportsScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("מסך דוחות מאפייה")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize transaction manager
        self.transaction_manager = TransactionManager()
        
        # Configure Hebrew font
        self.hebrew_font = ('Arial', 10)
        self.header_font = ('Arial', 12, 'bold')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="מערכת דוחות מאפייה", 
                               font=('Arial', 20, 'bold'), fg='white', bg='#2c3e50')
        header_label.pack(expand=True)
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable sidebar frame
        self.create_scrollable_sidebar(content_frame)
        
        # Right frame for results
        results_frame = tk.Frame(content_frame, bg='white', relief=tk.SUNKEN, bd=2)
        results_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Results title
        self.results_title = tk.Label(results_frame, text="תוצאות הדוח", 
                                     font=self.header_font, bg='white')
        self.results_title.pack(pady=10)
        
        # Treeview for results
        self.create_results_table(results_frame)
    
    def create_scrollable_sidebar(self, parent):
        """Create a scrollable sidebar for buttons"""
        # Sidebar container frame
        sidebar_container = tk.Frame(parent, bg='#34495e', width=350)
        sidebar_container.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        sidebar_container.pack_propagate(False)
        
        # Create canvas and scrollbar for sidebar
        sidebar_canvas = tk.Canvas(sidebar_container, bg='#34495e', highlightthickness=0)
        sidebar_scrollbar = ttk.Scrollbar(sidebar_container, orient="vertical", command=sidebar_canvas.yview)
        
        # Create scrollable frame
        self.scrollable_sidebar = tk.Frame(sidebar_canvas, bg='#34495e')
        
        # Configure scrolling
        self.scrollable_sidebar.bind(
            "<Configure>",
            lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))
        )
        
        # Create window in canvas
        canvas_frame = sidebar_canvas.create_window((0, 0), window=self.scrollable_sidebar, anchor="nw")
        
        # Configure canvas scrolling
        sidebar_canvas.configure(yscrollcommand=sidebar_scrollbar.set)
        
        # Pack canvas and scrollbar
        sidebar_canvas.pack(side="left", fill="both", expand=True)
        sidebar_scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            sidebar_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel(event):
            sidebar_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_mousewheel(event):
            sidebar_canvas.unbind_all("<MouseWheel>")
        
        sidebar_canvas.bind('<Enter>', _bind_mousewheel)
        sidebar_canvas.bind('<Leave>', _unbind_mousewheel)
        
        # Update canvas width when scrollable_sidebar changes
        def _configure_canvas_width(event):
            canvas_width = event.width
            sidebar_canvas.itemconfig(canvas_frame, width=canvas_width)
        
        sidebar_canvas.bind('<Configure>', _configure_canvas_width)
        
        # Create buttons in the scrollable frame
        self.create_report_buttons(self.scrollable_sidebar)
        
    def create_report_buttons(self, parent):
        # Control buttons at top
        control_frame = tk.Frame(parent, bg='#34495e')
        control_frame.pack(fill=tk.X, pady=(20, 20), padx=10)
        
        # Refresh button
        refresh_btn = tk.Button(control_frame, text="רענן מסך", command=self.refresh_screen, 
                               font=self.hebrew_font, bg='#27ae60', fg='white',
                               relief=tk.FLAT, pady=5)
        refresh_btn.pack(fill=tk.X, pady=2)
        refresh_btn.bind("<Enter>", lambda e: refresh_btn.configure(bg='#229954'))
        refresh_btn.bind("<Leave>", lambda e: refresh_btn.configure(bg='#27ae60'))
        
        # Transaction control buttons
        self.commit_btn = tk.Button(control_frame, text="אשר שינויים", 
                                   command=self.commit_transaction, 
                                   font=self.hebrew_font, bg='#27ae60', fg='white',
                                   relief=tk.FLAT, pady=5, state='disabled')
        self.commit_btn.pack(fill=tk.X, pady=2)
        self.commit_btn.bind("<Enter>", lambda e: self.commit_btn.configure(bg='#229954') if self.commit_btn['state'] == 'normal' else None)
        self.commit_btn.bind("<Leave>", lambda e: self.commit_btn.configure(bg='#27ae60') if self.commit_btn['state'] == 'normal' else None)
        
        self.rollback_btn = tk.Button(control_frame, text="בטל שינויים", 
                                     command=self.rollback_transaction, 
                                     font=self.hebrew_font, bg='#e74c3c', fg='white',
                                     relief=tk.FLAT, pady=5, state='disabled')
        self.rollback_btn.pack(fill=tk.X, pady=2)
        self.rollback_btn.bind("<Enter>", lambda e: self.rollback_btn.configure(bg='#c0392b') if self.rollback_btn['state'] == 'normal' else None)
        self.rollback_btn.bind("<Leave>", lambda e: self.rollback_btn.configure(bg='#e74c3c') if self.rollback_btn['state'] == 'normal' else None)
        
        # Transaction status label
        self.transaction_status = tk.Label(control_frame, text="אין עסקה פעילה", 
                                          font=('Arial', 8), fg='#ecf0f1', bg='#34495e')
        self.transaction_status.pack(pady=5)
        
        # Separator
        separator = tk.Frame(parent, height=2, bg='#ecf0f1')
        separator.pack(fill=tk.X, pady=10, padx=20)
        
        # Select queries buttons
        select_label = tk.Label(parent, text="שאילתות SELECT", 
                               font=self.header_font, fg='#ecf0f1', bg='#34495e')
        select_label.pack(pady=(0, 10))
        
        select_buttons = [
            ("ממוצע קלוריות לפי קטגוריה", self.report_avg_calories),
            ("עובדים מובילים בייצור", self.report_top_employees),
            ("מוצרים עתירי שומן/סוכר", self.report_high_fat_sugar),
            ("ייצור יחסי לעובדים", self.report_production_per_employee),
            ("מוצרים יקרים מהממוצע", self.report_expensive_products),
            ("ייצור חודשי 2024", self.report_monthly_production),
            ("עובדים לפי סניפים", self.report_employees_by_branch),
            ("מוצרים שפג תוקפם", self.report_expired_products)
        ]
        
        for text, command in select_buttons:
            btn = tk.Button(parent, text=text, command=command, 
                           font=self.hebrew_font, bg='#3498db', fg='white',
                           relief=tk.FLAT, pady=8, width=30)
            btn.pack(pady=2, padx=10, fill=tk.X)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg='#2980b9'))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg='#3498db'))
        
        # Separator
        separator2 = tk.Frame(parent, height=2, bg='#ecf0f1')
        separator2.pack(fill=tk.X, pady=20, padx=20)
        
        # Update queries buttons
        update_label = tk.Label(parent, text="שאילתות UPDATE", 
                               font=self.header_font, fg='#ecf0f1', bg='#34495e')
        update_label.pack(pady=(0, 10))
        
        update_buttons = [
            ("עדכון מחירים (מע\"מ)", self.update_vat_prices),
            ("עדכון אופים בכירים", self.update_senior_bakers)
        ]
        
        for text, command in update_buttons:
            btn = tk.Button(parent, text=text, command=command, 
                           font=self.hebrew_font, bg='#e67e22', fg='white',
                           relief=tk.FLAT, pady=8, width=30)
            btn.pack(pady=2, padx=10, fill=tk.X)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg='#d35400'))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg='#e67e22'))
        
        # Separator
        separator3 = tk.Frame(parent, height=2, bg='#ecf0f1')
        separator3.pack(fill=tk.X, pady=20, padx=20)
        
        # Delete queries buttons
        delete_label = tk.Label(parent, text="שאילתות DELETE", 
                               font=self.header_font, fg='#ecf0f1', bg='#34495e')
        delete_label.pack(pady=(0, 10))
        
        delete_buttons = [
            ("מחק ייצור ישן (3+ שנים)", self.delete_old_production),
            ("מחק מוצרים לא מיוצרים", self.delete_unproduced_goods),
            ("מחק חומרי גלם לא בשימוש", self.delete_unused_materials)
        ]
        
        for text, command in delete_buttons:
            btn = tk.Button(parent, text=text, command=command, 
                           font=self.hebrew_font, bg='#e74c3c', fg='white',
                           relief=tk.FLAT, pady=8, width=30)
            btn.pack(pady=2, padx=10, fill=tk.X)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg='#c0392b'))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg='#e74c3c'))
        
        # Add some padding at the bottom
        bottom_padding = tk.Frame(parent, bg='#34495e', height=50)
        bottom_padding.pack(fill=tk.X)
    
    def create_results_table(self, parent):
        # Frame for treeview and scrollbars
        tree_frame = tk.Frame(parent, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.tree.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Configure treeview appearance
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", font=self.hebrew_font, rowheight=25)
        style.configure("Treeview.Heading", font=self.header_font)
    
    def clear_results(self):
        """Clear the results table"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def display_results(self, data, columns, title):
        """Display results in the table"""
        self.clear_results()
        self.results_title.configure(text=title)
        
        # Configure columns
        self.tree["columns"] = list(range(len(columns)))
        self.tree["show"] = "headings"
        
        # Set column headings and widths
        for i, col in enumerate(columns):
            self.tree.heading(i, text=col)
            self.tree.column(i, width=150, anchor=tk.CENTER)
        
        # Insert data
        for row in data:
            self.tree.insert("", tk.END, values=row)
    
    def execute_query(self, query, title, params=None):
        """Execute a query and display results"""
        try:
            data, columns = DatabaseManager.execute_query(query, params, fetch=True)
            self.display_results(data, columns, title)
            
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בביצוע השאילתה: {str(e)}")
    
    def execute_transactional_query(self, query, description, params=None):
        """Execute update/delete query within a transaction"""
        try:
            # Begin transaction if not already active
            if not self.transaction_manager.has_active_transaction():
                cursor = self.transaction_manager.begin_transaction(description)
                self.update_transaction_ui()
            else:
                # Use existing transaction
                cursor = self.transaction_manager.active_transaction['connection'].cursor()
            
            # Execute the query
            DatabaseManager.execute_in_transaction(cursor, query, params)
            
            messagebox.showinfo("הצלחה", f"{description} הוכן לביצוע!\nהשתמש ב'אשר שינויים' כדי לשמור או ב'בטל שינויים' כדי לבטל.")
            
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בביצוע {description}: {str(e)}")
            # Rollback on error
            if self.transaction_manager.has_active_transaction():
                try:
                    self.transaction_manager.rollback_transaction()
                    self.update_transaction_ui()
                except:
                    pass
    
    def commit_transaction(self):
        """Commit the active transaction"""
        if not self.transaction_manager.has_active_transaction():
            messagebox.showinfo("שגיאה", "אין עסקה פעילה לאישור")
            return
        
        transaction_info = self.transaction_manager.get_active_transaction_info()
        result = messagebox.askyesno("אישור שינויים", 
                                   f"האם אתה בטוח שברצונך לאשר:\n{transaction_info['description']}\n"
                                   f"מתאריך: {transaction_info['timestamp']}?")
        if result:
            try:
                success, description = self.transaction_manager.commit_transaction()
                if success:
                    messagebox.showinfo("הצלחה", f"השינויים נשמרו בהצלחה!")
                    self.update_transaction_ui()
                
            except Exception as e:
                messagebox.showerror("שגיאה", f"שגיאה באישור השינויים: {str(e)}")
    
    def rollback_transaction(self):
        """Rollback the active transaction"""
        if not self.transaction_manager.has_active_transaction():
            messagebox.showinfo("שגיאה", "אין עסקה פעילה לביטול")
            return
        
        transaction_info = self.transaction_manager.get_active_transaction_info()
        result = messagebox.askyesno("ביטול שינויים", 
                                   f"האם אתה בטוח שברצונך לבטל:\n{transaction_info['description']}\n"
                                   f"מתאריך: {transaction_info['timestamp']}?")
        if result:
            try:
                success, description = self.transaction_manager.rollback_transaction()
                if success:
                    messagebox.showinfo("הצלחה", f"השינויים בוטלו בהצלחה!")
                    self.update_transaction_ui()
                
            except Exception as e:
                messagebox.showerror("שגיאה", f"שגיאה בביטול השינויים: {str(e)}")
    
    def update_transaction_ui(self):
        """Update UI based on transaction state"""
        if self.transaction_manager.has_active_transaction():
            transaction_info = self.transaction_manager.get_active_transaction_info()
            self.transaction_status.configure(text=f"עסקה פעילה: {transaction_info['description']}")
            self.commit_btn.configure(state='normal')
            self.rollback_btn.configure(state='normal')
        else:
            self.transaction_status.configure(text="אין עסקה פעילה")
            self.commit_btn.configure(state='disabled')
            self.rollback_btn.configure(state='disabled')
    
    def refresh_screen(self):
        """Refresh the screen - clear results and reset state"""
        # Check if there's an active transaction
        if self.transaction_manager.has_active_transaction():
            result = messagebox.askyesno("רענון מסך", 
                                       "יש עסקה פעילה. רענון המסך יבטל את השינויים הלא שמורים.\nהאם להמשיך?")
            if result:
                try:
                    self.transaction_manager.rollback_transaction()
                except:
                    pass
            else:
                return
        
        self.clear_results()
        self.results_title.configure(text="תוצאות הדוח")
        self.update_transaction_ui()
        messagebox.showinfo("רענון", "המסך רוענן בהצלחה!")
    
    # SELECT Query Methods (unchanged)
    def report_avg_calories(self):
        query = """
        SELECT c.name AS categoryName, ROUND(AVG(nf.calories), 2) AS avgCalories
        FROM Categories c
        JOIN BakedGoods bg ON c.categoryId = bg.categoryId
        JOIN NutritionFacts nf ON bg.bakedGoodsId = nf.bakedGoodsId
        GROUP BY c.name
        ORDER BY avgCalories DESC;
        """
        self.execute_query(query, "ממוצע קלוריות לפי קטגוריה")
    
    def report_top_employees(self):
        query = """
        SELECT e.name, SUM(pl.quantity) AS totalProduction
        FROM Employee e
        NATURAL JOIN ProductionLine pl
        WHERE EXTRACT(YEAR FROM pl.productionDate) = 2024
        GROUP BY e.EmployeeId, e.name
        ORDER BY totalProduction DESC;
        """
        self.execute_query(query, "עובדים מובילים בייצור - 2024")
    
    def report_high_fat_sugar(self):
        query = """
        SELECT bg.name, nf.fat, nf.sugar
        FROM BakedGoods bg
        JOIN NutritionFacts nf ON bg.bakedGoodsId = nf.bakedGoodsId
        WHERE nf.fat > 20 OR nf.sugar > 10
        ORDER BY nf.fat DESC, nf.sugar DESC;
        """
        self.execute_query(query, "מוצרים עתירי שומן או סוכר")
    
    def report_production_per_employee(self):
        query = """
        SELECT 
            b.branchId,
            b.location,
            SUM(pl.quantity) AS totalProduction,
            COUNT(DISTINCT e.employeeId) AS numEmployees,
            ROUND(SUM(pl.quantity) * 1.0 / COUNT(DISTINCT e.employeeId), 2) AS productionPerEmployee
        FROM Branches b
        NATURAL JOIN Employee e 
        NATURAL JOIN ProductionLine pl 
        GROUP BY b.branchId, b.location
        HAVING COUNT(DISTINCT e.employeeId) > 0
        ORDER BY productionPerEmployee DESC;
        """
        self.execute_query(query, "ייצור יחסי לעובדים לפי סניף")
    
    def report_expensive_products(self):
        query = """
        SELECT DISTINCT bg.name, c.priceperweight
        FROM BakedGoods bg
        JOIN Categories c ON bg.categoryId = c.categoryId
        WHERE c.priceperweight > (
            SELECT AVG(priceperweight)
            FROM BakedGoods bg2
            JOIN Categories c2 ON bg2.categoryId = c2.categoryId)
        ORDER BY c.priceperweight DESC;
        """
        self.execute_query(query, "מוצרים יקרים מהממוצע")
    
    def report_monthly_production(self):
        query = """
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
        """
        self.execute_query(query, "ייצור חודשי - 2024")
    
    def report_employees_by_branch(self):
        query = """
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
        """
        self.execute_query(query, "מספר עובדים לפי סניפים")
    
    def report_expired_products(self):
        query = """
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
        """
        self.execute_query(query, "מוצרים שפג תוקפם")
    
    def update_vat_prices(self):
        result = messagebox.askyesno("עדכון מחירים", 
                                "האם אתה בטוח שברצונך לעדכן את כל המחירים בהתאם למע\"מ החדש?")
        if result:
            query = """
            UPDATE Categories
            SET pricePerWeight = ROUND(pricePerWeight * 1.18 / 1.17, 2);
            """
            
            self.execute_transactional_query(query, "עדכון מחירי מע\"מ")

    def update_senior_bakers(self):
        result = messagebox.askyesno("עדכון תפקידים", 
                                   "האם אתה בטוח שברצונך לעדכן אופים לאופים בכירים?")
        if result:
            query = """
            UPDATE Employee
            SET roleId = (SELECT roleId FROM Roles WHERE name = 'Senior Baker')
            WHERE roleId = (SELECT roleId FROM Roles WHERE name = 'Baker')
            AND branchId IN (
                SELECT B.branchId
                FROM Branches B
                JOIN Employee E ON B.branchId = E.branchId
                GROUP BY B.branchId, B.minAmountOfWorkers
                HAVING COUNT(E.employeeId) < B.minAmountOfWorkers
            );
            """
            
            self.execute_transactional_query(query, "עדכון תפקידי אופים בכירים")
        
    # DELETE Query Methods - Using proper transactions
    def delete_old_production(self):
        result = messagebox.askyesno("מחיקת נתונים", 
                                   "האם אתה בטוח שברצונך למחוק נתוני ייצור מלפני 3 שנים?")
        if result:
            query = """
            DELETE FROM productionLine
            WHERE productionDate < CURRENT_DATE - INTERVAL '3 years';
            """
            
            self.execute_transactional_query(query, "מחיקת נתוני ייצור ישנים")
    
    def delete_unproduced_goods(self):
        result = messagebox.askyesno("מחיקת מוצרים", 
                                   "האם אתה בטוח שברצונך למחוק מוצרים שלא יוצרו?")
        if result:
            query = """
            DELETE FROM bakedGoods
            WHERE bakedGoodsId NOT IN (
                SELECT DISTINCT bakeGoodsId 
                FROM productionLine 
                WHERE bakeGoodsId IS NOT NULL
            );
            """
            
            self.execute_transactional_query(query, "מחיקת מוצרים שלא יוצרו")
    
    def delete_unused_materials(self):
        result = messagebox.askyesno("מחיקת חומרי גלם", 
                                   "האם אתה בטוח שברצונך למחוק חומרי גלם לא בשימוש?")
        if result:
            query = """
            DELETE FROM RawMaterials
            WHERE RawMaterialsId NOT IN (
                SELECT r.RawMaterialsId
                FROM recipe r
                WHERE r.RawMaterialsId IS NOT NULL
            );
            """
            
            self.execute_transactional_query(query, "מחיקת חומרי גלם לא בשימוש")
