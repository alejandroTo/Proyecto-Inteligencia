import os
class CreateFolder:
    def createFolder(self,name):
        folder_name = f"{name}/p"
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)
        return folder_name