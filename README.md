# Audio Manager

## Overview

The Audio Manager project provides a solution for managing audio modules in a PulseAudio environment. It includes functionality to load and unload source and sink tunnel audio modules, enhancing audio quality and allowing flexible audio routing.

## Project Structure

The project is organized into the following components:

- `audio_manager`: Contains the main logic for the PulseAudio manager.
- `utils`: Includes utility classes such as `NetworkUtils` for network-related tasks.
- `scripts`: Contains executable scripts for running the project.

## Requirements

- Python 3.x
- PulseAudio
- Additional dependencies specified in the `requirements.txt` file.

## Usage

1. Clone the repository:

```bash
git clone https://github.com/your-username/audio-manager.git
cd audio-manager
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up the environment:

```bash
cp .env.example .env
```

Edit the `.env` file and provide the required configuration, including the `SERVER_IP` variable.

4. Run the project:

```bash
python scripts/main.py
```

## Additional Notes

- Ensure that PulseAudio is properly configured on both the server and client machines.
- The `SERVER_IP` should be set to the IP address of the Windows 10 machine acting as the server.
- The client machine is assumed to be running Ubuntu 22.04 LTS.
