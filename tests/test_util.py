from mktools_client.util import sixdigit2sec, format_6digit

def test_sixdifit2sec():
    assert sixdigit2sec("123456") ==  83.456
    assert sixdigit2sec("143456") ==  103.456
    assert sixdigit2sec("024566") ==  24.566

def test_format_6digit():
    assert format_6digit("123456") ==  "1'23\"456"
