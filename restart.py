import os


def createDirectory1(directoryName):
    directoryPath = os.path.join(os.getcwd(), directoryName)
    try:
        os.makedirs(directoryPath)
    except FileExistsError:
        print(f"Directory '{directoryPath}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


def createDirectory2(directoryName):
    initialPath = f"{os.getcwd()}\Sistem de Fisiere"
    directoryPath = os.path.join(initialPath, directoryName)
    try:
        os.makedirs(directoryPath)
    except FileExistsError:
        print(f"Directory '{directoryPath}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


createDirectory1("Sistem de Fisiere")
createDirectory2("Librarie Publica")
createDirectory2("Librarii Private")

# python restart.py