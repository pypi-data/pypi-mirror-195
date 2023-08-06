import os
import shutil
import rpy.util
import rpy.task_raii_printing

def __install(hooksPath):
    root_path = rpy.util.find_root()

    if not os.path.exists(hooksPath):
        return
    
    hooks = os.listdir(hooksPath)

    for hook in hooks:
        src = os.path.join(hooksPath, hook)
        dst = os.path.join(root_path, ".git", "hooks", hook)
        shutil.copy(src, dst)

def run(hooksPath):
    task = rpy.task_raii_printing.TaskRaiiPrint("Installing git hooks")
    __install(hooksPath)