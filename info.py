#!/usr/bin/env python3
import sys
import subprocess


def show_usage(reason):
    print(reason)
    print("Usage: info.py --timer timer_name")
    print("Usage: info.py --service service_name")
    sys.exit()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        show_usage("Invalid number of arguments")
    else:
        if sys.argv[1] == '--timer':
            option = 'timer'
            param = "ActiveState,LastTriggerUSec"
        elif sys.argv[1] == '--service':
            option = 'service'
            param = "ActiveState,User,Group,ExecMainStartTimestamp"
        else:
            show_usage("Unknown option")
        name = sys.argv[2]

    # create process to check if service or timer exists
    to_exec = "systemctl list-units -t service -t timer | grep -w \"" + sys.argv[2] + "." + option + "\""
    p = subprocess.Popen(to_exec, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if p.stdout.readlines():
        to_exec = "systemctl show " + sys.argv[2] + "." + option + " -p " + param
        p = subprocess.Popen(to_exec, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # create dictionary with neccesary information
        params = {}
        for line in p.stdout.readlines():
            line_cleaned = line.decode("utf-8").strip().split('=')
            if line_cleaned[1]:
                params[line_cleaned[0]] = line_cleaned[1]
            else:
                params[line_cleaned[0]] = None

        if option == 'service':
            print(name + "." + option + " " + str(params['ActiveState']) +
                  ', user ' + str(params['User']) +
                  ', group ' + str(params['Group']) +
                  ', last started ' + str(params['ExecMainStartTimestamp']))
        elif option == 'timer':
            print(name + "." + option + " " + str(params['ActiveState']) +
                  ', last started ' + str(params['LastTriggerUSec']))
    else:
        print("Sevice or timer is not found")
