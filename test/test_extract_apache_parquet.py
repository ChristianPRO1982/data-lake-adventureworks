from app.extract_apache_parquet import add

def test_add():
    assert add(1,2) == 3
    assert add(0,0) == 0
    assert add(-1,-1) == -2