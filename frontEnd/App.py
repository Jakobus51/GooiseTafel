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
from backEnd.gotaLabel import fetchOrders
from traceback import format_tb
from tkinter import messagebox
from pathlib import Path
from backEnd.gtHelpers import setDirectories
from backEnd.dataClasses.labelHelper import LabelHelper
from backEnd.dataClasses.appEnum import AppEnum
from backEnd.dataClasses.labelInterface import GTlabel
from tkinter.scrolledtext import ScrolledText
from backEnd.labelCreator import createLabels


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Makes everything a bit sharper
        self.tk.call("tk", "scaling", 1.5)

        # Set default fonts
        self.titleFont = tkfont.Font(
            family="Helvetica", size=18, weight="bold", underline=True
        )
        self.subTitleFont = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.normalFont = tkfont.Font(family="Helvetica", size=11)
        self.subNormalFont = tkfont.Font(family="Helvetica", size=9)

        # ttk widget fonts need to be set through styles
        s = ttk.Style()
        s.configure("TCheckbutton", font=("Helvetica", 9))
        s.configure("Gota.TCheckbutton", font=("Helvetica", 9), background="white")

        s.configure("TButton", font=("Helvetica", 9))

        # some general variables used throughout the frond end
        self.generalSuccessMessage = (
            "Success, u kunt de output vinden in de geselecteerde output folder."
        )
        self.generalFailureMessage = "Er is iets misgegaan. Controleer of de juiste documenten geselecteerd zijn en of de outputFile niet open staat.\r\n\r\nAls dit probleem zich blijft voordoen neem dan contact op met Jakob.\r\n\r\nError location:"

        self.orderSuccessMessage = "Success, de orders zijn geïmporteerd"
        self.orderFailureMessage = "Er is iets misgegaan. Controleer of de juiste documenten geselecteerd zijn.\r\n\r\nAls dit probleem zich blijft voordoen neem dan contact op met Jakob.\r\n\r\nError location:"

        self.printFailureMessage = "Er is iets misgegaan. Controleer of alle velden goed staan.\r\n\r\nAls dit probleem zich blijft voordoen neem dan contact op met Jakob.\r\n\r\nError location:"
        self.printSuccessMessage = "Success, de label(s) zijn naar de printer verstuurd"

        self.runLogo = tk.PhotoImage(file=paths.Run)
        self.importLogo = tk.PhotoImage(file=paths.Import)
        self.printLogo = tk.PhotoImage(file=paths.Print)
        self.extraWhiteSpace = "      "

        # Global settings
        self.geometry("1200x800")
        self.title("Gooise Tafel Software")
        self.configure(padx=5, pady=5)

        # Set the logo of the toplevel window
        self.GTSoftwareLogo = tk.PhotoImage(file=paths.GTSoftwareLogo)
        self.iconphoto(False, self.GTSoftwareLogo)

        # Container is where the menu and applications are in
        mainContainer = tk.Frame(self)
        mainContainer.pack(side="top", fill="both", expand=True)
        # makes the frames fill the entire width of the screen
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
        entPath.grid(
            row=row, column=column + 1, columnspan=2, sticky="nsew", pady=3, padx=5
        )
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
        cbCheckBox = ttk.Checkbutton(
            container,
            text=text,
            variable=inputVariable,
        )
        cbCheckBox.grid(row=row, column=column, sticky="nsew", padx=5, pady=3)
        return cbCheckBox

    def createRunButton(self, container, text, row, column, image) -> ttk.Button:
        btnRun = ttk.Button(
            container,
            image=image,
            text="    " + text,
            compound="left",
        )
        btnRun.grid(row=row, column=column, sticky="nsew", padx=5, pady=3)
        return btnRun

    def createDropDown(self, container, text, row, column, selectedVariable, command):
        lblText = tk.Label(container, text=text, font=self.normalFont)
        # put the label and optionMenu in the same column but center one west and other one east to make them closer to eachother
        lblText.grid(row=row, column=column, sticky="w")
        omDropDown = ttk.OptionMenu(container, selectedVariable, command=command)
        omDropDown.grid(row=row, column=column, sticky="e")
        return omDropDown

    def createLabelEntryRow(self, container, text, row, column, entryTextVariable):
        lblFrontText = tk.Label(container, text=text, font=self.normalFont)
        lblFrontText.grid(row=row, column=column, sticky="nsew", pady=3)
        entPath = tk.Entry(
            container,
            textvariable=entryTextVariable,
            font=self.subNormalFont,
        )
        entPath.grid(row=row, column=column + 1, columnspan=2, sticky="nsew", pady=3)

    def selectFile(self, inputFile: tk.StringVar, initialDir: Path, fileType: str):
        """Asks the user which file he wants to use,"""

        if fileType == "xlsx" or fileType == "xls":
            fileTypesLocal = [("Excel files", ".xlsx .xls")]
        elif fileType == "csv":
            fileTypesLocal = [("CSV Files", "*.csv")]

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
        btnRun = controller.createRunButton(self, "Start KAL", 9, 1, controller.runLogo)
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
                        controller.generalSuccessMessage,
                    )
            except Exception as err:
                messagebox.showerror(
                    "Error",
                    controller.generalFailureMessage + format_tb(err.__traceback__)[0],
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
        btnRun = controller.createRunButton(
            self, "Start Liex", 8, 1, controller.runLogo
        )
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
                    controller.generalSuccessMessage,
                )
            except Exception as err:
                messagebox.showerror(
                    "Error",
                    controller.generalFailureMessage + format_tb(err.__traceback__)[0],
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
        btnRun = controller.createRunButton(
            self, "Start Inkord", 8, 1, controller.runLogo
        )
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
                        controller.generalSuccessMessage,
                    )
            except Exception as err:
                messagebox.showerror(
                    "Error",
                    controller.generalFailureMessage + format_tb(err.__traceback__)[0],
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
        self.labelInput = LabelHelper(AppEnum.GotaLabel)

        # set up variable
        self.selectedDeliveryMethod = tk.StringVar("")
        self.selectedCustomerName = tk.StringVar("")
        self.selectedProductName = tk.StringVar("")
        self.checkedList = {}

        # Set title and subtitle
        controller.createTitle(self, "GotaLabel", 0, 0, 4)
        controller.createSubTitle(self, f"Input{controller.extraWhiteSpace}", 1, 0)

        # create User input where you ask the orders file
        controller.createAskUserInput(
            self, "Dag Orders:", 2, 0, ordersFile, sl.GotaLabelInput, True, "xlsx"
        )

        # Create button and assign import orders command to it
        btnImport = controller.createRunButton(
            self, "Importeer Dag Orders", 3, 1, controller.importLogo
        )
        btnImport.configure(command=lambda: importOrders())

        controller.createSubTitle(self, f"Selectie{controller.extraWhiteSpace}", 4, 0)
        self.stCheckBoxContainer = ScrolledText(self, height=20, state="disabled")
        self.stCheckBoxContainer.grid(
            row=5, column=1, columnspan=2, sticky="nsew", padx=5, pady=3
        )

        btnSelectAll = tk.Button(
            self,
            text="Select all",
            command=lambda: self.selectAll(),
            padx=10,
            pady=2,
            font=controller.subNormalFont,
        )
        btnSelectAll.grid(row=5, column=0, sticky="n", padx=5, pady=3)
        btnReset = tk.Button(
            self,
            text="Reset",
            command=lambda: self.reset(),
            padx=10,
            pady=2,
            font=controller.subNormalFont,
        )
        btnReset.grid(row=5, column=0, sticky="s", padx=5, pady=3)

        controller.spacer(self, row=6)
        # Create button and assign import orders command to it
        btnPrint = controller.createRunButton(
            self, "Print Label", 7, 1, controller.printLogo
        )
        btnPrint.configure(command=lambda: printLabels())

        def importOrders():
            """Fetches the orders and set the appropriate fields with the given import data"""
            try:
                self.labelInput = fetchOrders(Path(ordersFile.get()))
                self.cleanUp()
                self.fillCheckBoxes()

            except Exception as err:
                messagebox.showerror(
                    "Error",
                    controller.orderFailureMessage + format_tb(err.__traceback__)[0],
                )

        def printLabels():
            """Print the labels by first filtering on the selected routes, then converting the orders into GTLabels
            and lastly sending them the the labelCreator class (createLabels)"""
            try:
                self.getRoutesToPrint()
                self.labelInput.setLabelsFromDictionaries()
                createLabels(self.labelInput, sl.GotaLabelOutput)
                messagebox.showinfo(
                    "Success",
                    controller.printSuccessMessage,
                )

            except Exception as err:
                messagebox.showerror(
                    "Error",
                    controller.printFailureMessage + format_tb(err.__traceback__)[0],
                )

    def cleanUp(self, *args):
        """Clear the text field and also the checkedList dictionary"""
        self.stCheckBoxContainer.config(state="normal")
        self.stCheckBoxContainer.delete("1.0", tk.END)
        self.stCheckBoxContainer.config(state="disabled")
        self.checkedList.clear()

    def fillCheckBoxes(self, *args):
        """Fill the scrollable text box with checkboxes. Each entry in the dictionary gets its own checkbox and tk.BooleanVar"""
        self.stCheckBoxContainer.config(state="normal")
        for key in self.labelInput.labelDataPerDeliveryMethod:
            deliveries = self.labelInput.labelDataPerDeliveryMethod[key][
                "customerId"
            ].nunique()
            meals = self.labelInput.labelDataPerDeliveryMethod[key]["quantity"].sum()

            self.checkedList[key] = tk.BooleanVar(value=False, name=key)
            cb = ttk.Checkbutton(
                self.stCheckBoxContainer,
                variable=self.checkedList[key],
                text=f"{key} (Leveringen: {deliveries}, Maaltijden: {meals})",
                style="Gota.TCheckbutton",
            )
            # Insert the checkbox and start a new line
            self.stCheckBoxContainer.window_create("end", window=cb)
            self.stCheckBoxContainer.insert("end", "\n")
        self.stCheckBoxContainer.config(state="disabled")

    def selectAll(self, *args):
        """Sets all the boxes to true"""
        for key in self.checkedList:
            self.checkedList[key].set(True)

    def reset(self, *args):
        """Sets all the boxes to false"""
        for key in self.checkedList:
            self.checkedList[key].set(False)

    def getRoutesToPrint(self, *args):
        """Save only the selected routes who you are going to print"""
        routesToPrint = {}
        for key in self.checkedList:
            if self.checkedList[key].get():
                routesToPrint[key] = self.labelInput.labelDataPerDeliveryMethod[key]
        self.labelInput.setRoutesToPrint(routesToPrint)


class SingleLabel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Makes the entry widget the biggest and make the second and third column equal length
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # set variables which get set and will be passed into the function
        ordersFile = tk.StringVar()
        self.labelInput = LabelHelper(AppEnum.GotaLabel)

        # set up variable
        self.selectedDeliveryMethod = tk.StringVar("")
        self.selectedCustomerName = tk.StringVar("")
        self.selectedProductName = tk.StringVar("")

        # Set title and subtitle
        controller.createTitle(self, "SingleLabel", 0, 0, 4)
        controller.createSubTitle(self, f"Input", 1, 0)

        # create User input where you ask the orders file
        controller.createAskUserInput(
            self, "Dag Orders:", 2, 0, ordersFile, sl.GotaLabelInput, True, "xlsx"
        )

        # Create button and assign import orders command to it
        btnImport = controller.createRunButton(
            self, "Importeer Dag Orders", 3, 1, controller.importLogo
        )
        btnImport.configure(command=lambda: importOrders())

        controller.createSubTitle(self, f"Selectie", 4, 0)

        # Make some space and add the three dropdowns to select the appropriate meal
        # You cannot set the command of the dropdown after creation so, we have to use all the self nonsens
        self.ddDelivery = controller.createDropDown(
            self,
            "Selecteer de route:",
            5,
            1,
            self.selectedDeliveryMethod,
            self.deliveryRouteChanged,
        )
        self.ddCustomer = controller.createDropDown(
            self,
            "Selecteer de klant:",
            6,
            1,
            self.selectedCustomerName,
            self.customerNameChanged,
        )
        self.ddProduct = controller.createDropDown(
            self,
            "Selecteer de maaltijd:",
            7,
            1,
            self.selectedProductName,
            self.productNameChanged,
        )

        # Make some space and set output subtitle
        controller.createSubTitle(self, f"Label Velden", 8, 0)

        # all variables used for the label making
        self.lCustomerName = tk.StringVar()
        self.lCustomerId = tk.StringVar()
        self.lAddress = tk.StringVar()
        self.lZipCode = tk.StringVar()
        self.lCity = tk.StringVar()
        self.lPhoneNumber = tk.StringVar()
        self.lDeliveryDate = tk.StringVar()
        self.lProductName = tk.StringVar()
        self.lCustomerRemarks1 = tk.StringVar()

        # all widgets used for the label making
        startRow = 9
        controller.createLabelEntryRow(
            self, "Klant Naam:", startRow, 0, self.lCustomerName
        )
        controller.createLabelEntryRow(
            self, "Klant ID:", startRow + 1, 0, self.lCustomerId
        )
        controller.createLabelEntryRow(self, "Address:", startRow + 2, 0, self.lAddress)
        controller.createLabelEntryRow(
            self, "Postcode:", startRow + 3, 0, self.lZipCode
        )
        controller.createLabelEntryRow(self, "Plaats:", startRow + 4, 0, self.lCity)
        controller.createLabelEntryRow(
            self, "Telefoon:", startRow + 5, 0, self.lPhoneNumber
        )
        controller.createLabelEntryRow(
            self, "Aflever Datum:", startRow + 6, 0, self.lDeliveryDate
        )
        controller.createLabelEntryRow(
            self, "Maaltijd:", startRow + 7, 0, self.lProductName
        )
        controller.createLabelEntryRow(
            self, "Opmerking:", startRow + 8, 0, self.lCustomerRemarks1
        )

        controller.spacer(self, startRow + 9)
        # Create button and assign import orders command to it
        btnPrint = controller.createRunButton(
            self, "Print Label", startRow + 10, 1, controller.printLogo
        )
        btnPrint.configure(command=lambda: printLabel())

        def importOrders():
            """Fetches the orders and set the appropriate fields with the given import data"""
            try:
                self.labelInput = fetchOrders(Path(ordersFile.get()))
                self.resetDropDowns()
                messagebox.showinfo(
                    "Success",
                    controller.orderSuccessMessage,
                )

            except Exception as err:
                messagebox.showerror(
                    "Error",
                    controller.orderFailureMessage + format_tb(err.__traceback__)[0],
                )

        def printLabel():
            """Print the label"""
            try:
                # Set the single label and send it to the printer
                self.labelInput.setLabels(
                    [
                        GTlabel(
                            self.lCustomerName.get(),
                            self.lCustomerId.get(),
                            self.lAddress.get(),
                            self.lZipCode.get(),
                            self.lCity.get(),
                            self.lPhoneNumber.get(),
                            self.lDeliveryDate.get(),
                            self.lProductName.get(),
                            self.lCustomerRemarks1.get(),
                        )
                    ]
                )
                createLabels(self.labelInput, sl.GotaLabelOutput)

                messagebox.showinfo(
                    "Success",
                    controller.printSuccessMessage,
                )

            except Exception as err:
                messagebox.showerror(
                    "Error",
                    controller.printFailureMessage + format_tb(err.__traceback__)[0],
                )

    def resetDropDowns(self, *args):
        self.ddDelivery.set_menu(None, *self.labelInput.getDictionaryKeys())
        self.ddCustomer.set_menu(None)
        self.ddProduct.set_menu(None)
        self.selectedDeliveryMethod.set("")
        self.selectedCustomerName.set("")
        self.selectedProductName.set("")

    def deliveryRouteChanged(self, *args):
        """Fills the dropdown of the customer selector while also clearing the product selector
        and resetting the selected customer and selected product
        """
        self.ddCustomer.set_menu(
            None,
            *self.labelInput.getCustomerNamesFromKey(self.selectedDeliveryMethod.get()),
        )
        self.ddProduct.set_menu(None)
        self.selectedCustomerName.set("")
        self.selectedProductName.set("")

    def customerNameChanged(self, *args):
        """Fills the dropdown of the product selector and resets the selected product"""
        self.ddProduct.set_menu(
            None,
            *self.labelInput.getProductsForCustomer(
                self.selectedDeliveryMethod.get(), self.selectedCustomerName.get()
            ),
        )
        self.selectedProductName.set("")

    def productNameChanged(self, *args):
        product = self.labelInput.getProduct(
            self.selectedDeliveryMethod.get(),
            self.selectedCustomerName.get(),
            self.selectedProductName.get(),
        )

        self.lCustomerName.set(product["customerName"].values[0])
        self.lCustomerId.set(product["customerId"].values[0])
        self.lAddress.set(product["address"].values[0])
        self.lZipCode.set(product["zipCode"].values[0])
        self.lCity.set(product["city"].values[0])
        self.lPhoneNumber.set(product["phoneNumber"].values[0])
        self.lDeliveryDate.set(product["deliveryDate"].values[0])
        self.lProductName.set(product["productName"].values[0])
        self.lCustomerRemarks1.set(product["customerRemarks1"].values[0])


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
        btnRunRoute = controller.createRunButton(
            self, "Start PakLijst PER ROUTE", 8, 1, controller.runLogo
        )
        btnRunRoute.configure(command=lambda: runPakLijstApp(isPerRoute=True))
        btnRunTotal = controller.createRunButton(
            self, "Start PakLijst TOTAAL", 8, 2, controller.runLogo
        )
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
                        controller.generalSuccessMessage,
                    )
            except Exception as err:
                messagebox.showerror(
                    "Error",
                    controller.generalFailureMessage + format_tb(err.__traceback__)[0],
                )


if __name__ == "__main__":
    setDirectories()
    app = App()
    app.mainloop()
