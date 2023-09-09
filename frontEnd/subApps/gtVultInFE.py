from tkinter import Frame
from backEnd.GTVultIn import GTVultIn
from pandas import DataFrame
from frontEnd.subApps.gtVultInSubAppsFE.gtVultInWeekMenuFE import WeekMenu
from frontEnd.subApps.gtVultInSubAppsFE.gtVultInNewOrdersFE import NewOrders
from frontEnd.subApps.gtVultInSubAppsFE.gtVultInShowOrdersFE import ShowOrders


class GTVultInFE(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller
        # Makes the entry widget the biggest and make the second and third column equal length
        self.grid_columnconfigure(0, weight=1, uniform="fred")
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # Information about GTVultIn is passed around applications so the variable is set in the master frame
        self.gtVultInInput = GTVultIn()

        # General sub-app title
        controller.createTitle(self, "GTVultIn", 0, 0, 3)

        # Buttons to go to show orders frame
        btnNewOrders = controller.createRunButton(
            self, "Plaats nieuwe orders", 1, 0, controller.newLogo
        )
        btnNewOrders.configure(command=lambda: self.frames["NewOrders"].tkraise())

        # Buttons to go to weekMenu frame
        btnNewOrders = controller.createRunButton(
            self, "Maak een week menu", 1, 1, controller.createWeekMenuLogo
        )
        btnNewOrders.configure(command=lambda: self.frames["WeekMenu"].tkraise())

        # Buttons to go to show orders frame
        btnShowOrders = controller.createRunButton(
            self, "Laat orders zien", 1, 2, controller.showLogo
        )
        btnShowOrders.configure(command=lambda: self.frames["ShowOrders"].tkraise())

        # Create frames for the three sub menus
        self.frames = {}
        self.frames["ShowOrders"] = ShowOrders(parent=self, controller=controller)
        self.frames["ShowOrders"].grid(row=2, column=0, columnspan=3, sticky="nsew")

        self.frames["WeekMenu"] = WeekMenu(parent=self, controller=controller)
        self.frames["WeekMenu"].grid(row=2, column=0, columnspan=3, sticky="nsew")

        self.frames["NewOrders"] = NewOrders(parent=self, controller=controller)
        self.frames["NewOrders"].grid(row=2, column=0, columnspan=3, sticky="nsew")

    def setKalCustomers(self, KALCustomers: DataFrame):
        """Fills the KALCustomers and fills the customer selection labels with first entry
        Is called when KAL is finished running

        Args:
            KALCustomers (DataFrame): Customer retrieved from KAL for which can be easily ordered
        """
        if KALCustomers.size != 0:
            self.gtVultInInput.setKALcustomers(KALCustomers)
            self.frames["NewOrders"].customerIndex.set(0)
            self.frames["NewOrders"].setCustomerFields(0)
