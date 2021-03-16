#!/usr/bin/env python3
#include functionality to check for obo file and download+decompress 
import os
import subprocess
import urllib.request


class Term:
    def __init__(self, id):
        self.id = id
        self.parents = []
        self.children = []
        self.details = []
        self.namespace = []
    def __str__(self):
        return "{0} {1}".format(self.id, self.details)
    def __eq__(self, other):
        if not isinstance(other, Term):
            return False
        else:
            return self.id == other.id
    def __repr__(self):
        return self.__str__()
    def add_parent(self, parent):
        self.parents.append(parent)
    def add_children(self, child):
        self.children.append(child)
    def add_details(self, dets):
        self.details.append(dets)
    def add_namespace(self, space):
        self.namespace.append(space)
def obodownload():
    if os.path.exists('go-basic.obo'):
        return "file present"
    else:
        try:
            urllib.request.urlretrieve("http://purl.obolibrary.org/obo/go/go-basic.obo", "go-basic.obo")
        except urllib.error.URLError:
            print("error downloading")
        return "go-basic.obo download complete"
def go_lookup():
    obodownload()
    tree = {}
    #first have to clean the go-basic.obo file
    try:
        with open("./go-basic.obo", "r") as handle:
            terms = handle.read()
    except IOError as err:
        print(err)
    #seperate files via the double linefeed
    sep_terms = terms.split('\n\n') #splits file into chunks of GO terms and details
    filtered = sep_terms[1:len(sep_terms)-6] #filter unnecessary info from top and bottom of obo file, bottom is empty space
    for i in range(len(filtered)):  #for every [Term]
        if 'is_obsolete: true' in filtered[i]:  #don't want obsolete terms
            continue
        else:
            n = Term(filtered[i].split('\n')[1][4:])    #grabs just the go id itself, makes an Object of Term class
            chunklines = filtered[i].split('\n')
            for thing in chunklines:   #for every line in the chunk
                if 'is_a: ' != thing[:6]:   #searches for parents by looking for the is_a indicator
                    continue
                else:
                    n.add_parent(thing[6:16])   #for the moment, only inlcudes parent id, might make it easier to search parents of parents
            n.add_details(chunklines[2][6:])    #adds the 'name' of the term not the 'def'
            n.add_namespace(chunklines[3][11:]) #adds the namespace to object, useful for comparing two terms to maek sure they're in the same graph
            tree[n.id] = n  #inserts object into tree with the GO id as the key and object as value
    for id in tree: #populates the children list attribute
        for parent in tree[id].parents:
            tree[parent].add_children(id)
    for id in tree: #turned out to be very important to do this later
        if len(tree[id].parents) == 0:
            tree[id].add_parent('*')   #nodes that don't have parents get the * indicator
    return tree



