# Machine Troubleshooting Guide

## CNC Machine Issues

### Spindle Not Reaching Speed
- **Possible causes**: VFD fault, bearing wear, incorrect parameters, mechanical binding
- **Checks**: Check VFD error codes, measure bearing temperature, verify parameter settings, rotate spindle manually
- **Resolution**: Replace VFD if fault code indicates, replace bearings if noise/vibration present, recalibrate parameters

### Excessive Vibration During Machining
- **Possible causes**: Tool holder imbalance, spindle bearing wear, workpiece clamping issues, worn guideways
- **Checks**: Inspect tool holder runout, check spindle vibration with analyzer, verify clamping force, inspect guideway condition
- **Resolution**: Re-balance tool holder, replace spindle bearings, adjust or replace clamping, re-scrape guideways

### Positioning Error
- **Possible causes**: Encoder fault, scale contamination, thermal drift, servo tuning issues
- **Checks**: Compare actual vs commanded position, inspect encoder/scale, check temperature at location, review servo gains
- **Resolution**: Clean or replace encoder/scale, recalibrate, tune servo parameters, add thermal compensation

## Hydraulic Press Issues

### Pressure Drop
- **Possible causes**: Pump wear, valve leakage, cylinder seal wear, contaminated fluid
- **Checks**: Monitor pressure at idle vs under load, check valve spool condition, inspect cylinder rods for scoring, test fluid viscosity
- **Resolution**: Rebuild or replace pump, rebuild valve, replace seals, change hydraulic fluid and filters

### Cylinder Drift
- **Possible causes**: Seal leakage, valve spool wear, counterbalance valve failure
- **Checks**: Isolate cylinder and monitor pressure decay, inspect valve spool, test counterbalance valve
- **Resolution**: Replace cylinder seals, rebuild or replace valve, replace counterbalance valve

### Slow Cycle Time
- **Possible causes**: Pump flow reduction, flow control valve setting, restricted lines, low fluid level
- **Checks**: Measure pump flow rate, verify valve settings, check for line restrictions, check fluid level
- **Resolution**: Repair/replace pump, adjust valves, clean/replace lines, top up fluid

## Conveyor System Issues

### Belt Tracking Problem
- **Possible causes**: Misaligned pulleys, uneven belt tension, worn pulleys, material buildup
- **Checks**: Check pulley alignment with laser, verify tension across belt width, inspect pulley lagging
- **Resolution**: Realign pulleys, adjust tensioning, replace worn pulleys, clean pulleys

### Motor Overload
- **Possible causes**: Excessive load, bearing failure, electrical issues, mechanical binding
- **Checks**: Measure motor current (FLA), check bearing temperature, verify voltage, inspect for binding
- **Resolution**: Reduce load, replace bearings, troubleshoot electrical, clear mechanical obstructions

## Robot Issues

### Position Drift
- **Possible causes**: Encoder battery failure, gearbox backlash, calibration loss, thermal expansion
- **Checks**: Check encoder battery voltage, measure repeatability, run calibration routine, compare to baseline
- **Resolution**: Replace encoder batteries, tighten or replace gearbox, recalibrate, implement warm-up cycle

### Gripper Failure
- **Possible causes**: Pneumatic leak, jaw wear, sensor misalignment, insufficient grip force
- **Checks**: Listen for air leaks, inspect gripper jaws, verify sensor position, check air pressure
- **Resolution**: Replace seals/seals, replace jaws, realign sensors, adjust pressure regulator
