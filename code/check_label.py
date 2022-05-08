import os

def getDirectoryList(path):
    directoryList = []
    prefix = []
    #return nothing if path is a file
    if os.path.isfile(path):
        return []

    #add dir to directorylist if it contains .txt files
    if len([f for f in os.listdir(path) if f.endswith('.xml')])>0:
        directoryList.append(path)

    for d in os.listdir(path):
        new_path = os.path.join(path, d)
        if os.path.isdir(new_path):
            directoryList += getDirectoryList(new_path)
    return directoryList

#if __name__ == "__main__":
#   print(getDirectoryList('../data/images/'))