import sys
import os
from typing import Final

# Global vars
# TODO: put proper default value in TEMP_FILE
TEMP_FILE: str = "default_val"
EXT: str = ".py"
NAME: str = ""

def prompt() -> int:
    pass

def handle_err(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    exit(code)

def str2dirs(*args: str) -> list[str]:
    global NAME
    full_path: str = f"{os.getcwd()}/{NAME}/"

    if not os.access(full_path, os.F_OK):
        return list(map(lambda x: full_path + x, args))
    else:
        print(f"error! directory/file {NAME} already exists", file=sys.stderr)
        exit(1)

def str2files(*args: str) -> list[str]:
    global NAME
    full_path: str = f"{os.getcwd()}/{NAME}/"

    if not os.access(full_path, os.F_OK):
        return \
            list(
              map(
                lambda x: full_path + x + EXT if x.split('/')[0] == "src" else full_path + x,
                args
              )
            )
    else:
        print(f"error! file {NAME} already exists", file=sys.stderr)
        exit(1)

def parse_temp_file():
    pass

def parse_cli() -> tuple[list[str], list[str]]:
    index: int = 0
    dirs: list[str] = ["src/", "test/", "doc/"]
    files: list[str] = ["src/main"]
    global NAME
    global EXT
    global TEMP_FILE
    cli_cmds: list[str] = ["lib", "pro"]
    flags: dict[str, list[str]] = {
        sys.argv[0]: [
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
    iscmd = lambda x: sys.argv[x] not in cli_cmds
    check = lambda x: x+1 < len(sys.argv)
    dirify = lambda x: f"{x}/"

    cmd = sys.argv[index]
    assert len(flags[cmd]) == 2,  "exhaustive handling of mkpro cmds"
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

    return str2dirs(*dirs), str2files(*files)

                    

# def build_path(path: str) -> int:
#     if path[-1] != '/':
#         os.makedirs(path)
#     else:
#         pass
#     return 1

def main() -> None:
    f, d = parse_cli()
    print(f)
    print(d)
    print(NAME)
    print(EXT)
    print(TEMP_FILE)

if __name__ == "__main__":
    main()
