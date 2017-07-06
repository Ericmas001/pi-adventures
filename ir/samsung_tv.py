# Python port for RPI3
# Eric Masse (Ericmas001) - 2017-06-30
# https://github.com/Ericmas001/HVAC-IR-Control

# From original: https://github.com/r45635/HVAC-IR-Control
# (c)  Vincent Cruvellier - 10th, January 2016 - Fun with ESP8266

import ir_sender

class Buttons:
    """
    Buttons
    """
    Power = 0x40BF
    VolumeUp = 0xE01F
    VolumeDown = 0xD02F
    RightArrow = 0x46B9
    LeftArrow = 0xA659

class Delay:
    """
    Delay
    """
    HdrMark = 4580
    HdrSpace = 4447
    BitMark = 613
    OneSpace = 1623
    ZeroSpace = 517
    RptMark = 624
    RptSpace = 1623

class Constants:
    """
    Constants
    """
    Frequency = 38000       # 38khz
    PreData = 0xE0E0
    MaxMask = 0xFFFF
    NbBytes = 2
    NbPackets = 1

class Index:
    """
    Index
    """
    PreData = 0             # Byte 1 - PreData
    Button = 1              # Byte 2 - Button

class SamsungTv:
    """
    SamsungTv
    """
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin

    def send_command(self, button):
        """
        send_command
        """
        sender = ir_sender.IrSender(self.gpio_pin, "NEC", dict(
            leading_pulse_duration=Delay.HdrMark,
            leading_gap_duration=Delay.HdrSpace,
            one_pulse_duration=Delay.BitMark,
            one_gap_duration=Delay.OneSpace,
            zero_pulse_duration=Delay.BitMark,
            zero_gap_duration=Delay.ZeroSpace,
            trailing_pulse_duration=Delay.RptMark))

        data = [0] * Constants.NbBytes
        data[Index.PreData] = Constants.PreData
        data[Index.Button] = button

        # transmit packet more than once
        for _ in range(0, Constants.NbPackets):
            sender.send_data(data, Constants.MaxMask, False)

        sender.terminate()
