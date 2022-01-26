import sys
from typing import Optional, NamedTuple
from enum import Enum, auto
from collections import namedtuple

# Enums
#######

class Type(Enum):
    TITLE = auto()
    TEMP = auto()
    ERR = auto()
    EOF = auto()

# TypeDef's
###########

Tokan = NamedTuple("Tokan", [("value", str), ("type_t", Type)])
OpList = Optional[list[Tokan]]

# Lexer
#######

def lex_temp(content: str, idx: int) -> tuple[Tokan, int]:
    buf: list[str] = []

    while (idx:=idx+1) < len(content):
        if content[idx] == ";":
            if (idx+1) >= len(content):
                return Tokan("", Type.EOF), idx
            elif content[idx+1] == ';':
                idx += 1
                return Tokan("".join(buf), Type.TEMP), idx

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
    return Tokan("".join(buf), Type.EOF), idx

def lex_title(content: str, idx: int) -> tuple[Tokan, int]:
    buf: list[str] = []

    while (idx:=idx+1) < len(content):
        if content[idx] == '-':
            if (idx+1) >= len(content):
                return Tokan("", Type.EOF), idx
            elif content[idx+1] == '-':
                idx += 1
                return Tokan("".join(buf), Type.TITLE), idx
        elif content[idx] in (' ', '\t', '\n'):
            return Tokan(content[idx], Type.ERR), idx
        buf.append(content[idx])

    return Tokan("".join(buf), Type.TITLE), idx

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
                op_list.append(Tokan("", Type.EOF))
            elif content[idx+1] == '-':
                assert isinstance(op_list, list)
                idx += 1
                tokan, idx = lex_title(content, idx)
                op_list.append(tokan)
                continue
            else:
                assert isinstance(op_list, list)
                op_list.append(Tokan(content[idx], Type.ERR))

        elif content[idx] == ":":
            if (idx+1) >= len(content):
                assert isinstance(op_list, list)
                op_list.append(Tokan("", Type.EOF))
            elif content[idx+1] == "\n":
                assert isinstance(op_list, list)
                idx += 1
                tokan, idx = lex_temp(content, idx)
                op_list.append(tokan)
                continue
            else:
                assert isinstance(op_list, list)
                op_list.append(Tokan(content[idx], Type.ERR))
            
        elif content[idx] in (' ', '\t', '\n'):
            continue

        else:
            assert isinstance(op_list, list)
            op_list.append(Tokan(content[idx], Type.ERR))
            
    assert isinstance(op_list, list)
    op_list.append(Tokan("", Type.EOF))

    return op_list

# Parser
########

def handle_unexpected_tokan(tok: Tokan) -> str:
    if tok.type_t == Type.ERR:
        return f"lexer error\nunexpected symbol `{tok.value}`"
    elif tok.type_t == Type.TITLE:
        return "title"
    elif tok.type_t == Type.TEMP:
        return "template"
    elif tok.type_t == Type.EOF:
        return "end of file"
    return "Unknown"

def parse_temp_file(file_name: str) -> Optional[dict[str, str]]:
    key: str
    return_table: dict[str, str] = {}
    op_list: OpList = lex_temp_file(file_name)
    idx: int = 0

    assert op_list
    for tokan in op_list:
        val, tok_type = tokan
        if tok_type == Type.ERR:
            print(f"parser error! {handle_unexpected_tokan(tokan)}", file=sys.stderr)
            return None
        elif tok_type == Type.TITLE:
            if op_list[idx+1].type_t == Type.TEMP:
                key = val
            else:
                print(f"parser error! expected template type, got {handle_unexpected_tokan(op_list[idx+1])}", file=sys.stderr)
                return None
        elif tok_type == Type.TEMP:
            if idx == 0:
                print(f"parser error! expected title got {handle_unexpected_tokan(tokan)}", file=sys.stderr)
                return None
            else:
                return_table[key] = val
                
        idx += 1
    return return_table

                
if __name__ == "__main__":
    data = parse_temp_file("foo.fmt")
    assert data
    for k,v in data.items():
        print(k, ":")
        print(v)
        print("")
