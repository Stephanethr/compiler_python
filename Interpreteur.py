# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 13:06:50 2023

@author: Salam
"""
import ctypes

class Pile():
    def __init__(self):
        self.mem = []
        self.p_mem = 0
       
    
    def empiler(self,valeur):
        self.mem.append(valeur)
        
    def depiler(self):
       return self.mem.pop()
   
    def ADD(self):
        som = self.mem.pop() + self.mem.pop()
        return self.empiler(som)
    
    def MUL(self):
        mult =self.mem.pop() * self.mem.pop()
        return self.empiler(mult)
    
    def SUB(self):
        soust =self.mem.pop() - self.mem.pop()
        return self.empiler(soust)
    
    def DIV(self):
        divi =self.mem.pop() // self.mem.pop()
        return self.empiler(divi)
    # cette fonction imprime le sommet et le depile de la liste
    def PRN(self):
        print(self.mem[-1])
        self.depiler()
    
    #
    def INN(self):
        val = int(input("donner la valeur: "))
        tmp = self.mem[-1]
        self.mem[tmp]=val
        self.depiler()
        
        
    def INT(self,c):
        self.mem = [0]*abs(c)
        
        
    #empile la valeur de v
    def LDI(self,v):
        self.empiler(v)
        
    def LDV (self):
       val=self.mem.pop()
       self.empiler(self.mem[val])
    
        
    #empile l'adresse de a
    def LDA (self,a):
        self.empiler(a)
    
    def STO(self):
        
        value = self.mem.pop()  # Dépile la valeur à stocker
        value2 = int(self.mem.pop())  # Dépile l'adresse où stocker la valeur
       
        self.mem[value2]=value
        
    
    def BRN(self,i):
        arg = self.p_code[i]
        if arg =="ADD":
            self.ADD()
        elif arg == "SUB":
            self.SUB()
        elif arg == "MUL":
            self.MUL()
        elif arg == "DIV":
            self.DIV()
        elif arg == "PRN":
            self.PRN()
        elif arg == "INN":
            self.INN()
        elif arg == "INT":
            self.INT()
        elif arg == "LDI":
            self.LDI ()  
        elif arg == "LDV":
            self.LDV()
        elif arg == "LDA":
            self.LDA()
        elif arg == "STO":
            self.STO()
    def BZE(self,i):
        z =  self.mem.pop()
        if z == 0:
            self.BRN(i) 
            
    def EQL(self):
       if self.mem[-1]==self.mem[-2]:
           res = 1
       else:
           res = 0
       self.empiler(res)
    
        
           
    
    def __str__(self):
    		ch = ''
    		for x in self.mem:
    			ch = "|\t" + str(x) + "\t|" + "\n" + ch
    		ch = "\nEtat de la pile:\n" + ch
    		return ch
    


def interpreteur(pcode):
    p = Pile()
    
    for instructions in pcode:
        instruction = instructions.split(" ")
        inst = instruction[0]
        print(inst)
        print(len(instruction))
        arg = -1
        if (len(instruction) > 1):
            arg = int(instruction[1])
        
        if inst == "INT":
            p.INT(arg)
        elif inst == "LDA":
            p.LDA(arg)
        elif inst == "INN":
            p.INN()
        if inst =="ADD":
            p.ADD()
        elif inst == "SUB":
            p.SUB()
        elif inst == "MUL":
            p.MUL()
        elif inst == "DIV":
            p.DIV()
        elif inst == "PRN":
            p.PRN()
        elif inst == "STO":
            p.STO()
        elif inst == "BZE":
            p.BZE(arg)
        elif inst == "BRN":
            p.BRN(arg)
        elif inst == "EQL":
            p.EQL()
        

        print(p)


def main():
    pcodes = [
        "INT 2",
        "LDA 0",
        "INN",
        "LDA 1",
        "LDA 0",
        "LDV"
        "ADD",
        "STO",
        "LDA 0",
        "LDV",
        "LDI 0",
        "EQL",
        "BZE 1",
        "LDA 1",
        "LDV"
        "PRN"
        
        ]
    interpreteur(pcodes)
    
main()
    
p = Pile()
p.empiler(5)
p.empiler(7)
p.empiler(1)
print(p)
p.LDV()
print("teste ldv")
print(p)


 