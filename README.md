BsTrigger 1.1.0
========================================

A simple Python scripts / app to trigger BlueStacks':

1. FPS Uncap

2. FPS Counter

BsTrigger was build and tested with Python 3.7.7 .


Changelog
========================================

1. Changed: bs.cfg: BstkParams, BstkMisc -> BsParams, BsMisc.

2. Changed: BlueStacks Parameters: Log Directory Selector -> Player.log Selector.

3. Added: BlueStacks Parameters: Proper display and check on required parameters.

4. Added: BlueStacks Parameters: BlueStacks' Executable Selector, BlueStack Port, Run BlueStacks As Administrator, and Max. Run Checks. Required for (5).

5. Added: BlueStacks Booter: Boot specific BlueStacks' instance, apply BsTrigger's triggers (^^), and launch specific app.

6. Changed: Some functions / variables names and codes to accommodate the new features.

7. Fixed: turbo_entry's font color does not change to green when the saved turbo was loaded from inst.cfg . 

P/S:
Please delete bs.cfg and generate a new one using the built-in BlueStacks Parameters window.


How to "Install"
========================================

There are 2 options:

1. Install Python 3.7.x (https://www.python.org/downloads/), extract "BsTrigger" (bstrigger_1_1_0_src.zip) directory and open BsTrigger.py .

2. Extract "BsTrigger" (bstrigger_1_1_0_win_x86_exec.zip or bstrigger_1_1_0_win_x86_exec_noconsole.zip or the x86_64 counterparts) directory and open BsTrigger.exe . No Python installation required.

Note:

Option 2: For Windows OS < Windows 10, you might need to install VCRedist 2015 x86 / x64 (https://www.microsoft.com/download/details.aspx?id=48145) first.
As outlined here: https://pyinstaller.readthedocs.io/en/stable/usage.html#windows


1st Time Use
========================================

1. BlueStacks Parameters window: You need to import Installer_XXXX.log (XXXX = BlueStacks version number e.g. 4.150.10.6302) or BlueStacksUsers.log to get some of the required parameters.

2. The required parameters are as follow: (* denote the ones that can not be generated by (1) )

	- VM Data Directory: BlueStacks Installation Directory\Engine (e.g. C:\Program Data\BlueStacks\Engine).

	- Player log: BlueStacks Installation Directory\Logs\Player.log (e.g. C:\Program Data\BlueStacks\Logs\Player.log).

	- BlueStacks' Executable: BlueStacks Installation Directory\Client\BlueStacks.exe (e.g. C:\Program Data\BlueStacks\Client\BlueStacks.exe).

	- BlueStacks Port*: The default value is 2871 (Can be auto-generated from BlueStacksUI.log).

	- Max. Run Checks*: The default Value is 30.

	- API Token

3. All *.log files can be found in the directory where Player.log exists.


How to "Uninstall"
========================================

Just delete the extracted directory.
All files that were generated by BsTrigger are in the directory.


Additional Notes
========================================

1. FPS Uncap (AKA TURBO):

	- If you set it to at least double of the FPS set in BlueStacks Settings, some apps / games might double their FPS cap e.g. from 30 to 60 FPS.
	- Tested on Love Live! School Idol Festival: All Stars which has ~30 FPS cap in the menu.
	- You can replicate this without BsTrigger by:
		- Set the BlueStacks FPS to "A" FPS (e.g. 60 FPS) > Close BlueStacks.
		- Open BlueStacks > Settings > Engine > Enable High Frame Rate > Set the new FPS to at least double of "A" FPS (e.g. 120 FPS).
		- Open the targeted app / game.
	- The effect will be lost once BlueStacks is closed. The steps need to be repeated to regain the effect.
	- The FPS cap set by BsTrigger will not change the FPS set in BlueStacks Settings. It will only execute the function to trigger the cap change.

	WARNING:
	If you DISABLE Vertical SYNC (VSYNC) for BlueStacks in your Graphic Card's Control Panel, the BlueStacks FPS cap will be the same as TURBO FPS.
	Enable VSync or use FPS Limiter (Built-in inside Graphic Card's Control Panel or 3rd-party tools such as RivaTuner Statistics Server).
	And cap it to your monitor's refresh rate so that screen tearing / overheating can be prevented.

2. FPS Counter:

	Similar to FPS Uncap, this will not change the FPS counter set in BlueStacks Settings. It will only trigger the function for FPS counter display.

3. BlueStacks Booter:

	- You can boot specific BlueStacks instance and use arguments to enable BsTrigger features. The arguments must target BsTrigger.py / BsTrigger.exe.
	- To do this, create a new shortcut or edit an existing shorcut generated by BlueStacks.
	- Then, put the mouse cursor on the shortcut and right-click > Properties.
	- Change the "Target" to path_to_BsTrigger_py_or_exe (e.g. C:\BsTrigger\BsTrigger.py).
	- You can put the arguments after BsTrigger.py / BsTrigger.exe .
	- The arguments are:
		- -instance [instance name] (e.g. -instance Android_1) (default: Android).
		- -turbo [Turbo FPS value] (e.g. -turbo 120) (default: None).
		- -showfps (FPS Counter) (default: False)
		- -app [package name] (e.g. -app com.google.search) (default: None)
		- -silent (close BsTrigger once finished) (default: False)
	- You can get the app's package name by looking at the "id" value of the app's Play Store URL (e.g. https://play.google.com/store/apps/details?id=com.klab.lovelive.allstars.global)
	- If no argument is provided or there is an error during boot, BsTrigger will start normally.
	- If at least one argument is provided, BsTrigger will assign default values to the rest of the arguments that are not provided, and will try to boot the instance.
	- An example of the "Target" field with all of the arguments: C:\BsTrigger\BsTrigger.py -instance Android -turbo 120 -showfps -app com.klab.lovelive.allstars.global -silent
	- After filling the "Target" field, proceed to fill the "Start in" field with path_to_directory_where_BsTrigger_py_or_exe_exists (e.g. C:\BsTrigger).
	- If you want to change the shorcut's icon, all apps' icon that were installed in BlueStacks can be found in BlueStacks Installation Directory\Engine\UserData\Gadget (e.g. C:\Program Data\BlueStacks\Engine\UserData\Gadget).

4. bs.cfg:

	A JSON-formatted file generated by BsTrigger to save the required BlueStacks Parameters.

5. inst.cfg:

	A JSON-formatted file generated by BsTrigger to save instance-specific options (Turbo FPS, Bs Android Port and HD-Player Port).

6. BlueStacks Variants (MSI App Player etc.):

	BsTrigger was tested on MSI App Player (4.150.10.6302) and BlueStacks (4.180.10.1006). Might or might not work on other variants.

7. To BlueStacks Devs:
	
	Maybe the "trigger" for these features can be placed somewhere in the "MENU" where "PIN TO TOP" and "STREAMING MODE" are now?


Extra tools used
========================================

1. PyInstaller (http://www.pyinstaller.org/)

2. mitmproxy (https://mitmproxy.org/)

