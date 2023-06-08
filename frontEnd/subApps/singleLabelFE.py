from tkinter import (
    Frame,
    StringVar,
)
from backEnd.constants import saveLocations as sl
from backEnd.gotaLabel import fetchOrders
from tkinter import messagebox
from pathlib import Path
from backEnd.dataClasses.labelHelper import LabelHelper
from backEnd.dataClasses.appEnum import AppEnum
from backEnd.dataClasses.labelInterface import GTlabel
from backEnd.labelCreator import createLabels
from datetime import date


class SingleLabelFE(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        # Makes the entry widget the biggest and make the second and third column equal length
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # set variables which get set and will be passed into the function
        ordersFile = StringVar()
        self.labelInput = LabelHelper(
            AppEnum.SingleLabel, date.today().strftime("%d-%m-%Y")
        )

        # set up variable
        self.selectedDeliveryMethod = StringVar("")
        self.selectedCustomerName = StringVar("")
        self.selectedProductName = StringVar("")

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

        controller.createSubTitle(self, f"Label", 4, 0)

        # Tooltip about importing orders
        self.customerSelectionToolTip = controller.createSubTitle(
            self, "Importeer eerst de orders voordat je labels kan selecteren", 4, 1
        )
        self.customerSelectionToolTip.grid(padx=(0, 0), columnspan=2)

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
        self.lCustomerName = StringVar()
        self.lCustomerId = StringVar()
        self.lAddress = StringVar()
        self.lZipCode = StringVar()
        self.lCity = StringVar()
        self.lPhoneNumber = StringVar()
        self.lDeliveryDate = StringVar()
        self.lProductName = StringVar()
        self.lCustomerRemarks1 = StringVar()

        # all widgets used for the label making
        startRow = 9
        controller.createLabelEntryRow(
            self, "Klant Naam:", startRow, 0, 2, self.lCustomerName
        )
        controller.createLabelEntryRow(
            self, "Klant ID:", startRow + 1, 0, 2, self.lCustomerId
        )
        controller.createLabelEntryRow(
            self, "Address:", startRow + 2, 0, 2, self.lAddress
        )
        controller.createLabelEntryRow(
            self, "Postcode:", startRow + 3, 0, 2, self.lZipCode
        )
        controller.createLabelEntryRow(self, "Plaats:", startRow + 4, 0, 2, self.lCity)
        controller.createLabelEntryRow(
            self, "Telefoon:", startRow + 5, 0, 2, self.lPhoneNumber
        )
        controller.createLabelEntryRow(
            self, "Aflever Datum:", startRow + 6, 0, 2, self.lDeliveryDate
        )
        controller.createLabelEntryRow(
            self, "Maaltijd:", startRow + 7, 0, 2, self.lProductName
        )
        controller.createLabelEntryRow(
            self, "Opmerking:", startRow + 8, 0, 2, self.lCustomerRemarks1
        )

        btnReset = controller.createHelperButton(self, "Reset", startRow + 8, 3)
        btnReset.configure(command=lambda: self.resetFields())
        btnReset.grid(sticky="nsew")

        controller.spacer(self, startRow + 9)

        # Create button and assign import orders command to it
        btnPrint = controller.createRunButton(
            self, "Print Label", startRow + 10, 1, controller.printLogo
        )
        btnPrint.configure(command=lambda: printLabel())

        def importOrders():
            """Fetches the orders and set the appropriate fields with the given import data"""
            try:
                self.labelInput = fetchOrders(Path(ordersFile.get()), False)
                self.resetDropDowns()
                messagebox.showinfo(
                    "Success",
                    controller.orderSuccessText,
                )
                self.customerSelectionToolTip.configure(text="")

            # Error handling
            except PermissionError as permissionError:
                controller.permissionErrorMessage(permissionError)
            except FileNotFoundError as fileNotFoundError:
                controller.fileNotFoundErrorMessage(fileNotFoundError)
            except Exception as error:
                controller.generalErrorMessage(error, controller.generalFailureText)

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
                createLabels(self.labelInput, sl.SingleLabelOutput)

            # Error handling
            except PermissionError as permissionError:
                controller.permissionErrorMessage(permissionError)
            except FileNotFoundError as fileNotFoundError:
                controller.fileNotFoundErrorMessage(fileNotFoundError)
            except Exception as error:
                controller.generalErrorMessage(error, controller.printFailureText)

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

    def resetFields(self, *args):
        """Empty all the fields"""
        self.lCustomerName.set("")
        self.lCustomerId.set("")
        self.lAddress.set("")
        self.lZipCode.set("")
        self.lCity.set("")
        self.lPhoneNumber.set("")
        self.lDeliveryDate.set("")
        self.lProductName.set("")
        self.lCustomerRemarks1.set("")
