"""
Assessment module for the UL Teacher Helper application. This houses the code for the Assessment class, which is a child class of the Module class. 
This class is used to create an object that represents an assessment in the UL Teacher Helper application, which can be used to help the adminitration of the assessment, both
before and after the assessment has been completed.
"""

from ..dependencies import logging, datetime, List, pl, date, Tuple, Union
from ..Module import Module

class Assessment(Module):
    """
    Represents an assessment for a module in the UL Teacher Helper application.
    """

    def __init__(
        self,
        assessment_type: str,
        name: str,
        due_date: date,
        module_name: str,
        module_code: str,
        module_leader: str,
        percentage_of_module: float,
        module_year: str,
    ) -> None:
        """
        Constructor for the Assessment class. Initializes a new Assessment instance.

        Args:
            assessment_type (str): The type of assessment.
            name (str): The name of the assessment.
            due_date (date): The due date of the assessment.
            module_name (str): The name of the module the assessment is a part of.
            module_code (str): The code of the module the assessment is a part of.
            module_leader (str): The module leader.
            percentage_of_module (float): The percentage weightage of the assessment in the module.
            module_year (str): The year of study for the module.
        """
        super().__init__(module_name, module_code, module_leader)
        self.assessment_type = assessment_type
        self.name = name
        self.due_date = due_date
        self.percentage_of_module = percentage_of_module
        self.module_year = module_year

    def structure(self) -> None:
        """
        Sets up the module for the assessment by creating the necessary directory and subdirectory structure.

        Args:
            new_module (bool, optional): Whether it is a new module or an existing one. Defaults to False.
        """
        # Check if the method has already been executed
        if self._check_method_execution('structure'):
            raise RuntimeError("The 'structure' method has already been executed. "
                               "Running it again risks overwriting work.")

        # Create the module directory path
        self.root = self.root / 'Assessment' / f"{self.name} ({self.assessment_type})"
        # Make the module root directory
        try:
            self.root.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            print(f"Module {self.name} {self.code} has already been created at {self.root}. "
                  f"\nPlease use the existing module or delete it and create a new one.")
            return

        # Make the subdirectories by iterating over the list of subdirectories
        sub_dirs = ['Assessment Documents and Templates']
        for sub_dir in sub_dirs:
            (self.root / sub_dir).mkdir(parents=True, exist_ok=False)

        # Generate log file
        log_path = self.root / 'module_log.txt'
        logging.basicConfig(filename=log_path, level=logging.INFO)
        sub_dirs_str = '\n\t'.join(sub_dirs)
        logging.info(
            f"Module {self.name} {self.code} created at {datetime.now()}:"
            f"\nCreated Sub_directories:\n{sub_dirs_str}"
        )

        # Log the method execution
        logging.info(f"'structure' method deployed on {datetime.now()}.")


    # Creates a .txt file with the Graders names so this can be used during the marking process 
    def graders_list(self, graders: List[str]) -> Tuple[List[str], pl.Path]: 
        """This function creates a .txt file with the Graders names so this can be used during the marking process. 
        This is really important for other administratives tasks such as distributing the marking load between the markers, and then
        easily collating the marks at the end of the marking process. 
        
        """

        # Check if the method has already been executed
        if self._check_method_execution('graders_list'):
            raise RuntimeError("The 'graders_list' method has already been executed. "
                               "Running it again risks overwriting work.")

        # Create the graders list path
        graders_list_path = self.root / 'Graders List.txt'

        # Write the graders list to the file
        with open(graders_list_path, 'w') as f:
            for grader in graders:
                f.write(f'{grader}\n')

        # Log the method execution
        logging.info(f"'graders_list' method deployed on {datetime.now()}.")

        return graders_list_path
    

