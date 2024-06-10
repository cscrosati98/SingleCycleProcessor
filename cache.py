#!/usr/bin/env python3
#By Christopher Scrosati

"""
This code takes in hexadecimal addresses from the input file "memfile" , as well as the cache type, number of cacheways, cache size, and block size. Note that cache size and block size must be powers of 2
								python3 cache.py --type s --nway 1 --cache_size 256 --block_size 64 --memfile ./mem1.txt


"""
import os
import sys
import re
from pathlib import Path
import argparse
import string
import math

parser = argparse.ArgumentParser( 
prog = 'cache',
description = 'Cache Simulator',
)
parser.add_argument("--type", dest = 'mem_type', required=True) # input argument
parser.add_argument("--nway", dest = 'nway', required=False) # input argument
parser.add_argument("--cache_size", dest = 'cache_size', required=True) # input argument
parser.add_argument("--block_size", dest = 'block_size', required=True) # input argument
parser.add_argument("--memfile", dest = 'memfile', required=True) # input argument
args = parser.parse_args()

def hex2bin(strnum,length): #function used to convert hexadecimal strings to binary with a set number of bits
	num=int(strnum,16)
	return f'{num:0>{length}b}'
def po2(num): #checks if an int is a power of two and returns the result of the boolean
	num=math.log10(num)/math.log10(2)
	return math.ceil(num)==math.floor(num)
def cache_mem(memory, nway, c_size, b_size): #takes in cache parameters and a list of memeory addresses, processes them and outputs the cache result as an aggregated string
	result=""
	boffset_size=2
	membin=[]
	for line in memory:#convert hex to bin for processing
		if line!='\n':
			binlen=4*(len(line)-1)
			membin.append(hex2bin(line,binlen))
	index_size=int(math.log10((c_size/b_size)/nway)/math.log10(2)) #find segments for binary address
	woffset_size=int(math.log10(b_size/4)/math.log10(2))
	tag_size=binlen-index_size-woffset_size-boffset_size
	index_size=binlen-woffset_size-boffset_size
	woffset_size=binlen-boffset_size
	boffset_size=binlen
	i=0
	hit=0
	cache=[ [] for i in range(int((c_size/b_size)/nway))] #initialize nway cache
	for line in membin: #process the memory addresses
		lineint=int(line,2)
		tag_bits=line[0:tag_size]
		index_bits=line[tag_size:index_size]
		index=int(index_bits,2)
		if lineint%4!=0:#unaligned address
			res="U"
		else:
			if tag_bits in cache[index]:#cache hit
			    res="HIT"
			    hit=hit+1
			    indhit=cache[index].index(tag_bits)
			    cache[index].pop(indhit)
			    cache[index].append(tag_bits)
			else:#cache miss
			    res="MISS"
			    if len(cache[index])!=0:
			    	cache[index].pop(0)
			    cache[index].append(tag_bits)
		result=result+memory[i][0:len(memory[i])-1]+"|"+tag_bits+"|"+index_bits+"|"+str(index)+"|"+res+"\n"
		i=i+1
	result=result+"hit rate: "+str((hit/i)*100)
	return result
def main():
	if (args.mem_type=="s"):
		if(int(args.nway)<1):
			print("Error, you must specify a way size for cache greater than 0 if using an associative cache!")
	if not po2(int(args.cache_size)):
		print("Error, cache size input must be a power of 2!")
	if not po2(int(args.block_size)):
		print("Error, cache size input must be a power of 2!")
	if not (Path(args.memfile).is_file()):
		print("Error, source file must exist in specified directory!")
	if (Path("./cache.txt").is_file()):#check if file already exists, else ask to overwrite
		delfile=input("Cache Memory output file exists! Would you like to overwrite it? (Selecting N will exit the program) Y/N\n")
		if re.search("[yY]", delfile):
			os.system ("rm ./cache.txt")
		else:
			sys.exit()
	memfile_path=Path(args.memfile)
	if not(memfile_path.is_file()):#ensure file exists
		print("Error, cannot find file at location "+str(memfile_path.absolute()))
		sys.exit()
	with open(memfile_path, "r") as data: #read in memory file
		memory=data.readlines()
	data.close()
	if args.mem_type=="s":
		nway=int(args.nway)
	elif args.mem_type=="d":
		nway=1
	cache=cache_mem(memory, nway, int(args.cache_size), int(args.block_size))
	with open(Path("./cache.txt"), "w") as data: #read in memory file
		data.write(cache)
	data.close()
if __name__ == "__main__":
    sys.exit(main())