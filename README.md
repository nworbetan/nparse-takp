## Nomns' Parser fork for TAKP

Provides player location and spell tracking support for TAKP by reading the player log.

Supports selection of specific character log files to support multiboxing on TAKP.  Each nParse instance icon on your system tray will have a tooltip which indicates the character being tracked/parsed for the given nParse instance.

Please see the [Wiki](https://github.com/hitechhippie/nparse-takp/wiki) for more information or go to the [Releases](https://github.com/hitechhippie/nparse-takp/releases) for the latest release.

Credit for the original nparse to Nomns:  https://github.com/nomns/nparse

## Building

- Build in a 32-bit WINEPREFIX on linux.

- Install 32-bit Windows Python 3.8.10 distribution in WINEPREFIX to `c:\py38`.

- Update PIP:
  - `wine c:/py38/python.exe -m pip install --upgrade pip`

- Install python dependencies:
  - `wine c:/py38/python.exe -m pip install -r requirements.txt`

- Build:
  - `wine c:/py38/Scripts/pyinstaller.exe --onefile nparse_py.spec`
