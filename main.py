#!/usr/bin/env python3
# Copyright (c) 2025 Microsoft Corporation.
# Licensed under the MIT License

"""
Railway deployment launcher for NLWeb
This file runs from the root directory and sets up the proper Python path
"""

import sys
import os
import importlib.util

# Add the code directory to Python path
code_dir = os.path.join(os.path.dirname(__file__), 'code')
sys.path.insert(0, code_dir)

# Change working directory to code/
os.chdir(code_dir)

# Load and run the app-file.py module
spec = importlib.util.spec_from_file_location("app_file", os.path.join(code_dir, "app-file.py"))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

if __name__ == "__main__":
    app_module.main()
