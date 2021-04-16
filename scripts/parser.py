#!/usr/bin/python3
import os


def send_message():
    title = "Title"
    message = "Message"
    os.system('notify-send "{}" "{}"'.format(title, message))


def main():
    send_message()


if __name__ == '__main__':
    main()
