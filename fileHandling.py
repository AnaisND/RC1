import os
import requests
import shutil


def listFiles(fileList):
    listedFiles = ""

    if len(fileList) == 0: return listedFiles
    
    for fileName in fileList:
        listedFiles = listedFiles + fileName + ", "
    return listedFiles[:-2]


def clearFile(filePath):
    try:
        with open(filePath, 'w') as file:
            file.truncate(0)
    except Exception as e:
        print(f"{e}")


def writeBinaryFile(directoryName, fileName, data):
    directory = os.path.join(os.getcwd(), directoryName)
    filePath = os.path.join(directory, fileName)
    clearFile(filePath)
    try:
        with open(filePath, 'wb') as file:
            file.write(data.encode()) 
    except Exception as e:
        print(f"{e}")


def readBinaryFile(directoryName, fileName):
    directory = os.path.join(os.getcwd(), directoryName)
    filePath = os.path.join(directory, fileName)
    try:
        with open(filePath, 'rb') as file:
            binary_data = file.read()
            return binary_data.decode()
    except Exception as e:
        return None
    

def readTextFile(directoryName, fileName):
    initialPath = f"{os.getcwd()}\Sistem de Fisiere\Librarii Private"
    directory = os.path.join(initialPath, directoryName)
    filePath = os.path.join(directory, fileName)
    try:
        with open(filePath, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return None
    except Exception as e:
        return None


def createDirectory(directoryName):
    initialPath = f"{os.getcwd()}\Sistem de Fisiere\Librarii Private"
    directoryPath = os.path.join(initialPath, directoryName)
    try:
        os.makedirs(directoryPath)
    except FileExistsError:
        print(f"Directory '{directoryPath}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


def deleteDirectory(directoryName):
    initialPath = f"{os.getcwd()}\Sistem de Fisiere\Librarii Private"
    directoryPath = os.path.join(initialPath, directoryName)
    try:
        if os.path.exists(directoryPath):
            shutil.rmtree(directoryPath)
        else:
            print(f"Directory '{directoryPath}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


def downloadFileGithub(url, savePath):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(savePath, 'wb') as f:
                f.write(response.content)
    except Exception as e:
        print(f"{e}")


def deleteFile(filePath):
    try:
        if os.path.exists(filePath):
            os.remove(filePath)
    except Exception as e:
        print(f"{e}")


def listClientCommits(key, source):
    url = f"https://api.github.com/repos/{key}/{source}/commits"
    response = requests.get(url)
    commits = response.json()
    commit = commits[0]
    commitTree = commit['commit']['tree']
    url1 = commitTree['url']

    response = requests.get(url1)
    treeData = response.json()
    relativePaths = []
    for fileInfo in treeData['tree']:
        relativePaths.append(fileInfo['path'])
    return relativePaths


def listMyFiles(username):
    initialPath = f"{os.getcwd()}\Sistem de Fisiere\Librarii Private"
    directory = os.path.join(initialPath, username)

    try:
        files = os.listdir(directory)
        files = [f for f in files if os.path.isfile(os.path.join(directory, f))]
        return files
    except Exception as e:
        print(f"Error occurred while listing files in directory: {e}")
        return []
    

def listServerFiles():
    directory = f"{os.getcwd()}\Sistem de Fisiere\Librarie Publica"

    try:
        files = os.listdir(directory)
        files = [f for f in files if os.path.isfile(os.path.join(directory, f))]
        return files
    except Exception as e:
        print(f"Error occurred while listing files in directory: {e}")
        return []


def downloadClientCommits(key, source, receiver):
    url = f"https://api.github.com/repos/{key}/{source}/commits"
    response = requests.get(url)
    commits = response.json()
    commit = commits[0]
    commitTree = commit['commit']['tree']
    url1 = commitTree['url']

    response = requests.get(url1)
    treeData = response.json()
    relativePaths = []
    for fileInfo in treeData['tree']:
        relativePaths.append(fileInfo['path'])

    for path in relativePaths:
        absolutePath = f"https://raw.githubusercontent.com/{key}/{source}/main/{path}"
        initialPathPublic = f"{os.getcwd()}\Sistem de Fisiere\Librarie Publica"
        initialPathPrivate = f"{os.getcwd()}\Sistem de Fisiere\Librarii Private"
        directory = os.path.join(initialPathPrivate, receiver)

        if not os.path.exists(initialPathPublic):
            os.makedirs(initialPathPublic)
        downloadFileGithub(absolutePath, os.path.join(initialPathPublic, path))

        if not os.path.exists(directory):
            os.makedirs(directory)
        downloadFileGithub(absolutePath, os.path.join(directory, path))


def downloadClientFile(username, fileName):
    initialPathPublic = os.path.join(os.getcwd(), "Sistem de Fisiere\Librarie Publica")
    initialPathPrivate = os.path.join(os.getcwd(), "Sistem de Fisiere\Librarii Private")
    receive = os.path.join(initialPathPrivate, username)
    sourceFilePath = os.path.join(initialPathPublic, fileName)
    receiverFilePath = os.path.join(receive, fileName)
    try:
        with open(sourceFilePath, 'rb') as source_file:
            file_data = source_file.read()
            if not os.path.exists(receive):
                os.makedirs(receive)
            with open(receiverFilePath, 'wb') as receiver_file:
                receiver_file.write(file_data)
    except Exception as e:
        print(f"Error downloading file '{fileName}': {e}")


def deleteServerFilesClientOFF(fileList):
    directory = f"{os.getcwd()}\Sistem de Fisiere\Librarie Publica"
    for fileName in fileList:
        if not os.path.exists(directory):
            os.makedirs(directory)
        deleteFile(os.path.join(directory, fileName))


def deleteClientFile(username, fileName):
    initialPathPrivate = f"{os.getcwd()}\Sistem de Fisiere\Librarii Private"
    directory = os.path.join(initialPathPrivate, username)
    file_path = os.path.join(directory, fileName)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(f"File '{fileName}' does not exist in directory '{directory}'.")
    except Exception as e:
        print(f"An error occurred while deleting file '{fileName}': {e}")
