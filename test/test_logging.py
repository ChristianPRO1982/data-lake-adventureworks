import source.logs as logs



def test_init_log():
    result = logs.init_log()
    assert result == True


def test_init():
    result = logs.logging_msg("Test message", "info")
    assert result == True
    result = logs.logging_msg("Test message", "debug")
    assert result == True
    result = logs.logging_msg("Test message", "error")
    assert result == True
    result = logs.logging_msg("Test message", "warning")
    assert result == True