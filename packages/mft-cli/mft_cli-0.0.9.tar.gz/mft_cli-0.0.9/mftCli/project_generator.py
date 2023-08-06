import shutil
import os
import sys


class ProjectGenerator:

    # Init method
    # @param project_location -> The absolute path where the new project resides
    # @param project_name -> The new project name
    # @param default_project_location -> The absolute path where the default project resides
    # @param default_project_name -> The default project name
    def __init__(self, project_location, project_name, default_project_location, default_project_name):
        self.project_location = project_location
        self.project_name = project_name
        self.default_project_location = default_project_location
        self.default_project_name = default_project_name

    # Method to generate new project with the provided project name
    def generate_project(self):
        print(f"Generating new MFT Project...")
        try:
            shutil.copytree(self.default_project_location, self.project_location)
            print(f"Successfully generated MFT project in {self.project_location}")
            self.update_project_name()
            self.generate_version_file()
            return True
        except FileExistsError as error:
            print(f"Failed to generate MFT project -> Project already exists in {self.project_location}")
            print(error)
            sys.exit()

    # Method to update new project with the provided project name
    # @param project_location -> The absolute path where the new project resides
    # @param project_name -> The new project name
    # @param project_name -> The default project name
    def update_project_name(self):
        print(f"Updating MFT Project with project name...")
        # Iterate through subdirectories within parent directory
        try:
            for directory in os.listdir(self.project_location):
                # Replace default project name with new project name in directory name
                new_directory_name = directory.replace(self.default_project_name, self.project_name)
                # Get absolute path of directory to be renamed
                new_directory_path = os.path.join(self.project_location, new_directory_name)
                # Rename directory
                os.rename(os.path.join(self.project_location, directory), new_directory_path)
            # Iterate through subdirectories within parent directory
            for dir_name, dirs, files in os.walk(self.project_location):
                # Iterate through files within subdirectories and parent directory
                for file_name in files:
                    # Get absolute path of file to be renamed
                    file_path = os.path.join(dir_name, file_name)
                    if self.default_project_name in file_path:
                        new_file_path = file_path.replace(self.default_project_name, self.project_name)
                        os.rename(file_path, new_file_path)
                        file_path = new_file_path
                    # Open file to for renaming
                    with open(file_path) as file:
                        # Read file content into memory
                        file_content = file.read()
                    # Replace default project name with new project name within file
                    file_content = file_content.replace(self.default_project_name, self.project_name)
                    # Open file to write changes
                    with open(file_path, "w") as file:
                        # Write changes to file
                        file.write(file_content)
            print(f"Updated MFT Project with project name successfully!")
        except OSError as error:
            print("Failed to update MFT Project with project name")
            print(error)
            sys.exit()

    def generate_version_file(self):
        version_file_name = 'version.txt'
        default_project_version = '1.0.0.0'
        version_file_path = os.path.join(self.project_location, version_file_name)
        if not os.path.isfile(version_file_path):
            print("Generating version file...")
            with open(version_file_path, "w") as file:
                version_file_text = default_project_version
                file.write(version_file_text)


