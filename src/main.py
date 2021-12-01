import sys
import os
from typing import Final

CLI_CMDS: list[str] = ["lib", "pro"]

def prompt() -> int:
    pass

def str2path(name: str, *args: str) -> list[str]:
    full_path: list[str] = f"{os.getcwd()}/{name}"

    if not os.access(full_path, os.F_OK):
        return list(map(lambda x: full_path, args))
    else:
        print(f"error! directory/file {name} already exists", file=sys.stderr)
        exit(1)

def parse_cli() -> tuple[str, list[str]]:
    index: int = 0
    name: str = ""
    temp_file: str = ""
    paths: list[str] = ["src/", "test/", "doc/"]

    # check if mkpro has flags
    if sys.argv[index + 1] not in CLI_CMDS:

        # parse mkpro flags
        try:
            while((sys.argv[index + 1] not in CLI_CMDS) or \
                  (sys.argv[index] not in CLI_CMDS)):
                if sys.argv[index] == "-t":
                    index += 1
                    temp_file = sys.argv[index]
                    continue
                else:
                    print(f"error! unknown flag '{sys.argv[index]}' for mkpro", file=sys.stderr)
                    exit(1)
                index += 1
            index += 1
        except IndexError:
            print("error! command not given", file=sys.stderr)
            exit(1)
    else:
        index += 1

    # parse cmd & its flags
    assert len(CLI_CMDS) == 2, "error! possible unhandled command (dev)"
    if sys.argv[index] == "lib":
        print("error! not implemented", file=sys.stderr)
        exit(1)
    elif sys.argv[index] == "pro":
        index += 1
        try:
            name = sys.argv[index]
        except IndexError:
            print("error! command incomplete, project name was not given")
            exit(1)

        while (index := index + 1) < len(sys.argv):
            if sys.argv[index] == "-b":
                paths.append("bin/")
                continue
            elif sys.argv[index] == "-r":
                paths.append("README.md")
            elif sys.argv[index] == "-R":
                try:
                    index += 1
                    if sys.argv[index] in paths:
                        paths.remove(sys.argv[index])
                    else:
                        # NOTE: might want to continue program even if file doesn't exist
                        print("error! default directory to remove does not exist", file=sys.stderr)
                        exit(1)
                except IndexError:
                    print("error! file to be removed was not given", file=sys.stderr)
                    exit(1)
            elif sys.argv[index] == "-n":
                try:
                    index += 1
                    if sys.argv[index] not in paths:
                        paths.append(sys.argv[index])
                    else:
                        # NOTE: might want to continue program even if file already exists
                        print("error! directory to be added already exists", file=sys.stderr)
                        exit(1)
                except IndexError:
                    print("error! file to be added was not given", file=sys.stderr)
                    exit(1)
            else:
                print(f"error! unknown flag '{sys.argv[index]}' for command 'pro'", file=sys.stderr)
                exit(1)

            index += 1

    # pathefy list
    paths = str2path(name, *paths)
    
    return temp_file, paths
                        

def build_path(path: str) -> int:
    pass

def main() -> None:
    n, t, p = parse_cli()
    print(n)
    print(t)
    print(p)

if __name__ == "__main__":
    main()
