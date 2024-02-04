#!/usr/bin/env python3
import os
import subprocess
import time
from functools import wraps
from dotenv import load_dotenv
import sys
from os.path import abspath, dirname

# Add parent directory to sys.path
sys.path.append(abspath(dirname(abspath(__file__)) + '/../'))

from utils.network_utils import NetworkUtils

# Load environment variables from the .env file
load_dotenv()

def measure_execution_time(func):
    """
    Decorator to measure the execution time of a method.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} executed in {execution_time:.4f} seconds.")
        return result
    return wrapper

class PulseAudioManager:
    def __init__(self, server_ip):
        """
        Initializes the PulseAudio audio manager.

        Parameters:
        - server_ip (str): The IP address of the PulseAudio server.
        """
        self.server_ip = server_ip
        self.source_module = None
        self.sink_module = None

    @measure_execution_time
    def load_audio_modules(self):
        """
        Loads the source and sink tunnel audio modules.
        """
        self.source_module = self._load_module("module-tunnel-source", f"server={self.server_ip} source_name=remote_source channels=2")
        self.sink_module = self._load_module("module-tunnel-sink", f"server={self.server_ip}")

    @measure_execution_time
    def unload_audio_modules(self):
        """
        Unloads the source and sink tunnel audio modules.
        """
        if self.source_module is not None:
            self._unload_module(self.source_module)

        if self.sink_module is not None:
            self._unload_module(self.sink_module)

    def _load_module(self, module_type, options):
        """
        Loads a specific audio module.

        Parameters:
        - module_type (str): The type of module to load.
        - options (str): The options for the module.

        Returns:
        - module_id (str): The ID of the loaded module.
        """
        result = subprocess.run(["pactl", "load-module", module_type, options], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()

    def _unload_module(self, module_id):
        """
        Unloads a specific audio module.

        Parameters:
        - module_id (str): The ID of the module to unload.
        """
        subprocess.run(["pactl", "unload-module", module_id])

def main():
    # Get the server IP from environment variables
    server_ip = os.getenv("SERVER_IP")

    # Create an instance of the NetworkUtils utility class
    network_utils = NetworkUtils()

    # Wait until SERVER_IP is available
    if server_ip and network_utils.wait_for_server_ip(server_ip, timeout=3600):  # Wait for up to 1 hour (3600 seconds)
        # Create an instance of the PulseAudio audio manager
        pulse_manager = PulseAudioManager(server_ip)

        # Load audio modules
        pulse_manager.load_audio_modules()

        print("Modules loaded successfully.")

        # Wait for a few seconds (you can adjust as needed)
        time.sleep(10)

        # Unload modules (optional)
        # pulse_manager.unload_audio_modules()

if __name__ == "__main__":
    main()
