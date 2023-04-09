#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.pathchooserinput import PathChooserInput
from ttkthemes import ThemedTk
from media.media import paths
from PIL import Image, ImageTk


class TestApp:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)

        # toplevel1 = ThemedTk(theme="breeze") if master is None else tk.Toplevel(master)
        toplevel1.option_add("*tearOff", False)  # This is always a good idea
        toplevel1.geometry("1400x900")
        toplevel1.title("Gooise Tafel Software")
        toplevel1.configure(padx=5, pady=5)

        # Menu
        self.frmMenu = ttk.Frame(toplevel1)
        self.frmMenu.configure(height=120, width=800)
        self.frmMenu.pack(side="top")

        self.btnOpenKal = ttk.Button(self.frmMenu)
        self.logoKAL = tk.PhotoImage(file=paths.KAL)
        self.btnOpenKal.configure(
            image=self.logoKAL, text="KAL", compound="left", width=30
        )
        self.btnOpenKal.grid(column=0, row=0)

        # self.btnOpenKal.grid_rowconfigure(0, weight=1)
        # self.btnOpenKal.grid_columnconfigure(0, weight=1)
        # self.btnOpenKal.bind("<Button>", self.btnOpenKalClick, add="+")

        self.btnOpenLiex = ttk.Button(self.frmMenu)
        self.logoLiex = tk.PhotoImage(file=paths.Liex)
        self.btnOpenLiex.configure(
            image=self.logoLiex, text="Liex", compound="left", width=30
        )
        self.btnOpenLiex.grid(column=1, row=0)
        self.btnOpenLiex.bind("<Button>", self.btnOpenLiexClick, add="+")

        self.btnOpenInkord = ttk.Button(self.frmMenu)
        self.logoInkord = tk.PhotoImage(file=paths.Inkord)
        self.btnOpenInkord.configure(
            image=self.logoInkord, text="Inkord", compound="left", width=30
        )
        self.btnOpenInkord.grid(column=2, row=0)
        self.btnOpenInkord.bind("<Button>", self.btnOpenInkordClick, add="+")

        self.btnOpenGL = ttk.Button(self.frmMenu)
        self.logoGL = tk.PhotoImage(file=paths.GotaLabel)
        self.btnOpenGL.configure(
            image=self.logoGL, text="GotaLabel", compound="left", width=30
        )
        self.btnOpenGL.grid(column=3, row=0)
        self.btnOpenGL.bind("<Button>", self.btnOpenGLClick, add="+")
        self.frmKALMain = ttk.Frame(toplevel1)
        self.frmKALMain.configure(height=200, padding=10, width=200)

        # KAL
        self.lblKALTitle = ttk.Label(self.frmKALMain)
        self.lblKALTitle.configure(font="TkHeadingFont", text="KAL")
        self.lblKALTitle.pack(side="top")
        self.lfrmKALInput = ttk.Labelframe(self.frmKALMain)
        self.lfrmKALInput.configure(height=200, padding=5, text="Input")
        self.lfrmKALOrders = ttk.Labelframe(self.lfrmKALInput)
        self.lfrmKALOrders.configure(
            borderwidth=0, height=200, text="Selecteer de orders:", width=200
        )
        self.cpKALOrders = PathChooserInput(self.lfrmKALOrders)
        self.cpKALOrders.configure(
            defaultextension=".xlsx", mustexist=True, type="file"
        )
        self.cpKALOrders.pack(expand="true", fill="x")
        self.cpKALOrders.bind("<1>", self.callback, add="")
        self.lfrmKALOrders.pack(expand="true", fill="x", padx=5, pady=5)
        self.lfrmKALCustomers = ttk.Labelframe(self.lfrmKALInput)
        self.lfrmKALCustomers.configure(
            borderwidth=0, height=200, text="Selecteer het klantenbestand:", width=200
        )
        self.cpKALCustomers = PathChooserInput(self.lfrmKALCustomers)
        self.cpKALCustomers.configure(
            defaultextension="'.xlsx'", mustexist=True, type="file"
        )
        self.cpKALCustomers.pack(expand="true", fill="x")
        self.lfrmKALCustomers.pack(expand="true", fill="x", padx=5, pady=5)
        self.lfrmKALInput.pack(expand="true", fill="x", pady="0 10", side="top")
        self.lfrmOutput = ttk.Labelframe(self.frmKALMain)
        self.lfrmOutput.configure(height=200, padding=10, text="Output:")
        self.lfrmKALPDFSaveLocation = ttk.Labelframe(self.lfrmOutput)
        self.lfrmKALPDFSaveLocation.configure(
            borderwidth=0,
            height=200,
            text="Selecteer waar je de pdf wilt opslaan",
            width=200,
        )
        self.cpKALPDFSave = PathChooserInput(self.lfrmKALPDFSaveLocation)
        self.cpKALPDFSave.configure(
            defaultextension="'.xlsx'", mustexist=True, type="file"
        )
        self.cpKALPDFSave.pack(expand="true", fill="x")
        self.cbKALShowPdf = ttk.Checkbutton(self.lfrmKALPDFSaveLocation)
        self.cbKALShowPdf.configure(text="Open de PDF na het maken")
        self.cbKALShowPdf.pack(pady=5, side="left")
        self.cbKALShowPdf.bind("<1>", self.callback, add="")
        self.lfrmKALPDFSaveLocation.pack(expand="true", fill="x", padx=5, pady=5)
        self.btnKALRun = ttk.Button(self.lfrmOutput)
        self.btnKALRun.configure(text="Maak KAL uitdraai", width=40)
        self.btnKALRun.pack(side="top")
        self.btnKALRun.bind("<Button>", self.btnKALrunKAL, add="+")
        self.lfrmOutput.pack(expand="true", fill="x", side="top")
        self.frmKALMain.pack(expand="true", fill="both", side="top")
        self.frmInkordMain = ttk.Frame(toplevel1)
        self.frmInkordMain.configure(height=556, width=200)
        self.lblInkordTitle = ttk.Label(self.frmInkordMain)
        self.lblInkordTitle.configure(text="Inkord")
        self.lblInkordTitle.pack(side="top")
        self.frmInkordMain.pack(expand="true", fill="both", side="top")
        self.frmLiexMain = ttk.Frame(toplevel1)
        self.frmLiexMain.configure(height=200, width=200)
        self.lblLiexTitle = ttk.Label(self.frmLiexMain)
        self.lblLiexTitle.configure(text="Liex")
        self.lblLiexTitle.pack(side="top")
        self.frmLiexMain.pack(expand="true", fill="both", side="top")
        self.frmGLlMain = ttk.Frame(toplevel1)
        self.frmGLlMain.configure(height=200, width=200)
        self.lblGLTitle = ttk.Label(self.frmGLlMain)
        self.lblGLTitle.configure(text="label14")
        self.lblGLTitle.pack(side="top")
        self.frmGLlMain.pack(expand="true", fill="both", side="top")

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()

    def btnOpenKalClick(self, event=None):
        pass

    def btnOpenInkordClick(self, event=None):
        pass

    def btnOpenLiexClick(self, event=None):
        pass

    def btnOpenGLClick(self, event=None):
        pass

    def callback(self, event=None):
        pass

    def btnKALrunKAL(self, event=None):
        pass


if __name__ == "__main__":
    app = TestApp()
    app.run()
