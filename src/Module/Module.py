from .dependencies import *


class Module:
    """
    Represents a university module with attributes like name, code, year, semester, and leader.

    Attributes:
        name (str): The name of the module.
        code (str): The code of the module.
        year (str): The calendar year of study for the module.
        semester (str): The semester of study for the module (SPR or AUT).
        leader (str): The module/course leader.
        root (pl.Path): The root directory path.
            set to current working directory by default.  

    Example:
        >>> from Module import Module
        >>> module = Module('Software Engineering', 'CM10227', '2020', 'SPR', 'Dr. John Smith')
        

    """

    def __init__(
        self,
        name: str,
        code: str,
        year: str,
        semester: str,
        leader: str,
        root: pl.Path = pl.Path.cwd(),
        exams: int = 0,
        coursework: int = 0,
    ) -> None:
        """
        Initializes a new Module instance.

        Args:
            name (str): The name of the module.
            code (str): The code of the module.
            year (str): The year of study for the module.
            semester (str): The semester of study for the module (SPR or AUT).
            leader (str): The module leader.
            root (pl.Path, optional): The root directory path. Defaults to current working directory.
            exams (int, optional): The number of exams. Defaults to 0.
            coursework (int, optional): The number of coursework. Defaults to 0.
        """
        self.name = name
        self.code = code
        self.year = year
        self.semester = semester
        self.leader = leader
        self.root = root

    def __repr__(self) -> str:
        """
        Returns a string representation of the module.

        Returns:
            str: A string representation of the module.
        """
        return f"Module({self.name}, {self.code}, {self.year}, {self.semester}, {self.leader})"
    
    def structure(self, new_module: bool = False, sub_dirs=['Teaching Material', 'Assignments', 'Module Documents']) -> None:
        """
        Sets up the module by creating the module directory and subdirectory structure.

        Also generates a log file for the module to keep track of what has been done. This is hidden from the user, but can be accessed by 
        the module through a function that will be defined later. 

        Args:
            new_module (bool, optional): Whether it is a new module or an existing one. Defaults to False.
            sub_dirs (list, optional): List of subdirectories to create. Defaults to ['Teaching Material', 'Assignments', 'Module Documents'].

        Raises:
            FileExistsError: If the module already exists.

        Example:
            >>> module = Module('Software Engineering', 'CM10227', '2020', 'SPR', 'Dr. John Smith')
            >>> module.structure(root=pl.Path.cwd().parent, sub_dirs=['Teaching Material', 'Assignments', 'Module Documents'])

        """
        # Create the module directory path
        self.root = self.root / f'{self.code} {self.semester} {self.year}'
        # Make the module root directory
        try:
            self.root.mkdir(parents=True, exist_ok=False)

                    # Make the subdirectories by iterating over the list of subdirectories
            for sub_dir in sub_dirs:
                (self.root / sub_dir).mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            print(f"Module {self.name} {self.code} has already been created at {self.root}. "
                  f"\nPlease use the existing module or delete it and create a new one.")
            return

       
        # Generate log file
        log_path = self.root / '.module_log.txt'
        logging.basicConfig(filename=log_path, level=logging.INFO)
        sub_dirs_str = '\n'.join(sub_dirs)
        logging.info(
            f"Module {self.name} {self.code} created at {datetime.now()}:"
            f"\nCreated Sub_directories:\n{sub_dirs_str}"
        )