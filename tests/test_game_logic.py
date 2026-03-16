from logic_utils import check_guess, parse_guess

# --- Existing tests (fixed: check_guess returns a tuple, so we unpack outcome) ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

# --- New tests targeting the bugs we fixed ---

def test_too_high_message_says_go_lower():
    # Bug fix: when guess is too high the message should say go LOWER, not HIGHER
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_message_says_go_higher():
    # Bug fix: when guess is too low the message should say go HIGHER, not LOWER
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message

def test_same_guess_always_returns_same_result():
    # Bug fix: same guess should always return the same outcome, not flip between attempts
    result_first = check_guess(47, 50)
    result_second = check_guess(47, 50)
    assert result_first == result_second

def test_check_guess_always_uses_integer_secret():
    # Bug fix: passing secret as string should NOT produce a win for the correct integer guess
    # After fix, we only pass integers so this confirms integer comparison works correctly
    outcome, message = check_guess(47, 47)
    assert outcome == "Win"

# --- Edge case tests ---

def test_decimal_input_is_truncated_to_int():
    # "3.7" should be accepted and silently truncated to 3, not rejected
    ok, value, err = parse_guess("3.7")
    assert ok == True
    assert value == 3
    assert err is None

def test_negative_number_is_accepted_by_parser():
    # "-5" passes parsing successfully — it's a valid integer even if outside game range
    # check_guess will then correctly return "Too Low" since -5 < any secret in 1-100
    ok, value, err = parse_guess("-5")
    assert ok == True
    assert value == -5
    outcome, message = check_guess(-5, 50)
    assert outcome == "Too Low"

def test_extremely_large_number_is_accepted_and_too_high():
    # 999999 parses fine and check_guess correctly returns "Too High"
    ok, value, err = parse_guess("999999")
    assert ok == True
    assert value == 999999
    outcome, message = check_guess(999999, 50)
    assert outcome == "Too High"

def test_whitespace_only_input_is_rejected():
    # Spaces alone should not be accepted as a valid guess
    ok, value, err = parse_guess("   ")
    assert ok == False
    assert err is not None

def test_mixed_text_and_numbers_are_rejected():
    # "12abc" is not a valid number and should return an error
    ok, value, err = parse_guess("12abc")
    assert ok == False
    assert err == "That is not a number."
