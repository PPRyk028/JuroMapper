import os, sys, json, time, subprocess, keyboard, asyncio
from openai import OpenAI
from winsdk.windows.applicationmodel.datatransfer import Clipboard, StandardDataFormats

ROOT = os.path.dirname(os.path.abspath(__file__)) if not getattr(sys, 'frozen', 0) else os.path.dirname(sys.executable)
CONF_PATH = os.path.join(ROOT, "slots.json")
MAPPER_EXE = os.path.join(ROOT, "PythonLaunchedMapper.exe")

client = OpenAI(
    api_key="=======================Use your own api_key==========================", 
    base_url="=======================Use your own base_url=========================="
)

cur_file = "Slot_1.txt"
last_hit = 0
is_live = True 

async def get_clip_text():
    try:
        res = await Clipboard.get_history_items_async()
        if res.status != 0 or not res.items: return ""
        content = res.items[1].content
        return await content.get_text_async() if content.contains(StandardDataFormats.text) else ""
    except:
        return ""

def on_trigger(sid):
    global cur_file
    if not os.path.exists(CONF_PATH): return
    
    with open(CONF_PATH, 'r', encoding='utf-8') as f:
        conf = json.load(f)
        prefix = next((s["content"] for s in conf.get("slots", []) if s["id"] == sid), "")

    txt = asyncio.run(get_clip_text())
    if not txt: return

    chat = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": f"{prefix}\n\n{txt}"}]
    )
    
    cur_file = f"Slot_{sid}.txt"
    with open(os.path.join(ROOT, cur_file), "w", encoding="utf-8") as f:
        f.write(chat.choices[0].message.content)

def run_mapper():
    global last_hit
    if all(keyboard.is_pressed(k) for k in ['ctrl', 'shift', 'alt']):
        if time.time() - last_hit < 1.2: return 
        if os.path.exists(MAPPER_EXE):
            last_hit = time.time()
            env = dict(os.environ, TARGET_SLOT_FILE=cur_file)
            subprocess.Popen([MAPPER_EXE], env=env)

def main():
    global is_live
    os.chdir(ROOT)
    keyboard.add_hotkey("ctrl+alt+shift+o", lambda: globals().update(is_live=False))
    keyboard.add_hotkey("ctrl+shift+alt", run_mapper)

    if os.path.exists(CONF_PATH):
        with open(CONF_PATH, 'r', encoding='utf-8') as f:
            for s in json.load(f).get("slots", []):
                keyboard.add_hotkey(s["hotkey"].lower(), on_trigger, args=[s["id"]])

    while is_live:
        time.sleep(0.1)
    keyboard.unhook_all()

if __name__ == "__main__":
    main()