import pytest
from complex_math import eval_infix


class TestEvalInfix:
    """Comprehensive tests for the eval_infix function."""
    
    def test_simple_addition(self):
        """Test simple addition."""
        assert eval_infix("1 + 2") == 3.0
        assert eval_infix("10 + 5") == 15.0
        assert eval_infix("0 + 0") == 0.0
    
    def test_simple_subtraction(self):
        """Test simple subtraction."""
        assert eval_infix("5 - 3") == 2.0
        assert eval_infix("10 - 15") == -5.0
        assert eval_infix("0 - 5") == -5.0
    
    def test_simple_multiplication(self):
        """Test simple multiplication."""
        assert eval_infix("3 * 4") == 12.0
        assert eval_infix("2 * 0") == 0.0
        assert eval_infix("7 * 1") == 7.0
    
    def test_simple_division(self):
        """Test simple division."""
        assert eval_infix("8 / 2") == 4.0
        assert eval_infix("15 / 3") == 5.0
        assert eval_infix("1 / 2") == 0.5
    
    def test_division_by_zero(self):
        """Test division by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            eval_infix("5 / 0")
    
    def test_operator_precedence(self):
        """Test operator precedence (multiplication/division before addition/subtraction)."""
        assert eval_infix("2 + 3 * 4") == 14.0  # 2 + (3 * 4) = 2 + 12 = 14
        assert eval_infix("10 - 6 / 2") == 7.0  # 10 - (6 / 2) = 10 - 3 = 7
        assert eval_infix("2 * 3 + 4") == 10.0  # (2 * 3) + 4 = 6 + 4 = 10
        assert eval_infix("20 / 4 - 1") == 4.0  # (20 / 4) - 1 = 5 - 1 = 4
    
    def test_parentheses(self):
        """Test parentheses override operator precedence."""
        assert eval_infix("(2 + 3) * 4") == 20.0  # (2 + 3) * 4 = 5 * 4 = 20
        assert eval_infix("2 * (3 + 4)") == 14.0  # 2 * (3 + 4) = 2 * 7 = 14
        assert eval_infix("(10 - 6) / 2") == 2.0  # (10 - 6) / 2 = 4 / 2 = 2
    
    def test_nested_parentheses(self):
        """Test nested parentheses."""
        assert eval_infix("((2 + 3) * 4)") == 20.0
        assert eval_infix("2 * ((3 + 1) / 2)") == 4.0  # 2 * ((3 + 1) / 2) = 2 * (4 / 2) = 2 * 2 = 4
    
    def test_complex_expressions(self):
        """Test complex expressions combining all operations."""
        assert eval_infix("1 + 2 * (3 - 4 / 2)") == 3.0  # 1 + 2 * (3 - 2) = 1 + 2 * 1 = 3
        assert eval_infix("(1 + 2) * 3 - 4 / 2") == 7.0  # (1 + 2) * 3 - 4 / 2 = 3 * 3 - 2 = 9 - 2 = 7
    
    def test_decimal_numbers(self):
        """Test expressions with decimal numbers."""
        assert eval_infix("1.5 + 2.5") == 4.0
        assert eval_infix("3.14 * 2") == 6.28
        assert eval_infix("10.5 / 2.1") == 5.0
    
    def test_whitespace_handling(self):
        """Test that whitespace is handled correctly."""
        assert eval_infix("1+2") == 3.0
        assert eval_infix(" 1 + 2 ") == 3.0
        assert eval_infix("1  +  2") == 3.0
    
    def test_single_number(self):
        """Test single number expressions."""
        assert eval_infix("42") == 42.0
        assert eval_infix("3.14") == 3.14
        assert eval_infix("0") == 0.0
    
    def test_empty_expression(self):
        """Test empty expression returns 0."""
        assert eval_infix("") == 0.0
    
    def test_invalid_characters(self):
        """Test that invalid characters raise SyntaxError."""
        with pytest.raises(SyntaxError):
            eval_infix("1 + a")
        with pytest.raises(SyntaxError):
            eval_infix("1 @ 2")