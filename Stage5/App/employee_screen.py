import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from typing import Optional, List, Dict, Any

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'BAKERY_DB',
    'user': 'postgres',
    'password': 'pswd'
}

class DatabaseManager:
    """Handles all database operations"""
    """A singleton class to manage database connections and queries"""
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
                cur.close()
                conn.close()
                return result
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

class Employee:
    """Employee data model"""
    
    def __init__(self, employee_id: int = None, name: str = "", phone: str = "", 
                 email: str = "", dob: str = "", branch_id: int = None, role_id: int = None, branch_name: str = None, role_name: str = None):
        self.employee_id = employee_id
        self.name = name
        self.phone = phone
        self.email = email
        self.dob = dob
        self.branch_id = branch_id
        self.role_id = role_id
        self.branch_name = branch_name
        self.role_name = role_name
    
    def to_tuple(self) -> tuple:
        """Convert employee to tuple (for database operations)"""
        return (self.name, self.phone, self.email, self.dob, self.branch_id, self.role_id,)
    
    def to_display_tuple(self) -> tuple:
        """Convert employee to tuple for display"""
        return (self.name, self.phone, self.email, self.dob, self.branch_name, self.role_name)
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Employee':
        """Create Employee instance from database row"""
        return cls(
            employee_id=row[0],    # employeeId
            name=row[1],           # name
            phone=row[2],          # phone
            email=row[3],          # email
            dob=row[4],            # dob
            branch_id=row[5],      # branchId
            branch_name=row[6],    # branch_name
            role_id=row[7],        # roleId
            role_name=row[8]       # role_name
        )

class EmployeeRepository:
    """Data Access Layer - handles all Employee CRUD operations"""
    
    @staticmethod
    def create(employee: Employee) -> bool:
        """CREATE - Add new employee to database"""
        query = """
            INSERT INTO Employee (name, phone, email, dob, branchId, roleId) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            DatabaseManager.execute_query(query, employee.to_tuple())
            return True
        except Exception as e:
            raise Exception(f"Failed to create employee: {str(e)}")
    
    @staticmethod
    def read_all() -> List[Employee]:
        """READ - Get all employees from database with branch and role names"""
        query = """
        SELECT 
            e.employeeId, 
            e.name, 
            e.phone, 
            e.email, 
            e.dob, 
            e.branchId,
            b.location as branch_name,
            e.roleId,
            r.name as role_name
        FROM Employee e
        LEFT JOIN Branches b ON e.branchId = b.branchId
        LEFT JOIN Roles r ON e.roleId = r.roleId
        ORDER BY e.name
        """
        try:
            rows = DatabaseManager.execute_query(query, fetch=True)
            return [Employee.from_db_row(row) for row in rows]
        except Exception as e:
            raise Exception(f"Failed to read employees: {str(e)}")
    
    @staticmethod
    def read_by_id(employee_id: int) -> Optional[Employee]:
        """READ - Get employee by ID"""
        query = """
         SELECT 
            e.employeeId, 
            e.name, 
            e.phone, 
            e.email, 
            e.dob, 
            e.branchId,
            b.location as branch_name,
            e.roleId,
            r.name as role_name
        FROM Employee e
        LEFT JOIN Branches b ON e.branchId = b.branchId
        LEFT JOIN Roles r ON e.roleId = r.roleId
        WHERE employeeId = %s
        """
        try:
            rows = DatabaseManager.execute_query(query, (employee_id,), fetch=True)
            return Employee.from_db_row(rows[0]) if rows else None
        except Exception as e:
            raise Exception(f"Failed to read employee by ID: {str(e)}")
    
    @staticmethod
    def update(employee: Employee) -> bool:
        """UPDATE - Update existing employee"""
        query = """
            UPDATE Employee 
            SET name=%s, phone=%s, email=%s, dob=%s, branchId=%s, roleId=%s 
            WHERE employeeId=%s
        """
        try:
            params = (*employee.to_tuple(), employee.employee_id)
            DatabaseManager.execute_query(query, params)
            return True
        except Exception as e:
            raise Exception(f"Failed to update employee: {str(e)}")
    
    @staticmethod
    def delete(employee_id: int) -> bool:
        """DELETE - Remove employee from database"""
        query = "DELETE FROM Employee WHERE employeeId = %s"
        try:
            DatabaseManager.execute_query(query, (employee_id,))
            return True
        except Exception as e:
            raise Exception(f"Failed to delete employee: {str(e)}")
        
    @staticmethod
    def get_all_branches() -> list[tuple[int, str]]:
        """Get all branch IDs and names"""
        query = "SELECT branchId, location FROM Branches" 
        return DatabaseManager.execute_query(query, fetch=True)

    @staticmethod
    def get_all_roles() -> list[tuple[int, str]]:
        """Get all role IDs and names"""
        query = "SELECT roleId, name FROM Roles"  # Adjust table/column names as needed
        return DatabaseManager.execute_query(query, fetch=True)
    

class EmployeeService:
    """Business Logic Layer - handles business rules and validation"""
    
    def __init__(self):
        self.repository = EmployeeRepository()
    
    def validate_employee_data(self, employee: Employee) -> List[str]:
        """Validate employee data and return list of errors"""
        errors = []
        
        if not employee.name.strip():
            errors.append("Name is required")
        
        if not employee.phone.strip():
            errors.append("Phone is required")
        
        if not employee.email.strip():
            errors.append("Email is required")
        elif "@" not in employee.email:
            errors.append("Invalid email format")
        
        if not employee.dob.strip():
            errors.append("Date of birth is required")
        
        if employee.branch_id is None:
            errors.append("Branch ID is required")
        
        if employee.role_id is None:
            errors.append("Role ID is required")
        
        return errors
    
    def create_employee(self, employee: Employee) -> bool:
        """Create new employee with validation"""
        errors = self.validate_employee_data(employee)
        if errors:
            raise Exception("Validation errors:\n" + "\n".join(errors))
        
        return self.repository.create(employee)
    
    def get_all_employees(self) -> List[Employee]:
        """Get all employees"""
        return self.repository.read_all()
    
    def get_employee_by_id(self, employee_id: int) -> Optional[Employee]:
        """Get employee by ID"""
        return self.repository.read_by_id(employee_id)
    
    def update_employee(self, employee: Employee) -> bool:
        """Update employee with validation"""
        errors = self.validate_employee_data(employee)
        if errors:
            raise Exception("Validation errors:\n" + "\n".join(errors))
        
        return self.repository.update(employee)
    
    def delete_employee(self, employee_id: int) -> bool:
        """Delete employee"""
        return self.repository.delete(employee_id)
    
        # You'll also need these methods in your employee service:
    
    def get_branches(self) -> list[tuple[int, str]]:
        """Get all branches"""
        rows = EmployeeRepository.get_all_branches()  # Implement this in your repository
        return [(int(row[0]), row[1]) for row in rows]

    def get_roles(self) -> list[tuple[int, str]]:
        """Get all roles"""
        rows = EmployeeRepository.get_all_roles()  # Implement this in your repository
        return [(int(row[0]), row[1]) for row in rows]

class EmployeeApp(tk.Tk):
    """Presentation Layer - GUI Application"""
    
    def __init__(self):
        super().__init__()
        self.title("ניהול עובדים - מאפייה")
        self.geometry("1200x800")
        self.configure(bg="#f5f5f5")
        self.resizable(True, True)
        
        # Configure style
        self.setup_styles()
        
        # Initialize service layer
        self.employee_service = EmployeeService()
        self.selected_employee: Optional[Employee] = None
        self.mode = None  # 'add' or 'update'
        
        # Initialize UI
        self.setup_ui()
        self.load_employees()
    
    def setup_styles(self):
        """Setup custom styles for better appearance"""
        style = ttk.Style()
        
        # Configure styles
        style.configure('Title.TLabel', font=('Arial', 20, 'bold'), background='#f5f5f5', foreground='#2c3e50')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), background='#f5f5f5', foreground='#34495e')
        style.configure('Custom.Treeview', font=('Arial', 10))
        style.configure('Custom.Treeview.Heading', font=('Arial', 11, 'bold'))
        
        # Configure button styles
        style.configure('Action.TButton', font=('Arial', 10, 'bold'), padding=10)
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'), padding=10)
        style.configure('Danger.TButton', font=('Arial', 10, 'bold'), padding=10)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = ttk.Label(main_container, text="🍞 מערכת ניהול עובדים - מאפייה", 
                         style='Title.TLabel')
        title.pack(pady=(0, 20))
        
        top_frame = ttk.Frame(main_container)
        top_frame.pack(fill=tk.X, pady=(0, 10))
                
        # Action buttons
        self.setup_action_buttons(top_frame)
        
        # Main content frame
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Employee list
        left_frame = ttk.LabelFrame(content_frame, text="רשימת עובדים", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Employee tree
        self.setup_employee_tree(left_frame)
        
        # Right side - Employee form (initially hidden)
        self.setup_employee_form(content_frame)
    
    def setup_action_buttons(self, parent):
        """Setup action buttons"""
        btn_frame = ttk.LabelFrame(parent, text="פעולות", padding=10)
        btn_frame.pack(fill=tk.X)
        
        buttons_container = ttk.Frame(btn_frame)
        buttons_container.pack()
        
        ttk.Button(buttons_container, text="➕ הוסף עובד", command=self.show_add_form, style='Primary.TButton').grid(row=0, column=0, padx=5)
        ttk.Button(buttons_container, text="✏️ עדכן עובד", command=self.show_update_form, style='Action.TButton').grid(row=0, column=1, padx=5)
        ttk.Button(buttons_container, text="🗑️ מחק עובד", command=self.delete_employee, style='Danger.TButton').grid(row=0, column=2, padx=5)
        ttk.Button(buttons_container, text="🔄 רענן", command=self.refresh_screen, style='Action.TButton').grid(row=0, column=3, padx=5)
    
    def setup_employee_tree(self, parent):
        """Setup employee display tree"""
        # Create frame for tree and scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("name", "phone", "email", "dob", "branchId", "roleId")
        hebrew_headers = ["שם", "טלפון", "אימייל", "תאריך לידה", "סניף", "תפקיד"]
        
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20, style='Custom.Treeview')
        
        # Configure columns
        column_widths = [150, 120, 180, 120, 80, 80]
        for col, header, width in zip(columns, hebrew_headers, column_widths):
            self.tree.heading(col, text=header)
            self.tree.column(col, width=width, anchor='center', minwidth=60)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for tree and scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_employee_select)
        
        # Add alternating row colors
        self.tree.tag_configure('oddrow', background='#f9f9f9')
        self.tree.tag_configure('evenrow', background='#ffffff')
    
    def setup_employee_form(self, parent):
        """Setup employee form"""
        self.form_frame = ttk.LabelFrame(parent, text="פרטי עובד", padding=15)
        
        # Load branches and roles for dropdowns
        try:
            # Get branches (assuming you have a method to get branches)
            self.branches = self.employee_service.get_branches()  # Should return [(id, name), ...]
            self.branch_name_to_id = {name: id for id, name in self.branches}
            branch_names = list(self.branch_name_to_id.keys())
            
            # Get roles (assuming you have a method to get roles)
            self.roles = self.employee_service.get_roles()  # Should return [(id, name), ...]
            self.role_name_to_id = {name: id for id, name in self.roles}
            role_names = list(self.role_name_to_id.keys())
            
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בטעינת נתונים: {str(e)}")
            self.branch_name_to_id = {}
            self.role_name_to_id = {}
            branch_names = []
            role_names = []
        
        # Form fields
        labels = ["שם", "טלפון", "אימייל", "תאריך לידה (YYYY-MM-DD)", "קוד סניף", "קוד תפקיד"]
        self.entries = {}
        
        for i, label in enumerate(labels):
            # Label
            label_widget = ttk.Label(self.form_frame, text=label, style='Heading.TLabel')
            label_widget.grid(row=i, column=0, sticky=tk.W, pady=8, padx=(0, 10))
            
            # Branch dropdown (index 4 - "קוד סניף")
            if i == 4:
                self.branch_combobox = ttk.Combobox(
                    self.form_frame,
                    values=branch_names,
                    state="readonly",
                    font=('Arial', 10),
                    width=28
                )
                self.branch_combobox.grid(row=i, column=1, pady=8, padx=(0, 10), sticky=tk.W)
                
                # Set default value
                if branch_names:
                    self.branch_combobox.set(branch_names[0])
                
                self.entries[label] = self.branch_combobox
                
            # Role dropdown (index 5 - "קוד תפקיד")
            elif i == 5:
                self.role_combobox = ttk.Combobox(
                    self.form_frame,
                    values=role_names,
                    state="readonly",
                    font=('Arial', 10),
                    width=28
                )
                self.role_combobox.grid(row=i, column=1, pady=8, padx=(0, 10), sticky=tk.W)
                
                # Set default value
                if role_names:
                    self.role_combobox.set(role_names[0])
                
                self.entries[label] = self.role_combobox
                
            # Regular entry fields
            else:
                entry = ttk.Entry(self.form_frame, width=30, font=('Arial', 10))
                entry.grid(row=i, column=1, pady=8, padx=(0, 10), sticky=tk.W)
                self.entries[label] = entry
        
        # Form buttons
        button_frame = ttk.Frame(self.form_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=20)
        
        self.save_button = ttk.Button(button_frame, text="💾 שמור", command=self.save_employee, style='Primary.TButton')
        self.save_button.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(button_frame, text="❌ ביטול", command=self.cancel_form, style='Action.TButton').grid(row=0, column=1)
        
        # Initially hide form
        self.form_frame.pack_forget()
    
    def load_employees(self):
        """Load and display all employees"""
        try:
            employees = self.employee_service.get_all_employees()
            self.display_employees(employees)
        except Exception as e:
            messagebox.showerror("שגיאה", f"Error loading employees: {str(e)}")
    
    def display_employees(self, employees: List[Employee]):
        """Display employees in tree with alternating colors"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add employees to tree with alternating colors
        for i, employee in enumerate(employees):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', 
                           iid=employee.employee_id, 
                           values=employee.to_display_tuple(),
                           tags=(tag,))
    
    def on_employee_select(self, event):
        """Handle employee selection"""
        selection = self.tree.selection()
        if not selection:
            self.selected_employee = None
            return
        
        employee_id = int(selection[0])
        try:
            self.selected_employee = self.employee_service.get_employee_by_id(employee_id)
            if self.selected_employee and self.form_frame.winfo_ismapped():
                self.populate_form(self.selected_employee)
        except Exception as e:
            messagebox.showerror("שגיאה", f"Error loading employee details: {str(e)}")
    
    def populate_form(self, employee: Employee):
        """Populate form with employee data"""
        # Regular text fields
        text_fields = {
            "שם": employee.name,
            "טלפון": employee.phone,
            "אימייל": employee.email,
            "תאריך לידה (YYYY-MM-DD)": str(employee.dob)
        }
        
        # Clear and populate text fields
        for label, value in text_fields.items():
            entry = self.entries[label]
            entry.delete(0, tk.END)
            entry.insert(0, value)
        
        # Set branch dropdown to the employee's branch name
        if employee.branch_name:
            self.branch_combobox.set(employee.branch_name)
        else:
            # Fallback: find branch name by ID
            branch_name = None
            for bid, bname in self.branches:
                if bid == employee.branch_id:
                    branch_name = bname
                    break
            if branch_name:
                self.branch_combobox.set(branch_name)
        
        # Set role dropdown to the employee's role name
        if employee.role_name:
            self.role_combobox.set(employee.role_name)
        else:
            # Fallback: find role name by ID
            role_name = None
            for rid, rname in self.roles:
                if rid == employee.role_id:
                    role_name = rname
                    break
            if role_name:
                self.role_combobox.set(role_name)
    
    def clear_form(self):
        """Clear all form fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    
    def show_add_form(self):
        """Show form for adding new employee"""
        self.clear_form()
        self.mode = 'add'
        self.save_button.config(text="➕ הוסף עובד")
        self.form_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
    
    def show_update_form(self):
        """Show form for updating employee"""
        if not self.selected_employee:
            messagebox.showwarning("שגיאה", "אנא בחר עובד לעדכון")
            return
        
        self.mode = 'update'
        self.save_button.config(text="✏️ עדכן עובד")
        self.populate_form(self.selected_employee)
        self.form_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
    
    def cancel_form(self):
        """Cancel form operation"""
        self.form_frame.pack_forget()
        self.clear_form()
        self.mode = None
    
    def save_employee(self):
        """Save employee (add or update)"""
        try:
            # Get form data
            labels = ["שם", "טלפון", "אימייל", "תאריך לידה (YYYY-MM-DD)", "סניף", "תפקיד"]
            values = []
            
            # Get values from entries, but handle dropdowns specially
            for i, label in enumerate(labels):
                if label == "סניף":
                    # Get branch directly from the combobox
                    branch_name = self.branch_combobox.get()
                    values.append(branch_name)
                elif label == "תפקיד":
                    # Get role directly from the combobox
                    role_name = self.role_combobox.get()
                    values.append(role_name)
                else:
                    values.append(self.entries[label].get().strip())
            
            # Get branch and role IDs from the selected names
            branch_name = values[4]  # Branch is at index 4
            role_name = values[5]    # Role is at index 5
            
            branch_id = self.branch_name_to_id.get(branch_name)
            role_id = self.role_name_to_id.get(role_name)

            print(f"DEBUG: Selected branch name: '{branch_name}' -> ID: {branch_id}")
            print(f"DEBUG: Selected role name: '{role_name}' -> ID: {role_id}")

            if not branch_id:
                messagebox.showerror("שגיאה", "יש לבחור סניף")
                return
                
            if not role_id:
                messagebox.showerror("שגיאה", "יש לבחור תפקיד")
                return

            # Create employee object (adjust according to your Employee class structure)
            employee = Employee(
                name=values[0],
                phone=values[1],
                email=values[2],
                dob=values[3],  # You might want to validate date format
                branch_id=branch_id,
                role_id=role_id
            )
            
            # Set employee ID for updates
            if self.mode == 'update' and self.selected_employee:
                employee.employee_id = self.selected_employee.employee_id
            
            # Save employee
            if self.mode == 'add':
                self.employee_service.create_employee(employee)
                messagebox.showinfo("הצלחה", "✅ העובד נוסף בהצלחה!")
            elif self.mode == 'update':
                self.employee_service.update_employee(employee)
                messagebox.showinfo("הצלחה", "✅ פרטי העובד עודכנו בהצלחה!")
            
            # Refresh and hide form
            self.load_employees()
            self.cancel_form()
            
        except Exception as e:
            print(f"Error in save_employee: {str(e)}")
            messagebox.showerror("שגיאה", f"שגיאה בשמירת העובד: {str(e)}")
    
    def delete_employee(self):
        """Delete selected employee"""
        if not self.selected_employee:
            messagebox.showwarning("שגיאה", "אנא בחר עובד למחיקה")
            return
        
        # Confirm deletion
        result = messagebox.askyesno("אישור מחיקה", 
                                   f"האם אתה בטוח שברצונך למחוק את {self.selected_employee.name}?\n"
                                   f"פעולה זו לא ניתנת לביטול.")
        if not result:
            return
        
        try:
            self.employee_service.delete_employee(self.selected_employee.employee_id)
            messagebox.showinfo("הצלחה", "✅ העובד נמחק בהצלחה!")
            self.load_employees()
            self.cancel_form()
            self.selected_employee = None
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה במחיקה: {str(e)}")
    
    def refresh_screen(self):
        """Refresh the entire screen"""
        self.cancel_form()
        self.selected_employee = None
        self.title("ניהול עובדים - מאפייה")

# Note: This module is designed to be imported and used from a main menu
# The EmployeeApp class should be instantiated from the calling module
