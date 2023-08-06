#!/usr/bin/env python3
#
# Filename: suta_ble_bed_cli.py
#
# Author: Simon Redman <simon@ergotech.com>
# File Created: 03.03.2023
# Description: Scuffed CLI to control your bed. Mostly for testing.
#

import asyncio
import argparse
from argparse import Namespace
import logging

from ..suta_ble_bed import BleSutaBed
from ..suta_ble_scanner import discover

logger = logging.getLogger(__name__)

async def worker(args: Namespace):
    devices = await discover(args.MAC)

    for device in devices:
        logger.info(f"Discovered {device}")

    if len(devices) == 0:
        logger.error("No devices detected.")
        raise
    elif len(devices) > 1:
        logger.error("Multiple devices detected. Please select one using the MAC parameter.")
        raise

    device = devices[0]
    bed = BleSutaBed(device)

    match args.command:
        case "feet-up":
            await bed.raise_feet()
        case "feet-down":
            await bed.lower_feet()
        case "head-up":
            await bed.raise_head()
        case "head-down":
            await bed.lower_head()

def main():
    parser = argparse.ArgumentParser(
        prog="SUTA BLE Control",
        description="Control your Bluetooth-enabled SUTA (and other) bed.")

    parser.add_argument(
        "--MAC",
        required=False,
        help="MAC Address of your bed. May be ommitted, in which case we will attempt auto-discovery.")
    
    parser.add_argument(
        "command",
        choices=["feet-up", "feet-down", "head-up", "head-down"],
        help="Action to perform")
    
    args = parser.parse_args()
    
    asyncio.run(worker(args))

if __name__ == "__main__":
    main()