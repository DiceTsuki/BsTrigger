from pathlib import Path
import re
import json


# GUI-related
from tkinter import Toplevel as tk_tlvl
from tkinter import Frame as tk_frame
from tkinter import Label as tk_label
from tkinter import Button as tk_btn
from tkinter import Entry as tk_entry
from tkinter import messagebox as tk_msgbox
from tkinter import filedialog as tk_fdialog
from tkinter import END as tk_end


# Use class instead of def so that the UI is not initialized when the module is imported
class Main:
    # Initialize some global variables and UI
    def __init__(self, cfgpath):
        # Settings file
        self.cfgpath = cfgpath

        # UI Elements Colors
        self.frame_bg = "#2e2e2e"
        self.label_fg = "#ffffff"
        self.label_bg = "#2e2e2e"
        self.success_font_fg = "#009933"
        self.default_font_fg = "#000000"
        self.import_btn_fg = "#ffffff"
        self.import_btn_bg = "#2f9ee9"
        self.selectlogdir_btn_fg = "#ffffff"
        self.selectlogdir_btn_bg = "#4d4d4d"
        self.selectvmdatadir_btn_fg = "#ffffff"
        self.selectvmdatadir_btn_bg = "#4d4d4d"
        self.save_btn_fg = "#ffffff"
        self.save_btn_bg = "#4d4d4d"
        
        # Window Elements
        self.main_win = tk_tlvl()
        self.main_win.title("BlueStacks Parameters")
        self.main_win.minsize(500, 0)
        self.main_win.resizable(0, 0)
        
        # UI Elements
        left_frame = tk_frame(self.main_win, width=50, background=self.frame_bg)

        main_frame = tk_frame(self.main_win, background=self.frame_bg)
        import_btn = tk_btn(main_frame, text="Import BlueStacks Users/Installer Log", foreground=self.import_btn_fg, background=self.import_btn_bg, command=self.log_importer)
        importwhat_btn = tk_btn(main_frame, text="?", foreground=self.import_btn_fg, background=self.import_btn_bg, command=lambda:self.what_is_this("BlueStacksUsers.log or Installer_XXXX.log where XXXX is the BlueStacks version. Usually exists in BlueStacks Installation Directory\\Logs"))
        logdir_label = tk_label(main_frame, text="Log Directory", foreground=self.label_fg, background=self.label_bg)
        self.logdir_entry = tk_entry(main_frame, justify="center")
        selectlogdir_btn = tk_btn(main_frame, text="Select", foreground=self.selectlogdir_btn_fg, background=self.selectlogdir_btn_bg, command=lambda:self.selectdir(self.logdir_entry))
        vmdatadir_label = tk_label(main_frame, text="VM Data Directory", foreground=self.label_fg, background=self.label_bg)
        self.vmdatadir_entry = tk_entry(main_frame, justify="center")
        selectvmdatadir_btn = tk_btn(main_frame, text="Select", foreground=self.selectvmdatadir_btn_fg, background=self.selectvmdatadir_btn_bg, command=lambda:self.selectdir(self.vmdatadir_entry))
        oem_label = tk_label(main_frame, text="OEM", foreground=self.label_fg, background=self.label_bg)
        self.oem_entry = tk_entry(main_frame, justify="center")
        email_label = tk_label(main_frame, text="E-Mail", foreground=self.label_fg, background=self.label_bg)
        self.email_entry = tk_entry(main_frame, justify="center")
        machineid_label = tk_label(main_frame, text="Machine ID", foreground=self.label_fg, background=self.label_bg)
        self.machineid_entry = tk_entry(main_frame, justify="center")
        vermachineid_label = tk_label(main_frame, text="Version Machine ID", foreground=self.label_fg, background=self.label_bg)
        self.vermachineid_entry = tk_entry(main_frame, justify="center")
        apitoken_label = tk_label(main_frame, text="API Token", foreground=self.label_fg, background=self.label_bg)
        self.apitoken_entry = tk_entry(main_frame, justify="center")
        useragent_label = tk_label(main_frame, text="User-Agent", foreground=self.label_fg, background=self.label_bg)
        self.useragent_entry = tk_entry(main_frame, justify="center")
        notice_label = tk_label(main_frame, text="*E-Mail is optional", foreground=self.label_fg, background=self.label_bg)
        save_btn = tk_btn(main_frame, text="Save", foreground=self.save_btn_fg, background=self.save_btn_bg, command=self.save_details)
        
        right_frame = tk_frame(self.main_win, width=50, background=self.frame_bg)
        bottom_frame = tk_frame(self.main_win, height=10, background=self.frame_bg)
        
        # Make the UI elements visible
        self.main_win.columnconfigure(1, weight=1)
        self.main_win.rowconfigure(0, weight=1)

        left_frame.grid(row=0, column=0, sticky="NSWE")
        
        main_frame.grid(row=0, column=1, sticky="NSWE")
        main_frame.columnconfigure(0, weight=1)
        import_btn.grid(row=0, column=0, sticky="WE")
        importwhat_btn.grid(row=0, column=0, sticky="E")
        logdir_label.grid(row=1, column=0)
        self.logdir_entry.grid(row=2, column=0, sticky="WE")
        selectlogdir_btn.grid(row=2, column=0, sticky="E")
        vmdatadir_label.grid(row=3, column=0)
        self.vmdatadir_entry.grid(row=4, column=0, sticky="WE")
        selectvmdatadir_btn.grid(row=4, column=0, sticky="E")
        oem_label.grid(row=5, column=0)
        self.oem_entry.grid(row=6, column=0, sticky="WE")
        email_label.grid(row=7, column=0)
        self.email_entry.grid(row=8, column=0, sticky="WE")
        machineid_label.grid(row=9, column=0)
        self.machineid_entry.grid(row=10, column=0, sticky="WE")
        vermachineid_label.grid(row=11, column=0)
        self.vermachineid_entry.grid(row=12, column=0, sticky="WE")
        apitoken_label.grid(row=13, column=0)
        self.apitoken_entry.grid(row=14, column=0, sticky="WE")
        useragent_label.grid(row=15, column=0)
        self.useragent_entry.grid(row=16, column=0, sticky="WE")
        notice_label.grid(row=17, column=0)
        save_btn.grid(row=18, column=0)

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
        file = tk_fdialog.askopenfilename()
        
        if file != "":
            f = open(file, "r", encoding="utf-8")
            raw_log = f.read()
            f.close()
            
            # Set the log and VM data directories
            self.logdir_entry.delete(0, tk_end)
            self.logdir_entry.insert(0, str(Path(file).parents[0]))
            self.logdir_entry.configure(foreground=self.success_font_fg)
            self.vmdatadir_entry.delete(0, tk_end)
            self.vmdatadir_entry.insert(0, str(Path(file).parents[1] / "Engine"))
            self.vmdatadir_entry.configure(foreground=self.success_font_fg)
            
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
            
            if (log_oem and log_ver and log_guid):
                # OEM: BlueStacks = bgp; MSI App Player = msi2
                emu_name = "BlueStacks" # Set as default
                
                if log_oem.group(1) == "msi2":
                    emu_name = "MSI App Player"
                
                useragent = "%s/%s/%s gzip" % (emu_name, log_ver.group(1), log_guid.group(1))
                self.useragent_entry.delete(0, tk_end)
                self.useragent_entry.insert(0, useragent)
                self.useragent_entry.configure(foreground=self.success_font_fg)


    # Select Directory menu for related buttons
    def selectdir(self, entry):
        dir = tk_fdialog.askdirectory() # Will return a dir path using / separator
        
        if dir != "":
            entry.delete(0, tk_end)
            entry.insert(0, str(Path(dir))) # "Normalize" (/ -> \) the path using Pathlib.
            entry.configure(foreground=self.success_font_fg)


    # Load saved details from bs.cfg
    def load_details(self):
        try:
            with open(self.cfgpath, "r") as cfg:
                data = json.load(cfg)
                self.logdir_entry.delete(0, tk_end)
                self.logdir_entry.insert(0, data["BstkMisc"]["logdir"])
                self.vmdatadir_entry.delete(0, tk_end)
                self.vmdatadir_entry.insert(0, data["BstkMisc"]["vmdatadir"])
                self.oem_entry.delete(0, tk_end)
                self.oem_entry.insert(0, data["BstkParams"]["x_oem"])
                self.email_entry.delete(0, tk_end)
                self.email_entry.insert(0, data["BstkParams"]["x_email"])
                self.machineid_entry.delete(0, tk_end)
                self.machineid_entry.insert(0, data["BstkParams"]["x_machine_id"])
                self.vermachineid_entry.delete(0, tk_end)
                self.vermachineid_entry.insert(0, data["BstkParams"]["x_version_machine_id"])
                self.apitoken_entry.delete(0, tk_end)
                self.apitoken_entry.insert(0, data["BstkParams"]["x_api_token"])
                self.useragent_entry.delete(0, tk_end)
                self.useragent_entry.insert(0, data["BstkParams"]["User-Agent"])
        except:
            if Path(self.cfgpath).is_file():
                tk_msgbox.showerror(title="Error", message="Unable to read %s!" % (self.cfgpath))


    # Save the form data into bs.cfg
    def save_details(self):
        data = {
            "BstkParams": {
                "x_oem": self.oem_entry.get(),
                "x_email": self.email_entry.get(),
                "x_machine_id": self.machineid_entry.get(),
                "x_version_machine_id": self.vermachineid_entry.get(),
                "x_api_token": self.apitoken_entry.get(),
                "User-Agent": self.useragent_entry.get()
                }, 
            "BstkMisc": {
                "logdir": self.logdir_entry.get(),
                "vmdatadir": self.vmdatadir_entry.get()
                }
            }
        try:
            with open(self.cfgpath, "w") as cfg:
                json.dump(data, cfg)
            tk_msgbox.showinfo(title="Saved", message="BlueStacks parameters were saved successfully.")
        except:
            tk_msgbox.showerror(title="Error", message="Unable to save the BlueStacks parameters!")            


    # Helper popup for [?] button
    def what_is_this(self, text):
        tk_msgbox.showinfo(title="What is This?", message=text)


    # Handle the On Close event "properly"
    def on_close(self):
        self.main_win.quit() # Quit the mainloop()
        self.main_win.destroy()# Destroy the window
            
