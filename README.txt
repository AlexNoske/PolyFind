**INSTALLATION**

In order to run PolyFind a number of python packages need to be installed. These consists of:
networkx
tkinter

These can be installed with the respecitve commands:

pip install networkx
pip install tkinter

**RUNNING POLYFIND**

PolyFind involves two main input methods a command line input and a Graphical User Interface (GUI).
The command line has the structure:

python PolyFind.py -G1 graph1 -G2 graph2 -v polymoprhismVersion -m mode -pC aStringRepresentingACustomPolymorphismInput

Where G1 represent the graph you are mapping from. G2 represents the graph you are mapping too. -v is the polymorphism version
you want to search for. For example this could be siggers, malcev or custom. -m is set to 0 if no returned example is required
otherewise -m is set to 1. -pC is only looked at if -v is equal to custom and in this case -pC gives details on the extra
constraints the polymorphism requires.

An example of this command being used to check for a siggers polymorphism between C3 and C3 is given as follows:

python PolyFind.py -G1 C3 -G2 C3 -v siggers -m 0 -pC ""

An example of using a custom polymorphism constraint is as follows:

python PolyFind.py -G1 C3 -G2 C3 -v custom -m 0 -pC "f(X,X,X,X)=X^f(X,Y,Y,Z)=f(X,Z,Z,Y)"

Files can also be used as graph inputs for example:

python PolyFind.py -G1 graph1.txt -G2 graph2.txt -v siggers -m 0 -pC ""

where the graph.txt files have the following structure:

for each node, a list of zeros and ones separated by commas represents for a given node which edges it has. This 
is repeated for each node and the lists are separated by a semi-colon, for example, C3 would be written down as: 
0,1,0;0,0,1;1,0,0 

The GUI works similaly except input boxes are given for each of the required inputs.

In order to launch the GUI version PolyFind must be run through the IDLE

