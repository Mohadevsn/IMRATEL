import customtkinter as ctk
from interface import MainApp

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def main():
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
