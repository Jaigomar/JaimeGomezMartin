README

The program uses four classes, a father class and three daughters:
* correlationWilliam: is the parent class which has as attributes installed which indicates if it want the cost of the equipment ready to go and the correlation factor of William. It has the function calculate_cost which updates the cost price
* boiler, pump, steamTurbine: they are the child classes of correlationWilliam, which incorporates its particular attributes and implements its own function of calculating the cost, which initializes the value according to the conditions of each class, to later update it by calling the respective function of the parent class

Finally there is main.py which is not a class, it is the main file, which calls the other classes for and functions to get the results

Developer: Jaime Gómez Martín