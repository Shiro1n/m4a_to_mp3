from tkinterdnd2 import TkinterDnD
from src import ConverterGUI

def main():
    root = TkinterDnD.Tk()
    app = ConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()