#!/usr/bin/env python3

import asyncio

from kuksa_client.grpc.aio import VSSClient
from typing import Dict

vss_values: Dict[str, float] = {}
nbr_vss_signals: int = 0


def reset_vss_values():
    vss_values['Vehicle.Speed'] = -100
    vss_values['Vehicle.Chassis.Axle.Row1.Wheel.Left.Brake.Temperature'] = -100
    vss_values['Vehicle.Chassis.Axle.Row1.Wheel.Right.Brake.Temperature'] = -100
    vss_values['Vehicle.Chassis.Axle.Row2.Wheel.Left.Brake.Temperature'] = -100
    vss_values['Vehicle.Chassis.Axle.Row2.Wheel.Right.Brake.Temperature'] = -100


async def subscribe():
    global nbr_vss_signals
    async with VSSClient('127.0.0.1', 55555) as client:

        async for updates in client.subscribe_current_values([
            'Vehicle.Speed',
            'Vehicle.Chassis.Axle.Row1.Wheel.Left.Brake.Temperature',
            'Vehicle.Chassis.Axle.Row1.Wheel.Right.Brake.Temperature',
            'Vehicle.Chassis.Axle.Row2.Wheel.Left.Brake.Temperature',
            'Vehicle.Chassis.Axle.Row2.Wheel.Right.Brake.Temperature',
        ]):
            for path, dp in updates.items():
                if path == 'Vehicle.Speed':
                    if dp.value > vss_values[path]:
                        vss_values[path] = dp.value
                else:
                    vss_values[path] = dp.value
                nbr_vss_signals += 1


async def present():
    while True:
        print("Statistics: " + str(nbr_vss_signals) + " signals!")
        print("Current Temp FL: " + str(vss_values['Vehicle.Chassis.Axle.Row1.Wheel.Left.Brake.Temperature']))
        print("Current Temp FR: " + str(vss_values['Vehicle.Chassis.Axle.Row1.Wheel.Right.Brake.Temperature']))
        print("Current Temp RL: " + str(vss_values['Vehicle.Chassis.Axle.Row2.Wheel.Left.Brake.Temperature']))
        print("Current Temp RR: " + str(vss_values['Vehicle.Chassis.Axle.Row2.Wheel.Right.Brake.Temperature']))
        print("Max speed since last time: " + str(vss_values['Vehicle.Speed']))
        reset_vss_values()
        await asyncio.sleep(5)


nbr_vss_signals = 0
reset_vss_values()
loop = asyncio.get_event_loop()
loop.create_task(subscribe())
loop.create_task(present())
loop.run_forever()
