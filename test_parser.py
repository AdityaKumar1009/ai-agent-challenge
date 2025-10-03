#!/usr/bin/env python3
"""
Test script for the bank statement parsers using pytest
"""

import pandas as pd
import sys
import importlib.util
from pathlib import Path
import pytest

def test_icici_parser():
    """Test the ICICI parser functionality"""
    
    # Paths
    parser_path = "custom_parser/icici_parser.py"
    pdf_path = "data/icici/icici_sample.pdf"
    csv_path = "data/icici/icici_sample.csv"
    
    # Check if files exist
    assert Path(parser_path).exists(), f"Parser file not found: {parser_path}"
    assert Path(pdf_path).exists(), f"PDF file not found: {pdf_path}"
    assert Path(csv_path).exists(), f"CSV file not found: {csv_path}"
    
    # Load expected output
    expected_df = pd.read_csv(csv_path)
    
    # Dynamically import the parser
    spec = importlib.util.spec_from_file_location("custom_parser", parser_path)
    parser_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parser_module)
    
    # Run the parse function
    actual_df = parser_module.parse(pdf_path)
    
    # Test assertions
    assert isinstance(actual_df, pd.DataFrame), f"Expected DataFrame, got {type(actual_df)}"
    assert list(actual_df.columns) == list(expected_df.columns), f"Column mismatch: expected {list(expected_df.columns)}, got {list(actual_df.columns)}"
    assert actual_df.shape == expected_df.shape, f"Shape mismatch: expected {expected_df.shape}, got {actual_df.shape}"
    
    # Check data types
    for col in expected_df.columns:
        assert actual_df[col].dtype == expected_df[col].dtype, f"Data type mismatch for column {col}: expected {expected_df[col].dtype}, got {actual_df[col].dtype}"
    
    # CRITICAL: Use DataFrame.equals as specified in requirements
    assert expected_df.equals(actual_df), "Parser output does not match expected CSV via DataFrame.equals"

def test_parser_contract():
    """Test that parser follows the required contract: parse(pdf_path) -> pd.DataFrame"""
    parser_path = "custom_parser/icici_parser.py"
    
    # Import parser
    spec = importlib.util.spec_from_file_location("custom_parser", parser_path)
    parser_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parser_module)
    
    # Check function exists
    assert hasattr(parser_module, 'parse'), "Parser module must have a 'parse' function"
    
    # Check function signature
    import inspect
    sig = inspect.signature(parser_module.parse)
    assert len(sig.parameters) == 1, "parse() function must take exactly one parameter"
    
    param_name = list(sig.parameters.keys())[0]
    assert 'pdf' in param_name.lower() or 'path' in param_name.lower(), "Parameter should be pdf_path or similar"

if __name__ == "__main__":
    # Run tests manually if not using pytest
    try:
        test_icici_parser()
        test_parser_contract()
        print("✅ All tests passed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
