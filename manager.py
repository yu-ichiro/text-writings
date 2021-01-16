import json
import os
import shutil


if __name__ == "__main__":
    with open("_index.json") as index:
        settings = json.loads(index.read())
    if os.path.exists("tags"):
        shutil.rmtree("tags")
    os.mkdir("tags")
    for tag, items in settings["tags"].items():
        if not os.path.exists(f"tags/{tag}"):
            os.mkdir(f"tags/{tag}")
        for item in items:
            if not os.path.exists(f"tags/{tag}/{item}"):
                os.mkdir(f"tags/{tag}/{item}")

    for data_id, info in settings["data"].items():
        for tag, items in info["tags"].items():
            for item in items:
                os.symlink(f"../../../{info['path']}", f"tags/{tag}/{item}/{data_id}.md")
