from tkinter import (
    Tk,
    PhotoImage,
    Frame,
    Label,
    Entry,
    Button,
    StringVar,
)
from tkinter.ttk import Style as TStyle
from tkinter.ttk import Button as TButton
from tkinter.ttk import Checkbutton as TCheckbutton
from tkinter.ttk import OptionMenu as TOptionMenu
from media.media import paths
from tkinter import font as tkfont
from tkinter.filedialog import askopenfilename, askdirectory
from traceback import format_tb
from tkinter import messagebox
from pathlib import Path
from backEnd.gtHelpers import setDirectories, setExternalPackages
from frontEnd.subApps.KALFE import KALFE
from frontEnd.subApps.inkordFE import InkordFE
from frontEnd.subApps.liexFE import LiexFE
from frontEnd.subApps.gotaLabelFE import GotaLabelFE
from frontEnd.subApps.singleLabelFE import SingleLabelFE
from frontEnd.subApps.UALabelFE import UALabelFE
from frontEnd.subApps.pakLijstFE import PakLijstFE
from frontEnd.subApps.orderScanFE import OrderScanFE
from frontEnd.subApps.gtVultInFE import GTVultInFE
from backEnd.constants import appVersion
import os


class App(Tk):
    """This class creates the main app, and also contains all the front end elements which are used in multiple subApps"""

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Makes everything a bit sharper
        self.call("tk", "scaling", 1.5)

        # Set default fonts
        self.titleFont = tkfont.Font(
            family="Helvetica", size=18, weight="bold", underline=True
        )
        self.subTitleFont = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.normalFont = tkfont.Font(family="Helvetica", size=11)
        self.subNormalFont = tkfont.Font(family="Helvetica", size=9)

        # ttk widget fonts need to be set through styles
        s = TStyle()
        s.configure("TCheckbutton", font=("Helvetica", 9))
        s.configure("Gota.TCheckbutton", font=("Helvetica", 9), background="white")
        s.configure("TButton", font=("Helvetica", 9))

        # some general variables used throughout the frond end
        self.generalSuccessText = (
            "Success, u kunt de output vinden in de geselecteerde output folder."
        )

        self.orderSuccessText = "Success, de orders zijn geïmporteerd"
        self.mealOverviewSuccessText = "Success, het maaltijd overzicht is geïmporteerd"
        self.generalFailureText = (
            "Er is iets misgegaan. Controleer of de juiste bestanden zijn geselecteerd."
        )
        self.printFailureText = "Er is iets misgegaan. Controleer of alle velden goed staan en of de outputFile niet open staat."

        self.runLogo = PhotoImage(file=paths.Run)
        self.importLogo = PhotoImage(file=paths.Import)
        self.printLogo = PhotoImage(file=paths.Print)
        self.newLogo = PhotoImage(file=paths.New)
        self.showLogo = PhotoImage(file=paths.Show)
        self.addWeekMenuLogo = PhotoImage(file=paths.AddWeekMenu)
        self.createWeekMenuLogo = PhotoImage(file=paths.CreateWeekMenu)
        self.addLogo = PhotoImage(file=paths.Add)

        # Global settings
        self.configure(padx=5, pady=5)

        # Make app fullscreen and maximized window
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))
        self.state("zoomed")

        self.title(f"Gooise Tafel Software ({appVersion.appVersion})")

        # Set the logo of the toplevel window
        self.GTSoftwareLogo = PhotoImage(file=paths.GTSoftwareLogo)
        self.iconphoto(False, self.GTSoftwareLogo)

        # Container is where the menu and applications are in
        mainContainer = Frame(self)
        mainContainer.pack(side="top", fill="both", expand=True)
        # makes the frames fill the entire width of the screen
        mainContainer.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Loop over different subApps and initialize each one
        for F in (
            KALFE,
            GTVultInFE,
            InkordFE,
            LiexFE,
            GotaLabelFE,
            UALabelFE,
            SingleLabelFE,
            PakLijstFE,
            OrderScanFE,
        ):
            page_name = F.__name__
            frame = F(parent=mainContainer, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order will be the one that is visible.
            frame.grid(row=1, column=0, sticky="nsew")

        # Create the Menu frame on top of all the other frames
        self.frames["Menu"] = Menu(parent=mainContainer, controller=self)
        self.frames["Menu"].grid(row=0, column=0, sticky="nsew")
        self.frames["Menu"].configure(height=120)

        # First page to show is KAL
        self.showFrame("KALFE")

    def showFrame(self, pageName):
        """Show a frame for the given page name"""
        frame = self.frames[pageName]
        frame.tkraise()

    def createMenuButton(self, container, image, pageTitle, column):
        pageName = pageTitle + "FE"
        btnMenu = TButton(
            container,
            image=image,
            text=pageTitle,
            compound="left",
            command=lambda: self.showFrame(pageName),
            padding=5,
        )
        btnMenu.grid(row=0, column=column, sticky="nsew")
        return btnMenu

    def createTitle(self, container, text, row, column, columnSpan):
        lblTitle = Label(container, text=text, font=self.titleFont)
        lblTitle.grid(
            row=row, column=column, columnspan=columnSpan, sticky="nsew", pady=(8, 0)
        )
        return lblTitle

    def createSubTitle(self, container, text, row, column):
        lblSubTitle = Label(container, text=text, font=self.subTitleFont)
        lblSubTitle.grid(row=row, column=column, sticky="w", pady=3, padx=(20, 0))
        return lblSubTitle

    def createAskUserInput(
        self, container, text, row, column, inputFile, initialDir, isFile, fileType
    ):
        lblFrontText = Label(container, text=text, font=self.normalFont)
        lblFrontText.grid(row=row, column=column, sticky="w", pady=3, padx=(20, 0))
        entPath = Entry(
            container,
            textvariable=inputFile,
            width=100,
            font=self.subNormalFont,
        )
        entPath.grid(
            row=row, column=column + 1, columnspan=2, sticky="nsew", pady=3, padx=5
        )
        if isFile:
            btnAksInput = Button(
                container,
                text="Select",
                command=lambda: self.selectFile(inputFile, initialDir, fileType),
                padx=10,
                pady=2,
                font=self.subNormalFont,
            )
        else:
            # Otherwise you have to select a directory
            btnAksInput = Button(
                container,
                text="Select",
                command=lambda: self.selectOutputDir(inputFile, initialDir),
                padx=15,
                pady=2,
                font=self.subNormalFont,
            )
        btnAksInput.grid(
            row=row, column=column + 3, sticky="nsew", padx=(5, 20), pady=3
        )
        return

    def spacer(self, container, row):
        spacer = Label(container, text="")
        spacer.grid(row=row, column=0)

    def createCheckbox(self, container, text, row, column, inputVariable):
        cbCheckBox = TCheckbutton(
            container,
            text=text,
            variable=inputVariable,
        )
        cbCheckBox.grid(row=row, column=column, sticky="nsew", padx=5, pady=3)
        return cbCheckBox

    def createRunButton(self, container, text, row, column, image):
        btnRun = TButton(
            container,
            image=image,
            text="    " + text,
            compound="left",
        )
        btnRun.grid(row=row, column=column, sticky="nsew", padx=5, pady=3)
        return btnRun

    def createHelperButton(self, container, text, row, column):
        btnHelper = Button(
            container,
            text=text,
            padx=10,
            pady=2,
            font=self.subNormalFont,
        )
        btnHelper.grid(row=row, column=column, sticky="nsew", padx=(5, 20), pady=3)
        return btnHelper

    def createDropDown(self, container, text, row, column, selectedVariable, command):
        lblText = Label(container, text=text, font=self.normalFont)
        # put the label and optionMenu in the same column but center one west and other one east to make them closer to eachother
        lblText.grid(row=row, column=column, sticky="w")
        omDropDown = TOptionMenu(container, selectedVariable, command=command)
        omDropDown.grid(row=row, column=column, sticky="e")
        return omDropDown

    def createLabelEntryRow(
        self, container, text, row, column, columnspan, entryTextVariable
    ):
        lblFrontText = Label(container, text=text, font=self.normalFont)
        lblFrontText.grid(row=row, column=column, sticky="w", pady=3, padx=(20, 0))
        entPath = Entry(
            container,
            textvariable=entryTextVariable,
            font=self.subNormalFont,
        )
        entPath.grid(
            row=row,
            column=column + 1,
            columnspan=columnspan,
            sticky="nsew",
            pady=3,
            padx=5,
        )

    def selectFile(self, inputFile: StringVar, initialDir: Path, fileType: str):
        """Asks the user which file he wants to use,"""

        if fileType == "xlsx" or fileType == "xls":
            fileTypesLocal = [("Excel files", ".xlsx .xls")]
        elif fileType == "pdf":
            fileTypesLocal = [("PDF Files", "*.pdf")]
        elif fileType == "csv":
            fileTypesLocal = [("CSV Files", "*.csv")]

        filename = askopenfilename(
            initialdir=initialDir,
            filetypes=fileTypesLocal,
            title="Selecteer uw input",
        )
        if filename:
            inputFile.set(filename)

    def selectOutputDir(self, outputDir: StringVar, initialDir: Path):
        """Asks the user where he wants to save the output"""

        filename = askdirectory(
            initialdir=initialDir,
            title="Selecteer waar u de output wilt opslaan",
        )
        if filename:
            outputDir.set(filename)

    # Error handling and messaging
    def permissionErrorMessage(self, permissionError):
        if permissionError.filename == ".":
            messagebox.showwarning(
                "Error",
                "Selecteer eerst je input.",
            )
        else:
            messagebox.showwarning(
                "Error",
                "Sluit eerst de openstaande output.\r\n\r\nJe kan geen nieuwe output genereren voordat de vorige output gesloten is.",
            )

    def fileNotFoundErrorMessage(self, fileNotFoundError):
        messagebox.showwarning(
            "Error",
            "Kan het opgegeven input bestand of de output folder niet vinden.",
        )

    def generalErrorMessage(self, error, message):
        messagebox.showerror(
            "Error",
            message
            + "\r\n\r\nAls dit probleem zich blijft voordoen neem dan contact op met Jakob.\r\n\r\nError: "
            + error.args[0]
            + "\r\n\r\nErrorLocation: "
            + format_tb(error.__traceback__)[0],
        )


class Menu(Frame):
    """Creates the menu with its corresponding buttons"""

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(7, weight=1)
        self.grid_columnconfigure(8, weight=1)

        self.logoKal = PhotoImage(file=paths.KAL)
        self.logoGTVultIn = PhotoImage(file=paths.GTVultIn)
        self.logoLiex = PhotoImage(file=paths.Liex)
        self.logoInkord = PhotoImage(file=paths.Inkord)
        self.logoGotaLabel = PhotoImage(file=paths.GotaLabel)
        self.logoUALabel = PhotoImage(file=paths.UALabel)
        self.logoSingleLabel = PhotoImage(file=paths.SingleLabel)
        self.logoPakLijst = PhotoImage(file=paths.PakLijst)
        self.logoOrderScan = PhotoImage(file=paths.OrderScan)

        controller.createMenuButton(self, self.logoKal, "KAL", 0)
        controller.createMenuButton(self, self.logoGTVultIn, "GTVultIn", 1)
        controller.createMenuButton(self, self.logoLiex, "Liex", 2)
        controller.createMenuButton(self, self.logoInkord, "Inkord", 3)
        controller.createMenuButton(self, self.logoGotaLabel, "GotaLabel", 4)
        controller.createMenuButton(self, self.logoUALabel, "UALabel", 5)
        controller.createMenuButton(self, self.logoSingleLabel, "SingleLabel", 6)
        controller.createMenuButton(self, self.logoPakLijst, "PakLijst", 7)
        controller.createMenuButton(self, self.logoOrderScan, "OrderScan", 8)


if __name__ == "__main__":
    # $python -m frontEnd.App
    setExternalPackages()
    setDirectories()
    app = App()
    app.mainloop()
