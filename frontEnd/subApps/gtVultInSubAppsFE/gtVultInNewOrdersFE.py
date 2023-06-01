from tkinter import Frame, StringVar, IntVar
from backEnd.constants import saveLocations as sl
from pathlib import Path
from tkinter import messagebox
from pandas import DataFrame


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
        self.lCustomerRemarks = StringVar()

        # keeps track on which KAL customer you are
        self.customerIndex = IntVar()

        # Variables which keep track of the order selection variables
        selectedMeal = StringVar()
        selectedDate = StringVar()
        selectedQuantity = StringVar()

        # File containing the meal overview excel
        mealOverviewFile = StringVar()

        controller.createSubTitle(self, "Input", 0, 0)
        # create User input where you ask the meal overview of the week file
        controller.createAskUserInput(
            self,
            "Maaltijd Overzicht:",
            1,
            0,
            mealOverviewFile,
            sl.MealOverviewInput,
            True,
            "xlsx",
        )

        # Create button and assign import meal overview command to it
        btnImport = controller.createRunButton(
            self, "Importeer Maaltijd Overzicht", 2, 1, controller.importLogo
        )
        btnImport.configure(command=lambda: importOrders())

        controller.spacer(self, 3)

        # Customer selection
        controller.createSubTitle(self, "Klant", 4, 0)

        # Customer selection tooltip text
        self.customerCountLabel = controller.createSubTitle(
            self, "Draai eerst KAL om hier klanten te selecteren", 4, 1
        )
        self.customerCountLabel.grid(padx=(0, 0))

        # Customer information fields, these values are used for creating the order table
        controller.createLabelEntryRow(self, "Klant ID:", 5, 0, 2, self.lCustomerId)
        controller.createLabelEntryRow(self, "Klant Naam:", 6, 0, 2, self.lCustomerName)
        controller.createLabelEntryRow(
            self, "Opmerking:", 7, 0, 2, self.lCustomerRemarks
        )

        # Reset the customer selection input
        btnResetCustomer = controller.createHelperButton(self, "Reset", 7, 3)
        btnResetCustomer.configure(command=lambda: resetCustomer())

        # Previous button
        btnPreviousCustomer = controller.createHelperButton(self, "  <- Vorige", 8, 1)
        btnPreviousCustomer.grid(sticky="e")
        btnPreviousCustomer.configure(command=lambda: previousCustomer())

        # Next button
        btnNextCustomer = controller.createHelperButton(self, "Volgende ->", 8, 2)
        btnNextCustomer.grid(sticky="w")
        btnNextCustomer.configure(command=lambda: nextCustomer())

        # Meal selection
        controller.createSubTitle(self, "Maaltijd", 9, 0)

        # Meal selection tool tip and also used to keep track of customers once imported
        self.mealSelectionToolTip = controller.createSubTitle(
            self,
            "Importeer eerst een maaltijd overzicht om hier maaltijden te selecteren",
            9,
            1,
        )
        self.mealSelectionToolTip.grid(padx=(0, 0), columnspan=2)

        # Drop down menu's for meal selection
        ddDate = controller.createDropDown(
            self,
            "Selecteer de dag:",
            10,
            1,
            selectedDate,
            None,
        )
        ddMeal = controller.createDropDown(
            self,
            "Selecteer de maaltijd:",
            11,
            1,
            selectedMeal,
            None,
        )
        ddQuantity = controller.createDropDown(
            self,
            "Selecteer het aantal:",
            12,
            1,
            selectedQuantity,
            None,
        )

        # Reset the meal selection input
        btnResetMealSelection = controller.createHelperButton(self, "Reset", 12, 2)
        btnResetMealSelection.grid(sticky="w", pady=0)
        btnResetMealSelection.configure(command=lambda: resetMealSelection(), pady=0)

        # Add Order button
        btnAddOrder = controller.createRunButton(
            self, "Order Toevoegen", 13, 1, controller.addLogo
        )
        btnAddOrder.configure(command=lambda: addOrder())

        # Add Week menu button
        btnAddOrder = controller.createRunButton(
            self, "Week Menu Toevoegen", 13, 2, controller.addWeekMenuLogo
        )
        btnAddOrder.configure(command=lambda: addWeekMenu())

        def importOrders():
            """Fetches the orders and set the appropriate fields with the given import data
            als clears the import meal overview tooltip on successful import"""
            try:
                self.master.gtVultInInput.loadMealOverView(Path(mealOverviewFile.get()))
                # Fill the meal selection dropdowns in own frame as well in the WeekMenu frame
                fillDropDownMenus()
                self.master.frames["WeekMenu"].fillDropDownMenus()

                messagebox.showinfo(
                    "Success",
                    controller.mealOverviewSuccessText,
                )
                # Clear the tooltip of own frame as well as in the weekMenu frame
                self.mealSelectionToolTip.configure(text="")
                self.master.frames["WeekMenu"].mealSelectionToolTip.configure(text="")

            # Error handling
            except PermissionError as permissionError:
                controller.permissionErrorMessage(permissionError)
            except FileNotFoundError as fileNotFoundError:
                controller.fileNotFoundErrorMessage(fileNotFoundError)
            except Exception as error:
                controller.generalErrorMessage(error, controller.generalFailureText)

        def fillDropDownMenus():
            """Fills the dropdown menu with choices from the meal overview
            Also resets the selected choices
            """
            ddMeal.set_menu(None, *self.master.gtVultInInput.mealsAndCodesDict.keys())
            ddDate.set_menu(None, *self.master.gtVultInInput.orderDaysDict.keys())
            ddQuantity.set_menu(None, *list(range(9, 0, -1)))

            resetMealSelection()

        def resetCustomer():
            """Clear all customer selection input"""
            self.lCustomerName.set("")
            self.lCustomerId.set("")
            self.lCustomerRemarks.set("")

        def previousCustomer():
            """Changes customer information when pressed on previous button,
            First checks if KAL was ran
            """
            if checkKALCustomers():
                currentIndex = self.customerIndex.get()
                # Border condition, if at 0 show empty fields to make an order for customer not in KAL list
                if currentIndex == 0 or currentIndex == -1:
                    self.customerCountLabel.configure(
                        text=f"GT-Klant (0 uit {self.master.gtVultInInput.KALcustomers.shape[0]})"
                    )
                    self.lCustomerName.set("")
                    self.lCustomerId.set("")
                    self.lCustomerRemarks.set("")
                    self.customerIndex.set(-1)

                else:
                    newIndex = currentIndex - 1
                    self.setCustomerFields(newIndex)
                    self.customerIndex.set(newIndex)

        def nextCustomer():
            """Changes customer information when pressed on next button,
            First checks if KAL was ran
            """
            if checkKALCustomers():
                currentIndex = self.customerIndex.get()
                # Border condition of last customer, just fill it again with last customer information
                if (currentIndex + 1) == self.master.gtVultInInput.KALcustomers.shape[
                    0
                ]:
                    self.setCustomerFields(currentIndex)
                # Border condition when coming from zeroth index,
                elif currentIndex == -1:
                    self.setCustomerFields(0)
                    self.customerIndex.set(0)
                else:
                    newIndex = currentIndex + 1
                    self.setCustomerFields(newIndex)
                    self.customerIndex.set(newIndex)

        def checkKALCustomers() -> bool:
            """First checks if Kal was ran then if it had any GT Customers
            throws appropriate arrows if not the case

            Returns:
                bool: Returns True if customers can be selected, False otherwise
            """
            if hasattr(self.master.gtVultInInput, "KALcustomers"):
                if self.master.gtVultInInput.KALcustomers.size != 0:
                    return True
                else:
                    messagebox.showwarning(
                        "Error",
                        "De KAL uitdraai bevatten geen GT-klanten dus deze kan je ook niet selecteren.",
                    )
            else:
                messagebox.showwarning(
                    "Error",
                    "Draai eerst de KAL applicatie voordat je GT-klanten kunt selecteren.",
                )
            return False

        def resetMealSelection():
            """Resets the meal selection fields"""
            selectedMeal.set("")
            selectedDate.set("")
            selectedQuantity.set("1")

        def addOrder():
            """Adds an order to the meal overview table in the other frame
            First checks if all appropriate field were filled
            """
            if checkInputFields():
                # Add a new order to the Display Orders DataFrame in the GTVultIn class
                self.master.gtVultInInput.addOrder(
                    self.lCustomerName.get(),
                    self.lCustomerId.get(),
                    selectedMeal.get(),
                    selectedDate.get(),
                    selectedQuantity.get(),
                )
                # Empty the selection
                resetMealSelection()

                # Redraw the table in the other frame and auto adjust its columns
                self.master.frames["ShowOrders"].redrawTable()

        def addWeekMenu():
            """Adds the orders in the weekmenu to the meal overview table in the show orders frame
            First checks if meals are present in the weekmenu
            """
            if self.master.frames["WeekMenu"].checkIfDataFrameIsEmpty():
                weekMenuDf = DataFrame(
                    self.master.frames["WeekMenu"].tbWeekMenu.model.df
                )
                for index, row in weekMenuDf.iterrows():
                    self.master.gtVultInInput.addOrder(
                        self.lCustomerName.get(),
                        self.lCustomerId.get(),
                        row["Maaltijd"],
                        row["Wanneer"],
                        row["Aantal"],
                    )

                self.master.frames["ShowOrders"].redrawTable()

        def checkInputFields() -> bool:
            """Checks if all correct fields are not empty before adding a new order

            Returns:
                bool: Returns True if all correct fields were filled
            """
            if self.lCustomerId.get() == "":
                messagebox.showwarning(
                    "Error",
                    "De klant ID kan niet leeg zijn",
                )
                return False
            if selectedMeal.get() == "":
                messagebox.showwarning(
                    "Error",
                    "Selecteer eerst een maaltijd",
                )
                return False
            if selectedDate.get() == "":
                messagebox.showwarning(
                    "Error",
                    "Selecteer eerst een bestel dag",
                )
                return False
            if selectedQuantity.get() == "":
                messagebox.showwarning(
                    "Error",
                    "Selecteer eerst het aantal maaltijd(en)",
                )
                return False
            return True

    def setCustomerFields(self, index: int):
        """Fill the customer selection fields based on the given index in the KAL-GTCustomers dataframe

        Args:
            index (int): Index of the row for which you want to display the customer information
        """
        # Tooltip text showing which customer you have currently selected
        self.customerCountLabel.configure(
            text=f"GT-Klant ({index + 1} uit {self.master.gtVultInInput.KALcustomers.shape[0]})"
        )
        self.lCustomerId.set(
            self.master.gtVultInInput.KALcustomers["Klant Nr."].iloc[index]
        )
        self.lCustomerName.set(
            self.master.gtVultInInput.KALcustomers["Naam"].iloc[index]
        )
        self.lCustomerRemarks.set(
            self.master.gtVultInInput.KALcustomers["Opmerking"].iloc[index]
        )
