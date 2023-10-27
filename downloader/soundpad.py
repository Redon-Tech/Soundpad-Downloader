import win32file

class soundpadInterface():
    def __init__(self) -> None:
        self.handle = win32file.CreateFile(
            r'\\.\pipe\sp_remote_control',
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None
        )
    
    def addSound(self, path: str) -> None:
        win32file.WriteFile(self.handle, f"DoAddSound({path})".encode())
        resp = win32file.ReadFile(self.handle, 64*1024)
        print(f"message: {resp}")

soundpad = soundpadInterface()

# client = pipe_client()