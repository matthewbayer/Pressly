# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

async def send_iot_message(string):
    # Fetch the connection string from an enviornment variable
    #conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
    conn_str = 'HostName=mock-iot-device.azure-devices.net;DeviceId=mock-iot-python;SharedAccessKey=AcMz/o+M+36Jd2TEUbm3BVGpEKN+/4VHicP3jh7nkEQ='
    # Create instance of the device client using the connection string
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the device client.
    await device_client.connect()

    # Send a single message
    print("Sending message...")
    msg = Message(string)
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"
    await device_client.send_message(msg)
    print("Message successfully sent!")

    # Finally, shut down the client
    await device_client.shutdown()

    return