#!/usr/bin/env python 3.7

message = input("Enter a message: ")

print("First Character:", message[0])
print("Last Character:", message[-1])
print("Middle Character:", message[int(len(message) / 2)])
print("Even index characters", message[0::2])
print("Odd index characters", message[1::2])
print("Reversed message", message[::-1])

