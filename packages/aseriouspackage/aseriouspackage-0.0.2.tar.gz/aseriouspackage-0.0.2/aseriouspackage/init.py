#!/usr/bin/python

import os
import random
from faker import Faker
import numpy as np

def init_word():

	f = open('.puzzle.txt','a')
	candidates = ['plumb','souce','bewit','sixty','sling','crout','drama',
	'tyler','porer','taled','femur','obama','swift','faith','quirk','euler',
	'mouse','brain','elder','hello','savor','medal','forge','flame','budge',
	'quick','amend','nanny','slink','shirt','toxin','plein','refar','fever',
	'fleet','pound','whiff','issue','roper','fifth','flute','ralph','touch',
	'fruit','wiper','blunt','crane','flood','unfit','remix','begat','avant',
	'still','pipit','pupal','sirup','rouge','cable','ionic','cause','stone',
	'tined','early','tined','lynch','ounce','yearn','shots','heart','liver',
	'nifle','palsy']
	q1 = candidates[random.randint(0,len(candidates)-1)]
	f.write(q1)
	f.close()

	return hash(q1)

def init_key():

	f = open('.key.txt','a')
	candidates = [101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 
	157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 
	233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 
	313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 
	401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 
	487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 
	587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 
	661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 
	761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 
	859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 
	967, 971, 977, 983, 991, 997]
	q1 = candidates[random.randint(0,len(candidates)-1)]
	f.write(str(q1))
	f.close()

	return hash(q1)

def puzzleStart():

	encoded_word = init_word()
	key = init_key()

	received_msg=encoded_word*key
	print("Here is the product of two HASH-values: %d, enjoy the process."%received_msg)