import gpt_2_simple.gpt_2 as gpt2
import json
import os
import sys
import numpy as np
import argparse

def interact(run_name='run1', seed=None, length=200, temperature=.8, top_k=0):
    conversation = """
you: hi
bot: hey
you: i'm a human
bot: i'm you!
you: you ready?
bot: yes :)
you: ok let's start chatting
bot: sure, what do you want to talk about?"""
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, run_name=run_name)
    print(conversation)
    while True: 
        message = None
        while not message:
            message = input('you: ')
        text = gpt2.generate(sess, run_name=run_name, prefix=conversation, length=length, temperature=temperature, top_k=top_k, return_as_list=True)
        lines = text[0][len(conversation):].split('\n')
        reply = None
        for line in lines:
            if line is None:
                continue
            if not line.startswith('bot:'):
                continue
            message = line.split('bot:')[1].strip()
            if message == '':
                continue
            else:
                reply = line
                break
        if reply is None:
            print('[No message could be generated from the given input. Showing all output which was generated by bot:]')
            print(lines)
        else:
            print(reply)
            if not reply.endswith('\n'):
                reply += '\n'
            conversation = conversation + reply

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Interact with fine tuned model")
    parser.add_argument('-r', '--run-name', dest='run_name', help="Run name", default='run1')
    parser.add_argument('-t', '--temperature', dest='temperature', type=float, help="Temperature", default=1)
    parser.add_argument('--top-k', dest='top_k', type=float, help="Top k", default=0)
    args = parser.parse_args()
    interact(run_name=args.run_name, temperature=args.temperature, top_k=args.top_k)
