#!/usr/bin/env python3
# Copyright (c) 2025 Microsoft Corporation.
# Licensed under the MIT License

"""
Railway deployment launcher for NLWeb
This file runs from the code directory
"""

import sys
import os
import importlib.util

# We're already in the code directory, just load the app-file.py module
spec = importlib.util.spec_from_file_location("app_file", "app-file.py")
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

if __name__ == "__main__":
    app_module.main()
