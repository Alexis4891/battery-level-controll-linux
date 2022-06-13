# Battery Level Control - Linux

Having migrated on a Linux based Operating System i found out that there was no official application that could set my laptop's battery level. Therefore, i wrote this script to setup a battery level service.
__Disclamer__:
Check that your laptop's battery controller can actually handle different battery levels. This script does not guarantee that a battery level can be set.

## _How to Use_

I recommend running the script with __sudo__ privileges since there are a few commands that need admin permissions. Let's have a look at the options avaialable:

```sh
sudo python3 main.py -h
```

Options:
  -h, --help            show this help message and exit
  -i, --INITIALISE,      Initial battery level setup, [default: False]
  -s, --SET_LEVEL,       Set new battery level, [default: True]
  -b BATTERY_LEVEL, --BATTERY_LEVEL=BATTERY_LEVEL, Set the Battery Level, [default: 100]
  -n BATTERY_NAME, --BATTERY_NAME=BATTERY_NAME, Set the Battery Name, [default: BAT0]

You can either `--INITIALISE` or `--SET_LEVEL`.

__First time__ run the script with the `--INITIALISE` argument:
```sh
sudo python3 main.py -i
```
This would setup the battery level service with the default values, i.e. battery level at 100% and battery name _BAT0_

__Afterwards__ run the script whenever you need to change the battery level. The only accepted battery levels are 100%, 80% and 60%
For the full capacity, __Battery Level 100%__:
```sh
sudo python3 main.py -b 100
```
For a balanced battery level, __Battery Level 80%__:
```sh
sudo python3 main.py -b 80
```
For the maximum battery lifespan, __Battery Level 60%__ (Recommended when power adapter is constantly pluged-in):
```sh
sudo python3 main.py -b 60
```

You can also check that the script and therefore battery level is set correctly on your laptop. For example, setting the battery level to 60% 

## _Notes_

It should be noted that this was tested on an _Asus UX430U_ with _Ubuntu 20.04.4_ as the operating system. Python version: 3.8.10

## License

MIT
