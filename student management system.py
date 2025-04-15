import pickle
import os
import uuid
import csv
import sys
from colorama import init, Fore, Style
from pyfiglet import Figlet
from prettytable import PrettyTable

# Initialize colorama for auto-resetting color styles
init(autoreset=True)
f = Figlet(font='slant')  # ASCII art text

# Base User class with consistent attributes
class User:
    def __init__(self, username, role, email, password, phone_number, grade=None, eca=None):
        self.username = username
        self.role = role
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.grade = grade
        self.eca = eca

    def display_user_info(self):
        print(f'\nUsername: {self.username}\nRole: {self.role}\nEmail: {self.email}\nPhone Number: {self.phone_number}')
        if self.grade:
            print(f'Grade: {self.grade}')
        if self.eca:
            print(f'ECA: {self.eca}')

    @staticmethod
    def create_empty_files():
        file_names = ['users.txt', 'grades.txt', 'eca.txt', 'students.txt', 'users.csv']
        for file_name in file_names:
            if not os.path.exists(file_name):
                with open(file_name, 'w') as file:
                    if file_name == 'users.csv' and os.path.getsize(file_name) == 0:
                        writer = csv.writer(file)
                        writer.writerow(['ID', 'Username', 'Role', 'Email', 'Password', 'Phone Number', 'Grades', 'ECA'])

# Admin class with enhanced functionality
class Admin(User):
    def __init__(self, username, role, email=None, password=None, phone_number=None, grade=None, eca=None):
        super().__init__(username, role, email, password, phone_number, grade, eca)
        print(Fore.BLUE + "Welcome To Admin Portal System")
    
    def register_user(self, username, role, email, password, phone_number, grades=None, eca=None):
        try:
            # Generate a unique user ID
            new_user_id = str(uuid.uuid4())[:8]

            # Create a list with user details
            new_user = [new_user_id, username, role, email, password, phone_number]
            
            # Add grades and ECA if provided
            if grades is not None:
                new_user.append(','.join(map(str, grades)) if isinstance(grades, list) else grades)
            else:
                new_user.append('')
                
            if eca is not None:
                new_user.append(','.join(map(str, eca)) if isinstance(eca, list) else eca)
            else:
                new_user.append('')

            # Append the user details to users.txt file
            with open('users.txt', 'a') as file:
                file.write(f"{username},{role},{email},{password},{phone_number}\n")

            # Append to CSV file
            with open("users.csv", "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(new_user)

            print(Fore.GREEN + f"User registered successfully with ID: {new_user_id}")
            return new_user_id
        except Exception as e:
            print(Fore.RED + f"Error registering user: {e}")
            return None

    def view_users(self, search_term=None):
        try:
            with open('users.txt', 'r') as file:
                lines = file.readlines()

            if search_term:
                found_users = []
                for line in lines:
                    user_data = line.strip().split(',')
                    if len(user_data) >= 3 and search_term.lower() in user_data[0].lower():
                        found_users.append(user_data)
                
                if not found_users:
                    print(Fore.RED + "No matching users found.")
                else:
                    print(Fore.BLUE + "Matching Users:")
                    table = PrettyTable(['Username', 'Role', 'Email', 'Password', 'Phone Number'])
                    for user in found_users:
                        if len(user) >= 5:
                            table.add_row(user[:5])
                    print(table)
            else:
                if not lines:
                    print(Fore.RED + "No users found.")
                else:
                    print(Fore.BLUE + "All Users:")
                    table = PrettyTable(['Username', 'Role', 'Email', 'Password', 'Phone Number'])
                    for line in lines:
                        user_data = line.strip().split(',')
                        if len(user_data) >= 5:
                            table.add_row(user_data[:5])
                    print(table)
        except FileNotFoundError:
            print(Fore.RED + "Users file not found. Creating empty file.")
            with open('users.txt', 'w') as file:
                pass

    def find_user_by_username(self, username_to_search):
        try:
            with open('users.txt', 'r') as file:
                lines = file.readlines()
                
                for line in lines:
                    user_data = line.strip().split(',')
                    if len(user_data) >= 1 and user_data[0] == username_to_search:
                        return user_data
            return None
        except FileNotFoundError:
            print(Fore.RED + "Users file not found.")
            return None

    def delete_user(self, username):
        try:
            with open('users.txt', 'r') as file:
                lines = file.readlines()

            found = False
            with open('users.txt', 'w') as file:
                for line in lines:
                    user_data = line.strip().split(',')
                    if len(user_data) >= 1 and user_data[0] != username:
                        file.write(line)
                    else:
                        found = True

            # Also remove from CSV file
            try:
                with open('users.csv', 'r', newline='') as file:
                    reader = csv.reader(file)
                    rows = list(reader)
                
                with open('users.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    for row in rows:
                        if len(row) >= 2 and row[1] != username:
                            writer.writerow(row)
            except Exception as e:
                print(Fore.YELLOW + f"Warning: Error updating CSV file: {e}")

            if found:
                print(Fore.GREEN + f"User '{username}' deleted successfully!")
            else:
                print(Fore.YELLOW + f"User '{username}' not found.")
        except FileNotFoundError:
            print(Fore.RED + "Users file not found.")

    @staticmethod
    def save_eca(username, eca_description):
        try:
            with open("eca.txt", "a") as file:
                file.write(f"{username},{eca_description}\n")
            print(Fore.GREEN + f"ECA saved successfully for user: {username}")
        except Exception as e:
            print(Fore.RED + f"Error saving ECA: {e}")
            
    @staticmethod
    def save_grade(username, grade):
        try:
            with open("grades.txt", "a") as file:
                file.write(f"{username},{grade}\n")
            print(Fore.GREEN + f"Grade saved successfully for user: {username}")
        except Exception as e:
            print(Fore.RED + f"Error saving grade: {e}")
    
    @staticmethod
    def save_student_info(student):
        try:
            # Update in users.txt
            with open('users.txt', 'r') as file:
                lines = file.readlines()
                
            with open('users.txt', 'w') as file:
                for line in lines:
                    user_data = line.strip().split(',')
                    if len(user_data) >= 5 and user_data[0] == student.username:
                        file.write(f"{student.username},{student.role},{student.email},{student.password},{student.phone_number}\n")
                    else:
                        file.write(line)
                        
            # Update in users.csv
            try:
                with open('users.csv', 'r', newline='') as file:
                    reader = csv.reader(file)
                    rows = list(reader)
                
                with open('users.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    for row in rows:
                        if len(row) >= 6 and row[1] == student.username:
                            # Update the row with new info
                            row[3] = student.email
                            row[5] = student.phone_number
                        writer.writerow(row)
            except Exception as e:
                print(Fore.YELLOW + f"Warning: Error updating CSV file: {e}")
                
            print(Fore.GREEN + "Student information updated successfully!")
        except Exception as e:
            print(Fore.RED + f"Error updating student info: {e}")

    def get_all_users(self):
        try:
            with open('users.txt', 'r') as file:
                lines = file.readlines()
            user_data_list = []
            for line in lines:
                user_data = line.strip().split(',')
                if len(user_data) >= 5:
                    user_data_list.append(user_data)
            return user_data_list
        except FileNotFoundError:
            print(Fore.RED + "Users file not found.")
            return []

# Student class with enhanced functionality
class Student(User):
    def __init__(self, username, role, email=None, password=None, phone_number=None, grade=None, eca=None):
        super().__init__(username, role, email, password, phone_number, grade, eca)
        self.grades = [grade] if grade and not isinstance(grade, list) else grade or []
        
    def display_user_info(self):
        super().display_user_info()
        print(Fore.GREEN + f"Grades: {','.join([str(g) for g in self.grades]) if self.grades else 'No Grades'}")
        print(Fore.GREEN + f"ECA: {self.eca}" if self.eca else "No ECA")

    @staticmethod
    def read_user_from_txt(username):
        try:
            with open('users.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    user_data = line.strip().split(',')
                    if len(user_data) >= 1 and user_data[0] == username:
                        return user_data
            return None
        except FileNotFoundError:
            print(Fore.RED + "Users file not found.")
            return None

    @staticmethod
    def read_user_from_csv(username):
        try:
            with open('users.csv', 'r') as file:
                reader = csv.reader(file)
                headers = next(reader, None)  # Skip the headers if they exist
                for user in reader:
                    if len(user) >= 2 and user[1] == username:
                        return user
            return None
        except FileNotFoundError:
            print(Fore.RED + "Users CSV file not found.")
            return None
        except Exception as e:
            print(Fore.RED + f"Error reading user from CSV: {e}")
            return None

    def view_eca(self):
        user_data_txt = self.read_user_from_txt(self.username)
        user_data_csv = self.read_user_from_csv(self.username)
        
        if user_data_txt or user_data_csv:
            if user_data_txt and len(user_data_txt) > 4:
                eca_txt = user_data_txt[4] if len(user_data_txt) > 4 else "No ECA"
                print(Fore.YELLOW + f"ECA (from txt file): {eca_txt}")
            
            if user_data_csv and len(user_data_csv) > 7:
                eca_csv = user_data_csv[7] if user_data_csv[7] else "No ECA"
                print(Fore.YELLOW + f"ECA (from csv file): {eca_csv}")
                
            # If no specific ECA data found, show the object's ECA
            if not user_data_txt and not user_data_csv:
                print(Fore.YELLOW + f"ECA: {self.eca if self.eca else 'No ECA'}")
        else:
            print(Fore.RED + "Error: Student data not found.")

    def view_grades(self):
        user_data_txt = self.read_user_from_txt(self.username)
        user_data_csv = self.read_user_from_csv(self.username)
        
        if user_data_txt or user_data_csv:
            if user_data_txt and len(user_data_txt) > 3:
                grades_txt = "No grades recorded"
                print(Fore.YELLOW + f"Grades (from txt file): {grades_txt}")
            
            if user_data_csv and len(user_data_csv) > 6:
                grades_csv = user_data_csv[6] if user_data_csv[6] else "No grades recorded"
                print(Fore.YELLOW + f"Grades (from csv file): {grades_csv}")
                
            # If no specific grades data found, show the object's grades
            if not user_data_txt and not user_data_csv:
                print(Fore.YELLOW + f"Grades: {','.join(map(str, self.grades)) if self.grades else 'No grades recorded'}")
        else:
            print(Fore.RED + "Error: Student data not found.")

    def update_profile(self, new_username, new_email, new_phone_number):
        old_username = self.username
        self.username = new_username
        self.email = new_email
        self.phone_number = new_phone_number
        
        # Update user information in the files
        try:
            # Update in users.txt
            updated = False
            with open('users.txt', 'r') as file:
                lines = file.readlines()
                
            with open('users.txt', 'w') as file:
                for line in lines:
                    user_data = line.strip().split(',')
                    if len(user_data) >= 5 and user_data[0] == old_username:
                        file.write(f"{new_username},{user_data[1]},{new_email},{user_data[3]},{new_phone_number}\n")
                        updated = True
                    else:
                        file.write(line)
                        
            # Update in users.csv
            try:
                with open('users.csv', 'r', newline='') as file:
                    reader = csv.reader(file)
                    rows = list(reader)
                
                with open('users.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    for row in rows:
                        if len(row) >= 6 and row[1] == old_username:
                            # Update the row with new info
                            row[1] = new_username
                            row[3] = new_email
                            row[5] = new_phone_number
                            updated = True
                        writer.writerow(row)
            except Exception as e:
                print(Fore.YELLOW + f"Warning: Error updating CSV file: {e}")
                
            if updated:
                print(Fore.GREEN + "Student details updated successfully!")
            else:
                print(Fore.YELLOW + "No matching student record found to update.")
        except Exception as e:
            print(Fore.RED + f"Error updating profile: {e}")

    def add_grade(self, grade):
        try:
            grade_value = int(grade)
            self.grades.append(grade_value)
            Admin.save_grade(self.username, grade_value)
            print(Fore.GREEN + f"Grade added: {grade_value}")
        except ValueError:
            print(Fore.RED + "Error: Please enter a valid Grade (Numeric Value)")
    
    def add_eca(self, eca_description):
        self.eca = eca_description
        Admin.save_eca(self.username, eca_description)
        print(Fore.GREEN + f"ECA added: {eca_description}")

# Function to create empty files if they don't exist
def create_empty_files():
    file_names = ['users.txt', 'grades.txt', 'eca.txt', 'students.txt', 'users.csv']
    for file_name in file_names:
        if not os.path.exists(file_name):
            with open(file_name, 'w') as file:
                if file_name == 'users.csv':
                    writer = csv.writer(file)
                    writer.writerow(['ID', 'Username', 'Role', 'Email', 'Password', 'Phone Number', 'Grades', 'ECA'])

# Function for user login process
def login():
    print(Fore.CYAN + f"\n{f.renderText('Login Portal')}")
    print(Fore.YELLOW + "1. Admin Login")
    print(Fore.YELLOW + "2. Student Login")
    print(Fore.RED + "3. Exit\n")
    
    choice = input(Fore.CYAN + "Enter your choice: ")
    
    if choice == '1':
        # Admin login
        username = input(Fore.BLUE + "Enter admin username: ")
        password = input(Fore.BLUE + "Enter admin password: ")
        
        try:
            with open('users.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    user_data = line.strip().split(',')
                    if len(user_data) >= 4 and user_data[0] == username and user_data[3] == password:
                        if len(user_data) >= 2 and user_data[1].lower() == 'admin':
                            return username, 'admin'
                        else:
                            print(Fore.RED + "Error: User is not an admin.")
                            return None
            print(Fore.RED + "Error: Invalid admin credentials.")
        except FileNotFoundError:
            print(Fore.RED + "Users file not found.")
            
    elif choice == '2':
        # Student login
        username = input(Fore.BLUE + "Enter student username: ")
        password = input(Fore.BLUE + "Enter student password: ")
        
        try:
            with open('users.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    user_data = line.strip().split(',')
                    if len(user_data) >= 4 and user_data[0] == username and user_data[3] == password:
                        if len(user_data) >= 2 and user_data[1].lower() == 'student':
                            return username, 'student'
                        else:
                            print(Fore.RED + "Error: User is not a student.")
                            return None
            print(Fore.RED + "Error: Invalid student credentials.")
        except FileNotFoundError:
            print(Fore.RED + "Users file not found.")
            
    elif choice == '3':
        print(Fore.GREEN + "\nExiting the application...\n")
        sys.exit(0)
        
    else:
        print(Fore.RED + "Invalid choice.")
    
    return None

# Function to modify student records
def modify_student_record(admin, student_username=None):
    print(Fore.CYAN + f"\n{f.renderText('Modify Student Record')}")
    
    if not student_username:
        student_username = input(Fore.BLUE + "Enter username of student to modify: ")
    
    user_data = admin.find_user_by_username(student_username)
    
    if not user_data:
        print(Fore.RED + "Error: Student not found.")
        return
        
    if len(user_data) >= 2 and user_data[1].lower() != 'student':
        print(Fore.RED + "Error: This user is not a student.")
        return
        
    # Create a Student object with the found data
    student = Student(
        user_data[0],
        user_data[1],
        user_data[2] if len(user_data) > 2 else None,
        user_data[3] if len(user_data) > 3 else None,
        user_data[4] if len(user_data) > 4 else None
    )
    
    while True:
        print(Fore.YELLOW + "\n1. Add Grade\n2. Add ECA Record\n3. Update Profile\n4. Back")
        choice = input(Fore.CYAN + "Enter your choice: ")
        
        if choice == '1':
            grade = input(Fore.BLUE + "Enter grade: ")
            try:
                grade = int(grade)
                student.add_grade(grade)
            except ValueError:
                print(Fore.RED + "Error: Please enter a valid Grade (Numeric Value)")
                
        elif choice == '2':
            eca_description = input(Fore.BLUE + "Enter ECA description: ")
            student.add_eca(eca_description)
            
        elif choice == '3':
            new_username = input(Fore.BLUE + "Enter new username: ")
            new_email = input(Fore.BLUE + "Enter new email: ")
            new_phone_number = input(Fore.BLUE + "Enter new phone number: ")
            student.update_profile(new_username, new_email, new_phone_number)
            
        elif choice == '4':
            break
            
        else:
            print(Fore.RED + "Invalid choice.")

# Function to display student information
def display_student_info(student):
    print(Fore.CYAN + f"\n{f.renderText('Student Information')}")
    
    # Get user data from files
    user_data_txt = Student.read_user_from_txt(student.username)
    user_data_csv = Student.read_user_from_csv(student.username)
    
    # Create a PrettyTable instance with the required columns
    table = PrettyTable(['Username', 'Role', 'Email', 'Grades', 'ECA', 'Phone Number'])
    
    # Prepare data for display
    username = student.username
    role = student.role
    email = student.email if student.email else (user_data_txt[2] if user_data_txt and len(user_data_txt) > 2 else "N/A")
    
    grades = "N/A"
    if user_data_csv and len(user_data_csv) > 6:
        grades = user_data_csv[6] if user_data_csv[6] else "N/A"
    elif student.grades:
        grades = ", ".join(map(str, student.grades))
        
    eca = "N/A"
    if user_data_csv and len(user_data_csv) > 7:
        eca = user_data_csv[7] if user_data_csv[7] else "N/A"
    elif student.eca:
        eca = student.eca
        
    phone_number = student.phone_number if student.phone_number else (user_data_txt[4] if user_data_txt and len(user_data_txt) > 4 else "N/A")
    
    # Add the student's information as a row in the table
    table.add_row([username, role, email, grades, eca, phone_number])
    
    # Print the table
    print(table)

# Function to display users from txt file
def display_users_txt():
    try:
        with open('users.txt', 'r') as file:
            lines = file.readlines()
            
        if not lines:
            print(Fore.YELLOW + "No users found in users.txt.")
            return

        # Create a PrettyTable for users from users.txt
        table_txt = PrettyTable(['Username', 'Role', 'Email', 'Password', 'Phone Number'])
        
        for line in lines:
            user_data = line.strip().split(',')
            if len(user_data) >= 4:  # Check if the line has at least 4 values
                # Pad the array if needed
                while len(user_data) < 5:
                    user_data.append("N/A")
                table_txt.add_row(user_data[:5])

        print(Fore.LIGHTCYAN_EX + "------------------------!!--Users from users.txt:--!!--------------------------")
        print(table_txt)
    except FileNotFoundError:
        print(Fore.YELLOW + "users.txt file not found.")

# Function to display users from csv file
def display_users_csv():
    try:
        with open('users.csv', 'r') as file:
            reader = csv.reader(file)
            headers = next(reader, None)  # Skip headers if they exist
            users = list(reader)
            
        if not users:
            print(Fore.YELLOW + "No users found in users.csv.")
            return
            
        # Create a PrettyTable for users from users.csv
        if headers and len(headers) >= 7:
            table_csv = PrettyTable(headers[:7])  # Use first 7 headers
        else:
            table_csv = PrettyTable(['ID', 'Username', 'Role', 'Email', 'Password', 'Phone Number', 'Grades', 'ECA'])
            
        for user in users:
            if len(user) >= 6:  # Ensure there are enough fields
                # Pad the array if needed
                while len(user) < 8:
                    user.append("")
                table_csv.add_row(user[:8])

        print(Fore.LIGHTCYAN_EX + "-----------------!!--Users from users.csv:--!!----------------------")
        print(table_csv)
    except FileNotFoundError:
        print(Fore.YELLOW + "users.csv file not found.")
    except Exception as e:
        print(Fore.RED + f"Error displaying users from CSV: {e}")

# Function to handle actions performed by an admin
def admin_actions(admin):
    while True:
        print(Fore.CYAN + f"\n{f.renderText('Admin Portal')}")
        print(Fore.YELLOW + "\n1. Register a new user")
        print(Fore.YELLOW + "2. Search for user")
        print(Fore.YELLOW + "3. Modify student record")
        print(Fore.YELLOW + "4. Delete student record")
        print(Fore.YELLOW + "5. View Users")
        print(Fore.YELLOW + "6. Go to Dashboard")
        print(Fore.YELLOW + "7. Log Out")
        
        choice = input(Fore.CYAN + "\nEnter your choice: ")
        
        if choice == '1':
            print(Fore.CYAN + f"\n{f.renderText('Register New User')}")
            new_username = input(Fore.BLUE + "Enter username: ")
            new_role = input(Fore.BLUE + "Enter role (admin/student): ").lower()
            new_email = input(Fore.BLUE + "Enter email: ")
            new_password = input(Fore.BLUE + "Enter password: ")
            new_phone_number = input(Fore.BLUE + "Enter phone number: ")
            
            if new_role == "student":
                grades_input = input(Fore.BLUE + "Enter grades (comma-separated): ")
                eca_input = input(Fore.BLUE + "Enter ECA description: ")
                
                # Split the grades and eca_input strings into lists
                grades = grades_input.split(',') if grades_input else []
                eca = eca_input if eca_input else ""
                
                user_id = admin.register_user(new_username, new_role, new_email, new_password, new_phone_number, grades, eca)
                if user_id:
                    print(Fore.GREEN + f"Registration Successful with ID: {user_id}")
            else:
                user_id = admin.register_user(new_username, new_role, new_email, new_password, new_phone_number)
                if user_id:
                    print(Fore.GREEN + f"Registration Successful with ID: {user_id}")
                    
        elif choice == '2':
            print(Fore.CYAN + f"\n{f.renderText('Search User')}")
            username_to_search = input(Fore.BLUE + "Enter username to search: ")
            found_user = admin.find_user_by_username(username_to_search)
            
            if found_user:
                table = PrettyTable(['Username', 'Role', 'Email', 'Password', 'Phone Number'])
                # Pad the array if needed
                while len(found_user) < 5:
                    found_user.append("N/A")
                table.add_row(found_user[:5])
                print(table)
            else:
                print(Fore.RED + "No matching users found.")
                
        elif choice == '3':
            username_to_modify = input(Fore.BLUE + "Enter username to modify record: ")
            modify_student_record(admin, username_to_modify)
            
        elif choice == '4':
            print(Fore.CYAN + f"\n{f.renderText('Delete User')}")
            username_to_delete = input(Fore.BLUE + "Enter username to delete: ")
            confirm = input(Fore.YELLOW + f"Are you sure you want to delete user '{username_to_delete}'? (y/n): ")
            if confirm.lower() == 'y':
                admin.delete_user(username_to_delete)
            else:
                print(Fore.GREEN + "Deletion cancelled.")
                
        elif choice == '5':
            display_users_txt()
            print("\n")
            display_users_csv()
            
        elif choice == '6':
            print(Fore.YELLOW + "Dashboard feature is not implemented in this version.")
            
        elif choice == '7':
            print(Fore.GREEN + "Logging out...")
            break
            
        else:
            print(Fore.RED + "Invalid choice. Please try again.")


# Main function to control the program flow
def main():
    create_empty_files()
    
    print(Fore.CYAN + f"\n{f.renderText('Student Profile Management System')}")
    print(Fore.GREEN + "Welcome to Student Profile Management System!!")
    
    while True:
        user_data = login()
        
        if user_data:
            username, role = user_data
            
            if role == 'admin':
                admin = Admin(username, role)
                admin_actions(admin)
            elif role == 'student':
                # Retrieve student information from files
                user_data_txt = Student.read_user_from_txt(username)
                user_data_csv = Student.read_user_from_csv(username)
                
                # Initialize student object with available data
                email = user_data_txt[2] if user_data_txt and len(user_data_txt) > 2 else None
                password = user_data_txt[3] if user_data_txt and len(user_data_txt) > 3 else None
                phone_number = user_data_txt[4] if user_data_txt and len(user_data_txt) > 4 else None
                
                # Try to get grades and ECA from CSV file
                grades = None
                eca = None
                if user_data_csv:
                    if len(user_data_csv) > 6:
                        grades = user_data_csv[6] if user_data_csv[6] else None
                    if len(user_data_csv) > 7:
                        eca = user_data_csv[7] if user_data_csv[7] else None
                
                student = Student(username, role, email, password, phone_number, grades, eca)
                print(Fore.BLUE + f"Welcome, {username}!")
                
                # Student actions menu
                while True:
                    print(Fore.CYAN + f"\n{f.renderText('Student Portal')}")
                    print(Fore.YELLOW + "\n1. View Profile")
                    print(Fore.YELLOW + "2. View Grades")
                    print(Fore.YELLOW + "3. View ECA")
                    print(Fore.YELLOW + "4. Update Profile")
                    print(Fore.YELLOW + "5. Log Out")
                    
                    choice = input(Fore.CYAN + "\nEnter your choice: ")
                    
                    if choice == '1':
                        display_student_info(student)
                    elif choice == '2':
                        student.view_grades()
                    elif choice == '3':
                        student.view_eca()
                    elif choice == '4':
                        new_username = input(Fore.BLUE + "Enter new username: ")
                        new_email = input(Fore.BLUE + "Enter new email: ")
                        new_phone_number = input(Fore.BLUE + "Enter new phone number: ")
                        student.update_profile(new_username, new_email, new_phone_number)
                    elif choice == '5':
                        print(Fore.GREEN + "Logging out...")
                        break
                    else:
                        print(Fore.RED + "Invalid choice. Please try again.")
        else:
            # If login failed, ask if they want to try again
            retry = input(Fore.YELLOW + "Do you want to try again? (y/n): ")
            if retry.lower() != 'y':
                print(Fore.GREEN + "\nThank you for using the School Management System!")
                break

# Call the main function if this script is run directly
if __name__ == "__main__":
    main()