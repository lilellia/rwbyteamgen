# [Localized] RWBY Team Name Generator

An online version of this program can be found [here](https://rwbyteamgen.herokuapp.com). However, it is hosted on Heroku's free dyno servers, which means that it has only 500 hours (~21 days) of available runtime per month, meaning that it is unfortunately unavailable towards the end of the month.

If you're patient, you can wait for the new month to start, or you can use this localized version. This one requires a bit more setup.

## INSTALLATION

1. You will need Python 3.6+ to run this project. Downloads can be found [here](https://www.python.org/downloads/). While any version of 3.6/3.7/3.8/3.9 should work, it is recommended to use the most recent version. (This project was tested on 3.8.5.) Make sure to select the "Add Python to PATH" option.
   1. To test the installation, open a terminal and run the following commands:

        ```bash
        python3 --version
        python3 -c 'import tkinter'
        ```

    The first command should output the Python version that's being used (e.g., "3.8.5"). The second shouldn't display anything: if you get a `ModuleNotFoundError`, then you need to install the `tkinter` libraries.

    If they don't work, try replacing the commands with `python`, `python3.X`, or `python3X` (where `X` is the minor version number of the Python version you installed) instead of `python3`.

2. Linux users *will* need to install the `tkinter` libraries since they aren't packaged with the standard library on Linux. This can be done by executing:

    ```bash
    // on Ubuntu, etc. //
    sudo apt-get install python3-tk

    // on Fedora //
    sudo dnf install python3-tkinter
    ```

3. Open a terminal/command prompt and navigate to the folder where this project was downloaded. For example:

    ```bash
    // Windows //
    C:\Users\pixielf> cd "My Documents\rwbyteamgen"
    C:\Users\pixielf\My Documents\rwbyteamgen>

    // Linux //
    pixielf@pixielf:~$ cd Documents/rwbyteamgen
    pixielf@pixielf:~/Documents/rwbyteamgen$
    ```

4. Run the program from the terminal with `python3 main.py`.
