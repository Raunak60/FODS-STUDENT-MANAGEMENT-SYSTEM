from colorama import init, Fore, Style  # Import colorama for colored output
from pyfiglet import Figlet  # Import Figlet for ASCII art

class Dashboard:
    def __init__(self, admin):
        self.admin = admin
        self.user_statistics = None

    def start(self):
        print(' !!....Welcome to Student Management System....!!')
        self.display_main_menu()

    def display_main_menu(self):
        print("\nMain Menu:")
        print("1. View User Statistics")
        print("2. View Recent Activities")
        print("3. Manage Settings")
        print("4. Exit Dashboard")

        choice = input("Enter your choice: ")

        if choice == '1':
            self.view_user_statistics()
        elif choice == '2':
            self.view_recent_activities()
        elif choice == '3':
            self.manage_settings()
        elif choice == '4':
            print("Exiting Dashboard. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please try again.")
            self.display_main_menu()

    def view_user_statistics(self):
        print('Displaying user statistics...')
        if self.user_statistics is not None:
            self.display_user_statistics()
        else:
            print("No user statistics data available.")

    def display_user_statistics(self):
        if self.user_statistics:
            print("Username: ", self.user_statistics["username"])
            print("Email: ", self.user_statistics["email"])
            print("Student ID: ", self.user_statistics["student_id"])
            print("Total logins: ", self.user_statistics["total_logins"])
        else:
            print("No user statistics data available.")

    def view_recent_activities(self):
        print('Viewing recent activities...')
        if self.recent_activities:
            for i, activity in enumerate(self.recent_activities, start=1):
                print(f"{i}. {activity}")
        else:
            print("No recent activities available.")

    def manage_settings(self):
        print('Managing settings...')
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
        if new_email.strip().lower() in ["", "none", "null"]:
            self.user_settings["email"] = None
        else:
            self.user_settings["email"] = new_email.strip().lower()
        print(f"Email changed to {self.user_settings['email']}.")

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

if __name__ == "__main__":
    admin = {}  # Replace {} with your admin object
    dashboard = Dashboard(admin)
    dashboard.start()
