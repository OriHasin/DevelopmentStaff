import pytest


def people_on_the_bus(bus_stops_stream):
    total_enter = 0
    total_exit = 0

    for enter, exit in bus_stops_stream:

        total_enter += enter
        total_exit += exit

        # invalid case - incompatible enter-leave ratio in the next bus stop.
        if total_exit > total_enter:
            raise Exception(f'invalid sensor input - total entered to the bus: {total_enter} < total leave the bus: {total_exit}')

    return total_enter - total_exit



# valid unit-tests
def test_bus():
    assert 6 == people_on_the_bus([(1, 0), (2, 0), (3, 0)])
    assert 5 == people_on_the_bus([(1, 0), (2, 1), (3, 0)])
    assert 3 == people_on_the_bus([(1, 0), (2, 0), (3, 3)])
    assert 3 == people_on_the_bus([(1, 0), (2, 1), (3, 2)])


# invalid unit-tests
def test_bus_invalid():
    with pytest.raises(Exception):
        people_on_the_bus([(1, 1), (2, 3), (3, 0)])
        people_on_the_bus([(1, 0), (2, 4), (3, 0)])