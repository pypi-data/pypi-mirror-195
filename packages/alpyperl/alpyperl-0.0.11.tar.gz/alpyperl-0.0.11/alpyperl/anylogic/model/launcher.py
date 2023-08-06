import os
import platform
import re
import string
import random


class ALModelLauncher():
    """This class in in charge of launching the AnyLogic model. The main
    functionality comes by notifying the model what ports need to be connecting
    to so communication with python script is possible.
    """

    def __init__(
        self,
        java_port=25333,
        python_port=25334,
        folder_location='./exported_model',
        show_terminal=False
    ):
        # Check if exported model exists.
        if not os.path.exists(folder_location):
            raise Exception(
                f"Could not find exported model folder '{folder_location}'. "
                "Model execution could not proceed. Please export your model at "
                f"'{folder_location}'"
            )
        self.folder_location = folder_location
        self.show_terminal = show_terminal
        # Get operating system compiling this code
        self.os_name = platform.system()
        # Create command-line arguments that refer to the Java and Python ports
        # java model needs to connect to.
        self.port_arg_str = '-jp ' + str(java_port) + ' -pp ' + str(python_port)
        # Get project name.
        self.project_name = self.__get_project_name(folder_location=folder_location)

    def compileAndRun(self):
        """Compile the script and execute it considering the operating system
        it is running on"""

        # Execute exported version of the model depending on OS
        if self.os_name == 'Linux':
            # Generate executable file
            exec_loc = self.__create_exec_file('linux.sh')
            # Execute model
            if self.show_terminal:
                os.system('gnome-terminal -e "bash -c ' + exec_loc + ';bash"')
            else:
                os.system('bash -c ' + exec_loc)

        elif self.os_name == 'Darwin' or self.os_name == 'Windows':
            # Generate executable file
            exec_loc = self.__create_exec_file(
                'mac' if self.os_name == 'Darwin' else 'windows.bat'
            )
            # Execute model
            os.system('open ' + exec_loc)

        # Delete file after launch
        #os.delete(exec_loc)

    def __get_project_name(self, folder_location):
        """ A function to extract the AnyLogic project name automatically based on
        the expected files to be found after exporting the model to a standalone
        """
        for f in os.listdir(folder_location):
            matches = re.search('(.*)_linux\.sh', f)
            if matches:
                return matches.group(1)

        raise Exception(
            f"Could not find any executable file in '{folder_location}'. "
            "Have you exported your model correctly?"
        )

    def __id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        """This is to avoid re-writting the an active script. It can happen when
        asyncronous execution"""
        return ''.join(random.choice(chars) for _ in range(size))

    def __create_exec_file(self, file_type):
        """Insert ports information and create executable file"""
        # Read file as string
        with open(f'{self.folder_location}/{self.project_name}_{file_type}', 'r') as file:
            orig_exec_file_str = file.read()
        # Apply regex to insert ports information
        exec_file_str = re.sub(
            '([\s\S]*)(\$\*)([\s\S]*)', f'\g<1>{self.port_arg_str} \g<2>\g<3>', orig_exec_file_str
        )
        # File name and location
        exec_loc = f'{self.folder_location}/{self.project_name}-{self.__id_generator()}.sh'
        # Create and write bash script
        unix_executable = open(exec_loc, "w+")
        unix_executable.write(exec_file_str)
        unix_executable.close()
        # Parse text file to unix executable extension
        os.system('chmod +x ' + exec_loc)

        return exec_loc
