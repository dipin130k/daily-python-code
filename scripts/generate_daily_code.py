import os
from datetime import datetime
import random

# Make sure folder exists
os.makedirs("daily_code", exist_ok=True)

today = datetime.utcnow().strftime("%Y-%m-%d")
file_path = f"daily_code/{today}.py"

snippets = [
    "print('Hello from your daily Python script!')",
    "print('Coding is fun — keep going!')",
    "for i in range(1, 6): print(f'Square of {i} is {i*i}')",
    "print(sum(range(1, 101)))",
]

code = random.choice(snippets)

with open(file_path, "w") as f:
    f.write(f"# Auto-generated on {today}\n")
    f.write(code + "\n")

# Update README.md log
entry = f"- {today}: Added `{file_path}`\n"
if os.path.exists("README.md"):
    with open("README.md", "a") as readme:
        readme.write(entry)
else:
    with open("README.md", "w") as readme:
        readme.write("# Daily Python Code Log\n\n")
        readme.write(entry)

print(f"Generated {file_path}")
