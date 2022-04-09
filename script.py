import sys
import os
import shutil
from jsmin import jsmin

is_release = False

def minifie(src, dest):
    if is_release:
        with open(src) as input:
            minified = jsmin(input.read())
            output = open(dest, 'w+')
            output.write(minified)
            output.close()
    else:
        shutil.copy2(src, dest)

def main():
    global is_release

    if len(sys.argv) == 2:
        if sys.argv[1] == "release":
            is_release = True
        elif sys.argv[1] == "test":
            os.system("cargo test && wasm-pack test --node")
            return

    if not os.path.exists("build"):
        os.makedirs("build")

    os.system("wasm-pack build --no-typescript --target no-modules " +
              ("--release" if is_release else ""))
    shutil.copy2("pkg/roguelike_bg.wasm", "build/roguelike_bg.wasm")
    minifie("pkg/roguelike.js", "build/roguelike.js")

    shutil.copy2("index.html", "build/index.html")


if __name__ == "__main__":
    main()