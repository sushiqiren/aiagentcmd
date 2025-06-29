from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


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


    result = get_file_content("calculator", "main.py")
    print("Content of main.py:")
    print(result)
    print("\n" + "-"*50 + "\n")
    
    # Test case 3: Reading a file in subdirectory
    result = get_file_content("calculator", "pkg/calculator.py")
    print("Content of pkg/calculator.py:")
    print(result)
    print("\n" + "-"*50 + "\n")
    
    # Test case 4: Attempting to read a file outside the permitted directory
    result = get_file_content("calculator", "/bin/cat")
    print("Attempt to read /bin/cat:")
    print(result)

if __name__ == "__main__":
    test()