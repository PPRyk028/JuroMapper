### File Descriptions:

- readme.txt: Project overview and introduction.
- editor.py: Provides a Graphical User Interface (GUI) to modify settings, including hotkeys and prompt words. These configurations are stored in slots.json.
- launcher.py: Acts as the launcher for the PythonLaunchedMapper.exe script.


### Global Controls

While the launcher is running, press L-Ctrl + L-Alt + L-Shift + O to completely exit the launcher.
- Script Control: Press L-Ctrl + L-Alt + L-Shift to launch the AHK script; press R-Ctrl to exit the AHK script.
- Mapping Control: While the AHK script is running, press R-Shift to toggle the Mapping Mode on or off.
- LLM Integration: By pressing the bound hotkeys (viewable in slots.json or the editor.py GUI), the script automatically combines your prompt prefix with the second item in the Windows clipboard history and sends it to the LLM. The AI's response is then saved to Slot_i.txt.
- Dynamic Loading: After an LLM query is completed, the next time the AHK script is launched, it will automatically map the content of the corresponding Slot_i.txt. By default, it maps Slot_1.txt if no queries have been performed.


### PythonLaunchedMapper.ahk & PythonLaunchedMapper.exe
Receives parameters set by launcher.py via environment variables.
Exit: Press R-Ctrl to exit the script.
Toggle: Press R-Shift to start or stop Mapping Mode.
Core Logic: It automatically masks left-side function keys and letter keys, simulating physical scan codes to output the content of Slot_i.txt.

- Human-like Simulation:
Automatically simulates randomized typing intervals (including pauses after periods, commas, etc.).
Automatically simulates typos (inputting adjacent characters on a physical keyboard) and performs corrections.
Automatically simulates the Shift key to output uppercase letters and special symbols (supports English content only).

- Slot_1.txt to Slot_10.txt
Storage locations for the text outputted by the LLM. Slot_1.txt serves as the default output content upon launching the program.

- ScriptDetection.html
A self-test webpage used to verify the mapping functionality.

- slots.json
The configuration file for custom hotkeys and prompt words.

---

If you need to run or debug the .py files, please manually replace the placeholder: "=======================Use your own api_key==========================" with your actual API key, and replace: "=======================Use your own base_url==========================" with your actual base URL.


