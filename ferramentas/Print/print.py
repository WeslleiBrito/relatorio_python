import os
import platform
import tkinter as tk
from tkinter import messagebox
import win32api
import win32print


class Print:
    def __init__(self, file_path: str, printer_name=None):
        self.__file_path = file_path
        self.__printer_name = printer_name

    def print_pdf(self):
        try:
            if platform.system() == "Windows":
                # Se nenhuma impressora for especificada, obtém a impressora padrão
                if self.__printer_name is None:
                    self.__printer_name = win32print.GetDefaultPrinter()

                # Usa o Adobe Reader para imprimir
                print(f"Imprimindo em: {self.__printer_name}")
                win32api.ShellExecute(0, "printto", self.__file_path, f'"{self.__printer_name}"', ".", 0)

            elif platform.system() == "Darwin":  # Mac
                os.system(f"open -a 'Preview' {self.__file_path} "
                          f"&& osascript -e 'tell application \"Preview\" to print document 1'")
            else:  # Linux
                os.system(f"lp {self.__file_path}")

        except Exception as e:
            # Exibe uma mensagem de erro usando tkinter
            root = tk.Tk()
            root.withdraw()  # Oculta a janela principal
            messagebox.showerror("Erro ao imprimir", str(e))


# Exemplo de uso
# printer = Print(file_path="C:/caminho/para/seu_arquivo.pdf", printer_name="EPSON L395 Series")
# printer.print_pdf()
