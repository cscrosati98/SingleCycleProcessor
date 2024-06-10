
**singleCycleProcessor.py:**
<br/>
This code takes in binary code and executes the given file, outputting both the registers at each cycle as well as the data path control result. Input MUST be 32 bits.
<br/>
*<p align="center">python3 singleCycleProcessor.py -in ./alpha.bin -mem ./memory.txt*
</p>

<br/><br/>
**mips2bin.py:**
<br/>
This code takes in a MIPS program and converts it to binary using regex and simple python dictionaries, as well as some parsing and string manipulation.
Simply establish the input and output file, for example:
<br/>
*<p align="center">python3 mips2bin.py -input ./test.asm -output ./out_code.txt*
</p>

<br/><br/>
**cache.py:**
<br/>
This code takes in hexadecimal addresses from the input file "memfile" , as well as the cache type, number of cacheways, cache size, and block size. Note that cache size and block size must be powers of 2
<br/>
*<p align="center">python3 cache.py --type s --nway 1 --cache_size 256 --block_size 64 --memfile ./mem1.txt*
</p>
