import math
import sys
from itertools import count
import random
from subprocess import check_call
import os
from PIL import Image


class Factorization():

    def __init__(self) -> None:
        self.graph_description = []
        self.nodenames = set()
        self.edgeset = set()
        self.whitenode = ' [fixedsize=True, width=0.1, height=0.1, color = white, fontcolor = white, shape = circle]'
        self.blacknode = ' [color = black, style = filled, fontcolor = black, shape = circle]'
        self.one = ' [style=filled,color = black, fontcolor =black, shape = circle]'

    def prime_factors(self, n: int) -> list:
        """[Extracting prime factors]

        Args:
            n (int): [Integer]

        Returns:
            list: [list of prime factors]
        """
        L = []
        i = 2
        while n > 1:
            while n % i == 0:
                L.append(i)
                n = n/i
            i = i+1
        return L

    def pgcd(self, a:int, b:int)->int:
        """[the Greatest Common Divisor (GCD) of two integers A and B (Euclidean
        Algorithm)]

        Args:
            a (int): [Integer]
            b (int): [Integer]

        Returns:
            int: [greatest common divisor]
        """
        
        while b:
            a, b = b, a % b
        return a

    def pollardrho(self, n: int)->list:
        """[Pollard Rho factorization algorithm]

        Args:
            n (int): [number to factorize]

        Returns:
            list: [d (int): non-trivial factor, n//d]
        """
        f=lambda t:(t**2+1)
        x, y, d = 2, 2, 1
        while d == 1:
            x = f(x)%n
            y = f(f(y))%n
            d = self.pgcd(x-y, n)
        infos = [d, n//d]
        infos.sort()
        return infos

    def to_string(self, factors: list)-> str:
        ""
        string = str(factors[0])
        for i in range(1, len(factors)):
            string += " x {}".format(factors[i])
        return string

    def Graph_description(self, graph_description:list)-> str:
        """[generate a factorization graph description ]

        Args:
            graph_description (list): [list of nodes and edges of graph]

        Returns:
            str: [description of the graph]
        """
        description = 'graph G { \noverlap = false '
        k = '\n'.join(self.graph_description)
        description = description+"\n"+k+"\n}"
        return description

    def factorization(self, n: int, function_name: str)->dict:
        """[function to generate a number factorization based on function name]

        Args:
            n (int): [number to factorize]
            function_name (str): [Factorization function name used to get the factors]

        Returns:
            dict: [dictionary of each factor's multiplicity]
        """
        factors = {}
        for p1 in eval("self."+function_name+"("+str(n)+")"):
            try:
                factors[p1] += 1
            except KeyError:
                factors[p1] = 1
        return factors

    def createnode(self, x:int)->str:
        """[function to create a new node in the graph]

        Args:
            x (int): [type of nodes]

        Returns:
            str: [description]
        """
        global nodenames
        name = random.random()
        while name in self.nodenames:
            name = random.random()
        self.nodenames.add(name)
        if x == 1:
            self.graph_description.append('"'+str(name)+'"'+self.whitenode)
        else:
            self.graph_description.append('"'+str(name)+'"'+self.blacknode)
        return '"'+str(name)+'"'

    def createedge(self, x:str, y:str, t:int)-> str:
        """[function to create connection be]

        Args:
            x (str): [nodes 1]
            y (str): [nodes 2]
            t (int): [nodes type : 0=last stage of the tree, 1=all other stages]

        Returns:
            str: [description]
        """
        if t == 1:
            self.graph_description.append(x + '--' + y + ' [color="#DDDDDD"]')
        if t == 0:
            self.graph_description.append(x + '--' + y + ' [color=grey]')
        return x + '--' + y

    def draw_factor(self, n: int, fact_method: str, save: bool, show: bool) -> bool:
        """[Function that generates a diagram for a number]

        Args:
            n (int): [Number to which we draw the diagram]
            fact_method (str): [Factorization function name used to get the factors]
            save (bool): [True = to save automatically the diagram/False = to not]
            show (bool): [True = to show automatically the diagram/False = to not]

        Returns:
            (bool): [operation state]
        """
        try:
            description = self.get_graph(n, fact_method)
            with open("InputFile.dot", "w")as file:
                file.write(description)
            check_call(['circo', '-Tpng', 'InputFile.dot',
                       '-o', str(n)+"\'s_Diagram.png"])
            os.remove("InputFile.dot")
            image = Image.open(str(n)+"\'s_Diagram.png")
            if show:
                image.show(title=str(n)+"\'s_Diagram.png")
            if not save:
                os.remove(str(n)+"\'s_Diagram.png")
            return True
        except:
            print("dot/circo command not found please install graphviz")
            return False

    def draw_factor_poster(self, numbers: list, fact_method: str) -> None:
        """[Function that generates list of numbers' diagrams]

        Args:
            numbers (list): [List of numbers]
            fact_method (str): [Factorization function name used to get the factors]
        """

        if not os.path.exists("../poster"):
            os.mkdir("../poster")
        else:
           for f in os.listdir("../poster"):
            os.remove(os.path.join("../poster",f))

        numbers.sort()
        try:
            for n in numbers:
                description = self.get_graph(n, fact_method)
                with open("InputFile.dot", "w")as file:
                    file.write(description)
                check_call(['circo', '-Tpng', 'InputFile.dot', '-o',
                           "../poster/"+str(n)+"\'s_Diagram.png"])
                os.remove("InputFile.dot")
        except:
            print("dot/circo command not found please install graphviz")

    def get_graph(self, n: int, name: str)->list:
        """[function to create a graph for a number ]

        Args:
            n (int): [number to factor]
            name (str): [Factorization function name used to get the factors]

        Returns:
            list: [list describing the nodes and the edges of graph]
        """
        self.graph_description = []
        if n == 1:
            self.graph_description.append('"0"' + self.one)
            return self.Graph_description(self.graph_description)
        else:
            # keys are factors, values are the multiplicity of the prime factors
            pf = self.factorization(n, name)
            factors = []
            for fac in pf:
                for multiplicity in range(0, pf[fac]):
                    factors.append(fac)
            factors = sorted(factors, reverse=True)
            rootnode = self.createnode(1)
            currentset = set()
            currentset.add(rootnode)
            level = len(factors) + 1
            for i in range(0, len(factors)):
                level -= 1
                f = factors[i]
                nodetype = 1
                if i == len(factors) - 1:
                    nodetype = 0
                newnodeset = set()
                for eachnode in currentset:
                    for j in range(0, f):
                        newnode = self.createnode(nodetype)
                        newnodeset.add(newnode)
                        self.edgeset.add(self.createedge(
                            eachnode, newnode, nodetype))
                currentset = newnodeset
            return self.Graph_description(self.graph_description)