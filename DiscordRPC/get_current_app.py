import psutil
import win32process
import win32gui

def GCAR():
    r"""
    GCAR : Get Current Application Running. a method to get your current application you open.
    ---
    Parameter :
    Nothing just add () after GCAR, like `GCAR()`
    """
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    app = psutil.Process(pid[-1]).name()
    app = app.replace(".exe", "")
    app = app.capitalize()
    if app == "Code": # Because if you open visual studio code, only "Code" will appears, so I just changed it ;>
        app = "Visual Studio Code"
    
    return app
