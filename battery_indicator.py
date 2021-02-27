#!/usr/bin/env python3
''' This is a small script to generate a battery charge indicator for
i3blocks to be used on a Asus C201 Chromebook'''

import time
import fontawesome as fa

PATH = "/sys/class/power_supply/sbs-20-000b/"

def get_status():
    '''gets status; "charging,"discharging","full" etc'''
    with open(PATH+"status") as file:
        status = file.read().rstrip()
    return status

def get_charge_full():
    '''checks if charge is full'''
    with open(PATH+"charge_full") as file:
        charge_full = int(file.read().rstrip())
    return charge_full

def get_charge_now():
    '''gets current charge'''
    with open(PATH+"charge_now") as file:
        charge_now= int(file.read().rstrip())
    return charge_now

def get_time_to_empty():
    '''returns time until battery in dead in seconds'''
    with open(PATH+"time_to_empty_avg") as file:
        time_to_empty = int(file.read().rstrip())
    return time_to_empty

def get_time_to_full():
    '''returns time until battery in full in seconds'''
    with open(PATH+"time_to_full_avg") as file:
        time_to_full = int(file.read().rstrip())
    return time_to_full

def format_time(seconds):
    '''turns seconds into string formated as "(h:m)"'''
    return time.strftime("%H:%M", time.gmtime(seconds))

def get_icon(percent):
    '''returns fontawesome icon corresponding to charge level'''
    full = fa.icons['battery-full']
    three_quarters = fa.icons['battery-three-quarters']
    half = fa.icons['battery-half']
    quarter = fa.icons['battery-quarter']
    empty = fa.icons['battery-empty']

    icons = {
            '100' : full,
            '75' : three_quarters,
            '50' : half,
            '25' : quarter,
            '0'  : empty
    }

    old_diff = 100 # just some numb

    for value in icons:
        numb = float(value)
        diff = abs(percent-numb)
        if diff < old_diff or diff == 0:
            least = value
            old_diff = diff
        elif diff == old_diff:
            break
    return icons[least]

def main():
    '''foad pylint'''
    charge_now = get_charge_now()
    charge_full = get_charge_full()
    percent = round((charge_now*1.0/charge_full)*100)

    status = get_status()
    time_to_empty = get_time_to_empty()
    time_to_full = get_charge_full()

    bolt = fa.icons['bolt']
    if status == "Discharging":
        status = ""
        time_str = format_time(time_to_empty)
    elif status == "Charging":
        status = bolt
        if percent == 100:
            time_str = ""
        else:
            # this section is messed up.
            time_str = format_time(time_to_full)
            if ":" not in time_str:
                tmp_time = time_str[1:-1]
                if int(tmp_time) < 61:
                    time_str = ""
    elif status == "Full":
        status = bolt
        if percent == 100:
            time_str = ""
        else:
            time_str = format_time(time_to_full)
    elif status == "Not charging":
        status = bolt
        time_str = ""

    percent_str = str(percent)
    if percent < 10:
        percent_str = "0"+str(percent)
    output = percent_str + "% "+ time_str + status

    color = ""
    if percent < 20:
        color = "yellow"
        if percent < 16:
            color = "orange"
            if percent < 11:
                color = "red"

    icon = get_icon(percent)
    output = icon +"  "+ output
    if color:
        output = "<span color='"+color+"'>"+output+"</span>"
        if percent < 6:
            output = "<b>"+output+"</b>"
    print(output)

if __name__ == '__main__':
    main()
