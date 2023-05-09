from tkinter import Frame, StringVar, Button
from backEnd.constants import saveLocations as sl
from pandastable import Table, TableModel
from pandas import DataFrame
import random


class GTVultIn(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        # Makes the entry widget the biggest and make the second and third column equal length
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # Create frames for the show orders and new orders screens
        self.frames = {}
        self.frames["ShowOrders"] = ShowOrders(parent=self, controller=controller)
        self.frames["ShowOrders"].grid(row=2, column=0, columnspan=4, sticky="nsew")

        self.frames["NewOrders"] = NewOrders(parent=self, controller=controller)
        self.frames["NewOrders"].grid(row=2, column=0, columnspan=4, sticky="nsew")

        # General sub-app title
        controller.createTitle(self, "GTVultIn", 0, 0, 4)

        # Buttons to go to show orders and new orders
        btnNewOrders = controller.createRunButton(
            self, "Plaats nieuwe orders", 1, 1, controller.newLogo
        )
        btnNewOrders.configure(command=lambda: self.frames["NewOrders"].tkraise())

        btnShowOrders = controller.createRunButton(
            self, "Laat orders zien", 1, 2, controller.showLogo
        )
        btnShowOrders.configure(command=lambda: self.frames["ShowOrders"].tkraise())


class NewOrders(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Makes the entry widget the biggest and make the second and third column equal length
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # all variables used for the label making
        self.lCustomerName = StringVar()
        self.lCustomerId = StringVar()
        self.lCustomerRemarks1 = StringVar()

        self.selectedMeal = StringVar("")
        self.selectedDate = StringVar("")
        self.selectedQuantity = StringVar("")

        mealOverviewFile = StringVar()

        controller.createSubTitle(self, "Input", 0, 0)
        # create User input where you ask the meal overview of the week file
        controller.createAskUserInput(
            self,
            "Week menu:",
            1,
            0,
            mealOverviewFile,
            sl.MealOverviewInput,
            True,
            "xlsx",
        )

        # Create button and assign import orders command to it
        btnImport = controller.createRunButton(
            self, "Importeer Maaltijd Overzicht", 2, 1, controller.importLogo
        )
        btnImport.configure(command=lambda: importOrders())

        controller.spacer(self, 3)

        # Customer selection
        customerSubtitle = controller.createSubTitle(self, "Klant (1 uit 14)", 4, 0)

        # Previous button
        btnPreviousCustomer = controller.createHelperButton(self, "  <- Vorige", 4, 1)
        btnPreviousCustomer.grid(sticky="e")
        btnPreviousCustomer.configure(command=lambda: self.previousCustomer())

        # Next button
        btnNextCustomer = controller.createHelperButton(self, "volgende ->", 4, 2)
        btnNextCustomer.grid(sticky="w")
        btnNextCustomer.configure(command=lambda: self.nextCustomer())

        # Customer information fields
        controller.createLabelEntryRow(self, "Klant ID:", 5, 0, 2, self.lCustomerId)
        controller.createLabelEntryRow(self, "Klant Naam:", 6, 0, 2, self.lCustomerName)
        controller.createLabelEntryRow(
            self, "Opmerking:", 7, 0, 2, self.lCustomerRemarks1
        )

        controller.spacer(self, 8)
        controller.createSubTitle(self, "Maaltijd", 9, 0)
        self.ddMeal = controller.createDropDown(
            self,
            "Selecteer de maaltijd:",
            10,
            1,
            self.selectedMeal,
            None,
        )
        self.ddMeal.set_menu(None, *["maaltijd1", "maaltijd2"])

        self.ddDate = controller.createDropDown(
            self,
            "Selecteer de dag:",
            11,
            1,
            self.selectedDate,
            None,
        )
        self.ddDate.set_menu(None, *["MA 13 FEB", "DI 14 FEB"])

        self.ddQuantity = controller.createDropDown(
            self,
            "Selecteer de hoeveelheid:",
            12,
            1,
            self.selectedQuantity,
            None,
        )
        self.ddQuantity.set_menu(None, *["1", "2", "3"])

        # Order toevoegen
        btnAddOrder = controller.createRunButton(
            self, "Order Toevoegen", 13, 1, controller.newLogo
        )
        btnAddOrder.configure(command=lambda: self.addOrder())

        def importOrders():
            """Fetches the orders and set the appropriate fields with the given import data"""
            try:
                print("import")

            # Error handling
            except PermissionError as permissionError:
                controller.permissionErrorMessage(permissionError)
            except FileNotFoundError as fileNotFoundError:
                controller.fileNotFoundErrorMessage(fileNotFoundError)
            except Exception as error:
                controller.generalErrorMessage(error, controller.generalFailureText)

    def previousCustomer(self):
        print("previous")

    def nextCustomer(self):
        print("next")

    def addOrder(self):
        print("Order added")


class ShowOrders(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Makes the entry widget the biggest and make the second and third column equal length
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        names = []
        ages = []
        genders = []
        salaries = []

        # generate random data and append to lists
        for i in range(30):
            names.append("Person " + str(i + 1))
            ages.append(random.randint(20, 60))
            genders.append(random.choice(["M", "F"]))
            salaries.append(random.randint(30000, 100000))

        # create the dataframe using the lists
        data = {"name": names, "age": ages, "gender": genders, "salary": salaries}
        df = DataFrame(data)

        # create the dataframe using the dictionary
        df = DataFrame(data)

        controller
        tbOrders = Table(
            self,
            dataframe=df,
            showtoolbar=False,
            showstatusbar=False,
        )
        tbOrders.grid(row=0, column=0, columnspan=4, sticky="nsew")
        tbOrders.show()

        controller.spacer(self, 2)

        # Order toevoegen
        btnAddOrder = controller.createRunButton(
            self, "Maak csv van de orders", 3, 1, controller.runLogo
        )
        btnAddOrder.configure(command=lambda: self.addOrder())

    def createCSV(self):
        print("CSV created")
