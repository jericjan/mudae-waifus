import re
from pathlib import Path
import os

name = input("Enter waifu name: ")
img = input("Enter waifu image url: ")


hugo_str = f"\n{{{{< gallery src=\"{img}\" title=\"{name}\" >}}}}"

accs = ['kur0.md', 'biggus.md', 'lemonika.md']

posts_folder = Path('content/posts/')

for idx, file in enumerate(accs):
    print(f"{idx+1}: {file}")

while True:
    try:
        choice = int(input("Pick an acc number: "))
    except ValueError:
        print("Not a number")
        continue
    if (1 <= choice <= len(accs)):
        choice -= 1
        break
    print("Invalid!")

target_file = posts_folder / accs[choice]

with open(target_file, "a", encoding="utf-8", newline='') as f:
    f.write(hugo_str)

os.system(f"neovide --opengl {str(target_file.absolute())}")

        
