from colorama import init, Fore
from pyfiglet import Figlet
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os

# Initialize colorama
init(autoreset=True)

class Dashboard:
    def __init__(self, admin):
        self.admin = admin
        self.user_statistics = {
            "username": "john_doe",
            "email": "john@example.com",
            "student_id": "S123",
            "total_logins": 12
        }
        self.recent_activities = ["Logged in", "Viewed grades", "Changed ECA"]
        self.user_settings = {
            "email": "john@example.com",
            "student_id": "S123",
            "grade": "A",
            "eca": "Football"
        }

    def start(self):
        print(Fore.YELLOW + ' !!....Welcome to Student Management System....!!')
        self.display_main_menu()

    def display_main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. View User Statistics")
            print("2. View Recent Activities")
            print("3. Manage Settings")
            print("4. Performance Analytics")
            print("5. Exit Dashboard")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.view_user_statistics()
            elif choice == '2':
                self.view_recent_activities()
            elif choice == '3':
                self.manage_settings()
            elif choice == '4':
                self.performance_analytics()
            elif choice == '5':
                print("Exiting Dashboard. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def view_user_statistics(self):
        print(Fore.GREEN + 'Displaying user statistics...')
        if self.user_statistics:
            self.display_user_statistics()
        else:
            print("No user statistics data available.")

    def display_user_statistics(self):
        print("Username:", self.user_statistics.get("username"))
        print("Email:", self.user_statistics.get("email"))
        print("Student ID:", self.user_statistics.get("student_id"))
        print("Total logins:", self.user_statistics.get("total_logins"))

    def view_recent_activities(self):
        print(Fore.CYAN + 'Viewing recent activities...')
        if self.recent_activities:
            for i, activity in enumerate(self.recent_activities, start=1):
                print(f"{i}. {activity}")
        else:
            print("No recent activities available.")

    def manage_settings(self):
        print(Fore.MAGENTA + 'Managing settings...')
        while True:
            print("\n1. Change email address")
            print("2. Change student ID")
            print("3. Change grade")
            print("4. Change ECA")
            print("5. Back to main menu")
            try:
                option = int(input("Enter an option: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if option == 1:
                self.change_email_address()
            elif option == 2:
                self.change_student_id()
            elif option == 3:
                self.change_grade()
            elif option == 4:
                self.change_eca()
            elif option == 5:
                break
            else:
                print("Invalid option. Please try again.")

    def change_email_address(self):
        new_email = input("Enter the new email: ")
        self.user_settings["email"] = new_email.strip().lower() if new_email.strip().lower() not in ["", "none", "null"] else None
        print(f"Email changed to {self.user_settings['email']}")

    def change_student_id(self):
        new_student_id = input("Enter the new student ID: ")
        self.user_settings["student_id"] = new_student_id
        print(f"Student ID changed to {new_student_id}.")

    def change_grade(self):
        new_grade = input("Enter the new grade: ")
        self.user_settings["grade"] = new_grade
        print(f"Grade changed to {new_grade}.")

    def change_eca(self):
        new_eca = input("Enter the new ECA: ")
        self.user_settings["eca"] = new_eca
        print(f"ECA changed to {new_eca}.")

    def performance_analytics(self):
        try:
            # Create a clean fallback users.csv if it doesn't exist
            if not os.path.exists("users.csv"):
                with open("users.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Username", "Role", "Grades", "ECA", "Email", "StudentID", "TotalLogins"])
                    writer.writerow(["john_doe", "student", "75", "Football,Music", "john@example.com", "S123", "12"])
                    writer.writerow(["jane_smith", "student", "65", "Art", "jane@example.com", "S124", "10"])
                    writer.writerow(["tom_black", "student", "82", "Debate,Music", "tom@example.com", "S125", "15"])

            # Read with protection from bad lines
            df = pd.read_csv("users.csv", on_bad_lines='warn')
            df = df[df['Role'].str.lower() == 'student']
            df['Grades'] = pd.to_numeric(df['Grades'], errors='coerce')
            df['ECA_Count'] = df['ECA'].fillna('').apply(lambda x: len(x.split(',')) if x else 0)

            print(Fore.CYAN + "\nGenerating Grade Trend Chart...")
            df_sorted = df.sort_values('Username')
            plt.figure(figsize=(10, 4))
            plt.plot(df_sorted['Username'], df_sorted['Grades'], marker='o', color='blue')
            plt.title('Grade Trends by Student')
            plt.xlabel('Student Username')
            plt.ylabel('Grades')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.grid(True)
            plt.show()

            print(Fore.CYAN + "\nGenerating ECA Impact Chart...")
            plt.figure(figsize=(6, 4))
            plt.scatter(df['ECA_Count'], df['Grades'], color='green')
            plt.title('ECA Involvement vs. Academic Performance')
            plt.xlabel('Number of ECAs')
            plt.ylabel('Grades')
            plt.grid(True)
            plt.tight_layout()
            plt.show()

            print(Fore.CYAN + "\nPerformance Alerts (Grades < 70):")
            low_performers = df[df['Grades'] < 70]
            if not low_performers.empty:
                print(low_performers[['Username', 'Grades']])
            else:
                print("All students are above the threshold.")

        except Exception as e:
            print(Fore.RED + f"Error generating analytics: {e}")

# Entry point
if __name__ == "__main__":
    admin = {}
    dashboard = Dashboard(admin)
    dashboard.start()
