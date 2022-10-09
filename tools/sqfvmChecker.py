import os
import sys
import subprocess
import concurrent.futures

addon_base_path = os.path.dirname(os.getcwd())

files_to_ignore_lower = [
    x.lower() for x in ["initSettings.sqf", "initKeybinds.sqf", "XEH_PREP.sqf"]
]
sqfvm_exe = os.path.join(addon_base_path, "sqfvm.exe" if sys.platform == 'win32' else "sqfvm")
virtual_paths = [
    # would need to add more even more to /include to use it
    "{}|/x/cba".format(os.path.join(addon_base_path, 'include', 'x', 'cba')),
    "{}|/z/ace".format(os.path.join(addon_base_path, 'include', 'z', 'ace')),
    "{}|/x/tun".format(addon_base_path),
]


def get_files_to_process(basePath):
    arma_files = []
    for root, _dirs, files in os.walk(os.path.join(addon_base_path, "addons")):
        for file in files:
            if file.endswith(".sqf") or file == "config.cpp":
                if file.lower() in files_to_ignore_lower:
                    continue
                filePath = os.path.join(root, file)
                arma_files.append(filePath)
    return arma_files


def process_file(filePath, skipA3Warnings=True):
    with open(filePath, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
        if content.startswith("//pragma SKIP_COMPILE"):
            return False
    cmd = [sqfvm_exe, "--input", filePath, "--parse-only", "--automated"]
    for v in virtual_paths:
        cmd.append("-v")
        cmd.append(v)
    # cmd.append("-V")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    try:
        ret = proc.wait(12)  # max wait - seconds
    except Exception as _e:
        print("sqfvm timed out: {}".format(filePath))
        return True
    # print("{} = {}".format(filePath, ret))

    fileHasError = False
    keepReadingLines = True
    while keepReadingLines:
        line = proc.stdout.readline()
        if not line:
            keepReadingLines = False
        else:
            line = line.rstrip()
            if line.startswith("[ERR]"):
                fileHasError = True
            if not (
                skipA3Warnings
                and line.startswith("[WRN]")
                and ("a3/" in line)
                and (("Unexpected IFDEF" in line) or ("defined twice" in line))
            ):
                print("  {}".format(line))
    return fileHasError


def main():
    if not os.path.isfile(sqfvm_exe):
        print("Error: sqfvm.exe not found in base folder [{}]".format(sqfvm_exe))
        return 1

    error_count = 0
    arma_files = get_files_to_process(addon_base_path)
    print("Checking {} files".format(len(arma_files)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        for fileError in executor.map(process_file, arma_files):
            if fileError:
                error_count += 1

    print("Errors: {}".format(error_count))
    return error_count


if __name__ == "__main__":
    sys.exit(main())
