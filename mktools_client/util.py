def sixdigit2sec(txt):
    m = int(txt[0])
    s = int(txt[1:3])
    f = int(txt[3:])
    return m * 60 + s + f / 1000

def format_6digit(txt):
    if txt is None:
        return None
    m = txt[0]
    s = txt[1:3]
    f = txt[3:]
    return f"{m}'{s}\"{f}"
