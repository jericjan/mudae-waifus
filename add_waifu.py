import os
import re
import subprocess
import webbrowser
from typing import Any

import pyperclip  # type: ignore
from InquirerPy.base.control import Choice
from InquirerPy.resolver import prompt
from pathlib import Path

def do_popen(coms: list[str]):
    return subprocess.Popen(coms, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def open_url(url: str):
    webbrowser.register(
        "chrome",
        None,
        webbrowser.BackgroundBrowser(
            "C://Program Files (x86)//Google//Chrome//Application//chrome.exe"
        ),
    )
    webbrowser.get("chrome").open(url)


def select_options(msg: str, choices: list[Any], type: str = "list", default: str = ""):
    return {
        "type": type,
        "message": msg,
        "choices": choices,
        "default": default,
        "max_height": "70%",
    }


hugo_proc = do_popen(["hugo", "serve", "--quiet"])

while True:
    name = input("Enter waifu name: ")
    img = input("Enter waifu image url: ")


    accs = ["kur0", "biggus", "lemonika"]

    questions = [select_options("Select acc:", accs)]

    selected_acc: str = prompt(questions=questions)[0]  # type: ignore

    open_url(f"http://localhost:1313/posts/{selected_acc}/")

    name_reg = re.compile(r"title=\"(.+?)(?:\||\")")

    with open(Path("content/posts/") / f"{selected_acc}.md", encoding="utf-8") as f:
        txt = f.readlines()

    all_names = name_reg.findall("".join(txt))

    questions = [
        select_options("Select waifu to place before/after:", all_names, "fuzzy"),
        select_options(
            "Select direction to insert in:",
            [Choice(value=0, name="above"), Choice(value=1, name="below")],
            default="above",
        ),
    ]
    result = prompt(questions=questions)

    target = result[0]
    offset: int = result[1]  # type: ignore

    hugo_str = f'{{{{< gallery src="{img}" title="{name}" >}}}}\n'

    for line_no, line in enumerate(txt):
        match = name_reg.search(line)
        if match:
            if match.group(1) == target:
                txt.insert(line_no + offset, hugo_str)
                break

    if offset == 0:  # Above
        smp = f"$smp {name} $ {target}"
    else:  # Below
        smp = f"$smp {target} $ {name}"

    with open(Path("content/posts/") / f"{selected_acc}.md", "w", encoding="utf-8", newline="") as f:
        f.write("".join(txt))

    pyperclip.copy(smp)  # type: ignore
    print(f"Your $smp command is: {smp}\nIt has been copied to the clipboard.\n")

    questions = [
            select_options("Select an option:", ["Build static site", "Add another waifu"]),
    ]
    result = prompt(questions=questions)[0]

    if result == "Build static site":
        break


hugo_proc.kill()

os.system("hugo")

os.system("git status")

questions = [
    select_options("Do you also want to commit and push?", ['yes', 'no']),
]
result = prompt(questions=questions)[0]

if result == "yes":
    os.system("git commit -m '.'")
    os.system("git push origin main")
