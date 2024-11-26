import source.logging as logging



def test_init_log():
    result = logging.init_log()
    assert result == True


def test_init():
    result = logging.logging_msg("Test message", "info")
    assert result == True
    result = logging.logging_msg("Test message", "debug")
    assert result == True
    result = logging.logging_msg("Test message", "error")
    assert result == True
    result = logging.logging_msg("Test message", "warning")
    assert result == True