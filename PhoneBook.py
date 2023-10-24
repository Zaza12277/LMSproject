import tkinter as tk
from tkinter import ttk
import sqlite3

class EmployeeDatabase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                phone TEXT,
                email TEXT,
                salary REAL
            )
        ''')
        self.conn.commit()

    def insert_employee(self, name, phone, email, salary):
        self.cur.execute('''
            INSERT INTO employees (name, phone, email, salary)
            VALUES (?, ?, ?, ?)
        ''', (name, phone, email, salary))
        self.conn.commit()

    def update_employee(self, employee_id, name, phone, email, salary):
        self.cur.execute('''
            UPDATE employees
            SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?
        ''', (name, phone, email, salary, employee_id))
        self.conn.commit()

    

    def delete_employee(self, employee_id):
        self.cur.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        self.conn.commit()

    def search_employees(self, keyword):
        self.cur.execute('''
            SELECT * FROM employees
            WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
        ''', ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
        return self.cur.fetchall()

    def get_all_employees(self):
        self.cur.execute('SELECT * FROM employees')
        return self.cur.fetchall()

    def __del__(self):
        self.conn.close()

class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Employee Management App')
        self.db = EmployeeDatabase('employee.db')

        self.create_ui()

    def create_ui(self):
        self.tree = ttk.Treeview(self.root, columns=('ID', 'Name', 'Phone', 'Email', 'Salary'))
        self.tree.heading('#1', text='ID')
        self.tree.heading('#2', text='Name')
        self.tree.heading('#3', text='Phone')
        self.tree.heading('#4', text='Email')
        self.tree.heading('#5', text='Salary')
        self.tree.pack()

        self.refresh_button = tk.Button(self.root, text='Перезагрузить', command=self.refresh_data)
        self.refresh_button.pack()

        self.add_button = tk.Button(self.root, text='Добавить данные Сотрудника', command=self.open_add_employee_dialog)
        self.add_button.pack()

        self.edit_button = tk.Button(self.root, text='Редактировать данные Сотрудника', command=self.open_edit_employee_dialog)
        self.edit_button.pack()

        self.delete_button = tk.Button(self.root, text='Удалить данные Сотрудника', command=self.delete_employee)
        self.delete_button.pack()

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()
        self.search_button = tk.Button(self.root, text='Search', command=self.search_employee)
        self.search_button.pack()

        self.refresh_data()

    def refresh_data(self):
        records = self.db.get_all_employees()
        self.populate_tree(records)

    def populate_tree(self, records):
        for record in self.tree.get_children():
            self.tree.delete(record)
        for row in records:
            self.tree.insert('', 'end', values=row)

    def open_add_employee_dialog(self):
        AddEmployeeDialog(self)

    def open_edit_employee_dialog(self):
        selected_item = self.tree.selection()
        if selected_item:
            employee_id = self.tree.item(selected_item)['values'][0]
            employee = self.db.get_employee_by_id(employee_id)
            if employee:
                EditEmployeeDialog(self, employee)

    def delete_employee(self):
        selected_item = self.tree.selection()
        if selected_item:
            employee_id = self.tree.item(selected_item)['values'][0]
            self.db.delete_employee(employee_id)
            self.refresh_data()

    def search_employee(self):
        keyword = self.search_entry.get()
        if keyword:
            results = self.db.search_employees(keyword)
            self.populate_tree(results)

class EmployeeDialog:
    def __init__(self, app, title):
        self.app = app
        self.dialog = tk.Toplevel()
        self.dialog.title(title)

        self.name_label = tk.Label(self.dialog, text='Name')
        self.name_label.pack()
        self.name_entry = tk.Entry(self.dialog)
        self.name_entry.pack()

        self.phone_label = tk.Label(self.dialog, text='Phone')
        self.phone_label.pack()
        self.phone_entry = tk.Entry(self.dialog)
        self.phone_entry.pack()

        self.email_label = tk.Label(self.dialog, text='Email')
        self.email_label.pack()
        self.email_entry = tk.Entry(self.dialog)
        self.email_entry.pack()

        self.salary_label = tk.Label(self.dialog, text='Salary')
        self.salary_label.pack()
        self.salary_entry = tk.Entry(self.dialog)
        self.salary_entry.pack()

        self.save_button = tk.Button(self.dialog, text='Save', command=self.save_employee)
        self.save_button.pack()

    def save_employee(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        salary = self.salary_entry.get()

        self.app.db.insert_employee(name, phone, email, salary)
        self.app.refresh_data()
        self.dialog.destroy()

class AddEmployeeDialog(EmployeeDialog):
    def __init__(self, app):
        super().__init__(app, 'Add Employee')

class EditEmployeeDialog(EmployeeDialog):
    def __init__(self, app, employee):
        super().__init__(app, 'Edit Employee')
        self.employee = employee
        self.fill_fields()

    def fill_fields(self):
        self.name_entry.insert(0, self.employee[1])
        self.phone_entry.insert(0, self.employee[2])
        self.email_entry.insert(0, self.employee[3])
        self.salary_entry.insert(0, self.employee[4])





if __name__ == '__main__':
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()