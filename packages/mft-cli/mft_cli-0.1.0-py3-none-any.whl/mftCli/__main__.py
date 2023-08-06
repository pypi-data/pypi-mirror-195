import os
import click
import sys
sys.path.append(os.path.dirname(__file__))
from auto_project_generator import AutoProjectGenerator
from manual_project_generator import ManualProjectGenerator
from importlib import resources
import io

# The name of the default project
default_project_name = '_TN_Mft_Transfer_'
# The absolute path of the default project
default_project_location = os.path.join(os.path.abspath(os.path.dirname(__file__)), default_project_name)
# The directory where the default project is copied to
default_project_generation_location = os.getcwd()
# The absolute path of the new project
project_location = ''
# If the new project has been generated successfully
generated = False


@click.command()
@click.option('--name', '-n', help="Name of the MFT project.", required=True,
              prompt="Please provide a name for your MFT project?\n")
def supercli(name):
    """
    param name: This is the name of the MFT project
    """
    if name.strip() == "":
        print("Error! You have not provided a valid project name.\nPlease try again...")
        sys.exit()

    print(f"Project name: {name}")
    manual_project_generator = ManualProjectGenerator(default_project_generation_location, name,
                                                      default_project_location, default_project_name)
    manual_project_generator.generate_project()


def main():
    try:
        operation = sys.argv[1]
    except IndexError:
        operation = ''
    match operation.lower():
        case "-f":
            print("Running MFT Project Generator from properties file...")
            try:
                properties_file_location = sys.argv[2]
                auto_project_generator = AutoProjectGenerator(default_project_location, default_project_name,
                                                              default_project_generation_location,
                                                              properties_file_location)
                auto_project_generator.generate_project()
            except IndexError:
                print("Error! Please provide the path to your properties file.")
                sys.exit()
        case _:
            supercli()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # f = open('art.txt', 'r')
    # print(''.join([line for line in f]))
    # print("\n")
    main()
