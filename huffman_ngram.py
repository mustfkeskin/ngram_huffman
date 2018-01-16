#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 08:51:28 2018

@author: mustafa
"""

import heapq
import os
import csv

class HeapNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __cmp__(self, other):
        if(other == None):
            return -1
        if(not isinstance(other, HeapNode)):
            return -1
        return self.freq > other.freq


class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    # functions for compression:
        
        
    def make_frequency_dict(self, text):
        frequency = {}
        for i in range(len(text) - 3):
            
            character = text[i]
            if not character in frequency:
                frequency[character] = 1
            frequency[character] += 1
            
            
            character = text[i : i + 2]
            if not character in frequency:
                frequency[character] = 1
            frequency[character] += 1
            
            
            character = text[i : i + 3]
            if not character in frequency:
                frequency[character] = 1
            frequency[character] += 1
            
        
        
        i += 1    
        character = text[i]
        if not character in frequency:
            frequency[character] = 1
        frequency[character] += 1
        
        character = text[i + 1]
        if not character in frequency:
            frequency[character] = 1
        frequency[character] += 1
        
        character = text[i + 2]
        if not character in frequency:
            frequency[character] = 1
        frequency[character] += 1
        
            
        character = text[i : i + 2]
        if not character in frequency:
            frequency[character] = 1
        frequency[character] += 1
        
        character = text[i + 1 : i + 3]
        if not character in frequency:
            frequency[character] = 1
        frequency[character] += 1
        
        
        character = text[i : i + 3]
        if not character in frequency:
            frequency[character] = 1
        frequency[character] += 1
        
        
        total = sum(frequency.values())
        length = len(frequency)
        mean = float(total) / length
        frequency  = dict((k, v) for k, v in frequency.items() if v >= mean or len(k) == 1)
        
        
        
        
        print "ilk ortalama: " + str(mean)
        print "ilk uzunluk: " + str(length)
        print "Son ortalama: " + str(float(sum(frequency.values())) / len(frequency))
        print "Son uzunluk: " + str(len(frequency))
               
        #print frequency
        return frequency
    

    def make_heap(self, frequency):
        for key in frequency:
            node = HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while(len(self.heap)>1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)


    def make_codes_helper(self, root, current_code):
        if(root == None):
            return

        if(root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")


    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)


    def get_encoded_text(self, text, dictionary):
        encoded_text = ""
        i = 0
        while i < len(text) - 3:
            
             
            if(text[i : i + 3] in dictionary):
                character = text[i : i + 3]
                encoded_text += self.codes[character]
                i += 3
            
            elif(text[i : i + 2] in dictionary):
                character = text[i : i + 2]
                encoded_text += self.codes[character]
                i += 2
            
            elif(text[i] in dictionary):
                character = text[i]
                encoded_text += self.codes[character]
                i += 1
       
        # son 3 karakter için n gram hesabı
        
        if(i < len(text) - 3 and text[i : i + 3] in dictionary):
            character = text[i : i + 3]
            encoded_text += self.codes[character]
               
        if(i < len(text) - 2 and text[i : i + 2] in dictionary):
            character = text[i : i + 2]
            encoded_text += self.codes[character]
       
        if(i < len(text) - 3 and text[i + 1 : i + 3] in dictionary):
            character = text[i + 1 : i + 3]
            encoded_text += self.codes[character]
                
        if(i < len(text) and text[i] in dictionary):
            character = text[i]
            encoded_text += self.codes[character]
        
        if(i < len(text) - 1 and text[i + 1] in dictionary):
            character = text[i + 1]
            encoded_text += self.codes[character]
        
        if(i < len(text) - 2 and text[i + 2] in dictionary):
            character = text[i + 2]
            encoded_text += self.codes[character]
                
                
        i = len(text)        
        #print encoded_text
              
            
        return encoded_text


    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text


    def get_byte_array(self, padded_encoded_text):
        if(len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b


    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            frequency = self.make_frequency_dict(text)
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()

            encoded_text = self.get_encoded_text(text, frequency)
            padded_encoded_text = self.pad_encoded_text(encoded_text)

            b = self.get_byte_array(padded_encoded_text)
            output.write(bytes(b))
            
        header_path = filename + ".header"    
        w = csv.writer(open(header_path, "w"))
        for key, val in self.reverse_mapping.items():
            w.writerow([key, val])  
            
        #print "Codes: " + str(self.codes)        
        print("Compressed")
        return output_path


    """ functions for decompression: """

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-1*extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text


    def decompress(self, compressed_path, header_path):
        filename, file_extension = os.path.splitext(compressed_path)
        output_path = filename + "_decompressed" + ".txt"
        
        with open(header_path) as header:
            self.reverse_mapping = dict(filter(None, csv.reader(header)))

        with open(compressed_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""

            byte = file.read(1)
            while(byte != ""):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)
            output.write(decompressed_text)

        print("Decompressed")
        return output_path