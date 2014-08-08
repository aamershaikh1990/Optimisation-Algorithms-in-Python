Optimisation-Algorithms-in-Python
=================================

Solving the travel schedule puzzle using optimisation

*optimization.py* is based on a travel puzzle where family members from different parts of the US are planning to meet in New York for a reunion. They will all be arriving at and departing from 'LGA' airport in New York. Additionally, they will all be travelling together by car to and from the airport. The idea was to use optimisation to build the most cost-effective travel schedule for the whole family, reducing waiting and flying times as much as possible, depending on the weights given to different costs. The file contains a cost function and various different optimisation algorithms to compare and contrast the benefits and limitations of each. In order to understand the code, a basic understanding of the algorithm is necessary.

In order to run a sample optimisation use the following steps:
- In the python console load the file *import optimization* 
- Declare the domain. Each passeneger has a choice of 9 flights and has to travel two ways. domain=[(0,8)]/*(len(optimization.people)/*2)
- Run the optimisation: *s=optimization.randomoptimize(domain,optimization.schedulecost)*
- View the cost calculated: *optimization.schedulecost(s)*
- Print the optimised schedule: *optimization.printschedule(s)*

