from tkinter import Frame, StringVar
from backEnd.constants import saveLocations as sl
from pandastable import Table, TableModel
from pathlib import Path
from tkinter import messagebox


class ShowOrders(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Makes the entry widget the biggest and make the second and third column equal length
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")
        self.grid_rowconfigure(1, weight=0, uniform="fred")

        # Place were you will be saving the output
        outputDir = StringVar(value=sl.GTVultInOutput)

        controller.createSubTitle(self, "Orders", 0, 0)

        # Put the table in a seperate frame since that makes it easier to manage
        tableFrame = Frame(self)
        tableFrame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        # Load the (empty) dataframe into the table that will be shown
        self.tbOrders = Table(
            tableFrame,
            showtoolbar=False,
            showstatusbar=False,
            maxcellwidth=1500,
        )
        self.redrawTable()
        # Some cosmetics of the table
        self.tbOrders.font = "Helvetica"
        self.tbOrders.rowselectedcolor = "#f2b588"
        self.tbOrders.show()

        # Delete button for selected order
        btnDeleteRow = controller.createHelperButton(self, "Verwijder", 1, 3)
        btnDeleteRow.grid(sticky="ews")
        btnDeleteRow.configure(command=lambda: deleteRow())

        # Delete all orders
        btnDeleteAll = controller.createHelperButton(self, "Verwijder allen", 2, 3)
        btnDeleteAll.configure(command=lambda: deleteAll())

        # Output
        controller.createSubTitle(self, f"Output", 2, 0)

        # Ask for the location to save the csv
        controller.createAskUserInput(
            self, "Opslag:", 3, 0, outputDir, sl.GTVultInOutput, False, None
        )
        controller.spacer(self, 4)

        # Button to make the orders into a csv
        btnAddOrder = controller.createRunButton(
            self, "Maak csv van de orders", 5, 1, controller.runLogo
        )
        btnAddOrder.configure(command=lambda: createCSV())

        def deleteRow():
            """Deletes the selected row from the table and update the DisplayOrders property"""
            self.tbOrders.deleteRow()
            self.master.gtVultInInput.setDisplayOrders(self.tbOrders.model.df)
            self.redrawTable()

        def deleteAll():
            """Set an empty table as the displayOrders and use that empty Dataframe to redraw the table
            First ask the user if he is really sure"""
            deleteAll = messagebox.askyesno(
                "Alles verwijderen",
                "Weet u zeker dat u alle orders wilt verwijderen?",
            )
            if deleteAll:
                self.master.gtVultInInput.setDisplayOrders(
                    self.master.gtVultInInput.initializeShowOrders()
                )
                self.redrawTable()

        def createCSV():
            """Make a csv of the orders in the Table frame, throw error if something goes wrong"""
            try:
                if checkIfDataFrameIsEmpty():
                    self.master.gtVultInInput.createCSv(
                        self.tbOrders.model.df, Path(outputDir.get())
                    )
                    messagebox.showinfo(
                        "Success",
                        controller.generalSuccessText,
                    )
            # standard error handling
            except PermissionError as permissionError:
                controller.permissionErrorMessage(permissionError)
            except FileNotFoundError as fileNotFoundError:
                controller.fileNotFoundErrorMessage(fileNotFoundError)
            except Exception as error:
                controller.generalErrorMessage(error, controller.generalFailureText)

        def checkIfDataFrameIsEmpty() -> bool:
            """Throw error if there are no orders

            Returns:
                bool: Returns False if there are no orders
            """
            if self.tbOrders.model.df.size == 0:
                messagebox.showwarning(
                    "Error",
                    "Zorg ervoor dat er minstens één order is",
                )
                return False
            return True

    def redrawTable(self):
        """Set a copy of the displayOrders as the display table"""
        copyDf = self.master.gtVultInInput.displayOrders.copy()
        self.tbOrders.updateModel(TableModel(copyDf))
        # Reset the index otherwise funky stuff happens
        self.tbOrders.resetIndex(ask=False, drop=True)
