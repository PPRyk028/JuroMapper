#Requires AutoHotkey v2.0
#SingleInstance Force
#NoTrayIcon
#UseHook True
SetWorkingDir A_ScriptDir


envFile := EnvGet("TARGET_SLOT_FILE")
global targetFile := (envFile != "") ? envFile : "Slot_1.txt"
global errorRate := 10
global last_launch_time := 0
global mappingMode := false
global textIndex := 1
global typingState := 0
global pendingChar := ""
global lastChar := ""
global textContent := ""

SetCapsLockState "AlwaysOff"

; Wait for file system release: Prevents AHK from reading before Python finishes writing
if !FileExist(targetFile) {
    Loop 5 { ; Attempt to wait for 0.5 seconds
        if FileExist(targetFile)
            break
        Sleep 100
    }
}

if !FileExist(targetFile) {
    MsgBox "Error: File [" . targetFile . "] not found`nPlease confirm file existence in: " . A_WorkingDir
    ExitApp()
}

try {
    textContent := FileRead(targetFile, "UTF-8")
    textContent := StrReplace(textContent, "`r`n", "`n") 
} catch as e {
    MsgBox "Read failed: " . e.Message
    ExitApp()
}

; keys to be intercepted
global keyList := []
loop 26
    keyList.Push(Chr(A_Index + 96)) 
loop 10
    keyList.Push(Chr(A_Index + 48))

global extraKeys := [",", ".", "/", ";", "[", "]", "-", "=", "``", "'", "\"]
for k in extraKeys
    keyList.Push(k)

global symbolKeys := ["Space", "Enter", "Tab"]

; Hotkey Bindings
Hotkey("RShift", ToggleMappingMode)
Hotkey("RControl", (*) => ExitApp())

for key in keyList
    Hotkey("*" key, HandleMappedKey, "Off")
for key in symbolKeys
    Hotkey("*" key, HandleMappedKey, "Off")





ToggleMappingMode(*) {
    global mappingMode := !mappingMode
    setting := mappingMode ? "On" : "Off"
    
    if (!mappingMode)
        SendEvent "{LShift up}{LCtrl up}{LAlt up}"
    
    ; Toggle interception for standard keys
    for key in keyList
        Hotkey("*" key, setting)
    for key in symbolKeys
        Hotkey("*" key, setting)
    
    ; Invalidate left function keys when mapping is enabled
    Hotkey("*LShift", (*) => "", setting)
    Hotkey("*LCtrl", (*) => "", setting)
    Hotkey("*LAlt", (*) => "", setting)
    
    TrayTip "Mode Switch", mappingMode ? "Mapping Enabled" : "Mapping Disabled", 1
}

HandleMappedKey(ThisHotkey) {
    Critical
    global textIndex, typingState, pendingChar, lastChar, textContent
    
    if (textIndex > StrLen(textContent)) {
        ToggleMappingMode() ; Auto-disable
        return
    }

    targetCh := SubStr(textContent, textIndex, 1)
    pressDur := Random(55, 90) 

    if (typingState == 0) {
        if (IsAlpha(targetCh) && Random(1, 100) <= errorRate) {
            errorChar := GetNeighborKey(StrLower(targetCh))
            errorRaw := GetRawKey(errorChar)
            SimulateKey(errorRaw, errorChar, pressDur)
            
            pendingChar := targetCh
            typingState := 1
        } else {
            PerformNormalInput(targetCh, pressDur)
            textIndex += 1
            lastChar := targetCh
        }
    }
    else if (typingState == 1) {
        SendEvent "{Blind}{BackSpace down}"
        Sleep pressDur
        SendEvent "{Blind}{BackSpace up}"
        typingState := 2
    }
    else if (typingState == 2) {
        PerformNormalInput(pendingChar, pressDur)
        lastChar := pendingChar
        textIndex += 1
        typingState := 0
    }
}

PerformNormalInput(ch, dur) {
    global textIndex, textContent
    needShift := RegExMatch(ch, '[A-Z?!:@#$%^&*()_+{}|<>"]')
    raw := GetRawKey(ch)
    
    Sleep Random(10, 25)

    if (ch = "`n" || ch = "`r") {
        SendEvent "{Blind}{Enter down}"
        Sleep dur
        SendEvent "{Blind}{Enter up}"
    } else if (ch = " " || ch = "　") {
        SendEvent "{Blind}{Space down}"
        Sleep dur
        SendEvent "{Blind}{Space up}"
    } else {
        ; Use virtual Shift state to avoid affecting physically masked LShift
        if (needShift) {
            SendEvent "{LShift down}"
            Sleep Random(25, 55)
            SimulateKey(raw, ch, dur)
            SendEvent "{LShift up}"
        } else {
            SimulateKey(raw, ch, dur)
        }
    }
}

SimulateKey(raw, txt, dur) {
    if (raw != "") {
        SendEvent "{Blind}{" raw " down}"
        Sleep dur
        SendEvent "{Blind}{" raw " up}"
    } else {
        SendEvent "{Blind}{Text}" txt
        Sleep dur
    }
}

GetNeighborKey(char) {
    static neighborMap := Map(
        "q", "wa", "w", "qesa", "e", "wrsd", "r", "etdf", "t", "ryfg", "y", "tugh", "u", "yijh", "i", "uokj", "o", "iplk", "p", "ol",
        "a", "qwsz", "s", "awedxz", "d", "serfcx", "f", "drtgvc", "g", "ftyhbv", "h", "gyujnb", "j", "huikmn", "k", "jiolm", "l", "kop",
        "z", "asx", "x", "zsdc", "c", "xdfv", "v", "cfgb", "b", "vghn", "n", "bhjm", "m", "njk"
    )
    return neighborMap.Has(char) ? SubStr(neighborMap[char], Random(1, StrLen(neighborMap[char])), 1) : "e"
}

GetRawKey(char) {
    if IsLower(char) || IsDigit(char)
        return char
    if IsUpper(char)
        return StrLower(char)
    static keyMap := Map(
        "!", "1", "@", "2", "#", "3", "$", "4", "%", "5", "^", "6", "&", "7", "*", "8", "(", "9", ")", "0", 
        "_", "-", "+", "=", "{", "[", "}", "]", "|", "\", ":", ";", '"', "'", "<", ",", ">", ".", "?", "/",
        " ", "Space", "`n", "Enter", "`t", "Tab"
    )
    return keyMap.Has(char) ? keyMap[char] : ""
}