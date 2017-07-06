#!/usr/bin/python
from hvac_ircontrol.mitsubishi import ClimateMode, FanMode, VanneVerticalMode, VanneHorizontalMode, ISeeMode, AreaMode, Constants
from models import AvailableCommands

def get_index(app):
    return "Ralph is listening !!!"

def list_config(app):
    res = AvailableCommands()
    res.climate_modes = (a for a in dir(ClimateMode) if not a.startswith('_'))
    res.isee_modes = (a for a in dir(ISeeMode) if not a.startswith('_'))
    res.vanne_horizontal_modes = (a for a in dir(VanneHorizontalMode) if not a.startswith('_'))
    res.fan_modes = (a for a in dir(FanMode) if not a.startswith('_'))
    res.vanne_vertical_modes = (a for a in dir(VanneVerticalMode) if not a.startswith('_'))
    res.area_modes = (a for a in dir(AreaMode) if not a.startswith('_'))
    res.min_temp = Constants.MinTemp
    res.max_temp = Constants.MaxTemp
    return res
