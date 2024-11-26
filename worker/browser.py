import subprocess
import os
import signal


class Chrome:
    """
    Class to manage the Chrome browser in fullscreen mode with an optional URL.
    """

    def __init__(self) -> None:
        """
        Initialises the Chrome instance.
        """
        self.running = False
        self.process = None
        self.url = None

    def start(self, url: str = None) -> None:
        """
        Starts the Chrome browser with a specified URL or a new window.
        
        Args:
            url (str): Optional URL to open in the browser.
        """
        if self.running:
            print("Chrome is already running.")
            return

        if url:
            if not isinstance(url, str):
                print("The provided URL is invalid.")
                return
            self.url = url

        # Builds the command to open Chrome
        command = self._build_command(self.url)

        try:
            # Starts the Chrome process
            self.process = subprocess.Popen(command, shell=True, executable="/bin/bash")
            self.running = True
            print(f'Chrome started with URL: {self.url}' if self.url else 'Chrome started without URL.')
        except Exception as e:
            print(f'Error while trying to start Chrome: {e}')
            self.running = False

    def stop(self) -> None:
        """
        Closes the Chrome browser if it is running.
        """
        if not self.running:
            print("Chrome is not running.")
            return

        if self.process:
            try:
                os.kill(self.process.pid, signal.SIGTERM)
                self.process = None
                self.running = False
                print("Chrome has been closed successfully.")
            except Exception as e:
                print(f"Error while trying to close Chrome: {e}")

    def _build_command(self, url: str = None) -> str:
        """
        Builds the command to launch Chrome.

        Args:
            url (str): Optional URL to open.

        Returns:
            str: Command to execute Chrome.
        """
        base_command = 'google-chrome'
        return f'{base_command} "{url}"' if url else base_command