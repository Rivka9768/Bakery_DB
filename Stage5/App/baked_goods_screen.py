import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from typing import Optional, List, Dict, Any
from typing import List

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

class BakedGoods:
    """BakedGoods data model"""
    
    def __init__(self, bakedGood_id: int = None, name: str = "", category: str = "", category_id: int = None, nutritionfacts_id: int = "", 
                 price_per_weight	: float = "", calories: float = "", carbs : float = None, protein : float = None,
                 fat 	: float = "", sugar : float = "", allergen_Info : str = None, shelf_Life : int = None):
        self.bakedGood_id = bakedGood_id
        self.name = name  
        self.category = category
        self.category_id = category_id
        self.nutritionfacts_id = nutritionfacts_id 
        self.price_per_weight = price_per_weight
        self.calories = calories
        self.carbs = carbs
        self.protein = protein
        self.fat = fat
        self.sugar = sugar
        self.allergen_Info = allergen_Info
        self.shelf_Life = shelf_Life
    
    
    def to_bakedgoods_tuple(self) -> tuple:
        """Convert bakedgood to tuple (for database operations)"""
        return (self.name, self.shelf_Life, self.allergen_Info, self.category_id)
    
    def to_nutritionfacts_tuple(self) -> tuple:
        """Convert nutrition facts to tuple (for database operations)"""
        return (self.calories, self.carbs, self.protein, self.fat, self.sugar)

    
    def to_display_tuple(self) -> tuple:
        """Convert bakedGood to tuple for display"""
        return ( self.name, self.category, self.price_per_weight, self.calories, self.carbs, self.protein, self.fat, self.sugar,
                self.allergen_Info, self.shelf_Life)

    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'BakedGoods':
        """Create Bakedgood instance from database row"""
        return cls(
            bakedGood_id=row[0],
            name=row[1],
            category=row[2],
            category_id=row[3],
            price_per_weight=row[4],
            calories=row[5],
            carbs=row[6],
            protein=row[7],
            fat=row[8],
            sugar=row[9],
            allergen_Info=row[10],
            shelf_Life=row[11]
        )

class BakedGoodsRepository:
    """Data Access Layer - handles all Bakedgoods CRUD operations"""
    
    @staticmethod
    def create(bakedgood: BakedGoods) -> bool:
        """CREATE - Add new bakedgood and its nutrition facts to the database in a single transaction"""
        bakedgoods_query = """
            INSERT INTO BakedGoods (name, lifetime, allergeninfo, categoryid) 
            VALUES (%s, %s, %s, %s)
            RETURNING bakedgoodsId
        """
        
        nutrition_query = """
            INSERT INTO nutritionFacts (bakedgoodsId, calories, carbs, protein, fat, sugar) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        try:
            # Start transaction
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            
            # Insert into BakedGoods and get the new ID
            cursor.execute(bakedgoods_query, bakedgood.to_bakedgoods_tuple())
            bakedgoods_id = cursor.fetchone()[0]
            
            # Insert into NutritionFacts using the retrieved ID
            nutrition_data = (bakedgoods_id,) + bakedgood.to_nutritionfacts_tuple()
            cursor.execute(nutrition_query, nutrition_data)

            # Commit the transaction
            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            raise Exception(f"Failed to create bakedgood and nutrition facts: {str(e)}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    
    @staticmethod
    def read_all() -> List[BakedGoods]:
        """READ - Get all baked goods from database"""
        query = """
            SELECT 
                bg.bakedGoodsid as bakedGood_id,
                bg.name,
                c.name as category,
                c.categoryid as category_id,
                nf.nutritionfactid as nutritionfacts_id,
                c.Priceperweight as price_per_weight,
                nf.calories,
                nf.carbs,
                nf.protein,
                nf.fat,
                nf.sugar ,
                bg.AllergenInfo as allergen_Info,
                bg.lifetime as shelf_Life
            FROM 
                BakedGoods bg
            JOIN 
                Categories c ON bg.categoryid = c.categoryid
            JOIN 
                NutritionFacts nf ON nf.bakedgoodsid = bg.bakedgoodsid
            ORDER BY 
                bg.name
        """
        try:
            rows = DatabaseManager.execute_query(query, fetch=True)
            return [BakedGoods(
                bakedGood_id=row[0],
                name=row[1],
                category=row[2],
                category_id=row[3],
                nutritionfacts_id=row[4],
                price_per_weight=row[5],
                calories=row[6],
                carbs=row[7],
                protein=row[8],
                fat=row[9],
                sugar=row[10],
                allergen_Info=row[11],
                shelf_Life=row[12]
            ) for row in rows]
        except Exception as e:
            raise Exception(f"Failed to read baked goods: {str(e)}")

    
    @staticmethod
    def read_by_id(bakedGood_id: int) -> Optional[BakedGoods]:
        """READ - Get baked good by ID"""
        query = """
            SELECT 
                bg.bakedGoodsid as bakedGood_id,
                bg.name,
                c.name as category,
                c.categoryid as category_id,
                nf.nutritionfactid as nutritionfacts_id,
                c.Priceperweight as price_per_weight,
                nf.calories,
                nf.carbs,
                nf.protein,
                nf.fat,
                nf.sugar ,
                bg.AllergenInfo as allergen_Info,
                bg.lifetime as shelf_Life
            FROM 
                BakedGoods bg
            JOIN 
                Categories c ON bg.categoryid = c.categoryid
            JOIN 
                NutritionFacts nf ON nf.bakedgoodsid = bg.bakedgoodsid
            WHERE 
                bg.bakedGoodsid = %s
        """
        try:
            rows = DatabaseManager.execute_query(query, (bakedGood_id,), fetch=True)
            return BakedGoods(
                bakedGood_id=rows[0][0],
                name=rows[0][1],
                category=rows[0][2],
                category_id=rows[0][3],
                nutritionfacts_id=rows[0][4],
                price_per_weight=rows[0][5],
                calories=rows[0][6],
                carbs=rows[0][7],
                protein=rows[0][8],
                fat=rows[0][9],
                sugar=rows[0][10],
                allergen_Info=rows[0][11],
                shelf_Life=rows[0][12]
            ) if rows else None
        except Exception as e:
            raise Exception(f"Failed to read baked good by ID: {str(e)}")

    
    @staticmethod
    def update(bakedgood: BakedGoods) -> bool:
        """UPDATE - Update existing baked good and its nutrition facts"""
        bakedgoods_query = """
            UPDATE BakedGoods
            SET name=%s, lifetime=%s, Allergeninfo=%s, categoryId=%s
            WHERE bakedGoodsId = %s
        """
        nutrition_query = """
            UPDATE NutritionFacts
            SET calories=%s, carbs=%s, protein=%s, fat=%s, sugar=%s
            WHERE bakedGoodsId = %s
        """
        conn = None
        cursor = None

        try:
            # Start transaction
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()

            # Update BakedGoods
            bakedgoods_data = (
                bakedgood.name,
                bakedgood.shelf_Life,
                bakedgood.allergen_Info,
                bakedgood.category_id,
                bakedgood.bakedGood_id
            )
            print("Updating BakedGoods with:", bakedgoods_data)
            cursor.execute(bakedgoods_query, bakedgoods_data)

            # Update NutritionFacts
            nutrition_data = (
                bakedgood.calories,
                bakedgood.carbs,
                bakedgood.protein,
                bakedgood.fat,
                bakedgood.sugar,
                bakedgood.bakedGood_id
            )

            cursor.execute(nutrition_query, nutrition_data)

            # Commit the transaction
            conn.commit()
            return True

        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"Failed to update baked good and nutrition facts: {str(e)}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    
    @staticmethod
    def delete(bakedGoods_id: int) -> bool:
        """DELETE - Remove bakedGood from database"""
        query = "DELETE FROM BakedGoods WHERE bakedgoodsId = %s"
        try:
            DatabaseManager.execute_query(query, (bakedGoods_id,))
            return True
        except Exception as e:
            raise Exception(f"Failed to delete bakedGood: {str(e)}")
    
    @staticmethod
    def search(column: str, search_term: str) -> List[BakedGoods]:
        """SEARCH - Find bakedGoods by column and search term"""
        # Valid searchable columns (security measure)
        valid_columns = {
            "name": "name",
            "category": "categoryId",
            "price_per_weight": "price_per_weight",
            "calories": "calories",
            "carbs": "carbs",
            "protein": "protein",
            "fat": "fat",
            "sugar": "sugar",
            "allergen_info": "allergen_Info",
            "shelf_life": "shelf_Life"
        }
        
        if column.lower() not in valid_columns:
            raise Exception(f"Invalid search column: {column}")
        
        db_column = valid_columns[column.lower()]
        
        # Use parameterized query to prevent SQL injection
        query = f"""
        SELECT 
            bg.bakedGoodsid as bakedGood_id,
            bg.name,
            c.category,
            c.categoryid as category_id,
            nf.nutritionfactsid as nutritionfacts_id,
            c.Priceperweight as price_per_weight,
            nf.calories,
            nf.carbs,
            nf.protein,
            nf.fat,
            nf.sugar ,
            bg.AllergenInfo as allergen_Info,
            bg.lifetime as shelf_Life
        FROM
            BakedGoods bg
        JOIN
            Categories c ON bg.category_id = c.category_id
        JOIN
            NutritionFacts nf ON bg.nutritionfacts_id = nf.nutritionfacts_id
        WHERE
            {db_column} ILIKE %s
        """
        
        try:
            search_pattern = f"%{search_term}%"
            rows = DatabaseManager.execute_query(query, (search_pattern,), fetch=True)
            return [BakedGoods.from_db_row(row) for row in rows]
        except Exception as e:
            raise Exception(f"Search failed: {str(e)}")
    
    @staticmethod
    def get_all_categories() -> list[tuple[int, str]]:
        """שליפת מזהים ושמות של כל הקטגוריות"""
        query = "SELECT categoryId, name FROM Categories"
        return DatabaseManager.execute_query(query, fetch=True)

class BakedGoodsService:
    """Business Logic Layer - handles business rules and validation"""
    
    def __init__(self):
        self.repository = BakedGoodsRepository()
    
    def validate_bakedGood_data(self, bakedgood: BakedGoods) -> List[str]:
        """Validate bakedGood data and return list of errors"""
        errors = []
        
        if not bakedgood.name:
            errors.append("שם המוצר לא יכול להיות ריק")
        if not bakedgood.category_id:
            errors.append("יש לבחור קטגוריה למוצר") 
        if not bakedgood.calories or bakedgood.calories < 0:
            errors.append("קלוריות חייבות להיות מספר לא שלילי")
        if not bakedgood.carbs or bakedgood.carbs < 0:
            errors.append("פחמימות חייבות להיות מספר לא שלילי")
        if not bakedgood.protein or bakedgood.protein < 0:
            errors.append("חלבון חייב להיות מספר לא שלילי")
        if not bakedgood.fat or bakedgood.fat < 0:
            errors.append("שומן חייב להיות מספר לא שלילי")
        if not bakedgood.sugar or bakedgood.sugar < 0:
            errors.append("סוכר חייב להיות מספר לא שלילי")
        if not bakedgood.shelf_Life or bakedgood.shelf_Life < 0:
            errors.append("חיי מדף חייבים להיות מספר לא שלילי")
        if not bakedgood.allergen_Info:
            errors.append("יש למלא מידע על אלרגנים")
        if len(bakedgood.name) > 100:
            errors.append("שם המוצר לא יכול להיות ארוך מ-100 תווים")
        
        return errors
    
    def create_bakedGood(self, bakedgood: BakedGoods) -> bool:
        """Create new bakedGood with validation"""
        errors = self.validate_bakedGood_data(bakedgood)
        if errors:
            raise Exception("Validation errors:\n" + "\n".join(errors))
        print(bakedgood.to_bakedgoods_tuple())
        return self.repository.create(bakedgood)
    
    def get_all_bakedGoods(self) -> List[BakedGoods]:
        """Get all bakedGoods"""
        return self.repository.read_all()
    
    def get_bakedGood_by_id(self, bakedGood_id: int) -> Optional[BakedGoods]:
        """Get bakedGood by ID"""
        return self.repository.read_by_id(bakedGood_id)
    
    def update_bakedGood(self, bakedGood: BakedGoods) -> bool:
        """Update bakedGood with validation"""
        errors = self.validate_bakedGood_data(bakedGood)
        if errors:
            raise Exception("Validation errors:\n" + "\n".join(errors))
        
        return self.repository.update(bakedGood)
    
    def delete_bakedGood(self, bakedGood_id: int) -> bool:
        """Delete bakedGood by ID"""
        return self.repository.delete(bakedGood_id)
    
    def search_bakedGoods(self, column: str, search_term: str) -> List[BakedGoods]:
        """Search bakedGoods"""
        if not search_term.strip():
            return self.get_all_bakedGoods()
        
        return self.repository.search(column, search_term)

    def get_search_columns(self) -> Dict[str, str]:
        """Get available search columns with Hebrew labels"""
        column_mapping = {
            "name": "שם מוצר",
            "category": "קטגוריה",
            "calories": "קלוריות",
            "carbs": "פחמימות",
            "protein": "חלבון",
            "fat": "שומן",
            "sugar": "סוכר",
            "allergen_Info": "מידע על אלרגנים",
            "shelf_Life": "חיי מדף"
        }
        return column_mapping
    
    def get_categories(self) -> list[tuple[int, str]]:
        rows = BakedGoodsRepository.get_all_categories()
        return [(int(row[0]), row[1]) for row in rows]



    def get_category_id_by_name(self, name: str) -> int | None:
        """מחזיר את מזהה הקטגוריה לפי השם שלה"""
        return self.category_name_to_id.get(name)
    

class BakedGoodsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ניהול מוצרי מאפה")
        self.geometry("1200x800")
        self.configure(bg="#f5f5f5")
        self.resizable(True, True)

        # Configure style
        self.setup_styles()
        
        # Initialize service layer
        self.bakedGood_service = BakedGoodsService()
        self.selected_bakedGood: Optional[BakedGoods] = None
        self.mode = None  # 'add' or 'update'
        
        # Initialize UI
        self.setup_ui()
        self.load_bakedGoods()

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
        title = ttk.Label(main_container, text="🍞 מערכת ניהול מוצרים - מאפייה", 
                         style='Title.TLabel')
        title.pack(pady=(0, 20))
        
        # Top section (search and actions)
        top_frame = ttk.Frame(main_container)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search frame
        self.setup_search_frame(top_frame)
        
        # Action buttons
        self.setup_action_buttons(top_frame)
        
        # Main content frame
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - BakedGood list
        left_frame = ttk.LabelFrame(content_frame, text="רשימת מוצרי מאפה", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # BakedGood tree
        self.setup_bakedGood_tree(left_frame)
        
        # Right side - BakedGood form (initially hidden)
        self.setup_bakedGood_form(content_frame)


    def setup_search_frame(self, parent):
        """Setup search controls"""
        search_frame = ttk.LabelFrame(parent, text="חיפוש מוצרי מאפה", padding=10)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Get search columns
        try:
            self.column_mapping = self.bakedGood_service.get_search_columns()
        except Exception as e:
            messagebox.showerror("שגיאה", f"Error loading search columns: {str(e)}")
            self.column_mapping = {}
        
        # Search controls frame
        controls_frame = ttk.Frame(search_frame)
        controls_frame.pack(fill=tk.X)
        
        # Search by label
        ttk.Label(controls_frame, text="חפש לפי:", style='Heading.TLabel').grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        
        # Search column selector
        self.search_by_var = tk.StringVar()
        self.search_menu = ttk.Combobox(
            controls_frame,
            textvariable=self.search_by_var,
            values=list(self.column_mapping.values()),
            state="readonly",
            width=15,
            font=('Arial', 10)
        )
        self.search_menu.grid(row=0, column=1, padx=(0, 10))
        if self.column_mapping:
            self.search_by_var.set(list(self.column_mapping.values())[0])
        
        # Search entry
        ttk.Label(controls_frame, text="מחרוזת חיפוש:", style='Heading.TLabel').grid(row=0, column=2, padx=(10, 5), sticky=tk.W)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(controls_frame, textvariable=self.search_var, width=25, font=('Arial', 10))
        self.search_entry.grid(row=0, column=3, padx=(0, 10))
        
        # Bind Enter key to search
        self.search_entry.bind('<Return>', lambda e: self.search_bakedGoods())
        
        # Search buttons
        btn_frame = ttk.Frame(controls_frame)
        btn_frame.grid(row=0, column=4, padx=10)
        
        ttk.Button(btn_frame, text="🔍 חפש", command=self.search_bakedGoods, style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="🗑️ נקה", command=self.clear_search, style='Action.TButton').pack(side=tk.LEFT)

    def setup_action_buttons(self, parent):
            """Setup action buttons"""
            btn_frame = ttk.LabelFrame(parent, text="פעולות", padding=10)
            btn_frame.pack(fill=tk.X)
            
            buttons_container = ttk.Frame(btn_frame)
            buttons_container.pack()
            
            ttk.Button(buttons_container, text="➕ הוסף מוצר", command=self.show_add_form, style='Primary.TButton').grid(row=0, column=0, padx=5)
            ttk.Button(buttons_container, text="✏️ עדכן מוצר", command=self.show_update_form, style='Action.TButton').grid(row=0, column=1, padx=5)
            ttk.Button(buttons_container, text="🗑️ מחק מוצר", command=self.delete_bakedGood, style='Danger.TButton').grid(row=0, column=2, padx=5)
            ttk.Button(buttons_container, text="🔄 רענן", command=self.refresh_screen, style='Action.TButton').grid(row=0, column=3, padx=5)
    

    def setup_bakedGood_tree(self, parent):
            """Setup bakedGood display tree"""
            # Create frame for tree and scrollbars
            tree_frame = ttk.Frame(parent)
            tree_frame.pack(fill=tk.BOTH, expand=True)
            
            columns = ( "name", "category", "price_per_weight", "calories", "carbs", "protein", "fat", "sugar", "allergen_Info", "shelf_Life")
            hebrew_headers = [ "שם מוצר", "קטגוריה", "מחיר ליחידה", "קלוריות", "פחמימות", "חלבון", "שומן", "סוכר", "מידע על אלרגנים", "חיי מדף"]
            
            self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20, style='Custom.Treeview')
            
            # Configure columns
            column_widths = [120, 50, 50, 50, 50, 50, 50, 50, 120, 50]
            total_width = sum(column_widths)
            for col, header, width in zip(columns, hebrew_headers, column_widths):
                self.tree.heading(col, text=header)
                self.tree.column(col, anchor='center',stretch=True, width=int((width / total_width) * total_width))  # Adjust width based on total width
        

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
            self.tree.bind('<<TreeviewSelect>>', self.on_bakedGood_select)
            
            # Add alternating row colors
            self.tree.tag_configure('oddrow', background='#f9f9f9')
            self.tree.tag_configure('evenrow', background='#ffffff')


    def setup_bakedGood_form(self, parent):
        self.form_frame = ttk.LabelFrame(parent, text="פרטי מוצר", padding=15)

        # טען קטגוריות (למפה שם ↔ ID)
        try:
            self.categories = self.bakedGood_service.get_categories()
            self.category_name_to_id = {name: id for id, name in self.categories}
            category_names = list(self.category_name_to_id.keys())
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בטעינת קטגוריות: {str(e)}")
            self.category_name_to_id = {}
            category_names = []

        labels = ["שם מוצר", "קטגוריה", "קלוריות", "פחמימות", "חלבון", "שומן", "סוכר", "מידע על אלרגנים", "חיי מדף"]
        self.entries = {}

        for i, label in enumerate(labels):
            # Label
            label_widget = ttk.Label(self.form_frame, text=label, style='Heading.TLabel')
            label_widget.grid(row=i, column=0, sticky=tk.W, pady=8, padx=(0, 10))

            # קטגוריה כקומבובוקס
            if i == 1:  # Category is the second item (index 1)
                self.category_combobox = ttk.Combobox(
                    self.form_frame,
                    values=category_names,
                    state="readonly",
                    font=('Arial', 10),
                    width=28
                )
                self.category_combobox.grid(row=i, column=1, pady=8, padx=(0, 10), sticky=tk.W)
                
                # Set default value
                if category_names:
                    self.category_combobox.set(category_names[0])
                
                # Store reference for easy access
                self.entries[label] = self.category_combobox
            else:
                # שאר השדות
                entry = ttk.Entry(self.form_frame, width=30, font=('Arial', 10))
                entry.grid(row=i, column=1, pady=8, padx=(0, 10), sticky=tk.W)
                self.entries[label] = entry

        # כפתורים
        button_frame = ttk.Frame(self.form_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=20)

        self.save_button = ttk.Button(button_frame, text="💾 שמור", command=self.save_bakedGood, style='Primary.TButton')
        self.save_button.grid(row=0, column=0, padx=(0, 10))

        ttk.Button(button_frame, text="❌ ביטול", command=self.cancel_form, style='Action.TButton').grid(row=0, column=1)

        # טופס מוסתר בהתחלה
        self.form_frame.pack_forget()


    def load_bakedGoods(self):
        """Load and display all bakedGoods"""
        try:
            bakedGoods = self.bakedGood_service.get_all_bakedGoods()
            self.display_bakedGoods(bakedGoods)
        except Exception as e:
            messagebox.showerror("שגיאה", f"Error loading bakedGoods: {str(e)}")
    
    def display_bakedGoods(self, bakedGoods: List[BakedGoods]):
        """Display bakedGoods in tree with alternating colors"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add bakedGoods to tree with alternating colors
        for i, bakedGood in enumerate(bakedGoods):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', 
                            iid=bakedGood.bakedGood_id,
                            values=bakedGood.to_display_tuple(),
                            tags=(tag,))  
        


    def search_bakedGoods(self):
        """Search for bakedGoods"""
        search_term = self.search_var.get().strip()
        search_column_hebrew = self.search_by_var.get()
        
        # Find English column name
        search_column_english = None
        for eng, heb in self.column_mapping.items():
            if heb == search_column_hebrew:
                search_column_english = eng
                break
        
        if not search_column_english:
            messagebox.showerror("שגיאה", "Invalid search column selected")
            return
        
        try:
            bakedGoods = self.bakedGood_service.search_bakedGoods(search_column_english, search_term)
            self.display_bakedGoods(bakedGoods)
            
            # Show search results info
            status_text = f"נמצאו {len(bakedGoods)} מוצרים"
            if search_term:
                status_text += f" עבור '{search_term}'"
            
            # Update window title to show search results
            self.title(f"ניהול מוצרים - מאפייה ({status_text})")
            
        except Exception as e:
            messagebox.showerror("שגיאה", f"Search error: {str(e)}")
    


    def clear_search(self):
        """Clear search and show all bakedGoods"""
        self.search_var.set("")
        self.title("ניהול מוצרים - מאפייה")
        self.load_bakedGoods()

    def on_bakedGood_select(self, event):
        """Handle bakedGood selection"""
        selection = self.tree.selection()
        if not selection:
            self.selected_bakedGood = None
            return
        
        bakedGood_id = int(selection[0])
        try:
            self.selected_bakedGood = self.bakedGood_service.get_bakedGood_by_id(bakedGood_id)
            if self.selected_bakedGood and self.form_frame.winfo_ismapped():
                self.populate_form(self.selected_bakedGood)
        except Exception as e:
            messagebox.showerror("שגיאה", f"Error loading bakedGood details: {str(e)}")



    def populate_form(self, bakedGood: BakedGoods):
        """Populate form with bakedGood data"""
        values = [
            bakedGood.name, 
            bakedGood.category,
            bakedGood.calories,
            bakedGood.carbs,
            bakedGood.protein,
            bakedGood.fat,
            bakedGood.sugar,
            bakedGood.allergen_Info,
            bakedGood.shelf_Life
        ]
        labels = [ "שם מוצר", "קטגוריה", "קלוריות", "פחמימות", "חלבון", "שומן", "סוכר", "מידע על אלרגנים", "חיי מדף"]
        
        for label, value in zip(labels, values):
            entry = self.entries[label]
            entry.delete(0, tk.END)
            entry.insert(0, value)   
    
    def clear_form(self):
        """Clear all form fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def show_add_form(self):
        """Show form for adding new bakedGood"""
        self.clear_form()
        self.mode = 'add'
        self.save_button.config(text="➕ הוסף מוצר")
        self.form_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

    def show_update_form(self):
        """Show form for updating bakedGood"""
        if not self.selected_bakedGood:
            messagebox.showwarning("שגיאה", "אנא בחר מוצר לעדכון")
            return
        
        self.mode = 'update'
        self.save_button.config(text="✏️ עדכן מוצר")
        self.populate_form(self.selected_bakedGood)
        self.form_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

    def cancel_form(self):
        """Cancel form operation"""
        self.form_frame.pack_forget()
        self.clear_form()
        self.mode = None
 


    def save_bakedGood(self):
        """Save bakedGood (add or update)"""
        try:
            # Get form data
            labels = ["שם מוצר", "קטגוריה", "קלוריות", "פחמימות", "חלבון", "שומן", "סוכר", "מידע על אלרגנים", "חיי מדף"]
            values = []
            
            # Get values from entries, but handle category specially
            for label in labels:
                if label == "קטגוריה":
                    # Get category directly from the combobox
                    category_name = self.category_combobox.get()
                    values.append(category_name)
                else:
                    values.append(self.entries[label].get().strip())
            
            # Get category ID from the selected name
            category_name = values[1]  # Category is at index 1
            category_id = self.category_name_to_id.get(category_name)

            print(f"DEBUG: Selected category name: '{category_name}'")
            print(f"DEBUG: Mapped category ID: {category_id}")

            if not category_id:
                messagebox.showerror("שגיאה", "יש לבחור קטגוריה")
                return

            # Create bakedGood object
            bakedGood = BakedGoods(
                name=values[0],
                category_id=category_id,
                calories=float(values[2]) if values[2] else 0.0,
                carbs=float(values[3]) if values[3] else 0.0,
                protein=float(values[4]) if values[4] else 0.0,
                fat=float(values[5]) if values[5] else 0.0,
                sugar=float(values[6]) if values[6] else 0.0,
                allergen_Info=values[7],
                shelf_Life=int(values[8]) if values[8].isdigit() else 0
            )
            
            # Set bakedGood ID for updates
            if self.mode == 'update' and self.selected_bakedGood:
                bakedGood.bakedGood_id = self.selected_bakedGood.bakedGood_id
            
            # Save bakedGood
            if self.mode == 'add':
                self.bakedGood_service.create_bakedGood(bakedGood)
                messagebox.showinfo("הצלחה", "✅ המוצר נוסף בהצלחה!")
            elif self.mode == 'update':
                self.bakedGood_service.update_bakedGood(bakedGood)
                messagebox.showinfo("הצלחה", "✅ פרטי המוצר עודכנו בהצלחה!")
            
            # Refresh and hide form
            self.load_bakedGoods()
            self.cancel_form()
            
        except Exception as e:
            print(f"Error in save_bakedGood: {str(e)}")
            messagebox.showerror("שגיאה", f"שגיאה בשמירת המוצר: {str(e)}")



    def delete_bakedGood(self):
        """Delete selected bakedGood"""
        if not self.selected_bakedGood:
            messagebox.showwarning("שגיאה", "אנא בחר מוצר למחיקה")
            return
        
        # Confirm deletion
        result = messagebox.askyesno("אישור מחיקה", 
                                    f"האם אתה בטוח שברצונך למחוק את {self.selected_bakedGood.name}?\n"
                                    f"פעולה זו לא ניתנת לביטול.")
        if not result:
            return
        
        try:
            self.bakedGood_service.delete_bakedGood(self.selected_bakedGood.bakedGood_id)
            messagebox.showinfo("הצלחה", "✅ המוצר נמחק בהצלחה!")
            self.load_bakedGoods()
            self.cancel_form()
            self.selected_bakedGood = None
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה במחיקה: {str(e)}")
    
    def refresh_screen(self):
        """Refresh the entire screen"""
        self.cancel_form()
        self.clear_search()
        self.selected_bakedGood = None
        self.title("ניהול מוצרים - מאפייה")

# Note: This module is designed to be imported and used from a main menu
# The BakedGoodדApp class should be instantiated from the calling module
