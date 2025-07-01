from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

def test():
    # result = get_files_info("calculator", ".")
    # print("Result for current directory:")
    # print(result)
    # print("")

    # result = get_files_info("calculator", "pkg")
    # print("Result for 'pkg' directory:")
    # print(result)

    # result = get_files_info("calculator", "/bin")
    # print("Result for '/bin' directory:")
    # print(result)

    # result = get_files_info("calculator", "../")
    # print("Result for '../' directory:")
    # print(result)
    # result = get_file_content("calculator", "lorem.txt")
    # print("Content of lorem.txt:")
    # print(result)
    # print("")
    # print("\n" + "-"*50 + "\n")


    # result = get_file_content("calculator", "main.py")
    # print("Content of main.py:")
    # print(result)
    # print("\n" + "-"*50 + "\n")
    
    # # Test case 3: Reading a file in subdirectory
    # result = get_file_content("calculator", "pkg/calculator.py")
    # print("Content of pkg/calculator.py:")
    # print(result)
    # print("\n" + "-"*50 + "\n")
    
    # # Test case 4: Attempting to read a file outside the permitted directory
    # result = get_file_content("calculator", "/bin/cat")
    # print("Attempt to read /bin/cat:")
    # print(result)

    # Test case 1: Write to a file in the calculator directory
    # result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    # print(result)

    # # Test case 2: Write to a file in a subdirectory
    # result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    # print(result)

    # # Test case 3: Attempt to write to a file outside the permitted directory
    # result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    # print("Attempt to write to /tmp/temp.txt:")
    # print(result)

    # Test case 1: Run a Python file in the calculator directory
    print("Running main.py in calculator directory:")
    result = run_python_file("calculator", "main.py")
    print(result)
    print("\n" + "-" * 50 + "\n")
    
    # Test case 2: Run tests.py in calculator directory
    print("Running tests.py in calculator directory:")
    result = run_python_file("calculator", "tests.py")
    print(result)
    print("\n" + "-" * 50 + "\n")
    
    # Test case 3: Try to run a Python file outside the permitted directory
    print("Attempt to run a file outside permitted directory:")
    result = run_python_file("calculator", "../main.py")
    print(result)
    print("\n" + "-" * 50 + "\n")
    
    # Test case 4: Try to run a nonexistent Python file
    print("Attempt to run a nonexistent file:")
    result = run_python_file("calculator", "nonexistent.py")
    print(result)


if __name__ == "__main__":
    test()