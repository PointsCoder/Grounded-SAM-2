#!/usr/bin/env python3
"""
Script to build SAM-2 CUDA extension only.
This script will trigger the CUDA build and ignore other install steps.
"""
import os
import sys
from setuptools import setup
from setuptools.command.build_ext import build_ext

# Ensure environment variables are set to build CUDA and allow errors if needed
os.environ["SAM2_BUILD_CUDA"] = "1"
os.environ["SAM2_BUILD_ALLOW_ERRORS"] = "1"

# Import the setup.py functions
import importlib.util

setup_path = os.path.join(os.path.dirname(__file__), "setup.py")
spec = importlib.util.spec_from_file_location("sam2_setup", setup_path)
sam2_setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sam2_setup)

# Trigger build_ext
build_cmd = sam2_setup.BuildExtensionIgnoreErrors if hasattr(sam2_setup, "BuildExtensionIgnoreErrors") else sam2_setup.BuildExtension
ext_modules = sam2_setup.get_extensions() if hasattr(sam2_setup, "get_extensions") else []

setup(
    name="SAM-2-CUDA-Build",
    version="1.0",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_cmd.with_options(no_python_abi_suffix=True)},
)
