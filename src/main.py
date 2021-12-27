import sys
import os
from typing import Final

# Global vars
# TODO: put proper default value in TEMP_FILE
TEMP_FILE: str = "default_val"
EXT: str = ".py"
NAME: str = ""
DEBUG: bool = False

def prompt() -> int:
    pass

def handle_err(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    exit(code)

def str2dirs(args: list[str]) -> list[str]:
    global NAME
    full_path: str = f"{os.getcwd()}/{NAME}"
    cat_path = lambda x: f"{full_path}/{x}"

    if os.path.exists(full_path):
        handle_err(f"error! directory `{NAME}` already exists")
    # the casting of `set` is for the removal of duplicate paths
    # return list(set(map(cat_path, args)))
    return list({os.path.normpath(cat_path(x)) for x in args})

def str2files(args: list[str]) -> list[str]:
    global NAME
    full_path: str = f"{os.getcwd()}/{NAME}"
    cat_path = lambda x: f"{full_path}/{x}{EXT}" if \
        x.split('/')[0] == "src" \
        else f"{full_path}/{x}"

    if os.path.exists(full_path):
        handle_err(f"error! file {NAME} already exists")
    # the casting of `set` is for the removal of duplicate paths
    # return list(set(map(cat_path, args)))
    return list({os.path.normpath(cat_path(x)) for x in args})


def build_dir_struct(dir_structure: list[str]) -> None:
    global DEGUG

    for dir_ in dir_structure:
        if DEBUG:
            print(f"[debug] mkdir {dir_}")
        
        try:
            os.makedirs(dir_)
        except FileExistsError:
            # the only way a directory can exist is if it was created already during the
            # recursive directory genoration of makedirs therefor this error can be ignored
            pass
        except:
            handle_err(f"error! unknown issue occured during creation of `{dir_}` directory", 2)

def parse_temp_file():
    pass

def parse_cli() -> tuple[list[str], list[str]]:
    index: int = 0
    dirs: list[str] = ["src/", "test/", "doc/"]
    files: list[str] = ["src/main"]
    global NAME
    global EXT
    global TEMP_FILE
    global DEBUG
    cli_cmds: list[str] = ["lib", "pro"]
    flags: dict[str, list[str]] = {
        sys.argv[0]: [
            "-t",
            "-e",
            "--debug"
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
    iscmd = lambda x: sys.argv[x] not in cli_cmds
    check = lambda x: x+1 < len(sys.argv)
    dirify = lambda x: f"{x}/"

    cmd = sys.argv[index]
    assert len(flags[cmd]) == 3,  "exhaustive handling of mkpro cmds"
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
            continue

        elif flag == "--debug":
            DEBUG = True
            continue

        else:
            if flag not in flags[cmd]:
                handle_err(f"error! unknown flag `{flag}`")
            else:
                handle_err(f"error! no argument given for flag `{flag}`")

    if not check(index): handle_err("error! no command given")

    assert len(cli_cmds) == 2
    index += 1
    cmd = sys.argv[index]
    if cmd == "lib":
        assert len(flags[cmd]) == 0, "exhaustive handling of lib flags"
        handle_err("error! lib command not implemented")
    elif cmd == "pro":
        assert len(flags[cmd]) == 6, "exhaustive handling of pro flags"
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

    return str2dirs(dirs), str2files(files)



def main() -> None:
    dirs, files = parse_cli()
    build_dir_struct(dirs)
    print(files)
    print(NAME)
    print(EXT)
    print(TEMP_FILE)

if __name__ == "__main__":
    main()
