import socket
import subprocess
import unittest
import sys
from os.path import abspath, dirname
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path
sys.path.append(abspath(dirname(abspath(__file__)) + '/../'))

from audio_manager.manager import PulseAudioManager
from utils.network_utils import NetworkUtils


class TestPulseAudioManager(unittest.TestCase):
    @patch('subprocess.run')
    def test_load_audio_modules(self, mock_run):
        """
        Test loading audio modules successfully.
        """
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "42"

        pulse_manager = PulseAudioManager("test_server")
        pulse_manager.load_audio_modules()

        self.assertEqual(pulse_manager.source_module, "42")
        self.assertEqual(pulse_manager.sink_module, "42")

    @patch('subprocess.run')
    def test_unload_audio_modules(self, mock_run):
        """
        Test unloading audio modules successfully.
        """
        pulse_manager = PulseAudioManager("test_server")
        pulse_manager.source_module = "42"
        pulse_manager.sink_module = "42"

        expected_result = MagicMock(spec=subprocess.CompletedProcess)
        expected_result.returncode = 0
        expected_result.stdout = "42"
        mock_run.return_value = expected_result

        pulse_manager.unload_audio_modules()

        mock_run.assert_called_with(
            ["pactl", "unload-module", "42"],
            capture_output=True,
            text=True,
            check=True,
            stdout=subprocess.PIPE if hasattr(subprocess, 'PIPE') else -1,
            stderr=subprocess.PIPE if hasattr(subprocess, 'PIPE') else -1
        )

class TestNetworkUtils(unittest.TestCase):
    @patch('socket.create_connection')
    @patch('time.sleep')
    @patch('subprocess.run')
    def test_wait_for_server_ip(self, mock_run, mock_sleep, mock_create_connection):
        """
        Test waiting for server IP with a successful connection.
        """
        mock_create_connection.return_value = True  # Indicates a successful connection
        mock_run.return_value.returncode = 0  # Simulates a successful ping

        network_utils = NetworkUtils()
        result = network_utils.wait_for_server_ip("test_server", timeout=10, retry_interval=2)

        self.assertTrue(result)
        mock_create_connection.assert_called_with(("test_server", 80), timeout=2)
        mock_sleep.assert_not_called()
        mock_run.assert_called_with(["ping", "-c", "1", "test_server"], check=True)

    @patch('socket.create_connection')
    @patch('time.sleep')
    @patch('subprocess.run')
    def test_wait_for_server_ip_timeout(self, mock_run, mock_sleep, mock_create_connection):
        """
        Test waiting for server IP with a timeout.
        """
        mock_create_connection.side_effect = [socket.timeout] * 5 + [True]  # Timeout on the first 5 calls, successful on the last one
        mock_run.side_effect = [subprocess.CalledProcessError(returncode=2, cmd=['ping', '-c', '1', 'test_server'])] * 5  # Simulates the ping command error

        network_utils = NetworkUtils()
        result = network_utils.wait_for_server_ip("test_server", timeout=10, retry_interval=2)

        self.assertFalse(result)  # Expects the function to return False in case of a timeout
        self.assertEqual(mock_create_connection.call_count, 6)
        self.assertEqual(mock_run.call_count, 5)  # The ping command should be called 5 times
        mock_sleep.assert_called_with(2)  # Called 5 times


if __name__ == '__main__':
    unittest.main()
