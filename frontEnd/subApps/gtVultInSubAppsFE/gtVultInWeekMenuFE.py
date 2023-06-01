from tkinter import Frame, StringVar
from pandastable import Table, TableModel
from tkinter import messagebox


class WeekMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Makes the entry widget the biggest and make the second and third column equal length
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")
        # Variables which keep track of the order selection variables

        self.selectedMeal = StringVar()
        self.selectedDate = StringVar()
        self.selectedQuantity = StringVar()

        # Meal selection
        controller.createSubTitle(self, "Maaltijd   ", 0, 0)

        # Meal selection tool tip and also used to keep track of customers once imported
        self.mealSelectionToolTip = controller.createSubTitle(
            self,
            "Importeer eerst een maaltijd overzicht om hier maaltijden te selecteren",
            0,
            1,
        )
        self.mealSelectionToolTip.grid(padx=(0, 0), columnspan=2)

        # Drop down menu's for meal selection
        self.ddDate = controller.createDropDown(
            self,
            "Selecteer de dag:",
            1,
            1,
            self.selectedDate,
            None,
        )
        self.ddMeal = controller.createDropDown(
            self,
            "Selecteer de maaltijd:",
            2,
            1,
            self.selectedMeal,
            None,
        )

        self.ddQuantity = controller.createDropDown(
            self,
            "Selecteer het aantal:",
            3,
            1,
            self.selectedQuantity,
            None,
        )

        # Reset the week meal selection input
        btnResetMealSelection = controller.createHelperButton(self, "Reset", 3, 2)
        btnResetMealSelection.grid(sticky="w", pady=0)
        btnResetMealSelection.configure(
            command=lambda: self.resetMealSelection(), pady=0
        )

        # Add Order to Week Menu button
        btnAddOrder = controller.createRunButton(
            self, "Order Toevoegen Aan Week Menu", 4, 1, controller.addLogo
        )
        btnAddOrder.configure(command=lambda: addOrderToWeekMenu())

        # Show the Week menu
        controller.createSubTitle(self, "Week Menu", 5, 0)

        # Put the table in a seperate frame since that makes it easier to manage
        tableFrame = Frame(self)
        tableFrame.grid(row=6, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)
        # Load the (empty) dataframe into the table that will be shown
        self.tbWeekMenu = Table(
            tableFrame,
            showtoolbar=False,
            showstatusbar=False,
            maxcellwidth=1500,
        )
        self.redrawTable()
        # Some cosmetics of the table
        self.tbWeekMenu.font = "Helvetica"
        self.tbWeekMenu.rowselectedcolor = "#f2b588"
        self.tbWeekMenu.show()

        # Delete button for selected order
        btnDeleteRow = controller.createHelperButton(self, "Verwijder", 6, 3)
        btnDeleteRow.grid(sticky="ews")
        btnDeleteRow.configure(command=lambda: deleteRow())

        # Delete all orders
        btnDeleteAll = controller.createHelperButton(self, "Verwijder allen", 7, 3)
        btnDeleteAll.configure(command=lambda: deleteAll())

        def deleteRow():
            """Deletes the selected row from the table and update the DisplayOrders property"""
            self.tbWeekMenu.deleteRow()
            self.master.gtVultInInput.setWeekMenu(self.tbWeekMenu.model.df)
            self.redrawTable()

        def deleteAll():
            """Set an empty table as the displayOrders and use that empty Dataframe to redraw the table
            First ask the user if he is really sure"""
            deleteAll = messagebox.askyesno(
                "Alles verwijderen",
                "Weet u zeker dat u het gehele week menu wilt verwijderen?",
            )
            if deleteAll:
                self.master.gtVultInInput.setWeekMenu(
                    self.master.gtVultInInput.initializeWeekMenu()
                )
                self.redrawTable()

        def addOrderToWeekMenu():
            """Adds an order to the week menu table in the other frame
            First checks if all appropriate field were filled
            """
            if checkInputFields():
                # Add a new order to the Week Menu DataFrame in the GTVultIn class
                self.master.gtVultInInput.addOrderToWeekMenu(
                    self.selectedMeal.get(),
                    self.selectedDate.get(),
                    self.selectedQuantity.get(),
                )
                # Empty the selection
                self.resetMealSelection()

                # Redraw the table in the other frame and auto adjust its columns
                self.redrawTable()

        def checkInputFields() -> bool:
            """Checks if all correct fields are not empty before adding a new order to the week menu

            Returns:
                bool: Returns True if all correct fields were filled
            """
            if self.selectedMeal.get() == "":
                messagebox.showwarning(
                    "Error",
                    "Selecteer eerst een maaltijd",
                )
                return False
            if self.selectedDate.get() == "":
                messagebox.showwarning(
                    "Error",
                    "Selecteer eerst een bestel dag",
                )
                return False
            if self.selectedQuantity.get() == "":
                messagebox.showwarning(
                    "Error",
                    "Selecteer eerst het aantal maaltijd(en)",
                )
                return False
            return True

    def resetMealSelection(self):
        """Resets the week meal selection fields"""
        self.selectedMeal.set("")
        self.selectedDate.set("")
        self.selectedQuantity.set("1")

    def fillDropDownMenus(self):
        """Fills the dropdown menu with choices from the meal overview
        Also resets the selected choices
        """
        self.ddMeal.set_menu(None, *self.master.gtVultInInput.mealsAndCodesDict.keys())
        self.ddDate.set_menu(None, *self.master.gtVultInInput.orderDaysDict.keys())
        self.ddQuantity.set_menu(None, *list(range(9, 0, -1)))

        self.resetMealSelection()

    def redrawTable(self):
        """Set a copy of the weekMenudf from the gtVultIn class as the weekmenu table"""
        copyDf = self.master.gtVultInInput.weekMenu.copy()
        self.tbWeekMenu.updateModel(TableModel(copyDf))
        # Reset the index otherwise funky stuff happens
        self.tbWeekMenu.resetIndex(ask=False, drop=True)

    def checkIfDataFrameIsEmpty(self) -> bool:
        """Throw error if the week menu is empty

        Returns:
            bool: Returns False if there is nothing in the week menu
        """
        if self.tbWeekMenu.model.df.size == 0:
            messagebox.showwarning(
                "Error",
                "Zorg ervoor dat er minstens één gerecht in het week menu zit",
            )
            return False

        if self.master.frames["NewOrders"].lCustomerId.get() == "":
            messagebox.showwarning(
                "Error",
                "De klant ID kan niet leeg zijn",
            )
            return False
        return True
