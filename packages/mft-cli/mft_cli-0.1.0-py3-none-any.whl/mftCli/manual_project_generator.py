import os
import shutil
import sys
from project_generator import ProjectGenerator
from registry_generator import RegistryGenerator

class ManualProjectGenerator:

    def __init__(self, default_project_generation_location, project_name, default_project_location, default_project_name):
        self.default_project_generation_location = default_project_generation_location
        self.project_name = project_name
        self.project_location = f'{default_project_generation_location}/{project_name}'
        self.default_project_location = default_project_location
        self.default_project_name = default_project_name
        self.composite_exporter_module_location = f"{self.project_location}/{project_name}CompositeExporter"
        self.registry_resources_module_location = f"{self.project_location}/{project_name}RegistryResources"

    def generate_project(self):
        print('Generating project...')
        if os.path.isdir(self.project_location):
            self.handle_duplicate_project()

        project_generator = ProjectGenerator(self.project_location, self.project_name, self.default_project_location,
                                             self.default_project_name)
        project_generator.generate_project()

        registry_generator = RegistryGenerator()
        registry_generator.generate_registry_file(self.composite_exporter_module_location,
                                                  self.registry_resources_module_location, self.project_location)



    def handle_duplicate_project(self):
        print(f'\nProject already exists within {self.project_location}')

        confirmed = False
        while not confirmed:
            response = ''
            response = input('Would you like to overwrite your MFT project? [y/n]\nAnswer: ')
            match response.lower():
                case 'y':
                    self.remove_project()
                    confirmed = True
                case 'yes':
                    self.remove_project()
                    confirmed = True
                case 'n':
                    print("Terminating program...")
                    sys.exit()
                case 'no':
                    print("Terminating program...")
                    sys.exit()
                case _:
                    print("Invalid input!")


    def remove_project(self):
        print(f'\nRemoving project: {self.project_location}')
        try:
            shutil.rmtree(self.project_location)
            print(f'Successfully removed project: {self.project_location}')
        except OSError as error:
            print(f'Failed to remove project: {self.project_location}')
            print(error)
            sys.exit()


