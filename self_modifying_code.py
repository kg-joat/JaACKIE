import os
import shutil

class CodeManager:
    def __init__(self, code_directory="code_versions"):
        self.code_directory = code_directory
        self.current_version = "current.py"
        self.backup_version = "backup.py"
        self.future_version = "future.py"

        # Ensure the code directory exists
        if not os.path.exists(self.code_directory):
            os.makedirs(self.code_directory)

    def save_version(self, version_name, code_content):
        version_path = os.path.join(self.code_directory, version_name)
        with open(version_path, "w") as file:
            file.write(code_content)

    def load_version(self, version_name):
        version_path = os.path.join(self.code_directory, version_name)
        if not os.path.exists(version_path):
            return None
        with open(version_path, "r") as file:
            return file.read()

    def switch_versions(self):
        # Move current to backup
        current_path = os.path.join(self.code_directory, self.current_version)
        backup_path = os.path.join(self.code_directory, self.backup_version)
        if os.path.exists(current_path):
            shutil.copy(current_path, backup_path)

        # Move future to current
        future_path = os.path.join(self.code_directory, self.future_version)
        if os.path.exists(future_path):
            shutil.copy(future_path, current_path)

        print("Version switch completed. Current code has been backed up.")

    def modify_code(self, modifications):
        """
        Apply modifications to the future version.
        `modifications` should be a function that takes and returns the code as a string.
        """
        current_code = self.load_version(self.current_version)
        if not current_code:
            print("No current code found to modify.")
            return

        modified_code = modifications(current_code)
        self.save_version(self.future_version, modified_code)
        print("Modifications saved to future version.")