import os
import shutil
import sys
import json
import subprocess
from project_generator import ProjectGenerator
from auto_registry_generator import AutoRegistryGenerator


class AutoProjectGenerator:

    def __init__(self, default_project_location, default_project_name, default_project_generation_location,
                 properties_file_location):
        self.default_project_location = default_project_location
        self.default_project_name = default_project_name
        self.default_project_generation_location = default_project_generation_location
        self.properties_file_location = properties_file_location
        self.project_name = ''
        self.overwrite = False
        self.registry_list = []
        self.project_location = ''
        self.maven_build = False

    def generate_project(self):
        print('Generating project...')
        self.validate_properties_file()

        if os.path.isdir(self.project_location):
            print(f'\nProject already exists in: {self.project_location}')
            self.overwrite_project()

        project_generator = ProjectGenerator(self.project_location, self.project_name, self.default_project_location,
                                             self.default_project_name)
        project_generator.generate_project()

        for registry in self.registry_list:
            auto_registry_generator = AutoRegistryGenerator(self.project_name, self.project_location,
                                                            registry['transferName'],  registry['localDownloadDirectory'])
            auto_registry_generator.generate_registry_file()
            for transfer in registry['transfers']:
                match transfer['type'].lower():
                    case 's3':
                        auto_registry_generator.add_s3_transfer(transfer['name'], transfer['url'])
                    case 'smb':
                        auto_registry_generator.add_smb_transfer(transfer['name'], transfer['url'])
                    case 'sftp':
                        auto_registry_generator.add_sftp_transfer(transfer['name'], transfer['url'])
                    case 'file':
                        auto_registry_generator.add_file_transfer(transfer['name'], transfer['url'])
                    case 'sharepoint':
                        auto_registry_generator.add_sharepoint_transfer(transfer['name'], transfer['url'],
                                                                        transfer['apiUrl'], transfer['tenantId'],
                                                                        transfer['clientId'], transfer['clientSecret'],
                                                                        transfer['folder'], transfer['dateFolder'], transfer['dateFormat'],
                                                                        transfer['overwriteFile'])
            auto_registry_generator.add_registry_file_to_project()

        if self.maven_build:
            if not shutil.which("mvn"):
                print('Failed to build project! Maven is not installed.')
            else:
                mvn = shutil.which("mvn")
                props = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'log4j.properties')
                process = subprocess.Popen(
                    f'{mvn} -f {os.path.join(self.project_location, "pom.xml")} clean install -Dlog4j.configurationFile={props}',
                    shell=True, stdout=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if process.returncode == 0:
                    print("Project has been built successfully!")
                    sys.exit()

                else:
                    print("Failed to build project.")


    def overwrite_project(self):
        if self.overwrite:
            try:
                print(f'Removing existing project in: {self.project_location}')
                shutil.rmtree(self.project_location)
                print(f'Successfully removed existing project in: {self.project_location}')
            except OSError as error:
                print(f'Failed to remove existing project in: {self.project_location}')
                print(error)
                sys.exit()
        else:
            print(f'Cannot overwrite project! Overwrite is set to: {self.overwrite}')
            sys.exit()

    def validate_properties_file(self):
        print('Verifying properties file...')

        # Verify properties file exists
        if not os.path.isfile(self.properties_file_location):
            print(f"Error! The provided path {{{self.properties_file_location}}}"
                  f" to your properties file does not exist.")
            sys.exit()

        # Verify properties file is json file and set values
        try:
            with open(self.properties_file_location) as file:
                props_data = json.load(file)
                if props_data['projectName'].strip() == "":
                    print("Error! Properties file does not contain a project name.")
                    file.close()
                    sys.exit()
                self.project_name = props_data['projectName']
                print(f'Project name: {self.project_name}')
                self.project_location = f'{self.default_project_generation_location}/{self.project_name}'
                print(f'Project location: {self.project_location}')
                if isinstance(props_data['overwrite'], bool):
                    self.overwrite = bool(props_data['overwrite'])
                print(f'Project overwrite: {self.overwrite}')
                if isinstance(props_data['mavenBuild'], bool):
                    self.maven_build = bool(props_data['mavenBuild'])
                print(f'Build project: {self.maven_build}')
                if len(props_data['registries']) == 0:
                    print("Error! Properties file does not contain any registries. Please provide transfer registries.")
                    file.close()
                    sys.exit()
                self.registry_list = props_data['registries']
                print(f'Registry artifact count: {len(self.registry_list)}')
                file.close()
        except ValueError as error:
            print(f'Properties file is not a valid json file: {self.properties_file_location}')
            print(error)
            sys.exit()

    def maven_build(self):
        print('Building project...')





