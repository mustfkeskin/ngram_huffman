#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 08:51:52 2018

@author: mustafa
"""

from huffman_ngram import HuffmanCoding
import os
import pandas as pd

'''
input_path = "/Users/mustafa/Downloads/text_compression_with_deep_learning-master/alice.txt"
output_path = "/Users/mustafa/Downloads/text_compression_with_deep_learning-master/alice.bin"
header_path = "/Users/mustafa/Downloads/text_compression_with_deep_learning-master/alice.header"

h = HuffmanCoding(input_path)
output_path = h.compress()
h.decompress(output_path, header_path)
'''




#input file path
directory = "/Users/mustafa/Downloads/text_compression_with_deep_learning-master/"
dirs =  os.listdir(directory)

for filename in dirs:
    if not filename.startswith(".DS_Store") and filename.endswith("txt"):
        print(filename)
        
        input_path = directory + filename
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + ".bin"
        header_path = filename + ".header"
        
        h = HuffmanCoding(input_path)
        
        output_path = h.compress()
        
        h.decompress(output_path, header_path)
       
        #print "Codes: " + str(h.codes)    
        print(os.path.getsize(output_path))
        print "                           "
        print "---------------------------"
        print "                           "  
    

df = pd.DataFrame()  
df["filename"] = ""
df["size"] = ""  
dirs =  os.listdir(directory)
for filename in dirs:
    if not filename.startswith(".DS_Store"):
        print(filename, os.path.getsize(directory + filename))  
        df = df.append({'filename' : filename, 'size': os.path.getsize(directory + filename)}, ignore_index=True)
           
df.sort_values(["filename"]).to_csv("/Users/mustafa/Downloads/text_compression_with_deep_learning-master/sonuclar.csv", index=False) 
print df.sort_values(["filename"])