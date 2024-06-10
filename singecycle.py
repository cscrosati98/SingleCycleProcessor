##!/usr/bin/env python3
#By Christopher Scrosati

"""
This code takes in a MIPS program and converts it to binary using regex and simple python dictionaries, as well as some parsing and string manipulation.
Simply establish the input and output file, for example:
								python3 mips2bin.py -input ./test.asm -output ./out_code.txt

"""
import os
import sys
import re
from pathlib import Path
import argparse
import string
import math

##parser = argparse.ArgumentParser( 
##prog = 'project3',
##description = 'Single Cycle Processor',
##)
##parser.add_argument("--file", dest = 'input', required=True) # input argument
##parser.add_argument("-output", dest = 'output', required=True) # input argument
##args = parser.parse_args()

# parameters:
#text - a single word string
#returns:
#text - a single word string
mipsreg={ #dictionary that uses the non-numerica values for registers as keys
"zero":0,
"v0":2,
"v1":3,
"a0":4,
"a1":5,
"a2":6,
"a3":7,
"t0":8,
"t1":9,
"t2":10,
"t3":11,
"t4":12,
"t5":13,
"t6":14,
"t7":15,
"s0":16,
"s1":17,
"s2":18,
"s3":19,
"s4":20,
"s5":21,
"s6":22,
"s7":23,
"t8":24,
"t9":25,
"gp":28,
"sp":29,
"fp":30,
"ra":31
}
mipsname = { #a nested dictionary that uses the function name as a key, and the corresponding information for this function in binary, such as op codes, types, and, funciton codes
	"add" :{
	"type" : "R",
	"opcode":"000000",
	"funct" :"100000",
	
	},
	"sub" :{
	"type" : "R",
	"opcode":"000000",
	"funct" :"100010",
	},
	"sll":{
	"type" : "R",
	"opcode":"000000",
	"funct" :"000000",
	},
	"srl":{
	"type" : "R",
	"opcode":"000000",
	"funct" :"000010",
	},
	"slt":{
	"type" : "R",
	"opcode":"000000",
	"funct" :"010101",
	},
	"addi":{
	"type" : "I",
	"opcode":"001000",
	},
	"beq":{
	"type" : "I",
	"opcode":"000100",
	},
	"bne":{
	"type" : "I",
	"opcode":"000101",
	},
	"lw":{
	"type" : "I",
	"opcode":"100011",
	},
	"sw":{
	"type" : "I",
	"opcode":"101011",
	}
}

def datapath(line): #converts a split line of mips code to binary
	opcode=line[0:6]
	reg1=line[6:11]
	reg2=line[11:16]
	reg3=line[16:21]
	shamt=line[21:26]
	funct=line[26:32]
	
	print(opcode)
	print(reg1)
	print(reg2)
	print(reg3)
	print(shamt)
	print(funct)
	print(line)
	print(opcode+reg1+reg2+reg3+shamt+funct)
			
def main():
    #datapath("00100000000000010000000000000011")
    out_path=Path("./out_code.txt")
    if (out_path.is_file()):#check if file already exists, else ask to overwrite
            delfile=input("Output file exists! Would you like to overwrite it? (Selecting N will exit the program) Y/N\n")
            if re.search("[yY]", delfile):
                    os.system ("rm " + out_path)
            else:
                    sys.exit()
            
    file_path=Path(args.input)
    if not(file_path.is_file()):#ensure file exists
            print("Cannot find file at location"+str(file_path.absolute()))
    else:
            with open(out_path, "w") as output:
                    with open(file_path, "r") as data:
                            for line in data:
                                    if (line[0] != "\n"):#if not a comment
                                            res=datapath(line)
                                            if(res==-1):#if an error returns, print error message and exit file
                                                    output.write(("!!! invalid input !!!")+"\n")
                                                    data.close()
                                                    output.close()
                                                    return
                                            else:
                                                    output.write(res+"\n")#write output
                                    else:
                                            output.write("\n")#new line if comment
                    data.close()
            output.close()
                            


if __name__ == "__main__":
    sys.exit(main())
