#!/usr/bin/env python3
#By Christopher Scrosati

"""
This code takes in binary code and executes the given file, outputting both the registers at each cycle as well as the data path control result. Input MUST be 32 bits. 
								python3 singleCycleProcessor.py -in ./alpha.bin -mem ./memory.txt

"""
import os
import sys
import re
from pathlib import Path
import argparse
import string
import math

parser = argparse.ArgumentParser( 
prog = 'singleCycleProcessor',
description = 'Single Cycle Proccessor',
)
parser.add_argument("-in", dest = 'input', required=True) # input argument
parser.add_argument("-mem", dest = 'mem', required=True) # input argument
args = parser.parse_args()
reg=[0,0,0,0,0,0,0,0,65536]
dest=[0,0] #result, address

def datapath(line,memory): #converts a split line of mips code to binary
	opcode=line[0:6]
	if opcode=="000000":
		rs=line[6:11]
		rt=line[11:16]
		rd=line[16:21]
		shamt=line[21:26]
		funct=line[26:32]
		if funct=="100000": #add
			dest[0]=reg[int(rs,2)]+reg[int(rt,2)] #result
			dest[1]=int(rd,2) #reg address
		elif funct=="100010": #sub
			dest[0]=reg[int(rs,2)]-reg[int(rt,2)]#result
			dest[1]=int(rd,2)#reg address
		dpath="100100010" #r-type control
		
	elif opcode=="001000": #addi
		rs=line[6:11]
		rt=line[11:16]
		immediate=line[16:32]
		if immediate[0]=="1":
			immediate=-1*((int(immediate,2)^65535)+1)
		else:
			immediate=int(immediate,2)
		dest[0]=reg[int(rs,2)] + immediate #result
		dest[1]=int(rt,2)#reg address
		dpath= "010100000" #i-type control
	elif opcode=="000100": #beq
		rs=line[6:11]
		rt=line[11:16]
		address=line[16:32]
		if address[0]=="1":
			address=-4*((int(address,2)^65535)+1)
		else:
			address=4*(int(address,2))
		if((reg[int(rs,2)]==reg[int(rt,2)])):
			 reg[8]=reg[8]+address#result
			 zbit="1"
		else: 
			zbit="0"
		return "X0X000101"+zbit
	elif opcode=="000101": #bne
		rs=line[6:11]
		rt=line[11:16]
		address=line[16:32]
		if address[0]=="1":
			address=-4*((int(address,2)^65535)+1)
		else:
			address=4*(int(address,2))
		if((reg[int(rs,2)]!=reg[int(rt,2)])):
			 reg[8]=reg[8]+address#result
			 zbit="0"
		else: 
			zbit="1"
		return "X0X000111"+zbit
	elif opcode=="100011": #lw
		rs=line[6:11]
		rt=line[11:16]
		offset=line[16:32]
		if offset[0]=="1":
			offset=-1*((int(offset,2)^65535)+1)
		else:
			offset=int(offset,2)
		address=int((reg[int(rs,2)]+offset)/4)
		if(address)>=len(memory):
			return "!!! Segmentation Fault !!!\r\n"
		if(memory[address]=="\n"):
			return "!!! Segmentation Fault !!!\r\n"
		address=int((reg[int(rs,2)]+offset)/4)
		if(address==0):
			zbit="0"
		else:
			zbit="1"
		dest[0]=int(memory[address])
		dest[1]=int(rt,2)
		return "011110000"+zbit
	elif opcode=="101011": #sw
		rs=line[6:11]
		rt=line[11:16]
		offset=line[16:32]
		if offset[0]=="1":
			offset=-1*((int(offset,2)^65535)+1)
		else:
			offset=int(offset,2)
		address=int((reg[int(rs,2)]+offset)/4)
		if(address)>=len(memory):
			return "!!! Segmentation Fault !!!\r\n"
		if(address==0):
			zbit="0"
		else:
			zbit="1"
		dest[0]=address
		dest[1]=int(rt,2)+100
		return "X1X001000"+zbit
		
	if dest[0]==0:
			dpath=dpath+"1"
	else:
			dpath=dpath+"0"
	return dpath

def registers(memory):
	if(dest[1]>99):
		dest[1]=dest[1]-100
		memory[dest[0]]=str(reg[dest[1]])+"\n"
	else:
		reg[dest[1]]=dest[0] #updates registers using values from previous cycle
	res=str(reg[8])
	for r in range(0,8):  #convert reg to string
		res=res+"|"+str(reg[r])
	return [res,memory]
def cycle(line,memory):
	res=registers(memory)
	memory=res[1] #update memory
	resreg=res[0] #update registers
	reg[8]=reg[8]+4 #increment pc counter
	resdp=datapath(line,memory) #create data path control string
	if(resdp=="!!! Segmentation Fault !!!\r\n"):
		return [-1,-1,-1]
	return [resreg,resdp,(reg[8]-65536)//4]
def main():
	out_reg=Path("./out_registers.txt")
	out_cont=Path("./out_control.txt")
	out_mem=Path("./out_memory.txt")
	if (out_reg.is_file()):#check if file already exists, else ask to overwrite
		delfile=input("Register output file exists! Would you like to overwrite it? (Selecting N will exit the program) Y/N\n")
		if re.search("[yY]", delfile):
			os.system ("rm " + str(out_reg))
		else:
			sys.exit()
	if (out_cont.is_file()):#check if file already exists, else ask to overwrite
		delfile=input("Control output file exists! Would you like to overwrite it? (Selecting N will exit the program) Y/N\n")
		if re.search("[yY]", delfile):
			os.system ("rm " + str(out_cont))
		else:
			sys.exit()
	if (out_mem.is_file()):#check if file already exists, else ask to overwrite
		delfile=input("Memory output file exists! Would you like to overwrite it? (Selecting N will exit the program) Y/N\n")
		if re.search("[yY]", delfile):
			os.system ("rm " + str(out_mem))
		else:
			sys.exit()
		
	file_path=Path(args.input)
	memory_file_path=Path(args.mem)
	if not(file_path.is_file()):#ensure file exists
		print("Cannot find file at location"+str(file_path.absolute()))
	else:
		with open(memory_file_path, "r") as data: #read in memory file
			memory=data.readlines()
		data.close()
		with open(file_path, "r") as inbin: #read in binary file
			input_inbin=inbin.readlines()
		inbin.close()
		datapath_file=register_file=""
		i=0
		cycle_count=0
		while (i<len(input_inbin)): #for each line of bin ,execute one clock cycle
			if(input_inbin[i]!=""):
				if cycle_count>=100:
					print("Error, more than 100 cycles have passed")
					break
				out=cycle(input_inbin[i],memory)
				if (out[0]==-1)|(out[2]>len(input_inbin)):
					register_file=register_file + "!!! Segmentation Fault !!!\r\n"
					datapath_file=datapath_file + "!!! Segmentation Fault !!!\r\n"
					break
				else:
					register_file=register_file + out[0] + "\n"
					datapath_file=datapath_file + out[1] + "\n"
					i=out[2]
					cycle_count=cycle_count+1
		register_file=register_file + registers(memory)[0] #additional partial cycle to update registers 
		with open(out_reg, "w") as outreg:
			outreg.write(register_file)#write output for register file
		outreg.close()
		with open(out_cont, "w") as outcont:
			outcont.write(datapath_file)#write output for datapath control
		outcont.close()
		with open(out_mem, "w") as outmem:
			for line in memory:
				outmem.write(line)#write output for datapath control
		outmem.close()
if __name__ == "__main__":
    sys.exit(main())
