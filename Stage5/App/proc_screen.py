import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class ProduceApp:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("הרצת ייצור לפי סניף")
        self.window.geometry("520x650")
        self.window.configure(bg="#f0f4f8")

        tk.Label(
            self.window,
            text="הרצת ייצור למוצר מאפה",
            font=("Segoe UI", 18, "bold"),
            fg="#2c3e50",
            bg="#f0f4f8"
        ).pack(pady=20)

        try:
            conn = psycopg2.connect(
                dbname="BAKERY_DB",
                user="postgres",
                password="Rcev9768!",
                host="localhost",
                port="5432"
            )
            cur = conn.cursor()

            cur.execute("SELECT branchId, location FROM Branches ORDER BY location;")
            branch_rows = cur.fetchall()

            cur.execute("SELECT bakedGoodsId, name FROM BakedGoods ORDER BY name;")
            baked_rows = cur.fetchall()

        except Exception as e:
            messagebox.showerror("שגיאת מסד נתונים", str(e))
            return
        finally:
            cur.close()
            conn.close()

        self.cmb_branch = self.create_combobox("בחר סניף:", branch_rows, self.on_branch_selected)
        self.cmb_employee = self.create_combobox("בחר עובד:", [])
        self.cmb_baked = self.create_combobox("בחר מוצר אפייה:", baked_rows)

        tk.Button(
            self.window,
            text="↻ בדוק חומרים למוצר",
            font=("Segoe UI", 9),
            bg="#3498db", fg="white",
            command=self.show_materials_summary
        ).pack(pady=5)

        self.entry_quantity = self.create_input("כמות לייצור:")

        tk.Button(
            self.window,
            text="✅ הרץ ייצור",
            command=self.validate_and_submit,
            font=("Segoe UI", 12, "bold"),
            bg="#27ae60", fg="white",
            activebackground="#219150",
            relief="flat",
            width=20, height=2
        ).pack(pady=20)

    def create_combobox(self, label_text, rows, callback=None):
        frame = tk.Frame(self.window, bg="#f0f4f8")
        frame.pack(pady=8, padx=30, fill="x")

        tk.Label(frame, text=label_text, font=("Segoe UI", 10), bg="#f0f4f8", fg="#5d6d7e")\
            .pack(side="right", padx=8)

        values = [f"{row[0]} - {row[1]}" for row in rows]
        cmb = ttk.Combobox(frame, values=values, font=("Segoe UI", 11), state="readonly", width=30, justify="right")
        cmb.pack(side="right")
        cmb.selected_map = {v: r[0] for v, r in zip(values, rows)}

        if callback:
            cmb.bind("<<ComboboxSelected>>", callback)
        return cmb

    def create_input(self, label_text):
        frame = tk.Frame(self.window, bg="#f0f4f8")
        frame.pack(pady=8, padx=30, fill="x")

        tk.Label(frame, text=label_text, font=("Segoe UI", 10), bg="#f0f4f8", fg="#5d6d7e")\
            .pack(side="right", padx=8)

        entry = tk.Entry(frame, font=("Segoe UI", 11), justify="right", relief="solid", bd=1, width=25)
        entry.pack(side="right")
        return entry

    def on_branch_selected(self, event=None):
        selected_text = self.cmb_branch.get()
        if not selected_text:
            return
        branch_id = self.cmb_branch.selected_map[selected_text]

        try:
            conn = psycopg2.connect(
                dbname="BAKERY_DB",
                user="postgres",
                password="Rcev9768!",
                host="localhost",
                port="5432"
            )
            cur = conn.cursor()
            cur.execute("SELECT employeeId, name FROM Employee WHERE branchId = %s ORDER BY name;", (branch_id,))
            rows = cur.fetchall()
        except Exception as e:
            messagebox.showerror("שגיאה בטעינת עובדים", str(e))
            return
        finally:
            cur.close()
            conn.close()

        values = [f"{r[0]} - {r[1]}" for r in rows]
        self.cmb_employee["values"] = values
        self.cmb_employee.set("")
        self.cmb_employee.selected_map = {v: r[0] for v, r in zip(values, rows)}

    def validate_and_submit(self):
        has_error = False
        widgets = [self.cmb_branch, self.cmb_employee, self.cmb_baked]

        for widget in widgets:
            if not widget.get():
                widget.configure(background="#ffdddd")
                has_error = True
            else:
                widget.configure(background="white")

        if not self.entry_quantity.get().strip():
            self.entry_quantity.configure(bg="#ffe6e6")
            has_error = True
        else:
            self.entry_quantity.configure(bg="white")

        if has_error:
            messagebox.showwarning("שגיאה", "יש למלא/לבחור את כל השדות.")
            return

        try:
            branch_id = self.cmb_branch.selected_map[self.cmb_branch.get()]
            employee_id = self.cmb_employee.selected_map[self.cmb_employee.get()]
            baked_id = self.cmb_baked.selected_map[self.cmb_baked.get()]
            quantity = int(self.entry_quantity.get())
        except:
            messagebox.showerror("שגיאה", "נתונים לא תקינים")
            return

        self.produce_batch(baked_id, quantity, employee_id, branch_id)



# להאזין ל־NOTICES
    def produce_batch(self, baked_id, quantity, employee_id, branch_id):
        try:
            conn = psycopg2.connect(
                dbname="BAKERY_DB",
                user="postgres",
                password="Rcev9768!",
                host="localhost",
                port="5432"
 )
            cur = conn.cursor()
            conn.set_isolation_level(0)  # חשוב: לקבל NOTICE בזמן אמת

            cur.execute("CALL produce_batch(%s, %s, %s, %s);", (baked_id, quantity, employee_id, branch_id))
            conn.commit()

        # בדיקת הודעות NOTICE
            for notice in conn.notices:
                if "Production failed" in notice:
                    messagebox.showwarning( notice)
                    self.show_material_input(branch_id)
                    return

            messagebox.showinfo("הצלחה", "✅ הייצור בוצע בהצלחה!")
            if hasattr(self, "material_frame"):
                self.material_frame.destroy()

        except Exception as e:
            messagebox.showerror("שגיאת פרוצדורה", str(e))
        finally:
            cur.close()
            conn.close()

    def show_material_input(self, branch_id):
        if hasattr(self, "material_frame"):
            self.material_frame.destroy()

        self.material_frame = tk.Frame(self.window, bg="#e8f0fe", bd=1, relief="solid")
        self.material_frame.pack(pady=15, padx=30, fill="x")

        tk.Label(self.material_frame, text="השלמת מלאי חסר", font=("Segoe UI", 12, "bold"),
                 bg="#e8f0fe", fg="#2c3e50").pack(pady=10)

        try:
            conn = psycopg2.connect(
                dbname="BAKERY_DB",
                user="postgres",
                password="Rcev9768!",
                host="localhost",
                port="5432"
            )
            cur = conn.cursor()
            cur.execute("""SELECT * FROM RawMaterials;""")
            rows = cur.fetchall()
        except Exception as e:
            messagebox.showerror("שגיאת טעינה", str(e))
            return
        finally:
            cur.close()
            conn.close()

        values = [f"{r[0]} - {r[1]}" for r in rows]
        self.cmb_material = ttk.Combobox(self.material_frame, values=values, font=("Segoe UI", 10), state="readonly", width=30)
        self.cmb_material.pack(pady=5)
        self.cmb_material.selected_map = {v: r[0] for v, r in zip(values, rows)}

        self.entry_amount = tk.Entry(self.material_frame, font=("Segoe UI", 10), width=15, justify="center")
        self.entry_amount.pack(pady=5)

        tk.Button(
            self.material_frame,
            text="➕ הוסף מלאי",
            font=("Segoe UI", 10, "bold"),
            bg="#2980b9", fg="white",
            command=lambda: self.insert_material(branch_id)
        ).pack(pady=10)

    def insert_material(self, branch_id):
        material_key = self.cmb_material.get()
        amount = self.entry_amount.get()

        if not material_key or not amount:
            messagebox.showwarning("שגיאה", "יש לבחור חומר ולהזין כמות")
            return

        try:
            material_id = self.cmb_material.selected_map[material_key]
            amount = float(amount)
        except:
            messagebox.showerror("שגיאה", "כמות לא תקינה")
            return

        try:
            conn = psycopg2.connect(
                dbname="BAKERY_DB",
                user="postgres",
                password="Rcev9768!",
                host="localhost",
                port="5432"
            )
            cur = conn.cursor()
            cur.execute("SELECT name, unitofmeasurement FROM rawmaterials WHERE RawMaterialsId = %s", (material_id,))
            result = cur.fetchone()
            if result:
                name, unit = result
            cur.execute("""
            SELECT 1 FROM rawmaterials WHERE RawMaterialsId = %s AND branchId = %s
        """, (material_id, branch_id))
            exists = cur.fetchone()

            if exists:
            # אם קיים – עדכון כמות
                cur.execute("""
                UPDATE rawmaterials
                SET quantity = quantity + %s
                WHERE RawMaterialsId = %s AND branchId = %s
            """, (amount, material_id, branch_id))
            else:
            # אם לא קיים – הכנס חומר חדש עם ID חדש
                cur.execute("SELECT MAX(RawMaterialsId) + 1 FROM rawmaterials")
                new_id = cur.fetchone()[0] or 1

                cur.execute("""
                INSERT INTO rawmaterials (RawMaterialsId, name, unitofmeasurement, quantity, branchId)
                VALUES (%s, %s, %s, %s, %s)
            """, (new_id, name, unit, amount, branch_id))
                
                cur.execute(""" UPDATE recipe
                SET rawmaterialsid = %s
                WHERE RawMaterialsId = %s """,(new_id, material_id))

            conn.commit()
            messagebox.showinfo("עודכן", "הכמות עודכנה בהצלחה!")
            self.material_frame.destroy()
        except Exception as e:
            messagebox.showerror("שגיאה בעדכון", str(e))
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def show_materials_summary(self):
        if not self.cmb_baked.get():
            messagebox.showwarning("שגיאה", "יש לבחור מוצר אפייה תחילה.")
            return

        baked_id = self.cmb_baked.selected_map[self.cmb_baked.get()]

        try:
            conn = psycopg2.connect(
                dbname="BAKERY_DB",
                user="postgres",
                password="Rcev9768!",
                host="localhost",
                port="5432"
            )
            cur = conn.cursor()
            cur.execute("BEGIN;")
            cur.callproc("get_materials_summary_for_product", [baked_id,'ref'])
            cur.execute("FETCH ALL FROM ref;")
            rows = cur.fetchall()
            cur.execute("COMMIT;")
        except Exception as e:
            messagebox.showerror("שגיאה בשליפת סיכום", str(e))
            return
        finally:
            cur.close()
            conn.close()

        if hasattr(self, "summary_frame"):
            self.summary_frame.destroy()

        self.summary_frame = tk.Frame(self.window, bg="#fefefe", bd=1, relief="solid")
        self.summary_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(self.summary_frame, text="סיכום חומרים נדרשים", font=("Segoe UI", 11, "bold"),
                 bg="#fefefe", fg="#2c3e50").pack(pady=5)

        for name, required, available, status in rows:
            color = "#2ecc71" if status == "OK" else "#e74c3c"
            status_text = f"{status} ✅" if status == "OK" else f"{status} ⚠️"
            row_text = f"{name} | נדרש: {required} | זמין: {available} | מצב: {status_text}"

            tk.Label(self.summary_frame, text=row_text, font=("Segoe UI", 10),
                     bg="#fefefe", fg=color, anchor="w", justify="right").pack(anchor="w", padx=10)