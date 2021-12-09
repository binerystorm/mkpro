import sys
import os
from typing import Final

# Global vars
CLI_CMDS: list[str] = ["lib", "pro"]
# TODO: put proper default value in TEMP_FILE
TEMP_FILE: str = "default_val"
EXT: str = ".py"
NAME: str = ""

def prompt() -> int:
    pass

def handle_err(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    exit(code)

def str2path(name: str, *args: str) -> list[str]:
    full_path: str = f"{os.getcwd()}/{name}"

    if not os.access(full_path, os.F_OK):
        return list(map(lambda x: full_path, args))
    else:
        print(f"error! directory/file {name} already exists", file=sys.stderr)
        exit(1)

def parse_cli2() -> tuple[list[str], list[str]]:
    index: int = 0
    dirs: list[str] = ["src/", "test/", "doc/"]
    files: list[str] = ["src/main"]
    global NAME
    global EXT
    global TEMP_FILE
    flags: dict[str, list[str]] = {
        # TODO: "main.py" must be "mkpro"
        "main.py": [
            "-t",
            "-e",
        ],
        "pro": [
            "-b",
            "-d",
            "-r",
            "-R",
            "-n",
            "-N"
        ],
        "lib": []
    }
    cmd: str
    flag: str
    # lacal funcs
    iscmd = lambda x: sys.argv[x] not in CLI_CMDS
    check = lambda x: x+1 < len(sys.argv)
    inc = lambda x: x+1
    dirify = lambda x: f"{x}/"

    cmd = sys.argv[index]
    while(check(index) and iscmd(index+1)):
        index += 1
        flag = sys.argv[index]

        if flag == "-t" and check(index):
            index += 1
            TEMP_FILE = sys.argv[index]
            continue

        elif flag == "-e" and check(index):
            index += 1
            EXT = sys.argv[index]
            # NOTE: not a fan of this solution
            if EXT[0] != '.': handle_err("error! file extentions require a `.` at the beggining")

        else:
            if flag not in flags[cmd]:
                handle_err(f"error! unknown flag `{flag}`")
            else:
                handle_err(f"error! no argument given for flag `{flag}`")

    if not check(index): handle_err("error! no command given")

    index += 1
    cmd = sys.argv[index]
    if cmd == "lib":
        handle_err("error! lib command not implemented")
    elif cmd == "pro":
        if check(index):
            index += 1
            NAME = sys.argv[index]
        else:
            handle_err(f"error! command `{cmd}` was not given a name")
        
        while(check(index)):
            dir_: str
            file_: str
            index += 1
            flag = sys.argv[index]

            if flag == "-b":
                dirs.append("bin/")
                continue
            elif flag == "-d":
                files.append("README.md")
                continue
            elif flag == "-r" and check(index):
                index += 1
                dir_ = dirify(sys.argv[index])
                dirs.remove(dir_)
                continue
            elif flag == "-R" and check(index):
                index += 1
                file_ = sys.argv[index]
                files.remove(file_)
                continue
            elif flag == "-n" and check(index):
                index += 1
                dir_ = dirify(sys.argv[index])
                dirs.append(dir_)
                continue
            elif flag == "-N" and check(index):
                index += 1
                file_ = sys.argv[index]
                files.append(file_)
                continue
            else:
                if flag not in flags[cmd]:
                    handle_err(f"error! unknown flag `{flag}`")
                else:
                    handle_err(f"error! argument was not given for flag `{flag}`")

    return dirs, files

                    
# def parse_cli() -> tuple[list[str], list[str]]:
#     index: int = 0
#     name: str = ""
#     dirs: list[str] = ["src/", "test/", "doc/"]
#     files: list[str] = ["src/main."]
# 
#     # check if mkpro has flags
#     try:
#         if sys.argv[index + 1] not in CLI_CMDS:
# 
#             # parse mkpro flags
#                 while((sys.argv[index + 1] not in CLI_CMDS) or \
#                       (sys.argv[index] not in CLI_CMDS)):
#                     if sys.argv[index] == "-t":
#                         index += 1
#                         TEMP_FILE = sys.argv[index]
#                         continue
#                     elif sys.argv[index] == "-e":
#                         index += 1
#                         EXT = sys.argv[index]
#                         continue
#                     else:
#                         print(f"error! unknown flag '{sys.argv[index]}' for mkpro", file=sys.stderr)
#                         exit(1)
#                     index += 1
#                 index += 1
#         else:
#             index += 1
#     except IndexError:
#         print(f"error! command not given or argument for flag {sys.argv[-1]} was not given", file=sys.stderr)
#         exit(1)
# 
#     # parse cmd & its flags
#     assert len(CLI_CMDS) == 2, "error! possible unhandled command (dev)"
#     if sys.argv[index] == "lib":
#         print("error! not implemented", file=sys.stderr)
#         exit(1)
#     elif sys.argv[index] == "pro":
#         index += 1
#         try:
#             name = sys.argv[index]
#         except IndexError:
#             print("error! command incomplete, project name was not given")
#             exit(1)
# 
#         while (index := index + 1) < len(sys.argv):
#             if sys.argv[index] == "-b":
#                 dirs.append("bin/")
#                 continue
#             elif sys.argv[index] == "-d":
#                 files.append("README.md")
#                 continue
#             elif sys.argv[index] in ("-r", "-R"):
#                 try:
#                     index += 1
#                     if (f"{sys.argv[index]}/" in dirs) or \
#                        (sys.argv[index] in files):
#                         if sys.argv[index - 1] == "-r":
#                             print(f"{sys.argv[index]}/")
#                             dirs.remove(f"{sys.argv[index]}/")
#                             continue
#                         else:
#                             files.remove(f"{sys.argv[index]}")
#                             continue
#                             
#                     else:
#                         # NOTE: might want to continue program even if file doesn't exist
#                         print(f"error! default directory/file {sys.argv[index]} to remove does not exist", file=sys.stderr)
#                         exit(1)
#                 except IndexError:
#                     print("error! directory/file to be removed was not given", file=sys.stderr)
#                     exit(1)
#             elif sys.argv[index] in ("-n", "-N"):
#                 try:
#                     index += 1
#                     if (f"{sys.argv[index]}" not in dirs) or \
#                        (sys.argv[index] not in files):
#                         if sys.argv[index - 1] == "-n":
#                             dirs.append(f"{sys.argv[index]}/")
#                             continue
#                         else:
#                             files.append(f"{sys.argv[index]}")
#                             continue
#                     else:
#                         # NOTE: might want to continue program even if file already exists
#                         print("error! directory to be added already exists", file=sys.stderr)
#                         exit(1)
#                 except IndexError:
#                     print("error! file to be added was not given", file=sys.stderr)
#                     exit(1)
#             else:
#                 print(f"error! unknown flag '{sys.argv[index]}' for command 'pro'", file=sys.stderr)
#                 exit(1)
# 
#             index += 1
# 
#     # pathefy list
#     
#     return dirs, files

# def build_path(path: str) -> int:
#     if path[-1] != '/':
#         os.makedirs(path)
#     else:
#         pass
#     return 1

def main() -> None:
    f, d = parse_cli2()
    print(f)
    print(d)
    print(NAME)
    print(EXT)
    print(TEMP_FILE)

if __name__ == "__main__":
    main()
