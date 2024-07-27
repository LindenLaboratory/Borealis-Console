# What is the Borealis Console project?
The Borealis Console is a project that uses a slightly modified version of the [Borealis network](https://github.com/LindenLaboratory/Borealis) with its own account database editing page to interface with small micro controller based devices to perform simple phone-like functions. The network allows the devices to work within a reasonably large range that does not require an internet connection in order to function, meaning the project can be set up anywhere. The devices communicate directly with the server which means the system is very centralised and through the Borealis network's _Composer_ device some functionalities can be controlled remotely through telegram.

## What functions can the Console devices perform?
Firstly, you can log messages in the _Conductor_'s log and read from said log in order to communicate with other devices on the network. Secondly, you can store, send and receive a digital currency that can be added by an Admin user on the accounts page (see [ACCOUNTS.md](ACCOUNTS.md)) which can be used for many purposes and finally run applications. These apps are coded in a custom miniature "programming language" called Aurora (I use quotations here because it isn't turing-complete and it is coded in Python so is not especially efficient) that allows you to very easily utilise the screens, buttons and network to make simple text-based single or multiplayer games. More detail about this is included in the [AURORA.md](AURORA.md) file and instructions on how to install applications is included in **ACCOUNTS.md**.

## The Console devices
The Borealis Console devices are made up of two simple hardware components:

- 1x [Raspberry Pi Pico WH](https://thepihut.com/products/raspberry-pi-pico-w?variant=41952994787523)
- 1x [1.3" OLED Display Module for Raspberry Pi Pico (64×128)
](https://thepihut.com/products/1-3-oled-display-module-for-raspberry-pi-pico-64x128?variant=39810640117955&currency=GBP&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&gad_source=1&gclid=CjwKCAjwko21BhAPEiwAwfaQCEHjXfxdrGalaUam1pjJR0_vidUftZoUu51jIuVXq9I01RZoHpKw5BoCeWQQAvD_BwE)

The Pico WH costs **£6.80** and the OLED Display Module costs **£10.80**, bringing the total cost for one console to **£17.60**, not including shipping. This makes each device reasonably cost effective considering the large amount of functions they can perform. Each device runs Micropython with software that is based off of the Micropython branch of the _Choir_ software (see Borealis network repo).

## How to set up the devices
First, follow the instructions in **NETWORK.md** of the Borealis repo to set up the actual network, forgoing installing the **main.py** files onto the _Choir_ and _Conductor_ devices. After you have completed this, install the **main.py** file from [the Conductor folder](Conductor) folder onto the _Conductor_ device. Next, attatch the screen to the _Choir_ device and install the **main.py** file from in [the Console folder](Console). Finally, read through **ACCOUNTS.md** and follow the instructions to create the account and link it to the device. You are now finished!
