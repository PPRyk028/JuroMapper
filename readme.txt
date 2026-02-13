Note:
If you need to run or debug the .py files, please manually replace the placeholder: "=======================Use your own api_key==========================" with your actual API key, and replace: "=======================Use your own base_url==========================" with your actual base URL.




File Descriptions:

readme.txt:
Project overview and introduction.

editor.py:
Provides a Graphical User Interface (GUI) to modify settings, including hotkeys and prompt words. These configurations are stored in slots.json.

launcher.py:
Acts as the launcher for the PythonLaunchedMapper.exe script.
Global Controls: While the launcher is running, press L-Ctrl + L-Alt + L-Shift + O to completely exit the launcher.
Script Control: Press L-Ctrl + L-Alt + L-Shift to launch the AHK script; press R-Ctrl to exit the AHK script.
Mapping Control: While the AHK script is running, press R-Shift to toggle the Mapping Mode on or off.
LLM Integration: By pressing the bound hotkeys (viewable in slots.json or the editor.py GUI), the script automatically combines your prompt prefix with the second item in the Windows clipboard history and sends it to the LLM. The AI's response is then saved to Slot_i.txt.
Dynamic Loading: After an LLM query is completed, the next time the AHK script is launched, it will automatically map the content of the corresponding Slot_i.txt. By default, it maps Slot_1.txt if no queries have been performed.

PythonLaunchedMapper.ahk & PythonLaunchedMapper.exe
Receives parameters set by launcher.py via environment variables.
Exit: Press R-Ctrl to exit the script.
Toggle: Press R-Shift to start or stop Mapping Mode.
Core Logic: It automatically masks left-side function keys and letter keys, simulating physical scan codes to output the content of Slot_i.txt.
Human-like Simulation:
Automatically simulates randomized typing intervals (including pauses after periods, commas, etc.).
Automatically simulates typos (inputting adjacent characters on a physical keyboard) and performs corrections.
Automatically simulates the Shift key to output uppercase letters and special symbols (supports English content only).

Slot_1.txt to Slot_10.txt
Storage locations for the text outputted by the LLM. Slot_1.txt serves as the default output content upon launching the program.

ScriptDetection.html
A self-test webpage used to verify the mapping functionality.

slots.json
The configuration file for custom hotkeys and prompt words.













注意：
如果需要使用/调试py文件，请自行将代码中的： "=======================Use your own api_key==========================" 替换成自己的apikey；
并将： "=======================Use your own base_url==========================" 替换成自己的base_url。




文件介绍：

readme.txt：
项目简介

editor.py：
提供用图形界面修改设置（快捷键与提示词）的功能，设置被存放在 "slots.json" 中。

launcher.py：
它作为PythonLaunchedMapper.exe脚本的启动器。在启动器运行时，如需快捷键彻底退出启动器，按左Ctrl + 左Alt + 左Shift + 字母O；按下左Ctrl + 左Alt + 左Shift以启动ahk脚本；按下右Ctrl以退出ahk脚本。当ahk脚本运行时，按下右Shift来启动与退出映射模式。在启动器运行时，通过绑定的快捷键（可在 "slots.json" 中或editor.py的GUI中查看），可以自动拼接提示词与windows剪贴板第二项的内容，并将LLM的回复写入Slot_i.txt。在每次执行完LLM询问时，下一次启动ahk脚本会自动映射出对应的Slot_i.txt的内容（在未执行任何询问时会默认映射Slot_1.txt中的内容）

PythonLaunchedMapper.ahk 与 PythonLaunchedMapper.exe：
通过环境变量来接受launcher.py设置的参数。按下右Ctrl以退出ahk脚本。当ahk脚本运行时，按下右Shift来启动与退出映射模式。它自动屏蔽左边键盘功能键与字母键输入并模拟按键的物理码来输出Slot_i.txt中的内容。自动模拟随机的真人打字的（句号，逗号等停顿后）间隔。自动模拟打错字（即输出字符在物理键盘上的周边字符）并修正。自动模拟Shift键来输出大写字母与特殊符号（只支持纯英文内容）

Slot_1.txt 至 Slot_10.txt：
LLM输出的文本存放位置。其中Slot_1.txt作为启动器启动后的默认映射输出内容

ScriptDetection.html：
映射的自测网页

slots.json：
自定义快捷键与提示词



--------------------------作者  @蒟蒻茶包   QQ：1591654291-------------------------------
2026/2/13
