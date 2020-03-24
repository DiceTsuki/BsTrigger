from pathlib import Path
import re
import json


# GUI-related
from tkinter import Toplevel as tk_tlvl
from tkinter import Frame as tk_frame
from tkinter import Label as tk_label
from tkinter import Button as tk_btn
from tkinter import Entry as tk_entry
from tkinter import Checkbutton as tk_chkbtn
from tkinter import messagebox as tk_msgbox
from tkinter import filedialog as tk_fdialog
from tkinter import END as tk_end
from tkinter import BooleanVar as tk_boolvar


# Use class instead of def so that the UI is not initialized when the module is imported
class Main:
    # Initialize some global variables and UI
    def __init__(self, cfgpath):
        # Settings file
        self.cfgpath = cfgpath

        # Default Values. Should be similar to the ones in BsTrigger.py
        self.def_bs_port = 2871
        self.def_runasadmin = False
        self.def_max_run_checks = 30

        # UI Elements Colors
        self.frame_bg = "#2e2e2e"
        self.label_fg = "#ffffff"
        self.label_bg = "#2e2e2e"
        self.important_label_fg = "#00ffff"
        self.important_label_bg = "#2e2e2e"
        self.chkbtn_fg = "#ffffff"
        self.chkbtn_bg = "#2e2e2e"
        self.success_font_fg = "#009933"
        self.default_font_fg = "#000000"
        self.import_btn_fg = "#ffffff"
        self.import_btn_bg = "#2f9ee9"
        self.selectplayerlog_btn_fg = "#ffffff"
        self.selectplayerlog_btn_bg = "#4d4d4d"
        self.selectvmdatadir_btn_fg = "#ffffff"
        self.selectvmdatadir_btn_bg = "#4d4d4d"
        self.selectbsexe_btn_fg = "#ffffff"
        self.selectbsexe_btn_bg = "#4d4d4d"
        self.autobsport_btn_fg = "#ffffff"
        self.autobsport_btn_bg = "#4d4d4d"
        self.maxruncheckswhat_btn_fg = "#ffffff"
        self.maxruncheckswhat_btn_bg = "#4d4d4d"
        self.save_btn_fg = "#ffffff"
        self.save_btn_bg = "#4d4d4d"
        
        # Window Elements
        self.main_win = tk_tlvl()
        self.main_win.title("BlueStacks Parameters")
        self.main_win.minsize(500, 0)
        self.main_win.resizable(0, 0)
        validate_cmd = (self.main_win.register(self.validate_entry), "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W")
        
        # UI Elements
        left_frame = tk_frame(self.main_win, width=50, background=self.frame_bg)

        main_frame = tk_frame(self.main_win, background=self.frame_bg)
        import_btn = tk_btn(main_frame, text="Import BlueStacks Users/Installer Log", foreground=self.import_btn_fg, background=self.import_btn_bg, command=self.log_importer)
        importwhat_btn = tk_btn(main_frame, text="?", foreground=self.import_btn_fg, background=self.import_btn_bg, command=lambda:self.what_is_this("BlueStacksUsers.log or Installer_XXXX.log where XXXX is the BlueStacks version. Usually exists in BlueStacks Installation Directory\\Logs ."))
        vmdatadir_label = tk_label(main_frame, text="VM Data Directory", foreground=self.important_label_fg, background=self.important_label_bg)
        self.vmdatadir_entry = tk_entry(main_frame, justify="center")
        selectvmdatadir_btn = tk_btn(main_frame, text="Select", foreground=self.selectvmdatadir_btn_fg, background=self.selectvmdatadir_btn_bg, command=lambda:self.select_dir(self.vmdatadir_entry, "VM Data Directory"))
        selectvmdatadirwhat_btn = tk_btn(main_frame, text="?", foreground=self.selectvmdatadir_btn_fg, background=self.selectvmdatadir_btn_bg, command=lambda:self.what_is_this("Directory which stores VM-related data such as Virtual HDD etc. Usually the path is BlueStacks Installation Directory\\Engine ."))
        playerlog_label = tk_label(main_frame, text="Player Log", foreground=self.important_label_fg, background=self.important_label_bg)
        self.playerlog_entry = tk_entry(main_frame, justify="center")
        selectplayerlog_btn = tk_btn(main_frame, text="Select", foreground=self.selectplayerlog_btn_fg, background=self.selectplayerlog_btn_bg, command=lambda:self.select_file(self.playerlog_entry, "Player.log"))
        selectplayerlogwhat_btn = tk_btn(main_frame, text="?", foreground=self.selectplayerlog_btn_fg, background=self.selectplayerlog_btn_bg, command=lambda:self.what_is_this("Player.log . Usually exists in BlueStacks Installation Directory\\Logs . Start BlueStacks' instance once to generate it."))
        bsexe_label = tk_label(main_frame, text="BlueStacks' Executable", foreground=self.important_label_fg, background=self.important_label_bg)
        self.bsexe_entry = tk_entry(main_frame, justify="center")
        selectbsexe_btn = tk_btn(main_frame, text="Select", foreground=self.selectbsexe_btn_fg, background=self.selectbsexe_btn_bg, command=lambda:self.select_file(self.bsexe_entry, "Bluestacks.exe"))
        selectbsexewhat_btn = tk_btn(main_frame, text="?", foreground=self.selectbsexe_btn_fg, background=self.selectbsexe_btn_bg, command=lambda:self.what_is_this("Bluestacks.exe . Used by BlueStacks Booter to launch BlueStacks' instances. Usually exists in BlueStacks Installation Directory\\Client ."))
        self.runasadmin_chkbtn_var = tk_boolvar()
        runasadmin_chkbtn = tk_chkbtn(main_frame, text="Run BlueStacks As Administrator", variable=self.runasadmin_chkbtn_var, foreground=self.chkbtn_fg, background=self.chkbtn_bg, activeforeground=self.chkbtn_fg, activebackground=self.chkbtn_bg, selectcolor=self.chkbtn_bg)
        self.runasadmin_chkbtn_var.set(self.def_runasadmin)
        bsport_label = tk_label(main_frame, text="BlueStacks Port", foreground=self.important_label_fg, background=self.important_label_bg)
        self.bsport_entry = tk_entry(main_frame, justify="center", validate="key", validatecommand=validate_cmd)
        self.bsport_entry.insert(0, self.def_bs_port)
        autobsport_btn = tk_btn(main_frame, text="Auto", foreground=self.autobsport_btn_fg, background=self.autobsport_btn_bg, command=self.set_bsport)
        autobsportwhat_btn = tk_btn(main_frame, text="?", foreground=self.autobsport_btn_fg, background=self.autobsport_btn_bg, command=lambda:self.what_is_this("Port used by Bluestacks.exe to listen to requests which includes app launch request. Auto button will set it based on BlueStacksUI.log . Usually exists in BlueStacks Installation Directory\\Logs . The default value is %d." % (self.def_bs_port)))
        maxrunchecks_label = tk_label(main_frame, text="Max. Run Checks", foreground=self.important_label_fg, background=self.important_label_bg)
        self.maxrunchecks_entry = tk_entry(main_frame, justify="center", validate="key", validatecommand=validate_cmd)
        self.maxrunchecks_entry.insert(0, self.def_max_run_checks)
        maxruncheckswhat_btn = tk_btn(main_frame, text="?", foreground=self.maxruncheckswhat_btn_fg, background=self.maxruncheckswhat_btn_bg, command=lambda:self.what_is_this("Maximum number for checks to be done when booting BlueStacks' instance in determining whether the boot is completed. If the limit is reached, BsTrigger will stop waiting and start normally. The default value is %d." % (self.def_max_run_checks)))
        oem_label = tk_label(main_frame, text="OEM", foreground=self.label_fg, background=self.label_bg)
        self.oem_entry = tk_entry(main_frame, justify="center")
        email_label = tk_label(main_frame, text="E-Mail", foreground=self.label_fg, background=self.label_bg)
        self.email_entry = tk_entry(main_frame, justify="center")
        machineid_label = tk_label(main_frame, text="Machine ID", foreground=self.label_fg, background=self.label_bg)
        self.machineid_entry = tk_entry(main_frame, justify="center")
        vermachineid_label = tk_label(main_frame, text="Version Machine ID", foreground=self.label_fg, background=self.label_bg)
        self.vermachineid_entry = tk_entry(main_frame, justify="center")
        apitoken_label = tk_label(main_frame, text="API Token", foreground=self.important_label_fg, background=self.important_label_bg)
        self.apitoken_entry = tk_entry(main_frame, justify="center")
        useragent_label = tk_label(main_frame, text="User-Agent", foreground=self.label_fg, background=self.label_bg)
        self.useragent_entry = tk_entry(main_frame, justify="center")
        notice_label = tk_label(main_frame, text="*Required", foreground=self.important_label_fg, background=self.important_label_bg)
        save_btn = tk_btn(main_frame, text="Save", foreground=self.save_btn_fg, background=self.save_btn_bg, command=self.save_details)
        
        right_frame = tk_frame(self.main_win, width=50, background=self.frame_bg)
        bottom_frame = tk_frame(self.main_win, height=10, background=self.frame_bg)
        
        # Make the UI elements visible
        self.main_win.columnconfigure(1, weight=1)
        self.main_win.rowconfigure(0, weight=1)

        left_frame.grid(row=0, column=0, sticky="NSWE")
        
        main_frame.grid(row=0, column=1, sticky="NSWE")
        main_frame.columnconfigure(0, weight=1)
        import_btn.grid(row=0, column=0, columnspan=2, sticky="WE")
        importwhat_btn.grid(row=0, column=2, sticky="E")
        vmdatadir_label.grid(row=1, column=0, columnspan=3)
        self.vmdatadir_entry.grid(row=2, column=0, sticky="WE")
        selectvmdatadir_btn.grid(row=2, column=1)
        selectvmdatadirwhat_btn.grid(row=2, column=2)
        playerlog_label.grid(row=3, column=0, columnspan=3)
        self.playerlog_entry.grid(row=4, column=0, sticky="WE")
        selectplayerlog_btn.grid(row=4, column=1)
        selectplayerlogwhat_btn.grid(row=4, column=2)
        bsexe_label.grid(row=5, column=0, columnspan=3)
        self.bsexe_entry.grid(row=6, column=0, sticky="WE")
        selectbsexe_btn.grid(row=6, column=1)
        selectbsexewhat_btn.grid(row=6, column=2)
        runasadmin_chkbtn.grid(row=7, column=0, columnspan=3)
        bsport_label.grid(row=8, column=0, columnspan=3)
        self.bsport_entry.grid(row=9, column=0, sticky="WE")
        autobsport_btn.grid(row=9, column=1)
        autobsportwhat_btn.grid(row=9, column=2)
        maxrunchecks_label.grid(row=10, column=0, columnspan=3)
        self.maxrunchecks_entry.grid(row=11, column=0, columnspan=2, sticky="WE")
        maxruncheckswhat_btn.grid(row=11, column=2)
        oem_label.grid(row=12, column=0, columnspan=3)
        self.oem_entry.grid(row=13, column=0, columnspan=3, sticky="WE")
        email_label.grid(row=14, column=0, columnspan=3)
        self.email_entry.grid(row=15, column=0, columnspan=3, sticky="WE")
        machineid_label.grid(row=16, column=0, columnspan=3)
        self.machineid_entry.grid(row=17, column=0, columnspan=3, sticky="WE")
        vermachineid_label.grid(row=18, column=0, columnspan=3)
        self.vermachineid_entry.grid(row=19, column=0, columnspan=3, sticky="WE")
        apitoken_label.grid(row=20, column=0, columnspan=3)
        self.apitoken_entry.grid(row=21, column=0, columnspan=3, sticky="WE")
        useragent_label.grid(row=22, column=0, columnspan=3)
        self.useragent_entry.grid(row=23, column=0, columnspan=3, sticky="WE")
        notice_label.grid(row=24, column=0, columnspan=3)
        save_btn.grid(row=25, column=0, columnspan=3)

        right_frame.grid(row=0, column=2, sticky="NSWE")
        bottom_frame.grid(row=1, column=0, columnspan=3, sticky="NSWE")
        
        # Load existing configuration file
        self.load_details()
        
        # "On Close" event
        self.main_win.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Start the loop
        self.main_win.mainloop()


    # BlueStacks Installer Log Importer
    def log_importer(self):
        file = self.select_file(filename="BlueStacksUsers.log or Installer_XXXX.log")
        
        if file != "":
            f = open(file, "r", encoding="utf-8")
            raw_log = f.read()
            f.close()
            
            # Set the log and VM data directories
            self.vmdatadir_entry.delete(0, tk_end)
            self.vmdatadir_entry.insert(0, str(Path(file).parents[1] / "Engine"))
            self.vmdatadir_entry.configure(foreground=self.success_font_fg)
            self.playerlog_entry.delete(0, tk_end)
            self.playerlog_entry.insert(0, str(Path(file).parents[0] / "Player.log"))
            self.playerlog_entry.configure(foreground=self.success_font_fg)
            self.bsexe_entry.delete(0, tk_end)
            self.bsexe_entry.insert(0, str(Path(file).parents[1] / "Client" / "Bluestacks.exe"))
            self.bsexe_entry.configure(foreground=self.success_font_fg)
            
            # Find required details using regex
            log_oem = re.search("OEM=(\S*)", raw_log)
            
            if log_oem:
                self.oem_entry.delete(0, tk_end)
                self.oem_entry.insert(0, log_oem.group(1))
                self.oem_entry.configure(foreground=self.success_font_fg)
                
            log_machineid = re.search("machineId=(\S*)", raw_log)
            
            if log_machineid:
                self.machineid_entry.delete(0, tk_end)
                self.machineid_entry.insert(0, log_machineid.group(1))
                self.machineid_entry.configure(foreground=self.success_font_fg)
                
            log_vermachineid = re.search("versionMachineId=(\S*)", raw_log)
            
            if log_vermachineid:
                self.vermachineid_entry.delete(0, tk_end)
                self.vermachineid_entry.insert(0, log_vermachineid.group(1))
                self.vermachineid_entry.configure(foreground=self.success_font_fg)
                
            log_apitoken = re.search("ApiToken=(\S*)", raw_log)
            
            if log_apitoken:
                self.apitoken_entry.delete(0, tk_end)
                self.apitoken_entry.insert(0, log_apitoken.group(1))
                self.apitoken_entry.configure(foreground=self.success_font_fg)
                
            log_ver = re.search("VERSION=(\S*)", raw_log)
            log_guid = re.search("GUID=(\S*)", raw_log)
            
            if log_oem and log_ver and log_guid:
                # OEM: BlueStacks = bgp; MSI App Player = msi2
                emu_name = "BlueStacks" # Set as default
                
                if log_oem.group(1) == "msi2":
                    emu_name = "MSI App Player"
                
                useragent = "%s/%s/%s gzip" % (emu_name, log_ver.group(1), log_guid.group(1))
                self.useragent_entry.delete(0, tk_end)
                self.useragent_entry.insert(0, useragent)
                self.useragent_entry.configure(foreground=self.success_font_fg)


    # Select File menu for related buttons
    def select_file(self, entry="", filename=""):
        path = tk_fdialog.askopenfilename(title="Select %s" % (filename)) # Will return a file path using / separator
        
        if path != "" and entry != "":
            entry.delete(0, tk_end)
            entry.insert(0, str(Path(path))) # "Normalize" (/ -> \) the path using Pathlib.
            entry.configure(foreground=self.success_font_fg)
        elif path != "" and entry == "":
            return str(Path(path))
        else:
            return ""


    # Select Directory menu for related buttons
    def select_dir(self, entry="", dirname=""):
        path = tk_fdialog.askdirectory(title="Select %s" % (dirname)) # Will return a dir path using / separator
        
        if path != "" and entry != "":
            entry.delete(0, tk_end)
            entry.insert(0, str(Path(path))) # "Normalize" (/ -> \) the path using Pathlib.
            entry.configure(foreground=self.success_font_fg)
        elif path != "" and entry == "":
            return str(Path(path))
        else:
            return ""


    # Load saved details from bs.cfg
    def load_details(self):
        try:
            with open(self.cfgpath, "r") as cfg:
                data = json.load(cfg)
                self.vmdatadir_entry.delete(0, tk_end)
                self.vmdatadir_entry.insert(0, data["BsMisc"]["vmdatadir"])
                self.playerlog_entry.delete(0, tk_end)
                self.playerlog_entry.insert(0, data["BsMisc"]["playerlog"])
                self.bsexe_entry.delete(0, tk_end)
                self.bsexe_entry.insert(0, data["BsMisc"]["bsexe"])
                self.runasadmin_chkbtn_var.set(data["BsMisc"]["runasadmin"])
                self.bsport_entry.delete(0, tk_end)
                self.bsport_entry.insert(0, data["BsMisc"]["bsport"])
                self.maxrunchecks_entry.delete(0, tk_end)
                self.maxrunchecks_entry.insert(0, data["BsMisc"]["maxrunchecks"])
                self.oem_entry.delete(0, tk_end)
                self.oem_entry.insert(0, data["BsParams"]["x_oem"])
                self.email_entry.delete(0, tk_end)
                self.email_entry.insert(0, data["BsParams"]["x_email"])
                self.machineid_entry.delete(0, tk_end)
                self.machineid_entry.insert(0, data["BsParams"]["x_machine_id"])
                self.vermachineid_entry.delete(0, tk_end)
                self.vermachineid_entry.insert(0, data["BsParams"]["x_version_machine_id"])
                self.apitoken_entry.delete(0, tk_end)
                self.apitoken_entry.insert(0, data["BsParams"]["x_api_token"])
                self.useragent_entry.delete(0, tk_end)
                self.useragent_entry.insert(0, data["BsParams"]["User-Agent"])
        except:
            if Path(self.cfgpath).is_file():
                tk_msgbox.showerror(title="Error", message="Unable to read %s!" % (self.cfgpath))


    # Save the form data into bs.cfg
    def save_details(self):
        if self.vmdatadir_entry.get() == "":
            tk_msgbox.showerror(title="Error", message="VM Data Directory is empty!")
        elif self.playerlog_entry.get() == "":
            tk_msgbox.showerror(title="Error", message="Player Log is empty!")
        elif self.bsexe_entry.get() == "":
            tk_msgbox.showerror(title="Error", message="BlueStacks' Executable is empty!")
        elif self.apitoken_entry.get() == "":
            tk_msgbox.showerror(title="Error", message="API Token is empty!")
        else:
            if self.bsport_entry.get() == "":
                tk_msgbox.showerror(title="Error", message="BlueStacks Port is empty! Resetting to default value.")
                self.bsport_entry.delete(0, tk_end)
                self.bsport_entry.insert(0, self.def_bs_port)

            if self.maxrunchecks_entry.get() == "":
                tk_msgbox.showerror(title="Error", message="Max. Run Checks is empty! Resetting to default value.")
                self.maxrunchecks_entry.delete(0, tk_end)
                self.maxrunchecks_entry.insert(0, self.def_max_run_checks)
            
            data = {
                "BsParams": {
                    "x_oem": self.oem_entry.get(),
                    "x_email": self.email_entry.get(),
                    "x_machine_id": self.machineid_entry.get(),
                    "x_version_machine_id": self.vermachineid_entry.get(),
                    "x_api_token": self.apitoken_entry.get(),
                    "User-Agent": self.useragent_entry.get()
                    }, 
                "BsMisc": {
                    "vmdatadir": self.vmdatadir_entry.get(),
                    "playerlog": self.playerlog_entry.get(),
                    "bsexe": self.bsexe_entry.get(),
                    "runasadmin": self.runasadmin_chkbtn_var.get(),
                    "bsport": int(self.bsport_entry.get()),
                    "maxrunchecks": int(self.maxrunchecks_entry.get())
                    }
                }
            try:
                with open(self.cfgpath, "w") as cfg:
                    json.dump(data, cfg)
                    
                tk_msgbox.showinfo(title="Saved", message="BlueStacks parameters were saved successfully.")
            except:
                tk_msgbox.showerror(title="Error", message="Unable to save the BlueStacks parameters!")


    # Set BlueStacks Port based on BlueStacksUI.log
    def set_bsport(self):
        bsuilog = self.select_file(filename="BlueStacksUI.log")

        if bsuilog != "":
            bs_port = self.def_bs_port
            pattern = "\(Bluestacks\) INFO: Server listening on port (\d+)"

            try:
                f = open(bsuilog, "r", encoding="utf-8")
                data = f.read()
                f.close()
                bs_port = int(re.findall(pattern, data)[-1])
                self.bsport_entry.configure(foreground=self.success_font_fg)
            except:
                tk_msgbox.showerror(title="Error", message="BlueStacks Port not found. Resetting it to default value.")
                self.bsport_entry.configure(foreground=self.default_font_fg)

            self.bsport_entry.delete(0, tk_end)
            self.bsport_entry.insert(0, bs_port)


    # Similar to BsTrigger.py. Restict entry inout to INT only
    def validate_entry(self, action, index, value_if_allowed,
    prior_value, text, validation_type, trigger_type, widget_name):
        if action == "1": # "1" = insert
            try:
                int(text)
                return True
            except ValueError:
                return False
        else:
            return True


    # Helper popup for [?] button
    def what_is_this(self, text):
        tk_msgbox.showinfo(title="What is This?", message=text)


    # Handle the On Close event "properly"
    def on_close(self):
        self.main_win.quit() # Quit the mainloop()
        self.main_win.destroy()# Destroy the window
            
