from fifa_country_codes import codes_to_names


def test_some_codes():
    assert ('SWE', 'Sweden') in codes_to_names
    assert ('ENG', 'England') in codes_to_names
