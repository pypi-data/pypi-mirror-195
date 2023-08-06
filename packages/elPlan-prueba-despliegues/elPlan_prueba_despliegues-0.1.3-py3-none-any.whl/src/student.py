"""Module Student class."""


class Student:
    """Class to instance student."""

    def __init__(self, name: str, surname: str):
        """Student class constructor.

        Args:
            name (str): Name of student
            surname (str): Surname of student
        """
        self.name = name
        self.surname = surname

    def say_hello(self) -> str:
        """Welcome student to class.

        Return:
            str: Welcome to class for a student
        """
        return "¡Hello, {} {}! ¡Welcome to class!".format(self.name, self.surname)
