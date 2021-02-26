#!/usr/bin/env python3

#if percent < 25 yellow
#if percent < 10 red
#if fully charged green?
#if status = something, then shorten
# CHR = charging
# DCHR ?
# FL

path = "/sys/class/power_supply/sbs-20-000b/"

def formatTime(seconds):
    hours = int(seconds / 3600)
    minutes = round((seconds - hours*3600)/60)
    if minutes < 10:
        minutes = "0"+str(minutes)
    if hours == 0:
        output = "("+str(minutes)+")"
    else:
        output = "("+str(hours)+":"+str(minutes)+")"
    return output

def getStatus():
    with open(path+"status") as f:
        status = f.read().rstrip()
    return status

def getChargeFull():
    with open(path+"charge_full") as f:
        charge_full = int(f.read().rstrip())
    return charge_full

def getChargeNow():
    with open(path+"charge_now") as f:
        charge_now= int(f.read().rstrip())
    return charge_now

def getTimeToEmpty():
    with open(path+"time_to_empty_avg") as f:
        time_to_empty = int(f.read().rstrip())
    return time_to_empty

def getTimeToFull():
    with open(path+"time_to_full_avg") as f:
        time_to_full = int(f.read().rstrip())
    return time_to_full

def main():
    charge_now = getChargeNow()
    charge_full = getChargeFull()
    percent = round((charge_now*1.0/charge_full)*100)

    status = getStatus()
    time_to_empty = getTimeToEmpty()
    time_to_full = getTimeToFull()

    if status == "Discharging":
        status = "DIS"
        time = formatTime(time_to_empty)
    elif status == "Charging":
        status = "CHR"
        if percent == 100:
            time = ""
        else:
            time = formatTime(time_to_full)
    elif spercentStrll: #wtf is going on here
        status = ""
        if percent == 100:
            time = ""
        else:
            time = formatTime(time_to_full)

    percentStr = str(percent)
    if percent < 10:
        percentStr = "0"+str(percent)
    output = percentStr+"% "+status+" "+time

    color = ""
    if percent < 20:
        color = "yellow"
        if percent < 16:
            color = "orange"
            if percent < 11:
                color = "red"

    if color:
        output = "<span color='"+color+"'>"+output+"</span>"
        if percent < 6:
            output = "<b>"+output+"</b>"
    print(output)

if __name__ == '__main__':
    main()
