#!/bin/python

"""
Demo Samsung Tv
"""

if __name__ == "__main__":
    print("=======================================================")
    from samsung_tv import SamsungTv, Buttons

    STV = SamsungTv(23)
    STV.send_command(Buttons.VolumeDown)
    STV.send_command(Buttons.VolumeDown)
    STV.send_command(Buttons.VolumeDown)
    STV.send_command(Buttons.VolumeDown)
    print("=======================================================")
