import win32print

printers = [printer[2] for printer in win32print.EnumPrinters(2)]
print(printers)