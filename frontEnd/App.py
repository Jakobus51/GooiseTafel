#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from media.media import paths
from tkinter import font as tkfont
from backEnd.constants import saveLocations as sl
from tkinter.filedialog import askopenfilename, askdirectory
from backEnd.KAL import runKal
from backEnd.liex import runLiex
from backEnd.inkord import runInkord
from backEnd.pakLijst import runPakLijst

from traceback import format_tb
from tkinter import messagebox
from pathlib import Path
from backEnd.gtHelpers import setDirectories


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.tk.call("tk", "scaling", 1.5)

        self.titleFont = tkfont.Font(
            family="Helvetica", size=18, weight="bold", underline=True
        )
        self.subTitleFont = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.normalFont = tkfont.Font(family="Helvetica", size=11)
        self.subNormalFont = tkfont.Font(family="Helvetica", size=9)

        self.successMessage = (
            "Success, u kunt de output vinden in de geselecteerde output folder."
        )
        self.failureMessage = "Er is iets misgegaan. Controleer of de juiste documenten geselecteerd zijn en of de outputFile niet open staat.\r\n\r\nAls dit probleem zich blijft voordoen neem dan contact op met Jakob.\r\n\r\nError location:"
        self.runLogo = tk.PhotoImage(file=paths.Run)

        self.extraWhiteSpace = "      "

        self.geometry("1200x900")
        self.title("Gooise Tafel Software")
        self.configure(padx=5, pady=5)

        # Container is where the menu and applications are in
        mainContainer = tk.Frame(self)
        mainContainer.pack(side="top", fill="both", expand=True)
        # makes the frames fill the entire widt of the screen
        mainContainer.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (KAL, Inkord, Liex, GotaLabel, SingleLabel, PakLijst):
            page_name = F.__name__
            frame = F(parent=mainContainer, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=1, column=0, sticky="nsew")

        self.frames["Menu"] = Menu(parent=mainContainer, controller=self)
        self.frames["Menu"].grid(row=0, column=0, sticky="nsew")
        self.frames["Menu"].configure(height=120)

        self.showFrame("KAL")

    def showFrame(self, pageName):
        """Show a frame for the given page name"""
        frame = self.frames[pageName]
        frame.tkraise()

    def createMenuButton(self, container, image, pageName, column):
        btnMenu = ttk.Button(
            container,
            image=image,
            text=pageName,
            compound="left",
            command=lambda: self.showFrame(pageName),
            padding=5,
        )
        btnMenu.grid(row=0, column=column, sticky="nsew")
        return btnMenu

    def createTitle(self, container, text, row, column, columnSpan):
        lblTitle = tk.Label(container, text=text, font=self.titleFont)
        lblTitle.grid(
            row=row, column=column, columnspan=columnSpan, sticky="nsew", pady=(8, 0)
        )
        return lblTitle

    def createSubTitle(self, container, text, row, column):
        lblSubTitle = tk.Label(container, text=text, font=self.subTitleFont)
        lblSubTitle.grid(row=row, column=column, sticky="nsew", pady=3, padx=(20, 0))
        return lblSubTitle

    def createAskUserInput(
        self, container, text, row, column, inputFile, initialDir, isFile, fileType
    ):
        lblFrontText = tk.Label(container, text=text, font=self.normalFont)
        lblFrontText.grid(row=row, column=column, sticky="nsew", pady=3)
        entPath = tk.Entry(
            container,
            textvariable=inputFile,
            width=100,
            font=self.subNormalFont,
        )
        entPath.grid(row=row, column=column + 1, columnspan=2, sticky="nsew", pady=3)
        if isFile:
            btnAksInput = tk.Button(
                container,
                text="Select",
                command=lambda: self.selectFile(inputFile, initialDir, fileType),
                padx=10,
                pady=2,
                font=self.subNormalFont,
            )
        else:
            btnAksInput = tk.Button(
                container,
                text="Select",
                command=lambda: self.selectOutputDir(inputFile, initialDir),
                padx=15,
                pady=2,
                font=self.subNormalFont,
            )
        btnAksInput.grid(
            row=row, column=column + 3, sticky="nsew", padx=(5, 22), pady=3
        )
        return

    def spacer(self, container, row):
        spacer = tk.Label(container, text="")
        spacer.grid(row=row, column=0)

    def createCheckbox(self, container, text, row, column, inputVariable):
        cbCheckBox = tk.Checkbutton(
            container,
            text=text,
            variable=inputVariable,
            anchor="w",
            font=self.subNormalFont,
        )
        cbCheckBox.grid(row=row, column=column, sticky="nsew", padx=5, pady=3)
        # cbShowPdf.select()
        return cbCheckBox

    def createRunButton(self, container, text, row, column) -> ttk.Button:
        btnRun = ttk.Button(
            container,
            image=self.runLogo,
            text="    " + text,
            compound="left",
            padding=4,
        )
        btnRun.grid(row=row, column=column, sticky="nsew", padx=5, pady=3)
        return btnRun

    def selectFile(self, inputFile: tk.StringVar, initialDir: Path, fileType: str):
        if fileType == "xlsx" or fileType == "xls":
            fileTypesLocal = [("Excel files", ".xlsx .xls")]
        elif fileType == "csv":
            fileTypesLocal = [("CSV Files", "*.csv")]

        print(fileTypesLocal)
        """Asks the user which file he wants to use,"""
        filename = askopenfilename(
            initialdir=initialDir,
            filetypes=fileTypesLocal,
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
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)

        self.logoKal = tk.PhotoImage(file=paths.KAL)
        self.logoLiex = tk.PhotoImage(file=paths.Liex)
        self.logoInkord = tk.PhotoImage(file=paths.Inkord)
        self.logoGotaLabel = tk.PhotoImage(file=paths.GotaLabel)
        self.logoSingleLabel = tk.PhotoImage(file=paths.SingleLabel)
        self.logoPakLijst = tk.PhotoImage(file=paths.PakLijst)

        controller.createMenuButton(self, self.logoKal, "KAL", 0)
        controller.createMenuButton(self, self.logoLiex, "Liex", 1)
        controller.createMenuButton(self, self.logoInkord, "Inkord", 2)
        controller.createMenuButton(self, self.logoGotaLabel, "GotaLabel", 3)
        controller.createMenuButton(self, self.logoSingleLabel, "SingleLabel", 4)
        controller.createMenuButton(self, self.logoPakLijst, "PakLijst", 5)


class KAL(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Make the last column span the screen, making the title center
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # set variables which get set and will be passed into the function
        ordersFile = tk.StringVar()
        customersFile = tk.StringVar()
        outputDir = tk.StringVar(value=sl.KALOutput)
        showPdfBool = tk.BooleanVar(value=True)

        # Set title and subtitle
        controller.createTitle(self, "KAL", 0, 0, 4)
        controller.createSubTitle(self, f"Input{controller.extraWhiteSpace}", 1, 0)

        # create User input where you ask the orders file
        controller.createAskUserInput(
            self, "Orders:", 2, 0, ordersFile, sl.KALInput, True, "xls"
        )

        # create User input where you ask the customer file
        controller.createAskUserInput(
            self, "Klanten:", 3, 0, customersFile, sl.CustomersInput, True, "xlsx"
        )

        # Make some space and set output subtitle
        controller.spacer(self, 4)
        controller.createSubTitle(self, f"Output{controller.extraWhiteSpace}", 5, 0)

        # Ask for the location to save the pdf
        controller.createAskUserInput(
            self, "Opslag:", 6, 0, outputDir, sl.KALOutput, False, None
        )

        # set whether or not you want to see he pdf after creation
        controller.createCheckbox(
            self, "Laat de pdf zien nadat hij gemaakt is", 7, 1, showPdfBool
        )
        controller.spacer(self, 8)

        # Create button and assign run command to it
        btnRun = controller.createRunButton(self, "Start KAL", 9, 1)
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
                        "Success",
                        controller.successMessage,
                    )
            except Exception as err:
                messagebox.showerror(
                    "Error",
                    controller.failureMessage + format_tb(err.__traceback__)[0],
                )


class Liex(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Make the last column span the screen, making the title center
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # set variables which get set and will be passed into the function
        WebShopOrdersFile = tk.StringVar()
        customersFile = tk.StringVar()
        outputDir = tk.StringVar(value=sl.LiexOutput)

        # Set title and subtitle
        controller.createTitle(self, "Liex", 0, 0, 4)
        controller.createSubTitle(self, f"Input{controller.extraWhiteSpace}", 1, 0)

        # create User input where you ask the webshop orders file
        controller.createAskUserInput(
            self, "LightSpeed:", 2, 0, WebShopOrdersFile, sl.LiexInput, True, "csv"
        )

        # create User input where you ask the customer file
        controller.createAskUserInput(
            self, "Klanten:", 3, 0, customersFile, sl.CustomersInput, True, "xlsx"
        )

        # Make some space and set output subtitle
        controller.spacer(self, 4)
        controller.createSubTitle(self, f"Output{controller.extraWhiteSpace}", 5, 0)

        # Ask for the location to save the pdf
        controller.createAskUserInput(
            self, "Opslag:", 6, 0, outputDir, sl.LiexOutput, False, None
        )
        controller.spacer(self, 7)

        # Create button and assign run command to it
        btnRun = controller.createRunButton(self, "Start Liex", 8, 1)
        btnRun.configure(command=lambda: runLiexApp())

        def runLiexApp():
            """Runs the Liex function with the entry fields as input, throws error if something goes wrong"""
            try:
                runLiex(
                    Path(WebShopOrdersFile.get()),
                    Path(customersFile.get()),
                    Path(outputDir.get()),
                )
                messagebox.showinfo(
                    "Success",
                    controller.successMessage,
                )
            except Exception as err:
                messagebox.showerror(
                    "Error",
                    controller.failureMessage + format_tb(err.__traceback__)[0],
                )


class Inkord(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Make the last column span the screen, making the title center
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # set variables which get set and will be passed into the function
        ordersFile = tk.StringVar()
        outputDir = tk.StringVar(value=sl.InkordOutput)
        showPdfBool = tk.BooleanVar(value=True)

        # Set title and subtitle
        controller.createTitle(self, "Inkord", 0, 0, 4)
        controller.createSubTitle(self, f"Input{controller.extraWhiteSpace}", 1, 0)

        # create User input where you ask the orders file
        controller.createAskUserInput(
            self, "Orders:", 2, 0, ordersFile, sl.InkordInput, True, "xlsx"
        )

        # Make some space and set output subtitle
        controller.spacer(self, 3)
        controller.createSubTitle(self, f"Output{controller.extraWhiteSpace}", 4, 0)

        # Ask for the location to save the pdf
        controller.createAskUserInput(
            self, "Opslag:", 5, 0, outputDir, sl.InkordOutput, False, None
        )

        # set whether or not you want to see he pdf after creation
        controller.createCheckbox(
            self, "Laat de pdf zien nadat hij gemaakt is", 6, 1, showPdfBool
        )
        controller.spacer(self, 7)

        # Create button and assign run command to it
        btnRun = controller.createRunButton(self, "Start Inkord", 8, 1)
        btnRun.configure(command=lambda: runInkordApp())

        def runInkordApp():
            """Runs the Inkord function with the entry fields as input, throws error if something goes wrong"""
            try:
                runInkord(
                    Path(ordersFile.get()),
                    Path(outputDir.get()),
                    showPdfBool.get(),
                )
                if not showPdfBool.get():
                    messagebox.showinfo(
                        "Success",
                        controller.successMessage,
                    )
            except Exception as err:
                messagebox.showerror(
                    "Error",
                    controller.failureMessage + format_tb(err.__traceback__)[0],
                )


class GotaLabel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Makes the entry widget the biggest and make the second and third column equal length
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # set variables which get set and will be passed into the function
        ordersFile = tk.StringVar()
        outputDir = tk.StringVar(value=sl.PakLijstOutput)
        showPdfBool = tk.BooleanVar(value=True)

        # Set title and subtitle
        controller.createTitle(self, "GotaLabel", 0, 0, 4)

        controller.createSubTitle(self, f"Input{controller.extraWhiteSpace}", 1, 0)

        # create User input where you ask the orders file
        controller.createAskUserInput(
            self, "Dag Orders:", 2, 0, ordersFile, sl.GotaLabelInput, True, "xlsx"
        )


class SingleLabel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Makes the entry widget the biggest and make the second and third column equal length
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # Set title and subtitle
        controller.createTitle(self, "SingleLabel", 0, 0, 4)


class PakLijst(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Makes the entry widget the biggest and make the second and third column equal length
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # set variables which get set and will be passed into the function
        ordersFile = tk.StringVar()
        outputDir = tk.StringVar(value=sl.PakLijstOutput)
        showPdfBool = tk.BooleanVar(value=True)

        # Set title and subtitle
        controller.createTitle(self, "PakLijst", 0, 0, 4)
        controller.createSubTitle(self, f"Input{controller.extraWhiteSpace}", 1, 0)

        # create User input where you ask the orders file
        controller.createAskUserInput(
            self, "Dag Orders:", 2, 0, ordersFile, sl.PakLijstInput, True, "xlsx"
        )

        # Make some space and set output subtitle
        controller.spacer(self, 3)
        controller.createSubTitle(self, f"Output{controller.extraWhiteSpace}", 4, 0)

        # Ask for the location to save the pdf
        controller.createAskUserInput(
            self, "Opslag:", 5, 0, outputDir, sl.InkordOutput, False, None
        )

        # set whether or not you want to see he pdf after creation
        controller.createCheckbox(
            self, "Laat de pdf zien nadat hij gemaakt is", 6, 1, showPdfBool
        )
        controller.spacer(self, 7)

        # Create button and assign run command to it
        btnRunRoute = controller.createRunButton(self, "Start PakLijst PER ROUTE", 8, 1)
        btnRunRoute.configure(command=lambda: runPakLijstApp(isPerRoute=True))
        btnRunTotal = controller.createRunButton(self, "Start PakLijst TOTAAL", 8, 2)
        btnRunTotal.configure(command=lambda: runPakLijstApp(isPerRoute=False))

        def runPakLijstApp(isPerRoute):
            """Runs the PakLijst function with the entry fields as input, throws error if something goes wrong"""
            try:
                runPakLijst(
                    Path(ordersFile.get()),
                    Path(outputDir.get()),
                    isPerRoute,
                    showPdfBool.get(),
                )
                if not showPdfBool.get():
                    messagebox.showinfo(
                        "Success",
                        controller.successMessage,
                    )
            except Exception as err:
                messagebox.showerror(
                    "Error",
                    controller.failureMessage + format_tb(err.__traceback__)[0],
                )


if __name__ == "__main__":
    setDirectories()
    app = App()
    app.mainloop()
