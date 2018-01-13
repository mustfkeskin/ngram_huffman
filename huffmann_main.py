#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 08:51:52 2018

@author: mustafa
"""

from huffman_ngram import HuffmanCoding
import os

#input file path
directory = "/Users/mustafa/Downloads/text_compression_with_deep_learning-master/"
dirs =  os.listdir(directory)

for filename in dirs:
    if not filename.startswith(".DS_Store") and filename.endswith("txt"):
        print(filename)
        
        path = directory + filename
        h = HuffmanCoding(path)
        output_path = h.compress()
        h.decompress(output_path)
       
        print "Codes: " + str(h.codes)    
        print(os.path.getsize(output_path))
        print "                           "
        print "---------------------------"
        print "                           "