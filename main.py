from optparse import OptionParser
from subprocess import Popen, PIPE
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

# from edit_file import change_file_threshold

path_to_file = "/etc/systemd/system/battery-charge-threshold.service"
lookup_string = "ExecStart"


def change_file_threshold(battery_level, battery_name):
    """
        Overwrite the Battery Charge Threshold File
    """
    change_to_string = f"ExecStart=/bin/bash -c 'echo {battery_level} > /sys/class/power_supply/{battery_name}/charge_control_end_threshold'"

    fd, abspath = mkstemp()
    with fdopen(fd, "w") as file1:
        with open("battery-charge-threshold.txt", "r") as file0:

            for line in file0:
                if lookup_string in line:
                    file1.write(change_to_string)
                else:
                    file1.write(line)
            file0.close()
        file1.close()
    copymode(path_to_file, abspath)
    remove(path_to_file)
    move(abspath, path_to_file)


if __name__ == "__main__":
    try:
        parser = OptionParser()
        parser.add_option("-i", "--INITIALISE", dest="initialise",
            action="store_true", default=False, 
            help="Initial battery level setup, [default: %default]")
        parser.add_option("-s", "--SET_LEVEL", dest="initialise",
            action="store_false",
            help="Set new battery level, [default: True]") 
        parser.add_option("-b", "--BATTERY_LEVEL", dest="battery_level",
            default=100,
            help="Set the Battery Level, [default: %default]")
        parser.add_option("-n", "--BATTERY_NAME", dest="battery_name",
            default="BAT0",
            help="Set the Battery Name, [default: %default]")
        (options, args) = parser.parse_args()

        accepted_battery_levels = [100, 80, 60]
        # Check Battery Level Option is Valid
        if not (int(options.battery_level) in accepted_battery_levels):
                raise Exception(f"Accepted Battery Levels:{accepted_battery_levels}")
    
        # Check Battery Name is Valid
        stdout = Popen("ls /sys/class/power_supply", shell=True, stdout=PIPE).stdout
        output = stdout.read().decode("utf-8")
        output = output.split("\n")
        sys_bat_name = output[1]
        if not (options.battery_name in sys_bat_name):
            raise Exception(f"Change --BATTERY_LEVEL argument to match {sys_bat_name}")

        if not options.initialise:
            # Set Battery Level
            print(f"Setting Battery Level to {options.battery_level}%")
            change_file_threshold(options.battery_level, options.battery_name)
            Popen("sudo systemctl daemon-reload", shell=True, stdout=PIPE).stdout
            Popen("sudo systemctl restart battery-charge-threshold.service", shell=True, stdout=PIPE).stdout
            print("DONE")
        else:
            # Initialise the process
            print(f"Initialising and setting Battery Level to {options.battery_level}%")
            Popen("sudo touch /etc/systemd/system/battery-charge-threshold.service", shell=True, stdout=PIPE).stdout
            change_file_threshold(options.battery_level, options.battery_name)
            Popen("sudo systemctl enable battery-charge-threshold.service", shell=True, stdout=PIPE).stdout
            Popen("sudo systemctl start battery-charge-threshold.service", shell=True, stdout=PIPE).stdout
            print("DONE")

    except Exception as e:
        print(e)