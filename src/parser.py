import sys
from typing import Optional
from enum import Enum, auto


class Type(Enum):
    TITLE = auto()
    TEMP = auto()
    ERR = auto()
    EOF = auto()

OpList = Optional[list[tuple[str, Type]]]
Tokan = tuple[str, Type]

def lex_temp(content: str, idx: int):
    buf: list[str] = []

    while (idx:=idx+1) < len(content):
        if content[idx] == ";":
            if (idx+1) >= len(content):
                return ("", Type.EOF), idx
            elif content[idx+1] == ';':
                idx += 1
                return ("".join(buf), Type.TEMP), idx

        elif content[idx] == '\\':
            if (idx+2) < len(content):
                if content[idx+1] == ';' and content[idx+2] == ';':
                    idx += 2
                    buf.append(';')
                    buf.append(';')
                    continue
            else:
                continue

        buf.append(content[idx])

def lex_title(content: str, idx: int) -> tuple[Tokan, int]:
    buf: list[str] = []

    while (idx:=idx+1) < len(content):
        if content[idx] == '-':
            if (idx+1) >= len(content):
                return ("", Type.EOF), idx
            elif content[idx+1] == '-':
                idx += 1
                print("title found...", "".join(buf)) # DEBUG
                return (("".join(buf), Type.TITLE), idx)
        elif content[idx] in (' ', '\t', '\n'):
            print("unknown found...", "".join(buf)) # DEBUG
            return ("", Type.ERR), idx
        buf.append(content[idx])

    return (("".join(buf), Type.TITLE), idx)

def lex_temp_file(file_name: str) -> OpList:
    content: str
    tokan: Tokan
    op_list: OpList = []
    idx: int = -1

    with open(file_name, "r") as f:
        content = "".join(f.readlines())

    while (idx:=idx+1) < len(content):
        if content[idx] == '-':
            if (idx+1) >= len(content):
                assert isinstance(op_list, list)
                op_list.append(("", Type.ERR))
                op_list.append(("", Type.EOF))
            elif content[idx+1] == '-':
                assert isinstance(op_list, list)
                idx += 1
                tokan, idx = lex_title(content, idx)
                op_list.append(tokan)
                continue
            else:
                assert isinstance(op_list, list)
                op_list.append(("", Type.ERR))

        elif content[idx] == ":":
            if (idx+1) >= len(content):
                assert isinstance(op_list, list)
                op_list.append(("", Type.ERR))
                op_list.append(("", Type.EOF))
            elif content[idx+1] == "\n":
                assert isinstance(op_list, list)
                idx += 1
                tokan, idx = lex_temp(content, idx)
                op_list.append(tokan)
                continue
            else:
                assert isinstance(op_list, list)
                op_list.append(("", Type.ERR))
            
        elif content[idx] in (' ', '\t', '\n'):
            continue

        else:
            assert isinstance(op_list, list)
            op_list.append((content[idx], Type.ERR))
            
    assert isinstance(op_list, list)
    op_list.append(("", Type.EOF))

    return op_list

def parse_temp_file(file_name: str) -> Optional[dict[str, str]]:
    pass

                
if __name__ == "__main__":
    data: OpList = lex_temp_file("foo.fmt")
    assert data
    for v,t in data:
        print(t, ":")
        print(v)
        print("")
