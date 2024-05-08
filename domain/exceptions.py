from .exceptions import DataHandlingException, ParseException

def parse_data(input_data):
    try:
        # Assume parse_logic is a function that might raise an error
        processed_data = parse_logic(input_data)
    except ValueError as e:
        raise ParseException("Failed to parse data", input_data) from e

def handle_data(data):
    try:
        # Assume process_data_logic is a function that might raise an error
        process_data_logic(data)
    except Exception as e:
        raise DataHandlingException("Failed to handle data", errors=e)
