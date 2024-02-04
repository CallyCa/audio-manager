import subprocess
import time

class NetworkUtils:
    @staticmethod
    def wait_for_server_ip(server_ip, retry_interval=5, timeout=None):
        """
        Waits until the server IP is accessible using ping.

        Parameters:
        - server_ip (str): The server's IP address.
        - retry_interval (int): The interval between attempts in seconds.
        - timeout (int or None): Maximum total waiting time in seconds. If None, waits indefinitely.

        Returns:
        - bool: True if the server is accessible, False otherwise.
        """
        start_time = time.time()

        while True:
            try:
                # Use subprocess to perform ping directly
                subprocess.run(["ping", "-c", "1", server_ip], check=True)
                print(f"SERVER_IP ({server_ip}) is available.")
                return True
            except subprocess.CalledProcessError as e:
                # Check if the error is related to name resolution failure
                if "Temporary failure in name resolution" not in str(e):
                    raise  # Re-raise the exception if it's not related to name resolution failure

                current_time = time.time()
                elapsed_time = current_time - start_time

                if timeout is not None and elapsed_time >= timeout:
                    print(f"Attention: Total waiting time exceeded. Could not connect to SERVER_IP.")
                    return False

                print(f"SERVER_IP ({server_ip}) is not available. Trying again in {retry_interval} seconds...")
                time.sleep(retry_interval)
