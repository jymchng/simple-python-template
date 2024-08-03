from simple_python_template import CUSTOM_GLOBAL, Custom


def test_default_initialization():
    """Test default initialization of Custom object."""
    obj = Custom()
    assert CUSTOM_GLOBAL == "CUSTOM_GLOBAL"
    assert obj.first == ""
    assert obj.last == ""
    assert obj.number == 0


def test_initialization_with_values():
    """Test initialization with specific values."""
    obj = Custom(first="John", last="Doe", number=42)
    assert obj.first == "John"
    assert obj.last == "Doe"
    assert obj.number == 42


def test_initialization_with_partial_values():
    """Test initialization with partial values."""
    obj = Custom(first="Jane")
    assert obj.first == "Jane"
    assert obj.last == ""
    assert obj.number == 0


def test_name_method():
    """Test the name method returns the correct full name."""
    obj = Custom(first="Alice", last="Smith")
    assert obj.name() == "Alice Smith"


def test_name_method_with_empty_last():
    """Test the name method when last name is empty."""
    obj = Custom(first="Bob", last="")
    assert obj.name() == "Bob "


def test_name_method_with_empty_first():
    """Test the name method when first name is empty."""
    obj = Custom(first="", last="Johnson")
    assert obj.name() == " Johnson"


def test_name_method_with_both_empty():
    """Test the name method when both names are empty."""
    obj = Custom(first="", last="")
    assert obj.name() == " "


def test_number_attribute():
    """Test the number attribute."""
    obj = Custom(number=100)
    assert obj.number == 100


def test_first_attribute_setter():
    """Test setting the first attribute."""
    obj = Custom()
    obj.first = "Charlie"
    assert obj.first == "Charlie"


def test_last_attribute_setter():
    """Test setting the last attribute."""
    obj = Custom()
    obj.last = "Brown"
    assert obj.last == "Brown"


# To run the tests, use the command : pytest test_custom.py
