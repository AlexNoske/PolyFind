import os
import networkx as nx
from tkinter import *
from tkinter.ttk import *
import re
import math
import argparse
import itertools
import subprocess
import sys
import tkinter.scrolledtext as tkst
def powerGraph(g,n):
    base=g.copy()
    for i in range(0,n-1):
        base=nx.tensor_product(base,g)
    return base.to_directed()
def product(g1,g2):
    base=nx.tensor_product(g1,g2)
    base = nx.convert_node_labels_to_integers(base, first_label=0, ordering='default', label_attribute=None)
    return base.to_directed()
def convertToUndirected(G):
    return G.to_directed()
def makeGraphs(string):
    instructions = string.split(",")
    graphs=[]
    for instruction in instructions:
        if instruction[0]=="K":
            instruction = instruction[1:]
            graphs.append(nx.complete_graph(int(instruction)))
        if instruction[0]=="C":
            instruction = instruction[1:]
            graphs.append(nx.cycle_graph(int(instruction)))
    return mergeGraphs(graphs)
def mergeGraphs(graphs):
    base = graphs[0]
    index=0
    for graph in graphs:
        graph = graph.to_directed()
        if index>0:
            base = product(base.to_directed(),graph.to_directed()).to_directed()
        index+=1
    return base.to_directed()
def polyCustom(polyInput,noNodesG1,noNodesG2):
    
    functionList = []
    constraints=[]
    data = polyInput.split("^")
    for line in data:
        sides = line.split("=")
        if "(" in sides[0]:
            functionInputs = sides[0][sides[0].index("(")+1:sides[0].index(")")]
            functionArity = len(functionInputs.split(","))
            functionList.append([sides[0][0],functionArity])
        if "(" in sides[1]:
            functionInputs = sides[1][sides[1].index("(")+1:sides[1].index(")")]
            functionArity = len(functionInputs.split(","))
            functionList.append([sides[1][0],functionArity])
    if not checkFunctions(functionList):
        return "error"
    for line in data:
        constraint="cnf(poly,axiom,"
        sides = line.split("=")
        if "(" in sides[0] and "(" in sides[1]:
            constraints.append(constraint+line + ").\n")
        elif "(" in sides[0]:
            constraint += line
            if (noNodesG2<noNodesG1):
                for i in range(noNodesG2,noNodesG1):
                    constraint = constraint + "|"+sides[1][0]+"=" + str(i)
            elif (noNodesG1<noNodesG2):
                for i in range(noNodesG1,noNodesG2):
                    constraint = constraint + "|"+sides[1][0]+"=" + str(i)        
            constraint = constraint + ").\n"
            constraints.append(constraint)
    for function in functionList:
        constraint = "cnf(preserves,axiom,("
        minia=""
        minib=""
        for i in range (0,int(function[1])):
            constraint = constraint + "~gr(X" + str(i*2) +",X"+ str(i*2+1)+")|"
            minia=minia+"X"+str(2*i)+","
            minib=minib+"X"+str(2*i+1)+","
        minia = minia[:-1]
        minib = minib[:-1]
        
        constraint = constraint +"grb("+function[0]+"("+minia+"),"+function[0]+"("+minib+")))).\n"
        constraints.append(constraint)
    return list(dict.fromkeys(constraints))
def checkFunctions(functions):
    for function in functions:
        for functionb in functions:
            if function[0] == functionb[0]:
                if function[1] != functionb[1]:
                    return False
    return True
def finpolFunctions(G1,G2,v,m,outputArea,custom):

    p=0
    symmetric=True

    answer=""
    text_file = open("para.txt", "w")
    noNodesG1 = len(G1.nodes())
    noNodesG2 = len(G2.nodes())
    edgesG1 = []
    edgesG2 = []
    n=0
    for edge in G1.edges():
        edgesG1.append([edge[0],edge[1]])
    for edge in G2.edges():
        edgesG2.append([edge[0],edge[1]])
    ### custom polys
    if (v=="siggers"):
        for line in polySiggers(noNodesG1,noNodesG2):
            text_file.write(line)
        n=4
    elif (v=="malcev"):
        for line in polyMalcev(noNodesG1,noNodesG2):
            text_file.write(line)
        n=3
    elif (v=="nu3"):
        for line in polyNU3(noNodesG1,noNodesG2):
            text_file.write(line)
        n=3
    elif (v=="nu4"):
        for line in polyNU4(noNodesG1,noNodesG2):
            text_file.write(line)
        n=4
    elif (v=="nu5"):
        for line in polyNU5(noNodesG1,noNodesG2):
            text_file.write(line)
        n=5
    elif (v=="wnu2"):
        for line in polyWnu2(noNodesG1,noNodesG2):
            text_file.write(line)
        n=2
    elif (v=="wnu3"):
        for line in polyWnu3(noNodesG1,noNodesG2):
            text_file.write(line)
        n=3
    elif (v=="wnu4"):
        for line in polyWnu4(noNodesG1,noNodesG2):
            text_file.write(line)
        n=4
    elif (v=="wnu5"):
        for line in polyWnu5(noNodesG1,noNodesG2):
            text_file.write(line)
        n=5
    elif (v=="2sml"):
        for line in poly2sml(noNodesG1,noNodesG2):
            text_file.write(line)
        n=2
    elif (v=="sml"):
        for line in polysml(noNodesG1,noNodesG2):
            text_file.write(line)
        n=2
    elif (v=="edge4"):
        for line in polyEdge4(noNodesG1,noNodesG2):
            text_file.write(line)
        n=4
    elif (v=="edge5"):
        for line in polyEdge5(noNodesG1,noNodesG2):
            text_file.write(line)
        n=5
    elif (v=="omit12"):
        for line in polyOmit12(noNodesG1,noNodesG2):
            text_file.write(line)
        n=4
    elif (v=="ts4"):
        for line in polyTs4(noNodesG1,noNodesG2):
            text_file.write(line)
        n=4
    elif (v=="ts3"):
        for line in polyTs3(noNodesG1,noNodesG2):
            text_file.write(line)
        n=3
    elif (v=="none"):
        p=0
    elif (v=="custom"):
        try:
            for line in polyCustom(custom,noNodesG1,noNodesG2):

                if line=="error":
                    raise 
                text_file.write(line)
        except:
            print("fail")
    else: #something went wrong
        p=0

    maxN = max(noNodesG1,noNodesG2)
    for x in range(0,maxN):
        for y in range(0,maxN):
            if [x,y] in edgesG1:
                text_file.write("cnf(graph,axiom,gr("+str(x)+","+str(y)+")).\n")
            else:
                text_file.write("cnf(graph,axiom,~gr("+str(x)+","+str(y)+")).\n")
    for x in range(0,maxN):
        for y in range(0,maxN):
            if [x,y] in edgesG2:
                text_file.write("cnf(graph,axiom,grb("+str(x)+","+str(y)+")).\n")
            else:
                text_file.write("cnf(graph,axiom,~grb("+str(x)+","+str(y)+")).\n")
    constraint = "cnf(elems,axiom,("
    for i in range(0,maxN):
        constraint = constraint + "X="+str(i)+"|"
    constraint = constraint[:-1]
    constraint=constraint + ")).\n"
    text_file.write(constraint)
    constraint = "cnf(preserves,axiom,("
    minia=""
    minib=""
    for i in range (0,int(n)):
        constraint = constraint + "~gr(X" + str(i*2) +",X"+ str(i*2+1)+")|"
        minia=minia+"X"+str(2*i)+","
        minib=minib+"X"+str(2*i+1)+","
    minia = minia[:-1]
    minib = minib[:-1]
    
    constraint = constraint +"grb(t("+minia+"),t("+minib+")))).\n"
    if (not v =="custom" and not v=="none"):
        text_file.write(constraint)
    if v=="omit12":
        n-=1
        minia=""
        minib=""
        for i in range (0,int(n)):
            constraint = constraint + "~gr(X" + str(i*2) +",X"+ str(i*2+1)+")|"
            minia=minia+"X"+str(2*i)+","
            minib=minib+"X"+str(2*i+1)+","
        minia = minia[:-1]
        minib = minib[:-1]
        constraint = constraint +"grb(s("+minia+"),s("+minib+")))).\n"
        text_file.write(constraint)
    isModel = True
    text_file.close()
    #create a bat file to do it for you
    if int(m)==1:
        result= (subprocess.check_output(['paradox.exe','para.txt','--model']))
    else :
        result= (subprocess.check_output(['paradox.exe','para.txt']))
    
    result = result.decode()
    resultString=""
    for char in result:
        resultString+=char
    resultString=resultString.split("\n")
    if not (outputArea=="stdout"):
        outputArea.config(state=NORMAL)
        outputArea.delete('1.0', END)
        for line in resultString:
            if ("Satisfiable" in line) or ("Unsatisfiable" in line):
                outputArea.insert(INSERT,line)
            try:
                if "= !" in line:
                    outputArea.insert(INSERT,re.sub('[!]', '', line) +"\n")
            except:
                p=0
        outputArea.config(state=DISABLED)
    else:
        for line in resultString:
            if ("Satisfiable" in line) or ("Unsatisfiable" in line):
                print(line)
            try:
                if "= !" in line:
                    print(re.sub('[!]', '', line))
            except:
                p=0
        
def polySiggers(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(X,X,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"

    
    #unclear if this constraint is in siggers definition
    constraints.append(constraint)

    
    constraints.append("cnf(sml,axiom, t(X,Y,X,Z)=t(Y,X,Z,Y)).\n")
    constraint = "cnf(sml,axiom,"
    for i in range(0,noNodesG2):
        constraint=constraint + "t(X,Y,Z,P)=" +str(i) +"|"
    constraint = constraint[:-1]
    constraint=constraint + ").\n"
    constraints.append(constraint)
    return constraints
def polyNU3(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(Y,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(X,Y,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(X,X,Y)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"
    constraints.append(constraint)
    return constraints
def polyNU4(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(Y,X,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(X,Y,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(X,X,Y,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(X,X,X,Y)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"
    constraints.append(constraint)
    return constraints
def polyNU5(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(Y,X,X,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(X,Y,X,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(X,X,Y,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(X,X,X,Y,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(X,X,X,X,Y)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"
    constraints.append(constraint)
    return constraints
#different polymorphisums constraints
def poly2sml(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    constraints.append("cnf(sml,axiom,t(X,Y)=t(Y,X)).\n")
    constraints.append("cnf(sml,axiom,t(X,t(X,Y))=t(X,Y)).\n")
    return constraints
def polysml(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    constraints.append("cnf(sml,axiom,t(X,Y)=t(Y,X)).\n")
    constraints.append("cnf(sml,axiom,t(X,t(X,Z))=t(t(X,Y),Z)).\n")
    return constraints
def polyWnu2(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint) 
    constraints.append("cnf(wnu,axiom,t(X,Y)=t(Y,X)).\n")
    return constraints
def polyWnu3(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(X,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint) 
    constraints.append("cnf(wnu,axiom,t(X,X,Y)=t(Y,X,X)).\n")
    constraints.append("cnf(wnu,axiom,t(X,X,Y)=t(X,Y,X)).\n")
    return constraints
def polyWnu4(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(X,X,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint) 
    constraints.append("cnf(wnu,axiom,t(Y,X,X,X)=t(X,Y,X,X)).\n")
    constraints.append("cnf(wnu,axiom,t(X,Y,X,X)=t(X,X,Y,X)).\n")
    constraints.append("cnf(wnu,axiom,t(X,X,Y,X)=t(X,X,X,Y)).\n")
    return constraints
def polyWnu5(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(X,X,X,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint) 
    constraints.append("cnf(wnu,axiom,t(Y,X,X,X,X)=t(X,Y,X,X,X)).\n")
    constraints.append("cnf(wnu,axiom,t(X,Y,X,X,X)=t(X,X,Y,X,X)).\n")
    constraints.append("cnf(wnu,axiom,t(X,X,Y,X,X)=t(X,X,X,Y,X)).\n")
    constraints.append("cnf(wnu,axiom,t(X,X,X,Y,X)=t(X,X,X,X,Y)).\n")
    return constraints
def polyTs3(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(X,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    constraints.append("cnf(wnu,axiom,t(X,Y,Z)=t(Y,X,Z)).\n")
    constraints.append("cnf(wnu,axiom,t(X,Y,Z)=t(Y,Z,X)).\n")
    constraints.append("cnf(wnu,axiom,t(X,Y,Z)=t(X,Z,Y)).\n")
    constraints.append("cnf(wnu,axiom,t(X,Y,Z)=t(Z,Y,X)).\n")
    constraints.append("cnf(wnu,axiom,t(X,Y,Z)=t(Z,X,Y)).\n")
    constraints.append("cnf(wnu,axiom,t(X,X,Y)=t(X,Y,Y)).\n")
    return constraints
def polyOmit12(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,s(X,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    constraints.append("cnf(wnu,axiom,s(X,X,Y)=s(Y,X,X)).\n")
    constraints.append("cnf(wnu,axiom,s(X,X,Y)=s(X,Y,X)).\n")
    constraint="cnf(sml,axiom,t(X,X,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    constraints.append("cnf(wnu,axiom,t(Y,X,X,X)=t(X,Y,X,X)).\n")
    constraints.append("cnf(wnu,axiom,t(X,Y,X,X)=t(X,X,Y,X)).\n")
    constraints.append("cnf(wnu,axiom,t(X,X,Y,X)=t(X,X,X,Y)).\n")
    constraints.append("cnf(wnu,axiom,s(X,X,Y)=t(X,X,X,Y)).\n")
    return constraints
def polyTs4(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(X,X,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    constraints.append("cnf(wnu,axiom,t(X,Y,Z,V)=t(Y,X,Z,V)).\n")
    constraints.append("cnf(wnu,axiom,t(X,Y,Z,V)=t(X,Z,Y,V)).\n")
    constraints.append("cnf(wnu,axiom,t(X,Y,Z,V)=t(X,Y,V,Z)).\n")
    constraints.append("cnf(wnu,axiom,t(X,X,Y,Z)=t(X,Y,Y,Z)).\n")
    constraints.append("cnf(wnu,axiom,t(X,X,X,Y)=t(X,X,Y,Y)).\n")
    constraints.append("cnf(wnu,axiom,t(X,X,X,Y)=t(X,Y,Y,Y)).\n")
    return constraints
def polyArith(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(X,Y,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(Y,X,X)=Y"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|Y=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|Y=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(X,X,Y)=Y"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|Y=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|Y=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    return constraints
def polyEdge4(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(Y,Y,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(Y,X,Y,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(X,X,X,Y)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    return constraints
def polyEdge5(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(Y,Y,X,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(Y,X,Y,X,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(X,X,X,Y,X)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(X,Y,X,X,Y)=X"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|X=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|X=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    return constraints
def polyMalcev(noNodesG1,noNodesG2):
    constraints=[]
    constraint="cnf(sml,axiom,t(Y,X,X)=Y"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|Y=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|Y=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    constraint="cnf(sml,axiom,t(X,X,Y)=Y"
    if (noNodesG2<noNodesG1):
        for i in range(noNodesG2,noNodesG1):
            constraint = constraint + "|Y=" + str(i)
    elif (noNodesG1<noNodesG2):
        for i in range(noNodesG1,noNodesG2):
            constraint = constraint + "|Y=" + str(i)        
    constraint = constraint + ").\n"   
    constraints.append(constraint)
    return constraints
#input example: f(X,Y,Z)=Z|f(X,Z,Z)=f(X,Z,X)
#split base on |
def makeGraphFromFile(data):
    for line in data:
        for let in line:
            let= re.sub('\n',  '',    let)
    G = nx.Graph().to_directed()
    for n in range(0,len(data)):
        G.add_node(n)
    for i in range(0,len(data)):
        for j in range(0,len(data)):
            if data[i][j]=='1':
                G.add_edge(i,j)
    return G
def getGraph(file_name):
    fileData = open(file_name, "r")
    data = fileData.read()
    fileData.close()
    data=data.rstrip()
    datalist = data.split(";")
    no = len(datalist)
    final_data=[]
    for line in datalist:
        final_data.append(line.split(","))

    for x in range(0,len(final_data)):
        for y in range(0,len(final_data)):
            if not len(final_data[x])==no:
                raise 
            if final_data[x][y]!="0" and final_data[x][y]!="1":
                
                raise
    graph = makeGraphFromFile(final_data)   
    return graph   
def getInputs(G1,G2,v,m,outputArea,custom):
    Graph1 = None
    Graph2 = None
    if "." in G1:
        try:
            Graph1 = getGraph(G1) 
        except:
            outputArea.config(state=NORMAL)
            outputArea.delete('1.0', END)

            outputArea.insert(INSERT,"Fail problem with graph 1")
            outputArea.config(state=DISABLED)
            sys.exit()
    else:
        if len (re.sub(r'[C,K][0-9]+(,[C,K][0-9]+)*', "", G1))>0:
            outputArea.config(state=NORMAL)
            outputArea.delete('1.0', END)

            outputArea.insert(INSERT,"Fail problem with graph 1")
            outputArea.config(state=DISABLED)
            sys.exit()
        else:
            Graph1 = makeGraphs(G1)
    if "." in G2:
        try:
            Graph2 = getGraph(G2)
        except:
            outputArea.config(state=NORMAL)
            outputArea.delete('1.0', END)

            outputArea.insert(INSERT,"Fail problem with graph 2")
            outputArea.config(state=DISABLED)
            sys.exit()
    else:
        if len (re.sub(r'[C,K][0-9]+(,[C,K][0-9]+)*', "", G1))>0:
            outputArea.config(state=NORMAL)
            outputArea.delete('1.0', END)

            outputArea.insert(INSERT,"Fail problem with graph 2")
            outputArea.config(state=DISABLED)
            sys.exit()
        else:
            Graph2 = makeGraphs(G2)
    
    finpolFunctions(Graph1,Graph2,v,m,outputArea,custom)

    
def main(G1,G2,v,m,pC):
    if G1=="launchGUI":
        master = Tk()
        master.title("PolyFind")
        master.geometry('600x300')
        lbl = Label(master, text="Graph being raised to the power")
        lbl.grid(column=0, row=0)
        lb2 = Label(master, text="Graph being mapped to")
        lb2.grid(column=1, row=0)
        lb3 = Label(master, text="Type of Polymorphism")
        lb3.grid(column=0, row=3)
        lb3 = Label(master, text="If custom")
        lb3.grid(column=2, row=2)
        txt = Entry(master,width=20)
        txt.grid(column=0, row=1)
        txt2 = Entry(master,width=20)
        txt2.grid(column=1, row=1)
        txt3 = Entry(master,width=20)
        txt3.grid(column=2, row=3)
        var1 = IntVar()
        Checkbutton(master, text="Return example", variable=var1).grid(column=1,row=4, sticky=W)
        combo = Combobox(master)    
        combo['values'] = ("none","custom","malcev", "nu3","nu4","nu5","edge4","edge5","bw","sml","2sml","ts4","ts3","wnu2","wnu3","wnu4","wnu5","siggers")
        combo.current(0)
        combo.grid(column=1, row=3)
        editArea = tkst.ScrolledText(master,wrap   = WORD,width  = 30,height = 10)
        editArea.config(state=DISABLED)
        editArea.grid(column=1, row=5)
        btn = Button(master, text="Find Polymorphism", command=lambda: getInputs(txt.get(),txt2.get(),combo.get(),var1.get(),editArea,txt3.get()))
        btn.grid(column=2, row=4)
    else:
        getInputs(G1,G2,v,m,"stdout",pC)

    
parser = argparse.ArgumentParser(description='parser')
parser.add_argument('-G1', metavar='string', required=True,
                        help='the path to workspace')
parser.add_argument('-G2', metavar='string', required=True,
                        help='path to dem')
parser.add_argument('-v', metavar='string', required=True,
                        help='path to dem')
parser.add_argument('-m', metavar='string', required=True,
                        help='path to dem')
parser.add_argument('-pC', metavar='string', required=True,
                        help='path to dem')
args = None
try :
    args = parser.parse_args()
    main(G1=args.G1, G2=args.G2,v=args.v,m=args.m,pC=args.pC)
except:
    main("launchGUI", "launchGUI", "launchGUI", "launchGUI","launchGUI")



