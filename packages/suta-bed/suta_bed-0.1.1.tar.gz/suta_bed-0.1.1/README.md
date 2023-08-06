# suta-ble-bed
BLE handling code for bed frames which use the SUTA app (and others)

Supports control of the bed but not access to the current state.
Expected to be used as a module to build your own integration with some
control system, but ships with a rough CLI to play with directly.

Does device discovery by name because (as far as I could tell) the bed
does not support discovery by the typical manufacturer UUID.

Notionally, this should be fine unless your neighbor is actively trying
to intercept your bed control.

## Usage

```
device = await suta_scanner.discover()[0]
bed = BleSutaBed(device)
await bed.raise_feet()
```

or

```
./suta_ble_bed_cli.py raise-feet
```

## Improvements

- It takes a really long time to connect to the bed, because when using Bluez
you must be actively scanning for the device in order to connect.

## Acknowledgements

This module would not have been possible without the research done by stevendodd on Github:
https://github.com/stevendodd/sleepmotion-ble/blob/main/pi-zero/sleepmotion-ble.py

Code structure inspirired by:
https://github.com/sopelj/python-ember-mug/blob/main/ember_mug/mug.py
