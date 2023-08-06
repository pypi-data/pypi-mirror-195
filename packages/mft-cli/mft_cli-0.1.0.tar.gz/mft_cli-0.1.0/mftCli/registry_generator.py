import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import sys


class RegistryGenerator:
    temp_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "tmp")
    project_location = ''
    new_registry_file_tmp_location = ''
    composite_exporter_module_location = ''
    registry_resources_module_location = ''
    default_registry_template_location = os.path.join(os.path.abspath(os.path.dirname(__file__)), "RegistryTemplate.xml")

    def generate_registry_file(self, composite_exporter_module_location, registry_resources_module_location,
                               project_location):
        print("\nGenerating registry file...")

        self.composite_exporter_module_location = composite_exporter_module_location
        self.registry_resources_module_location = registry_resources_module_location
        self.project_location = project_location

        registry_file_name = input("Please provide a name for your registry file.\nName: ")
        while registry_file_name.strip() == "":
            print("\nInvalid registry file name provided!")
            registry_file_name = input("Please provide a name for your registry file.\nName: ")
        print(f"Registry File Name: {registry_file_name}\n")

        transfer_name = input("Please provide a transfer name.\nName: ")
        while transfer_name.strip() == "":
            print("\nInvalid transfer name provided!")
            transfer_name = input("Please provide a transfer name.\nName: ")
        print(f"Transfer Name: {transfer_name}\n")

        local_download_directory = input("Please provide a local directory path where the"
                                         "\nFile Transfer will be downloaded to.\nPath: ")
        while local_download_directory.strip() == "":
            print("\nInvalid directory path provided!")
            local_download_directory = input("Please provide a local directory path where the"
                                             "\nFile Transfer will be downloaded to.\nPath: ")
        print(f"Download Location: {local_download_directory}\n")
        if not os.path.isdir(self.temp_dir):
            os.makedirs(self.temp_dir)
        new_registry_file_tmp_location = os.path.join(self.temp_dir, f'{registry_file_name}.xml')
        print(self.default_registry_template_location)
        print(new_registry_file_tmp_location)
        shutil.copyfile(self.default_registry_template_location, new_registry_file_tmp_location)

        new_registry_file_tree = ET.parse(new_registry_file_tmp_location)
        new_registry_file_tree.find('.//transferName').text = transfer_name
        new_registry_file_tree.find('.//localDownloadDirectory').text = local_download_directory
        new_registry_file_tree.write(new_registry_file_tmp_location)

        registry_setup_incomplete = True
        self.new_registry_file_tmp_location = new_registry_file_tmp_location
        self.setup_transfer(new_registry_file_tmp_location)

        end_of_registry_setup = ''
        while registry_setup_incomplete:
            end_of_registry_setup = input("\nWould you like to add an additional transfer? [y/n].\nAnswer: ")
            match end_of_registry_setup.lower():
                case "y":
                    print("\n")
                    self.setup_transfer(new_registry_file_tmp_location)
                case "yes":
                    print("\n")
                    self.setup_transfer(new_registry_file_tmp_location)
                case "n":
                    registry_setup_incomplete = False
                    break
                case "no":
                    registry_setup_incomplete = False
                    break
                case _:
                    print("\nInvalid option selected!")
        self.update_project_with_new_registry(new_registry_file_tmp_location, composite_exporter_module_location,
                                              registry_resources_module_location, registry_file_name)
        print("Registry setup complete")

    def setup_transfer(self, registry_file_location):
        # Available transfer options
        transfer_options = ['S3', 'SFTP', 'SHAREPOINT', 'SMB']
        # User input -> selected option
        selected_transfer_option = ''
        # User display message
        transfer_input_message = "Add a Transfer\nPick an option:\n"

        # Enumerate transfer options for user selection
        for index, item in enumerate(transfer_options):
            transfer_input_message += f'{index + 1}) {item}\n'

        # User display message
        transfer_input_message += 'Select Transfer: '

        while selected_transfer_option.lower() not in list(map(lambda x: x.lower(), transfer_options)):
            if selected_transfer_option in map(str, range(1, len(transfer_options) + 1)):
                selected_transfer_option = transfer_options[int(selected_transfer_option) - 1]
                break
            selected_transfer_option = input(transfer_input_message)

        print(f"Selected Transfer: {selected_transfer_option}\n")

        self.transfer_switch(selected_transfer_option.lower(), registry_file_location)

    def transfer_switch(self, selection, registry_file_location):
        match selection.lower():
            case "s3":
                self.generate_s3_transfer(registry_file_location)
            case "sftp":
                self.generate_sftp_transfer(registry_file_location)
            case "sharepoint":
                self.generate_sharepoint_transfer(registry_file_location)
            case 'smb':
                self.generate_smb_transfer(registry_file_location)

    def generate_sharepoint_transfer(self, tmp_registry_file_location):
        print("Generating Sharepoint Transfer entry...")

        sharepoint_transfer_name = input("\nPlease provide a name for your Sharepoint Transfer.\nName: ")
        while sharepoint_transfer_name.strip() == "":
            print("\nInvalid Sharepoint transfer name provided!")
            sharepoint_transfer_name = input("Please provide a name for your Sharepoint Transfer.\nName: ")

        sharepoint_url = input("\nPlease provide a url for your Sharepoint location.\nExample:\n\thttps:{"
                               "tenant_name}.sharepoint.com/{path/to/folder}\nURL: ")
        while sharepoint_url.strip() == "":
            print("\nInvalid Sharepoint URL provided!")
            sharepoint_url = input("Please provide a url for your Sharepoint location.\nExample:\n\thttps:{"
                                   "tenant_name}.sharepoint.com/{path/to/folder}\nURL: ")

        sharepoint_api_url = input("\nPlease provide an API url for your Sharepoint.\nExample:\n\thttps:{"
                                   "tenant_name}.sharepoint.com\nURL: ")
        while sharepoint_api_url.strip() == "":
            print("\nInvalid Sharepoint API URL provided!")
            sharepoint_api_url = input("Please provide an API url for your Sharepoint.\nExample:\n\thttps:{"
                                       "tenant_name}.sharepoint.com\nURL: ")

        sharepoint_tenant_id = input("\nPlease provide the tenant ID for your Sharepoint.\nID: ")
        while sharepoint_tenant_id.strip() == "":
            print("\nInvalid Sharepoint tenant ID provided!")
            sharepoint_tenant_id = input("Please provide the tenant ID for your Sharepoint.\nID: ")

        client_id = input("\nPlease provide the client ID for your Sharepoint.\nID: ")
        while client_id.strip() == "":
            print("\nInvalid Sharepoint client ID provided!")
            client_id = input("Please provide the client ID for your Sharepoint.\nID: ")

        sharepoint_client_secret = input("\nPlease provide the client secret for your Sharepoint.\nSecret: ")
        while sharepoint_client_secret.strip() == "":
            print("\nInvalid Sharepoint client secret provided!")
            sharepoint_client_secret = input("Please provide the client secret for your Sharepoint.\nSecret: ")

        sharepoint_redirect_url = input("\nPlease provide the token redirect url for your Sharepoint.\nURL: ")
        while sharepoint_redirect_url.strip() == "":
            print("\nInvalid Sharepoint token redirect url provided!")
            sharepoint_redirect_url = input("Please provide the token redirect url for your Sharepoint.\nURL: ")

        sharepoint_client_id = f'{client_id}@{sharepoint_tenant_id}'
        resource_domain = sharepoint_api_url[8:]
        sharepoint_resource = f'00000003-0000-0ff1-ce00-000000000000/{resource_domain.split("/")[0]}@{sharepoint_tenant_id}'

        sharepoint_folder = input("\nPlease provide the path to your Sharepoint folder.\nExample:\n\tShared Documents/REPORTS/Folder\nPath: ")
        while sharepoint_folder.strip() == "":
            print("\nInvalid Sharepoint folder provided!")
            sharepoint_folder = input("\nPlease provide the path to your Sharepoint folder.\nExample:\n\tShared Documents/REPORTS/Folder\nPath: ")

        date_folder = input("\nCreate dated folder in Sharepoint folder? [y/n]\nAnswer: ")

        match date_folder.lower():
            case 'y':
                create_date_folder = 'true'
            case 'n':
                create_date_folder = 'false'
            case _:
                create_date_folder = 'false'


        if create_date_folder == 'true':
            date_options = ['yyyy/MM/dd', 'yyyy-MM-dd', 'yyyy/MM']
            selected_date_option = ''
            # User display message
            date_input_message = "Select date format\nPick an option:\n"

            for index, item in enumerate(date_options):
                date_input_message += f'{index + 1}) {item}\n'

            date_input_message += 'Select Format: '

            while selected_date_option.lower() not in list(map(lambda x: x.lower(), date_options)):
                if selected_date_option in map(str, range(1, len(date_options) + 1)):
                    selected_date_option = date_options[int(selected_date_option) - 1]
                    break
                selected_date_option = input(date_input_message)
        else:
            selected_date_option = 'yyyy-MM-dd'


        confirmed = False
        while not confirmed:
            confirmation = input(
                f"\nConfirm input: [y/n]"
                f"\nSharepoint Transfer Name: {sharepoint_transfer_name}"
                f"\nSharepoint URL: {sharepoint_url}"
                f"\nSharepoint API URL: {sharepoint_api_url}"
                f"\nSharepoint Tenant ID: {sharepoint_tenant_id}"
                f"\nSharepoint Resource: {sharepoint_resource}"
                f"\nSharepoint Client ID: {sharepoint_client_id}"
                f"\nSharepoint Client Secret: {sharepoint_client_secret}"
                f"\nSharepoint token Redirect URL: {sharepoint_redirect_url}"
                f"\nSharepoint Folder: {sharepoint_folder}"
                f"\nCreate Dated Folder: {create_date_folder}"
                f"\nDated Folder Format: {selected_date_option}"
                f"\nIs this correct:")

            match confirmation.lower():
                case 'y':
                    print('\n')
                    confirmed = True
                    break
                case 'yes':
                    print('\n')
                    confirmed = True
                    break
                case 'n':
                    confirmed = True
                    print("Aborting...\n")
                    self.setup_transfer(self.new_registry_file_tmp_location)
                case 'no':
                    confirmed = True
                    print("Aborting...\n")
                    self.setup_transfer(self.new_registry_file_tmp_location)
                case _:
                    print("Invalid input!")

        sharepoint_transfer_template = ET.XML(f'''
            <destination>
                <name>{sharepoint_transfer_name}</name>
                <type>sharepoint</type>
                <url>{sharepoint_url}</url>
                <apiUrl>{sharepoint_api_url}</apiUrl>
                <resource>{sharepoint_resource}</resource>
                <clientId>{sharepoint_client_id}</clientId>
                <clientSecret>{sharepoint_client_secret}</clientSecret>
                <tenantId>{sharepoint_tenant_id}</tenantId>
                <redirectUri>{sharepoint_redirect_url}</redirectUri>
                <folderName>{sharepoint_folder}</folderName>
                <dateFolder>{create_date_folder}</dateFolder>
                <dateFormat>{selected_date_option}</dateFormat>
            </destination>
        ''')

        tmp_registry_file_tree = ET.parse(tmp_registry_file_location)
        tmp_registry_file_tree.find('.//destinations').append(sharepoint_transfer_template)
        ET.indent(tmp_registry_file_tree, space="\t", level=0)
        tmp_registry_file_tree.write(tmp_registry_file_location)

    def generate_s3_transfer(self, tmp_registry_file_location):
        print("Generating S3 Transfer entry...")

        s3_transfer_name = input("Please provide a name for your S3 Transfer.\nName: ")
        while s3_transfer_name.strip() == "":
            print("\nInvalid S3 transfer name provided!")
            s3_transfer_name = input("Please provide a name for your S3 Transfer.\nName: ")

        s3_url = input("Please provide a url for your S3 location.\nURL: ")
        while s3_url.strip() == "":
            print("\nInvalid S3 URL provided!")
            s3_url = input("Please provide a url for your S3 location.\nURL: ")

        confirmed = False
        while not confirmed:
            confirmation = input(
                f"\nConfirm input: [y/n]\nS3 Transfer Name: {s3_transfer_name}\nS3 URL: {s3_url}\nIs this correct:")
            match confirmation.lower():
                case 'y':
                    confirmed = True
                    break
                case 'yes':
                    confirmed = True
                    break
                case 'n':
                    confirmed = True
                    print("Aborting...\n")
                    self.setup_transfer(self.new_registry_file_tmp_location)
                case 'no':
                    confirmed = True
                    print("Aborting...\n")
                    self.setup_transfer(self.new_registry_file_tmp_location)
                case _:
                    print("Invalid input!")

        s3_transfer_template = ET.XML(f'''
            <destination>
                <name>{s3_transfer_name}</name>
                <type>s3</type>
                <url>{s3_url}</url>
            </destination>
        ''')

        tmp_registry_file_tree = ET.parse(tmp_registry_file_location)
        tmp_registry_file_tree.find('.//destinations').append(s3_transfer_template)
        ET.indent(tmp_registry_file_tree, space="\t", level=0)
        tmp_registry_file_tree.write(tmp_registry_file_location)

    def generate_sftp_transfer(self, tmp_registry_file_location):
        print("Generating SFTP Transfer entry...")

        sftp_transfer_name = input("Please provide a name for your SFTP Transfer.\nName: ")
        while sftp_transfer_name.strip() == "":
            print("\nInvalid SFTP transfer name provided!")
            sftp_transfer_name = input("Please provide a name for your SFTP Transfer.\nName: ")

        sftp_url = input("Please provide a url for your SFTP location.\nURL: ")
        while sftp_url.strip() == "":
            print("\nInvalid SFTP URL provided!")
            sftp_url = input("Please provide a url for your SFTP location.\nURL: ")

        confirmed = False
        while not confirmed:
            confirmation = input(
                f"\nConfirm input: [y/n]\nSFTP Transfer Name: {sftp_transfer_name}"
                f"\nSFTP URL: {sftp_url}\nIs this correct:")
            match confirmation.lower():
                case 'y':
                    confirmed = True
                    break
                case 'yes':
                    confirmed = True
                    break
                case 'n':
                    confirmed = True
                    print("Aborting...\n")
                    self.setup_transfer(self.new_registry_file_tmp_location)
                case 'no':
                    confirmed = True
                    print("Aborting...\n")
                    self.setup_transfer(self.new_registry_file_tmp_location)
                case _:
                    print("Invalid input!")

        sftp_transfer_template = ET.XML(f'''
            <destination>
                <name>{sftp_transfer_name}</name>
                <type>sftp</type>
                <url>{sftp_url}</url>
            </destination>
        ''')

        tmp_registry_file_tree = ET.parse(tmp_registry_file_location)
        tmp_registry_file_tree.find('.//destinations').append(sftp_transfer_template)
        ET.indent(tmp_registry_file_tree, space="\t", level=0)
        tmp_registry_file_tree.write(tmp_registry_file_location)


    def generate_smb_transfer(self, tmp_registry_file_location):
        print("Generating SMB Transfer entry...")

        smb_transfer_name = input("Please provide a name for your SMB Transfer.\nName: ")
        while smb_transfer_name.strip() == "":
            print("\nInvalid SMB transfer name provided!")
            smb_transfer_name = input("Please provide a name for your SMB Transfer.\nName: ")

        smb_url = input("Please provide a url for your SMB location.\nURL: ")
        while smb_url.strip() == "":
            print("\nInvalid SMB URL provided!")
            smb_url = input("Please provide a url for your SMB location.\nURL: ")

        confirmed = False
        while not confirmed:
            confirmation = input(
                f"\nConfirm input: [y/n]\nSMB Transfer Name: {smb_transfer_name}"
                f"\nSMB URL: {smb_url}\nIs this correct:")
            match confirmation.lower():
                case 'y':
                    confirmed = True
                    break
                case 'yes':
                    confirmed = True
                    break
                case 'n':
                    confirmed = True
                    print("Aborting...\n")
                    self.setup_transfer(self.new_registry_file_tmp_location)
                case 'no':
                    confirmed = True
                    print("Aborting...\n")
                    self.setup_transfer(self.new_registry_file_tmp_location)
                case _:
                    print("Invalid input!")

        smb_transfer_template = ET.XML(f'''
            <destination>
                <name>{smb_transfer_name}</name>
                <type>smb</type>
                <url>{smb_url}</url>
            </destination>
        ''')

        tmp_registry_file_tree = ET.parse(tmp_registry_file_location)
        tmp_registry_file_tree.find('.//destinations').append(smb_transfer_template)
        ET.indent(tmp_registry_file_tree, space="\t", level=0)
        tmp_registry_file_tree.write(tmp_registry_file_location)

    def update_project_with_new_registry(self, tmp_registry_file_location, composite_module_location,
                                         registry_module_location,
                                         artifact_name):
        print("Applying changes to project...")

        shutil.move(tmp_registry_file_location, os.path.join(registry_module_location, f'{artifact_name}.xml'))

        artifact_item_template = ET.XML(f'''
            <artifact name="{artifact_name}" groupId="za.co.dearx.resource" version="1.0.0" type="registry/resource" serverRole="EnterpriseIntegrator">
                <item>
                    <file>{artifact_name}.xml</file>
                    <path>/_system/governance/mftgeneric</path>
                    <mediaType>application/xml</mediaType>
                    <properties/>
                </item>
            </artifact>
        ''')

        artifact_file_location = os.path.join(registry_module_location, 'artifact.xml')
        artifact_file_tree = ET.parse(artifact_file_location)
        artifact_file_root = artifact_file_tree.getroot()
        artifact_file_root.append(artifact_item_template)
        ET.indent(artifact_file_root, space="\t", level=0)
        artifact_file_tree.write(artifact_file_location)

        composite_pom_properties_template = f'<za.co.dearx.resource_._{artifact_name}>capp/EnterpriseIntegrator</za.co.dearx.resource_._{artifact_name}>'
        with open(os.path.join(composite_module_location, 'pom.xml'), "r") as f:
            contents = f.readlines()

        contents.insert(16, composite_pom_properties_template)

        with open(os.path.join(composite_module_location, 'pom.xml'), "w") as f:
            contents = "".join(contents)
            f.write(contents)

        composite_pom_dependency_template = ET.XML(f'''
            <dependency>
                <groupId>za.co.dearx.resource</groupId>
                <artifactId>{artifact_name}</artifactId>
                <version>1.0.0</version>
                <type>zip</type>
            </dependency>
        ''')

        composite_pom_file_location = os.path.join(composite_module_location, 'pom.xml')
        composite_pom_file_tree = ET.parse(composite_pom_file_location)
        composite_pom_file_tree.find('.{http://maven.apache.org/POM/4.0.0}dependencies').append(
            composite_pom_dependency_template)
        ET.register_namespace("", "http://maven.apache.org/POM/4.0.0")
        ET.indent(composite_pom_file_tree, space="\t", level=0)
        composite_pom_file_tree.write(composite_pom_file_location, encoding="utf-8", xml_declaration=True)

        confirmed = False
        while not confirmed:
            add_registry = input("\nWould you like to add an additional registry file? [y/n]\nAnswer: ")
            match add_registry.lower():
                case 'y':
                    print('\n')
                    self.generate_registry_file(self.composite_exporter_module_location,
                                                self.registry_resources_module_location,
                                                self.project_location)
                    confirmed = True
                    break
                case 'yes':
                    print('\n')
                    self.generate_registry_file(self.composite_exporter_module_location,
                                                self.registry_resources_module_location,
                                                self.project_location)
                    confirmed = True
                    break
                case 'n':
                    confirmed = True
                    break
                case 'no':
                    confirmed = True
                    break
                case _:
                    print("Invalid input!")

        build = False
        while not build:
            mvn_build = input("\nWould you like to use Maven to build your project? [y/n]\nAnswer: ")
            match mvn_build.lower():
                case 'y':
                    self.build_project()
                    build = True
                    break
                case 'yes':
                    self.build_project()
                    build = True
                    break
                case 'n':
                    print('Project will not be built by Maven.')
                    build = True
                    break
                case 'no':
                    print('Project will not be built by Maven.')
                    build = True
                    break
                case _:
                    print("Invalid input!")

    def build_project(self):
        if not shutil.which("mvn"):
            print('Failed to build project! Maven is not installed.')
        else:
            mvn = shutil.which("mvn")
            props = os.path.abspath('log4j.properties')
            process = subprocess.Popen(
                f'{mvn} -f {os.path.join(self.project_location, "pom.xml")} clean install -Dlog4j.configurationFile={props}',
                shell=True, stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                print("Project has been built successfully!")
                sys.exit()

            else:
                print("Failed to build project.")
