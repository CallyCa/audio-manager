#!/usr/bin/env python3

import sys
from os.path import abspath, dirname

# Add the parent directory to sys.path
sys.path.append(abspath(dirname(abspath(__file__)) + '/../'))

from audio_manager.manager import main

def run_main():
    """
    Run the main function of the audio manager script, handling unexpected errors.
    """
    try:
        main()
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_main()
