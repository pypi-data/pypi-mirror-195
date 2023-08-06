"""Module entry point."""
from src.student import Student
import argparse


def main():
    """Application entry point."""
    # Define args by command line
    parser = argparse.ArgumentParser(description='Personal welcome for any student')
    parser.add_argument('--name', type=str, help='Student name')
    parser.add_argument('--surname', type=str, help='Student surname')

    args = parser.parse_args()

    # Create an object Person
    student = Student(name=args.name, surname=args.surname)

    # Call method say_hello
    print(student.say_hello())


if __name__ == '__main__':
    main()
