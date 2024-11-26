import source.extract_SQLserver as extract_SQLserver



def test_init():
    result = extract_SQLserver.init()
    assert result == True

def test_connect():
    result = extract_SQLserver.connect()
    assert result != None