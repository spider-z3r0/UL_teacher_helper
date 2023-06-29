from .dependencies import pl, sh, logging, tk, filedialog, datetime, List, Dict, Tuple, Union

class Module:
    """
    Represents a university module with attributes like name, code, year, semester, and leader.
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
    
    def structure(self, new_module: bool = False, sub_dirs=['Teaching Material', 'Assessments', 'Module Documents']) -> None:
        """
        Sets up the module by creating the module directory and subdirectory structure.

        Also generates a log file for the module to keep track of what has been done. This is hidden from the user, but can be accessed by 
        the module through a function that will be defined later. 

        Args:
            new_module (bool, optional): Whether it is a new module or an existing one. Defaults to False.
            sub_dirs (list, optional): List of subdirectories to create. Defaults to ['Teaching Material', 'Assignments', 'Module Documents'].
        """
        # Check if the method has already been executed
        if self._check_method_execution('structure'):
            raise RuntimeError("The 'structure' method has already been executed. "
                               "Running it again risks overwriting work.")

        # Create the module directory path
        self.root = self.root / f'{self.code} {self.semester} {self.year}'
        # Make the module root directory
        try:
            self.root.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            print(f"Module {self.name} {self.code} has already been created at {self.root}. "
                  f"\nPlease use the existing module or delete it and create a new one.")
            return

        # Make the subdirectories by iterating over the list of subdirectories
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
        logging.info(
            f"'structure' method deployed on {datetime.now()}."
            
        )
    
    def teaching_structure(self, weeks: int = 13, topics: List[str] = []) -> None:
        """
        Sets up the subdirectory structure in the Teaching Material directory.
        If the user provides a list of topics, the subdirectories will be named in the format 'Week {week_number} - {topic}',
        otherwise, they will be named 'Week {week_number}'.

        Args:
            weeks (int, optional): The number of weeks. Defaults to 13 (as this is the standard number of teaching weeks in a UL semester).
            topics (List[str], optional): A list of topics corresponding to each week. Defaults to [].

        Raises:
            RuntimeError: If the 'teaching_structure' method has already been executed.

            AssertionError: If the number of weeks is less than or equal to 0.

            AssertionError: If the number of topics provided is not equal to the number of weeks.

        Example:
            >>> module = Module("Example Module", "CODE123", "2022-23", "AUT", "John Doe")
            >>> module.teaching_structure() # using the default values
            # Creates subdirectories: 'Week 1', 'Week 2', ..., 'Week 13'
            >>> module.teaching_structure(5, ['Introduction', 'Topic A', 'Topic B', 'Topic C', 'Conclusion'])
            # Creates subdirectories: 'Week 1 - Introduction', 'Week 2 - Topic A', ..., 'Week 5 - Conclusion'
        """

        # Get the path to the Teaching Material directory
        material_dir = self.root / 'Teaching Material'

        # Check if the method has already been executed
        if self._check_method_execution('teaching_structure'):
            raise RuntimeError("The 'teaching_structure' method has already been executed. "
                            "Running it again risks overwriting work."
                            "You can manually create new folders in the Teaching Material directory.")

        # Assert the number of weeks
        assert weeks > 0, "The number of weeks must be greater than 0"

        # Assert that the number of topics matches the number of weeks (if provided)
        if topics:
            assert len(topics) == weeks, "The number of topics must be equal to the number of weeks"

        # Create the subdirectories based on the provided topics or default names
        for week in range(1, weeks + 1):
            topic_name = f'Week {week}'
            if topics:
                topic_name = f'Week {week} - {topics[week - 1]}'
            (material_dir / topic_name).mkdir(parents=True, exist_ok=False)

        # Log the method execution
        logging.info(f"'teaching_structure' method deployed on {datetime.now()}")

        
    # Need to think about how to capture documents from previous years of the module... or if this is even necessary
    # my sense is it is necessary, especially if using template documents like the module handbook, the departmental grading document, etc.
    # but it might be better to create a method that copies one document at a time and logs it, rather than a method that copies all documents at once


    def copy_documents(self, documents: Union[pl.Path, List[pl.Path]], sub_dir_name: str = 'Module Documents') -> None:
        """
        Copies documents to the Module Documents subdirectory.

        Args:
            documents (Union[pl.Path, List[pl.Path]]): Either a single path or a list of paths to the documents to be copied.
            sub_dir (str, optional): The subdirectory to copy the documents to. Defaults to 'Module Documents'.

        Raises:
            ValueError: If the provided documents argument is neither a path nor a list of paths.
        """
        # Get the path to the Module Documents subdirectory
        documents_dir = self.root / sub_dir_name

        # Convert single path to a list
        if isinstance(documents, pl.Path):
            documents = [documents]

        # Check if the method has already been executed
        method_executed = self._check_method_execution('copy_documents')

        # Check for existing files with the same name
        existing_files = [
            doc.name for doc in documents if (documents_dir / doc.name).exists()
        ]

        # Ask for user confirmation if there are existing files and the method has been executed before
        if existing_files and method_executed:
            print(
                "The following files already exist in the Module Documents folder:\n"
                f"{', '.join(existing_files)}"
            )
            confirmation = input(
                "Running 'copy_documents' again risks overwriting existing files. "
                "Are you sure you want to continue? (Y/N): "
            ).strip().lower() or 'n'
            if confirmation.strip().lower() != 'y':
                print("Method execution canceled.")
                return

        # Copy the documents to the Module Documents subdirectory
        for document in documents:
            document_name = document.name
            document_path = documents_dir / document_name
            sh.copy(document, document_path)

        # Log the method execution
        logging.info(f"'copy_documents' method deployed on {datetime.now()}"
                     f"\nCopied documents: {', '.join([doc.name for doc in documents])}")

    def gather_documents(self, explorer: bool = False) -> List[pl.Path]:
        """
        Interactive method to gather a list of document paths chosen by the user.

        Args:
            explorer (bool, optional): Whether to open a file explorer window for selecting documents.
                Defaults to False.

        Returns:
            List[Path]: A list of selected document paths.

        Example:
            >>> module = Module(...)
            >>> documents = module.gather_documents(explorer=True)
            >>> module.copy_documents(documents)
        """
        document_paths = []

        if explorer:
            root = tk.Tk()
            root.withdraw()

        print("Please select documents to add:")
        print("Enter 'q' to finish and proceed with copying.")

        if explorer:
            file_paths = filedialog.askopenfilenames()
            document_paths = [pl.Path(file_path) for file_path in file_paths]
        else:
            while True:
                file_path = input("Enter the path of a document: ").strip()
                if file_path.lower() == 'q':
                    break

                path = pl.Path(file_path)
                if not path.is_file():
                    print("Invalid file path. Please try again.")
                    continue

                document_paths.append(path)

        return document_paths
        

    def _check_method_execution(self, method_name: str) -> bool:
        """
        Checks if a method has already been executed by searching the log file.

        Args:
            method_name (str): The name of the method to check.

        Returns:
            bool: True if the method has been executed, False otherwise.
        """
        log_path = self.root / 'module_log.txt'
        if log_path.exists():
            with open(log_path, 'r') as log_file:
                log_contents = log_file.read()
                if f"'{method_name}' method deployed on" in log_contents:
                    return True
        return False
