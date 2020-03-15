#!/usr/bin/env python3
import config
import signal
import sys
from os import system, name 

def clear():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 
    
def main():
    clear()
    print (config.TRANSMISSION)
    print("************SETUP MENU************")
    choice = input("""
    A: Setup Trakt.TV
    B: Setup Transmission
    C: Setup Pushover.net
    Q: Quit and save
    
    (CTRL+C: Abort)

Please enter your choice: """)

    if choice == "A" or choice =="a":
        tratkTV()
    elif choice == "B" or choice =="b":
        transmission()
    elif choice == "C" or choice =="c":
        pushover()
    elif choice=="Q" or choice=="q":
        save()
        sys.exit
    else:
        print("You must only select either A,B,C, or D.")
        print("Please try again")
        main()

def tratkTV():
    clear()
    print("************TRAKT.TV************")
    print("Go to: https://trakt.tv/oauth/applications")
    print()
    config.CLIENT_ID = input("Trakt.TV Client Id: ")
    config.CLIENT_SECRET = input("Trakt.TV Client secret: ")

    main()
    
def transmission():
    clear()
    print("***********TRANSMISSION***********")
    print()
    config.TRANSMISSION = input("Transmission url (with port no): ")
    config.TRANSMISSION_USER = input("User name (Enter if empty): ")
    config.TRANSMISSION_PWD = input("Password (Enter if empty): ")
    main()
    
def pushover():
    clear()
    print("***********PUSHOVER.NET***********")
    print()
    config.PUSHOVER_USER = input("User key: ")
    config.PUSHOVER_APP = input("API Token/key): ")
    main()

def signal_handler(sig, frame):
    print()
    print("Aborted")
    sys.exit(0)
    
def save():
    f = open("config.py", "w")
    f.write("CLIENT_ID = '" + config.CLIENT_ID + "'\n")
    f.write("CLIENT_SECRET = '" + config.CLIENT_SECRET + "'\n")
    f.write("TRANSMISSION = '" + config.TRANSMISSION + "'\n")
    f.write("TRANSMISSION_USER = '" + config.TRANSMISSION_USER + "'\n")
    f.write("TRANSMISSION_PWD = '" + config.TRANSMISSION_PWD + "'\n")
    f.write("PUSHOVER_USER = '" + config.PUSHOVER_USER + "'\n")
    f.write("PUSHOVER_APP = '" + config.PUSHOVER_APP + "'")
    
    f.close()

signal.signal(signal.SIGINT, signal_handler)
main()