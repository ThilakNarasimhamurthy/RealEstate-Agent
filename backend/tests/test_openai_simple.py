#!/usr/bin/env python3
"""
Simple test to check OpenAI client initialization.
"""

import os
from dotenv import load_dotenv
load_dotenv()

import openai
from openai import OpenAI

print(f"OpenAI API Key configured: {bool(os.getenv('OPENAI_API_KEY'))}")

try:
    # Try different initialization methods
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        print("✅ OpenAI client created with api_key parameter")
    except Exception as e:
        print(f"❌ OpenAI client with api_key failed: {e}")
        try:
            client = OpenAI()
            print("✅ OpenAI client created without parameters")
        except Exception as e2:
            print(f"❌ OpenAI client without parameters failed: {e2}")
except ImportError as e:
    print(f"❌ OpenAI import failed: {e}")

print(f"OpenAI version: {openai.__version__}") 