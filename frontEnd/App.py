#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.pathchooserinput import PathChooserInput
from ttkthemes import ThemedTk
from media.media import paths
from PIL import Image, ImageTk
from tkinter import font as tkfont
from backEnd.constants import saveLocations as sl
from tkinter.filedialog import askopenfilename, askdirectory
from backEnd.KAL import runKal
from traceback import format_tb
from tkinter import messagebox
from pathlib import Path
from backEnd.gtHelpers import setDirectories


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.tk.call("tk", "scaling", 1.5)

        self.titleFont = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.subTitleFont = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.normalFont = tkfont.Font(family="Helvetica", size=12)
        self.subNormalFont = tkfont.Font(family="Helvetica", size=10)

        self.geometry("1400x600")
        self.title("Gooise Tafel Software")
        self.configure(padx=5, pady=5)

        # Menu is where the menu buttons are in
        menu = tk.Frame(self)

        # Container is where the menu and applications are in
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        # makes the frames fill the entire widt of the screen
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (KAL, Inkord, Liex, GotaLabel):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=1, column=0, sticky="nsew")

        self.frames["Menu"] = Menu(parent=container, controller=self)
        self.frames["Menu"].grid(row=0, column=0, sticky="nsew")
        self.frames["Menu"].configure(height=120)

        self.showFrame("KAL")

    def showFrame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

    def createTitle(self, container, text, row, column, columnSpan):
        lblTitle = tk.Label(container, text=text, font=self.titleFont)
        lblTitle.grid(
            row=row, column=column, columnspan=columnSpan, sticky="nsew", pady=8
        )
        return lblTitle

    def createSubTitle(self, container, text, row, column):
        lblSubTitle = tk.Label(container, text=text, font=self.subTitleFont)
        lblSubTitle.grid(row=row, column=column, sticky="nsew", pady=3)
        return lblSubTitle

    def createUserInput(
        self, container, text, row, column, inputFile, initialDir, isFile
    ):
        lblOrders = tk.Label(container, text=text, font=self.normalFont)
        lblOrders.grid(row=row, column=column, sticky="nsew", pady=3)
        entOrders = tk.Entry(
            container,
            textvariable=inputFile,
            width=100,
            font=self.subNormalFont,
        )
        entOrders.grid(row=row, column=column + 1, sticky="nsew", pady=3)
        if isFile:
            btnGetOrders = tk.Button(
                container,
                text="Select",
                command=lambda: self.selectFile(inputFile, initialDir),
                padx=10,
                pady=2,
                font=self.subNormalFont,
            )
        else:
            btnGetOrders = tk.Button(
                container,
                text="Select",
                command=lambda: self.selectOutputDir(inputFile, initialDir),
                padx=10,
                pady=2,
                font=self.subNormalFont,
            )
        btnGetOrders.grid(row=row, column=column + 2, sticky="nsew", padx=5, pady=3)
        return

    def spacer(self, container, row):
        spacer1 = tk.Label(container, text="")
        spacer1.grid(row=row, column=0)

    def createCheckbox(self, container, text, row, column, inputVariable):
        cbShowPdf = tk.Checkbutton(
            container,
            text=text,
            variable=inputVariable,
            anchor="w",
            font=self.subNormalFont,
        )
        cbShowPdf.grid(row=row, column=column, sticky="nsew", padx=5, pady=3)
        # cbShowPdf.select()
        return cbShowPdf

    def createRunButton(self, container, row, column) -> ttk.Button:
        self.logoKal = tk.PhotoImage(file=paths.Run)
        btnRunKAL = ttk.Button(
            container,
            image=self.logoKal,
            text="   Start KAL",
            compound="left",
            width=30,
            padding=4,
        )
        btnRunKAL.grid(row=row, column=column, sticky="nsew", padx=5, pady=3)
        return btnRunKAL

    def selectFile(self, inputFile: tk.StringVar, initialDir: Path):
        """Asks the user which file he wants to use,"""
        filename = askopenfilename(
            initialdir=initialDir,
            filetypes=[("Excel files", ".xlsx .xls")],
            title="Selecteer uw input",
        )
        if filename:
            inputFile.set(filename)

    def selectOutputDir(self, outputDir: tk.StringVar, initialDir: Path):
        """Asks the user where he wants to save the output"""

        filename = askdirectory(
            initialdir=initialDir,
            title="Selecteer waar u de output wilt opslaan",
        )
        if filename:
            outputDir.set(filename)


class Menu(tk.Frame):
    """Creates the menu with its corresponding buttons"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.logoKal = tk.PhotoImage(file=paths.KAL)
        self.logoLiex = tk.PhotoImage(file=paths.Liex)
        self.logoInkord = tk.PhotoImage(file=paths.Inkord)
        self.logoGotaLabel = tk.PhotoImage(file=paths.GotaLabel)

        buttonWidth = 30
        buttonPad = 5
        btnKal = ttk.Button(
            self,
            image=self.logoKal,
            text="KAL",
            compound="left",
            command=lambda: controller.showFrame("KAL"),
            width=buttonWidth,
            padding=buttonPad,
        )
        btnLiex = ttk.Button(
            self,
            image=self.logoLiex,
            text="Liex",
            compound="left",
            command=lambda: controller.showFrame("Liex"),
            width=buttonWidth,
            padding=buttonPad,
        )
        btnInkord = ttk.Button(
            self,
            image=self.logoInkord,
            text="Inkord",
            compound="left",
            command=lambda: controller.showFrame("Inkord"),
            width=buttonWidth,
            padding=buttonPad,
        )
        btnGotaLabel = ttk.Button(
            self,
            image=self.logoGotaLabel,
            text="GotaLabel",
            compound="left",
            command=lambda: controller.showFrame("GotaLabel"),
            width=buttonWidth,
            padding=buttonPad,
        )

        btnKal.grid(row=0, column=0, sticky="nsew")
        btnLiex.grid(row=0, column=1, sticky="nsew")
        btnInkord.grid(row=0, column=2, sticky="nsew")
        btnGotaLabel.grid(row=0, column=3, sticky="nsew")


class KAL(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_columnconfigure(3, weight=1)

        ordersFile = tk.StringVar()
        customersFile = tk.StringVar()
        outputDir = tk.StringVar(value=sl.KALOutput)
        showPdfBool = tk.BooleanVar(value=True)

        # Set title and subtitle
        controller.createTitle(self, "KAL", 0, 0, 4)
        controller.createSubTitle(self, "Input", 1, 0)

        # create User input where you ask the orders file
        controller.createUserInput(
            self, "     Orders:", 2, 0, ordersFile, sl.KALInput, True
        )

        # create User input where you ask the customer file
        controller.createUserInput(
            self, "     Klanten:", 3, 0, customersFile, sl.KALInput, True
        )

        # Make some space and set output subtitle
        controller.spacer(self, 4)
        controller.createSubTitle(self, "Output", 5, 0)

        # Ask for the location to save the pdf
        controller.createUserInput(
            self, "     Opslag:", 6, 0, outputDir, sl.KALOutput, False
        )

        # set whether or not you want to see he pdf after creation
        controller.createCheckbox(
            self, "Laat de pdf zien nadat hij gemaakt is", 7, 1, showPdfBool
        )
        controller.spacer(self, 8)

        btnRun = controller.createRunButton(self, 9, 1)
        btnRun.configure(command=lambda: runKALApp())

        def runKALApp():
            """Runs the KAL function with the entry fields as input, throws error if something goes wrong"""
            try:
                runKal(
                    Path(ordersFile.get()),
                    Path(customersFile.get()),
                    Path(outputDir.get()),
                    showPdfBool.get(),
                )
                if not showPdfBool.get():
                    messagebox.showinfo(
                        "Succes",
                        "Succes, u kunt de output vinden in de geselecteerde output folder.",
                    )
            except Exception as err:
                messagebox.showerror(
                    "Error",
                    "Er is iets misgegaan. Controleer of de juiste documenten geselecteerd zijn en of de outputFile niet open staat.\r\n\r\nAls dit probleem zich blijft voordoen neem dan contact op met Jakob.\r\n\r\nError location:"
                    + format_tb(err.__traceback__)[0],
                )


class Liex(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Liex", font=controller.titleFont)
        label.pack(side="top", fill="x", pady=10)


class Inkord(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Inkord", font=controller.titleFont)
        label.pack(side="top", fill="x", pady=10)


class GotaLabel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="GotaLabel", font=controller.titleFont)
        label.pack(side="top", fill="x", pady=10)


if __name__ == "__main__":
    setDirectories()
    app = App()
    app.mainloop()
