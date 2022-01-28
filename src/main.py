import sys
import os
from typing import Union, TextIO, Optional
from parsing import parse_temp_file, parse_temp

# Global vars
# TODO: put proper default value in TEMP_FILE
VAL_OPTS: dict[str, str] = {"TEMP_FILE": "c.fmt",
    "EXT": ".py",
    "NAME": ""}

BOOL_OPTS: dict[str, bool] = {"DEBUG": False}

def prompt() -> int:
    pass

def handle_err(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    exit(code)

def handle_prompt_typos(msg: str, opt: str, opt_list: list[str]) -> bool:
    pass

def str2dirs(args: list[str]) -> list[str]:
    global VAL_OPTS
    full_path: str = f"{os.getcwd()}/{VAL_OPTS['NAME']}"
    cat_path = lambda x: f"{full_path}/{x}"

    if os.path.exists(full_path):
        handle_err(f"error! directory `{VAL_OPTS['NAME']}` already exists")
    # the casting of `set` is for the removal of duplicate paths
    # return list(set(map(cat_path, args)))
    return list({os.path.normpath(cat_path(x)) for x in args})

def str2files(args: list[str]) -> list[str]:
    global VAL_OPTS
    full_path: str = f"{os.getcwd()}/{VAL_OPTS['NAME']}"
    cat_path = lambda x: f"{full_path}/{x}{VAL_OPTS['EXT']}" if \
        x.split('/')[0] == "src" \
        else f"{full_path}/{x}"

    if os.path.exists(full_path):
        handle_err(f"error! file {VAL_OPTS['NAME']} already exists")
    # the casting of `set` is for the removal of duplicate paths
    # return list(set(map(cat_path, args)))
    return list({os.path.normpath(cat_path(x)) for x in args})


def build_dir_struct(dir_structure: list[str]) -> None:
    global BOOL_OPTS

    for dir_ in dir_structure:
        if BOOL_OPTS['DEBUG']:
            print(f"[debug] mkdir {dir_}")
        
        try:
            os.makedirs(dir_)
        except FileExistsError:
            # the only way a directory can exist is if it was created already during the
            # recursive directory genoration of makedirs therefor this error can be ignored
            pass
        except:
            handle_err(f"error! unknown issue occured during creation of `{dir_}` directory", 2)

def norm_temp_path(file_name: str) -> str:
    user: str = os.path.expanduser('~')
    temp_dir: str = ".mkpro/templates"
    full_path: str = os.path.join(user, temp_dir, file_name)
    full_path = os.path.normpath(full_path)
    if not os.path.exists(full_path):
        handle_err("error! template file `{file_name}` does not exist in `{temp_dir}`")
    return full_path
        

def create_files(*files: str) -> None:
    global VAL_OPTS
    temp_file: str = norm_temp_path(VAL_OPTS["TEMP_FILE"])
    temp_map: Optional[dict[str, str]] = parse_temp_file(temp_file)
    if not temp_map:
        handle_err("error! failed to parse template file \nrun `mkpro check <file>` to try and find the error")
        if input("would you like files to still be created? (y/[n])").lower() == 'n':
            exit(1)

    for file_ in files:
        opt: str = input(f"format file `{os.path.basename(file_)}`? (y/[n])")
        with open(file_, "w") as f:
            if opt.lower() == 'n':
                continue
            elif opt.lower() in ('', 'y'):
                assert temp_map
                format_file(f, temp_map)

# TODO: remove this function

def format_file(output_file: TextIO, temp_map: dict[str, str]) -> bool:
    temp: str
    parsed_temp: str
    
    print("type template name to add template")
    print("to move on type `end`")
    while (temp:=input("template name> ")) != 'end':
        if temp in temp_map.keys():
            parsed_temp = parse_temp(temp_map[temp])
            output_file.write(parsed_temp)
        else:
            print("unknown template,\nmake sure spelling is correct and that the template is in the template file",
                  file=sys.stderr)
    return True

def parse_cli() -> tuple[list[str], list[str]]:
    index: int = 0
    dirs: list[str] = ["src/", "test/", "doc/"]
    files: list[str] = ["src/main"]
    global VAL_OPTS, BOOL_OPTS
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
        "lib": [],
        "check": []
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
            VAL_OPTS['TEMP_FILE'] = sys.argv[index]
            continue

        elif flag == "-e" and check(index):
            index += 1
            VAL_OPTS['EXT'] = sys.argv[index]
            # NOTE: not a fan of this solution
            if VAL_OPTS['EXT'][0] != '.': handle_err("error! file extentions require a `.` at the beggining")
            continue

        elif flag == "--debug":
            BOOL_OPTS['DEBUG'] = True
            continue

        else:
            if flag not in flags[cmd]:
                handle_err(f"error! unknown flag `{flag}`")
            else:
                handle_err(f"error! no argument given for flag `{flag}`")

    if not check(index): handle_err("error! no command given")

    assert len(cli_cmds) == 3
    index += 1
    cmd = sys.argv[index]
    if cmd == "lib":
        assert len(flags[cmd]) == 0, "exhaustive handling of lib flags"
        handle_err("error! lib command not implemented")
    elif cmd == "check":
        assert len(flags[cmd]) == 0
        index += 1
        if check(index):
            temp_map: Optional[dict[str, str]] = parse_temp_file(sys.argv[index])
            if temp_map:
                print("no errors found in file")
                exit(0)
            else:
                print("")
                print("errors found in file")
        else:
            handle_err("error! check command requires one arguement")
    elif cmd == "pro":
        assert len(flags[cmd]) == 6, "exhaustive handling of pro flags"
        if check(index):
            index += 1
            VAL_OPTS['NAME'] = sys.argv[index]
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
    # m = parse_temp_file(norm_temp_path(VAL_OPTS['TEMP_FILE']))
    # assert m
    # for k,v in m.items():
    #     print(k, ":")
    #     print(v)
    #     print("")
    dirs, files = parse_cli()
    build_dir_struct(dirs)
    create_files(*files)
    # print(VAL_OPTS["NAME"])
    # print(VAL_OPTS["EXT"])
    # print(VAL_OPTS["TEMP_FILE"])

if __name__ == "__main__":
    main()
