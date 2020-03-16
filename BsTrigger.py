from pathlib import Path
import re
import json


# GUI-related
from tkinter import Tk as tk_tk
from tkinter import Toplevel as tk_tlvl
from tkinter import Frame as tk_frame
from tkinter import Label as tk_label
from tkinter import Entry as tk_entry
from tkinter import Button as tk_btn
from tkinter import messagebox as tk_msgbox
from tkinter import StringVar as tk_strvar
from tkinter import OptionMenu as tk_optmenu
from tkinter import END as tk_end


# BsTrigger Modules
import bsconf
import bsconn


class Main:
    def __init__(self):
        # Global Variables
        self.bstr_ver = "1.0"
        self.bs_cfg = "bs.cfg"
        self.inst_cfg = "inst.cfg"
        self.def_bsa_port = 9999
        self.def_hdp_port = 2881
        self.def_turbo = 120
        self.inst_name = ""
        self.inst_id = 0
        self.inst_gadid = ""
        self.inst_aid = ""

        # Global Variables 2: Color Edition
        self.frame_bg = "#2e2e2e"
        self.label_fg = "#ffffff"
        self.label_bg = "#2e2e2e"
        self.success_font_fg = "#009933"
        self.default_font_fg = "#000000"
        self.success_btn_fg = "#ffffff"
        self.success_btn_bg = "#2f9ee9"
        self.turbo_btn_fg = "#ffffff"
        self.turbo_btn_bg = "#ff0000"
        self.fps_counter_on_btn_fg = "#ffffff"
        self.fps_counter_on_btn_bg = "#000000"
        self.fps_counter_off_btn_fg = "#000000"
        self.fps_counter_off_btn_bg = "#ffffff"
        self.auto_port_btn_fg = "#ffffff"
        self.auto_port_btn_bg = "#64b305"
        self.inst_optmenu_fg = "#ffffff"
        self.inst_optmenu_bg = "#4d4d4d"
        self.inst_info_btn_fg = "#ffffff"
        self.inst_info_btn_bg = "#4d4d4d"
        self.inst_refresh_btn_fg = "#ffffff"
        self.inst_refresh_btn_bg = "#4d4d4d"
        self.inst_save_btn_fg = "#ffffff"
        self.inst_save_btn_bg = "#4d4d4d"
        self.inst_load_btn_fg = "#ffffff"
        self.inst_load_btn_bg = "#4d4d4d"
        self.inst_delete_btn_fg = "#ffffff"
        self.inst_delete_btn_bg = "#4d4d4d"
        self.inst_delete_all_btn_fg = "#ffffff"
        self.inst_delete_all_btn_bg = "#4d4d4d"
        self.bs_btn_fg = "#ffffff"
        self.bs_btn_bg = "#2f9ee9"
        self.ok_btn_fg = "#ffffff"
        self.ok_btn_bg = "#4d4d4d"
        
        # Main Window
        self.main_win = tk_tk()
        self.main_win.title("BsTrigger %s" % (self.bstr_ver))
        self.main_win.minsize(500, 0)
        self.main_win.resizable(0, 0)
        self.main_win.configure(background=self.frame_bg)
        validate_cmd = (self.main_win.register(self.validate_entry), "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W") # For TK Entry validation

        self.main_win.columnconfigure(0, weight=1)
        self.main_win.columnconfigure(1, weight=1)
        self.main_win.rowconfigure(0, weight=1)
        self.main_win.rowconfigure(1, weight=1)

        # Controls Frame
        self.ctrl_frame = tk_frame(self.main_win, background=self.frame_bg)

        turbo_frame = tk_frame(self.ctrl_frame, background=self.frame_bg)
        self.turbo_btn = tk_btn(turbo_frame, text="TURBO", width=10, height=5, foreground=self.turbo_btn_fg, background=self.turbo_btn_bg, command=self.trigger_turbo)
        turbowhat_btn = tk_btn(turbo_frame, text="?", height=5, foreground=self.turbo_btn_fg, background=self.turbo_btn_bg, command=lambda:self.what_is_this("Trigger the BlueStacks' FPS cap change. This will not change the FPS set in BlueStacks Settings. May cause some apps / games to double their FPS cap (e.g. from 30 to 60 FPS) if the TURBO FPS is set to 2X of the FPS set in the BlueStacks Settings.\n\nMAKE SURE TO ENABLE VSYNC (If disabled for BlueStacks) or FPS LIMITER to prevent screen tearing / overheating."))
        turbo_label = tk_label(turbo_frame, text="FPS", foreground=self.label_fg, background=self.label_bg)
        self.turbo_entry = tk_entry(turbo_frame, justify="center", width=5, validate="key", validatecommand=validate_cmd)
        self.turbo_entry.insert(tk_end, self.def_turbo)

        fps_counter_frame = tk_frame(self.ctrl_frame, background=self.frame_bg)
        self.fps_counter_on_btn = tk_btn(fps_counter_frame, text="SHOW\n[FPS]", width=5, height=5, foreground=self.fps_counter_on_btn_fg, background=self.fps_counter_on_btn_bg, command=lambda:self.trigger_fps_counter(True))
        self.fps_counter_off_btn = tk_btn(fps_counter_frame, text="HIDE\n[FPS]", width=5, height=5, foreground=self.fps_counter_off_btn_fg, background=self.fps_counter_off_btn_bg, command=lambda:self.trigger_fps_counter(False))
        fps_counterwhat_btn = tk_btn(fps_counter_frame, text="?", height=5, foreground=self.fps_counter_off_btn_fg, background=self.fps_counter_off_btn_bg, command=lambda:self.what_is_this("Trigger the BlueStacks' FPS Counter. This will not change the FPS Counter set in BlueStacks Settings."))
        
        self.ctrl_frame.grid(row=0, column=0, sticky="NSWE")
        self.ctrl_frame.columnconfigure(0, weight=1)
        self.ctrl_frame.columnconfigure(1, weight=1)
        self.ctrl_frame.rowconfigure(0, weight=1)
        turbo_frame.grid(row=0, column=0, sticky="NSWE")
        turbo_frame.columnconfigure(0, weight=1)
        turbo_frame.columnconfigure(1, weight=1)
        turbo_frame.columnconfigure(2, weight=1)
        turbo_frame.columnconfigure(3, weight=1)
        turbo_frame.rowconfigure(0, weight=1)
        self.turbo_btn.grid(row=0, column=0, rowspan=4, columnspan=4)
        turbowhat_btn.grid(row=0, column=3, rowspan=4, sticky="W")
        turbo_label.grid(row=3, column=0, columnspan=2, sticky="E")
        self.turbo_entry.grid(row=3, column=2, columnspan=2, sticky="W")
        fps_counter_frame.grid(row=0, column=1, sticky="NSWE")
        fps_counter_frame.columnconfigure(0, weight=1)
        fps_counter_frame.columnconfigure(1, weight=1)
        fps_counter_frame.columnconfigure(2, weight=1)
        fps_counter_frame.columnconfigure(3, weight=1)
        fps_counter_frame.rowconfigure(0, weight=1)
        self.fps_counter_on_btn.grid(row=0, column=0, rowspan=4, columnspan=2, sticky="E")
        self.fps_counter_off_btn.grid(row=0, column=2, rowspan=4, columnspan=2, sticky="W")
        fps_counterwhat_btn.grid(row=0, column=3, rowspan=4, sticky="W")

        # Connection Frame
        self.conn_frame = tk_frame(self.main_win, background=self.frame_bg)
        
        conn_label = tk_label(self.conn_frame, text="Connection Ports", foreground=self.label_fg, background=self.label_bg, justify="center")
        bsa_port_label = tk_label(self.conn_frame, text="Bs Android", foreground=self.label_fg, background=self.label_bg)
        self.bsa_port_entry = tk_entry(self.conn_frame, justify="center", validate="key", validatecommand=validate_cmd)
        self.bsa_port_entry.insert(tk_end, self.def_bsa_port)
        hdp_port_label = tk_label(self.conn_frame, text="HD-Player", foreground=self.label_fg, background=self.label_bg)
        self.hdp_port_entry = tk_entry(self.conn_frame, justify="center", validate="key", validatecommand=validate_cmd)
        self.hdp_port_entry.insert(tk_end, self.def_hdp_port)
        auto_port_btn = tk_btn(self.conn_frame, text="Auto Set", foreground=self.auto_port_btn_fg, background=self.auto_port_btn_bg, command=self.autoset_conn_ports)
        auto_portwhat_btn = tk_btn(self.conn_frame, text="?", foreground=self.auto_port_btn_fg, background=self.auto_port_btn_bg, command=lambda:self.what_is_this("Load ports assigned to current instance from BlueStacks' player.log. Restart your BlueStacks' instance if the Auto Set does not work."))
        
        self.conn_frame.grid(row=0, column=1, sticky="E")
        conn_label.grid(row=0, column=0)
        bsa_port_label.grid(row=1, column=0)
        self.bsa_port_entry.grid(row=2, column=0)
        hdp_port_label.grid(row=3, column=0)
        self.hdp_port_entry.grid(row=4, column=0)
        auto_port_btn.grid(row=5, column=0, sticky="WE")
        auto_portwhat_btn.grid(row=5, column=0, sticky="E")
                
        # Instances Frame
        self.inst_frame = tk_frame(self.main_win, background=self.frame_bg)
        
        inst_label = tk_label(self.inst_frame, text="Instance:", foreground=self.label_fg, background=self.label_bg)
        inst_info_btn = tk_btn(self.inst_frame, text="?", foreground=self.inst_info_btn_fg, background=self.inst_info_btn_bg, command=self.inst_info)
        inst_refresh_btn = tk_btn(self.inst_frame, text="Refresh", foreground=self.inst_refresh_btn_fg, background=self.inst_refresh_btn_bg, command=self.set_inst)
        inst_save_btn = tk_btn(self.inst_frame, text="Save", foreground=self.inst_save_btn_fg, background=self.inst_save_btn_bg, command=self.save_inst)
        inst_load_btn = tk_btn(self.inst_frame, text="Load", foreground=self.inst_load_btn_fg, background=self.inst_load_btn_bg, command=self.load_inst)
        inst_delete_btn = tk_btn(self.inst_frame, text="Del", foreground=self.inst_delete_btn_fg, background=self.inst_delete_btn_bg, command=self.delete_inst)
        inst_delete_all_btn = tk_btn(self.inst_frame, text="Del All", foreground=self.inst_delete_all_btn_fg, background=self.inst_delete_all_btn_bg, command=self.delete_all_inst)

        self.inst_frame.grid(row=1, column=0, sticky="W")
        inst_label.grid(row=0, column=0)
        self.inst_var = tk_strvar(self.inst_frame)
        self.inst_var_traceid = "TRACE_NOT_STARTED"
        instances = self.get_inst_list()
        self.set_inst_selector(instances)
        inst_info_btn.grid(row=0, column=2)
        inst_refresh_btn.grid(row=0, column=3)
        inst_save_btn.grid(row=0, column=4)
        inst_load_btn.grid(row=0, column=5)
        inst_delete_btn.grid(row=0, column=6)
        inst_delete_all_btn.grid(row=0, column=7)

        # Settings Frame
        sett_frame = tk_frame(self.main_win, background=self.frame_bg)
        
        sett_frame.grid(row=1, column=1, sticky="E")
        
        bs_btn = tk_btn(sett_frame, text="BlueStacks Parameters", foreground=self.bs_btn_fg, background=self.bs_btn_bg, command=self.set_bsconf)
        
        bs_btn.grid(row=0, column=0, sticky="WE")

        # "Remove" related frames if current instance is / can not be set
        if self.inst_name == "":
            self.ctrl_frame.grid_remove()
            self.conn_frame.grid_remove()
            self.inst_frame.grid_remove()

        # Start the main window loop to listen to events
        self.main_win.mainloop()


    # Open BlueStacks Param Configurator
    def set_bsconf(self):
        self.main_win.withdraw()
        bsc = bsconf.Main(self.bs_cfg)
        self.set_inst_selector(self.get_inst_list())
        
        # Restore the frames once current instance is set (refer to __init__)
        # No need to re-set the .grid() options because .grid_remove() will still remember the previous options
        if self.inst_name != "":
            self.ctrl_frame.grid()
            self.conn_frame.grid()
            self.inst_frame.grid()
            
        self.main_win.deiconify()


    # Get value of a variable in bs.cfg
    def get_bsconf(self, cat, var):
        try:
            with open(self.bs_cfg, "r") as cfg:
                details = json.load(cfg)
                return details[cat][var]
        except:
            return ""


    # Set current instance values (Name, ID, Google Ads ID and Android ID) based on Option Menu state
    def set_inst(self, *args):
        self.inst_name = self.inst_var.get()
        
        if self.inst_name == "Android":
            self.inst_id = 0
        else:
            match = re.match("Android_(\d+)", self.inst_name)
            if match:
                self.inst_id = int(match.group(1))
            else:
                self.inst_id = 0
                
        # load selected instance saved config into related UI entries
        self.load_inst()
        
        # Get Google Ad ID and Android ID
        # But 1st, reset the global value of both variables
        # We dont want to send old values while looking for new values of same variable for different instance
        self.inst_gadid = ""
        self.inst_aid = ""
        port = self.def_bsa_port
        
        if self.bsa_port_entry.get() != "":
            port = int(self.bsa_port_entry.get())
        
        gadid_path = "/getGoogleAdID"
        gadid_conn = self.set_bsconn("GET_GOOGLEADID", port, gadid_path)
        gadid_resp = gadid_conn.get_response()
        aid_path = "/getAndroidID"
        aid_conn = self.set_bsconn("GET_ANDROIDID", port, aid_path)
        aid_resp = aid_conn.get_response()
        
        if "googleadid" in gadid_resp:
            json_gadid_resp = self.json_bsconn(gadid_resp)
            if json_gadid_resp != {}:
                self.inst_gadid = json_gadid_resp["googleadid"]
                
        if "androidID" in aid_resp:
            json_aid_resp = self.json_bsconn(aid_resp)
            if json_aid_resp != {}:
                self.inst_aid = json_aid_resp["androidID"]
                
        if self.inst_gadid == "" or self.inst_aid == "":
            self.main_win.title("BsTrigger %s (%s: Closed)" % (self.bstr_ver, self.inst_name))
        elif self.inst_gadid != "" and self.inst_aid != "":
            self.main_win.title("BsTrigger %s (%s : Running)" % (self.bstr_ver, self.inst_name))


    # Get the instances list from VM data directory
    def get_inst_list(self):
        vmdatadir = self.get_bsconf("BstkMisc", "vmdatadir")
        instances = list()
        
        if vmdatadir != "" and Path(vmdatadir).is_dir():
            for child in Path(vmdatadir).iterdir():
                if child.is_dir():
                    if child.name == "Android":
                        instances.append(child.name)
                    elif re.match("Android_\d+", child.name):
                        instances.append(child.name)
                        
        return instances


    # Contruct the Option Menu (Dropdown Menu) of instances list given
    def set_inst_selector(self, instances):
        if instances != []:
            # Disable previously set "trace" so that we will not invoke set_inst when updating the option menu
            if self.inst_var_traceid != "TRACE_NOT_STARTED":
                self.inst_var.trace_vdelete("w", self.inst_var_traceid)
                
            # Create/Update the option menu
            self.inst_var.set(instances[0])
            inst_optmenu = tk_optmenu(self.inst_frame, self.inst_var, *instances) # * = unpack list
            inst_optmenu.configure(foreground=self.inst_optmenu_fg, background=self.inst_optmenu_bg, activeforeground=self.inst_optmenu_fg, activebackground=self.inst_optmenu_bg)
            inst_optmenu["menu"].configure(foreground=self.inst_optmenu_fg, background=self.inst_optmenu_bg)
            inst_optmenu["highlightthickness"] = 0 # Bye bye border!
            inst_optmenu.grid(row=0, column=1)

            # Start the "trace"
            self.inst_var_traceid = self.inst_var.trace("w", self.set_inst)
            
            # Set the related global variables based on currently selected option
            self.set_inst()
            
            # Reset the color of buttons in ctrl_frame
            self.turbo_btn.configure(foreground=self.turbo_btn_fg, background=self.turbo_btn_bg)
            self.fps_counter_on_btn.configure(foreground=self.fps_counter_on_btn_fg, background=self.fps_counter_on_btn_bg)
            self.fps_counter_off_btn.configure(foreground=self.fps_counter_off_btn_fg, background=self.fps_counter_off_btn_bg)


    # Save current instance config
    def save_inst(self):
        if self.inst_name != "" and self.turbo_entry.get() != "" and self.bsa_port_entry.get() != "" and self.hdp_port_entry.get() != "":
            try:
                with open(self.inst_cfg, "r") as cfg:
                    data = json.load(cfg)
                    data.update({
                        self.inst_name: {
                            "turbo": int(self.turbo_entry.get()),
                            "bsa_port": int(self.bsa_port_entry.get()),
                            "hdp_port": int(self.hdp_port_entry.get())
                            }
                    })
                    try:
                        with open(self.inst_cfg, "w") as cfg:
                            json.dump(data, cfg)
                            tk_msgbox.showinfo(title="Saved", message="Current instance was saved successfully.")
                    except:
                        tk_msgbox.showerror(title="Error", message="Unable to modify %s to save current instance!" % (self.inst_cfg))
            except:
                data = {
                    self.inst_name: {
                        "turbo": int(self.turbo_entry.get()),
                        "bsa_port": int(self.bsa_port_entry.get()),
                        "hdp_port": int(self.hdp_port_entry.get())
                        }
                    }
                try:
                    with open(self.inst_cfg, "w") as cfg:
                        json.dump(data, cfg)
                        tk_msgbox.showinfo(title="Saved", message="Current instance was saved successfully.")
                except:
                    tk_msgbox.showerror(title="Error", message="Unable to create %s to save current instance!" % (self.inst_cfg))
        else:
            tk_msgbox.showerror(title="Error", message="Some values are not filled!")


    # Load current instance config into UI entries
    def load_inst(self):
        save_exists = False
        
        try:
            with open(self.inst_cfg, "r") as cfg:
                data = json.load(cfg)
                if self.inst_name in data:
                    self.turbo_entry.delete(0, tk_end)
                    self.turbo_entry.insert(0, data[self.inst_name]["turbo"])
                    self.bsa_port_entry.delete(0, tk_end)
                    self.bsa_port_entry.insert(0, data[self.inst_name]["bsa_port"])
                    self.bsa_port_entry.configure(foreground=self.success_font_fg)
                    self.hdp_port_entry.delete(0, tk_end)
                    self.hdp_port_entry.insert(0, data[self.inst_name]["hdp_port"])
                    self.hdp_port_entry.configure(foreground=self.success_font_fg)
                    save_exists = True
        except:
            if Path(self.inst_cfg).is_file():
                tk_msgbox.showerror(title="Error", message="Unable to read %s for loading the saved instances!" % (self.inst_cfg))
        finally:
            if (not save_exists):
                self.turbo_entry.delete(0, tk_end)
                self.turbo_entry.insert(0, self.def_turbo)
                self.bsa_port_entry.delete(0, tk_end)
                self.bsa_port_entry.insert(0, self.def_bsa_port)
                self.bsa_port_entry.configure(foreground=self.default_font_fg)
                self.hdp_port_entry.delete(0, tk_end)
                self.hdp_port_entry.insert(0, self.def_hdp_port)
                self.hdp_port_entry.configure(foreground=self.default_font_fg)

 
    # Delete current instance from the config (inst.cfg)
    def delete_inst(self):
        if tk_msgbox.askquestion("Delete Current Instance", "Delete current instance from %s?" % (self.inst_cfg), icon="warning") == "yes":
            try:
                with open(self.inst_cfg, "r") as cfg:
                    data = json.load(cfg)
                    if self.inst_name in data:
                        del data[self.inst_name]
                        with open(self.inst_cfg, "w") as cfg:
                            json.dump(data, cfg)
                            tk_msgbox.showinfo(title="Deleted", message="Current instance was deleted successfully.")
                    else:
                        tk_msgbox.showerror(title="Error", message="Current instance does not exist in %s!" % (self.inst_cfg))
            except:
                tk_msgbox.showerror(title="Error", message="Unable to read %s for deleting current instance!" % (self.inst_cfg))

    
    # Delete instances config (inst.cfg)
    def delete_all_inst(self):
        if tk_msgbox.askquestion("Delete All Saved Instances", "Delete all saved instances from %s?" % (self.inst_cfg), icon="warning") == "yes":
            try:
                target = Path(self.inst_cfg)
                if target.is_file():
                    target.unlink()
                    tk_msgbox.showinfo(title="Deleted", message="Instances were deleted successfully.")
                else:
                   tk_msgbox.showerror(title="Error", message="%s does not exist!" % (self.inst_cfg)) 
            except:
                tk_msgbox.showerror(title="Error", message="Unable to delete %s for deleting all saved instances!" % (self.inst_cfg))


    # View current instance info
    def inst_info(self):
        info_win = tk_tlvl()
        info_win.minsize(500, 0)
        info_win.resizable(0, 0)
        
        left_frame = tk_frame(info_win, width=50, background=self.frame_bg)

        info_frame = tk_frame(info_win, background=self.frame_bg)
        info_inst_name_label = tk_label(info_frame, text="Instance Name", foreground=self.label_fg, background=self.label_bg)
        info_inst_name_entry = tk_entry(info_frame, justify="center")
        info_inst_name_entry.insert(tk_end, self.inst_name)
        info_inst_id_label = tk_label(info_frame, text="Instance ID", foreground=self.label_fg, background=self.label_bg)
        info_inst_id_entry = tk_entry(info_frame, justify="center")
        info_inst_id_entry.insert(tk_end, self.inst_id)
        info_inst_gadid_label = tk_label(info_frame, text="Google Ads ID", foreground=self.label_fg, background=self.label_bg)
        info_inst_gadid_entry = tk_entry(info_frame, justify="center")
        info_inst_gadid_entry.insert(tk_end, self.inst_gadid)
        info_inst_aid_label = tk_label(info_frame, text="Android ID", foreground=self.label_fg, background=self.label_bg)
        info_inst_aid_entry = tk_entry(info_frame, justify="center",)
        info_inst_aid_entry.insert(tk_end, self.inst_aid)
        ok_btn = tk_btn(info_frame, text="OK", foreground=self.ok_btn_fg, background=self.ok_btn_bg, command=lambda:self.on_close(info_win))

        right_frame = tk_frame(info_win, width=50, background=self.frame_bg)
        bottom_frame = tk_frame(info_win, height=10, background=self.frame_bg)

        info_win.columnconfigure(1, weight=1)
        info_win.rowconfigure(0, weight=1)

        left_frame.grid(row=0, column=0, sticky="NSWE")

        info_frame.grid(row=0, column=1, sticky="NSWE")
        info_frame.columnconfigure(0, weight=1)
        info_inst_name_label.grid(row=0, column=0)
        info_inst_name_entry.grid(row=1, column=0, sticky="WE")
        info_inst_id_label.grid(row=2, column=0)
        info_inst_id_entry.grid(row=3, column=0, sticky="WE")
        info_inst_gadid_label.grid(row=4, column=0)
        info_inst_gadid_entry.grid(row=5, column=0, sticky="WE")
        info_inst_aid_label.grid(row=6, column=0)
        info_inst_aid_entry.grid(row=7, column=0, sticky="WE")
        ok_btn.grid(row=8, column=0)
        
        right_frame.grid(row=0, column=2, sticky="NSWE")
        bottom_frame.grid(row=1, column=0, columnspan=3, sticky="NSWE")
        
        info_win.protocol("WM_DELETE_WINDOW", lambda:self.on_close(info_win))
        info_win.mainloop()
        


    # Auto-set ports based on BlueStacks' player.log
    def autoset_conn_ports(self):
        # Default ports
        bsa_port = self.def_bsa_port
        hdp_port = self.def_hdp_port
        skip_bsa = False
        skip_hdp = False
        
        # Load from player.log
        logdir = self.get_bsconf("BstkMisc", "logdir")
        if logdir != "":
            playerlog = Path(logdir) / "player.log"
            if playerlog.is_file():
                inst_part = ""
                if self.inst_name != "Android":
                    inst_part = " %s:" % (self.inst_name)
                pattern1 = "\(HD-Player\) INFO:%s Bst Android Port Updated to (\d+)" % (inst_part)
                pattern2 = "\(HD-Player\) INFO:%s Server listening on port (\d+)" % (inst_part)
                try:
                    # Newer BlueStacks version encoded player.log/Player.log with UTF-8
                    f = open(playerlog, "r", encoding="utf-8")
                    data = f.read()
                    f.close()
                    bsa_port = int(re.findall(pattern1, data)[-1])
                    hdp_port = int(re.findall(pattern2, data)[-1])
                except:
                    tk_msgbox.showerror(title="Error", message="Unable to read the required values from player.log! Please restart current instance and try again.")
                    if self.bsa_port_entry.get() != "":
                        skip_bsa = True
                    if self.hdp_port_entry.get() != "":
                        skip_hdp = True
            else:
                tk_msgbox.showerror(title="Error", message="Unable to find player.log! Make sure that the Log Directory is right and current instance was launched once before trying again.")
                
        if (not skip_bsa):
            self.bsa_port_entry.delete(0, tk_end)
            self.bsa_port_entry.insert(0, bsa_port)
            self.bsa_port_entry.configure(foreground=self.success_font_fg)
            
        if (not skip_hdp):
            self.hdp_port_entry.delete(0, tk_end)
            self.hdp_port_entry.insert(0, hdp_port)
            self.hdp_port_entry.configure(foreground=self.success_font_fg)


    # Set-up bsconn module with required fields
    def set_bsconn(self, mode, port, path):
        conn = bsconn.Main()
        conn.h_oem = self.get_bsconf("BstkParams", "x_oem")
        conn.h_email = self.get_bsconf("BstkParams", "x_email")
        conn.h_machineid = self.get_bsconf("BstkParams", "x_machine_id")
        conn.h_vermachineid = self.get_bsconf("BstkParams", "x_version_machine_id")
        conn.h_apitoken = self.get_bsconf("BstkParams", "x_api_token")
        conn.h_vmname = self.inst_name
        conn.h_googleaid = self.inst_gadid
        conn.h_androidid = self.inst_aid
        conn.h_vmid = self.inst_id
        conn.h_useragent = self.get_bsconf("BstkParams", "User-Agent")
        conn.mode = mode
        conn.port = port
        conn.path = path
        return conn


    # Convert the response (JSON text) from BlueStacks to a valid python object
    def json_bsconn(self, resp):
        try:
            json_resp = json.loads(resp)
            # Some of the BlueStacks command will return a list containing JSON Text
            # e.g. [{"A": "B"}] instead of {"A":"B"}
            # Eventhough there is only one json text
            # So we opt on getting the json text from the 1st index
            if type(json_resp) in (tuple, list):
                json_resp = json_resp[0]
            return json_resp
        except:
            return {}


    # Turbo trigger
    def trigger_turbo(self):
        success = False
        
        if self.bsa_port_entry.get() == "":
            tk_msgbox.showerror(title="Error", message="Bs Android Port is empty!")
        elif self.turbo_entry.get() == "":
            tk_msgbox.showerror(title="Error", message="TURBO FPS is empty!")
        else:
            mode = "SET_FPS"
            port = int(self.bsa_port_entry.get())
            fps = int(self.turbo_entry.get())
            path = "/setfpsvalue?fps=%d" % (fps)
            conn = self.set_bsconn(mode, port, path)
            resp = conn.get_response()
            
            if "result" in resp:
                json_resp = self.json_bsconn(resp)
                if json_resp != {}:
                    result = json_resp["result"]
                    if result == "ok":
                        success = True
                        #tk_msgbox.showinfo(title="Success", message="FPS cap was changed successfully.")
                    else:
                        tk_msgbox.showerror(title="Error", message="The command to change the FPS cap was deemed invalid by BlueStacks!")
                else:
                    tk_msgbox.showerror(title="Error", message="Invalid responce received from BlueStacks!")
            else:
                tk_msgbox.showerror(title="Error", message="Unable to contact BlueStacks! Please make sure that the Bs Android port is valid and current instance is running.")
        
        fg = self.turbo_btn_fg
        bg = self.turbo_btn_bg
        
        if success:
            fg = self.success_btn_fg
            bg = self.success_btn_bg
            
        self.turbo_btn.configure(foreground=fg, background=bg)


    # FPS Counter trigger
    def trigger_fps_counter(self, switch_on):
        mode = "SET_SHOWFPSOFF"
        
        if switch_on:
            mode = "SET_SHOWFPSON"
            
        success = False
        
        if self.hdp_port_entry.get() == "":
            tk_msgbox.showerror(title="Error", message="HD-Player Port is empty!")
        else:
            port = int(self.hdp_port_entry.get())
            path = "/showFPS"
            conn = self.set_bsconn(mode, port, path)
            resp = conn.get_response()
            
            if "success" in resp:
                json_resp = self.json_bsconn(resp)
                if json_resp != {}:
                    resp_success = json_resp["success"]
                    if type(resp_success) == bool and resp_success:
                        success = True
                        #tk_msgbox.showinfo(title="Success", message="FPS Counter status was changed successfully.")
                    else:
                        tk_msgbox.showerror(title="Error", message="The command to change the FPS counter was deemed invalid by BlueStacks!")
                else:
                    tk_msgbox.showerror(title="Error", message="Invalid responce received from BlueStacks!")
            else:
                tk_msgbox.showerror(title="Error", message="Unable to contact BlueStacks! Please make sure that the HD-Player port is valid and current instance is running.")
        
        btn = self.fps_counter_on_btn
        fg = self.fps_counter_on_btn_fg
        bg = self.fps_counter_on_btn_bg
        alt_btn = self.fps_counter_off_btn
        alt_fg = self.fps_counter_off_btn_fg
        alt_bg = self.fps_counter_off_btn_bg
        
        if mode == "SET_SHOWFPSOFF":
            # Swap them up
            btn = alt_btn
            fg = alt_fg
            bg = alt_bg
            alt_btn = self.fps_counter_on_btn
            alt_fg = self.fps_counter_on_btn_fg
            alt_bg = self.fps_counter_on_btn_bg
        
        if success:
            fg = self.success_btn_fg
            bg = self.success_btn_bg
            
        btn.configure(foreground=fg, background=bg)
        alt_btn.configure(foreground=alt_fg, background=alt_bg)


    # Validate TK Entry and restrict it to INT only
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

    # Explanation triggered by [?] button
    def what_is_this(self, text):
        tk_msgbox.showinfo(title="What is This?", message=text)
    
    # Handle the On Close event "properly"
    def on_close(self, window):
        window.quit() # Quit the mainloop()
        window.destroy()# Destroy the window             

if __name__ == "__main__":
    main = Main()
