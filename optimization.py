import time
import random
import math

people = [('Seymour','BOS'),('Franny','DAL'),('Zooey','CAK'),('Walt','MIA'),('Buddy','ORD'),('Les','OMA')]

#LaGuardia airport in New York
destination = 'LGA'

flights ={}

# read in flight schedules and convert to a dictionary
for line in file('schedule.txt'):
	origin,dest,depart,arrive,price = line.strip().split(',')
	flights.setdefault((origin,dest),[])
	#vals to be useds as dictionary values
	#depart and arrive to be used as keys
	vals = (depart,arrive,int(price))
	flights[(origin,dest)].append(vals)

# convert time into minutes
def getminutes(t):
	x=time.strptime(t,'%H:%M')
	return x[3]*60 + x[4]

def printschedule(r):
	for d in range (len(r)/2): #loop over the number of people
		name=people[d][0]
		origin=people[d][1]
		out = flights[(origin,destination)][r[2*d]] #get the outward flight details
		ret = flights[(destination,origin)][r[2*d+1]] #get the return flight details
		print '%10s %10s %5s-%5s $%3s %5s-%5s $%3s' %(name, origin, out[0],out[1],out[2], ret[0], ret[1], ret[2])		

#Cost function to calculate the cost of the given schedule
def schedulecost(sol):
	totalprice=0
	latestarrival=0
	earliestdep=24*60

	for d in range(len(sol)/2):
		#get the inbound and outbound flights
		origin = people[d][1]
		outbound = flights[(origin,destination)][int(sol[2*d])] #get the outward flight details
		returnf = flights[(destination,origin)][int(sol[2*d+1])] #get the return flight details

		# Total price is the price of all outbound and return fligts
		totalprice +=outbound[2]
		totalprice +=returnf[2]

		#Track the latest arrival and earliest departure
		if latestarrival < getminutes(outbound[1]): latestarrival=getminutes(outbound[1])
		if earliestdep>getminutes(returnf[0]): earliestdep=getminutes(returnf[0])

	#Every person must wait at the airport until the latest person arives.
	# They also must arrive at the same time and wait for their flights
	totalwait=0
	for d in range(len(sol)/2):
		origin=people[d][1]
		outbound = flights[(origin,destination)][int(sol[2*d])] #get the outward flight details
		returnf = flights[(destination,origin)][int(sol[2*d+1])] #get the return flight details
		totalwait+=latestarrival- getminutes(outbound[1])
		totalwait+=getminutes(returnf[0]) - earliestdep

	#Does the solution require an extra day of car rental?
	if latestarrival<earliestdep: totalprice+= 50

	return totalprice + totalwait


#Most basic optimization technique. Generate random variables for the input 		
def randomoptimize(domain, costf): 
	best=99999999
	bestr=None
	for i in range (10000):
		#Create a random solution
		r=[random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
		
		#get the cost 
		cost = costf(r)

		#Compare it to the best one so far
		if cost<best:
			best=cost
			bestr=r
	return r

#Hill climbing optimization, look at neighboring solutions and move in the direction of the least cost
def hillclimb(domain,costf):
	#Create a random solution
	sol= [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]

	#Main loop

	while 1:

		#Create a list of neighbouring solutions
		neighbors=[]
		for j in range (len(domain)):

			#one way in each direction
			if sol[j]>domain[j][0] and sol[j]<domain[j][1]: #If solution index > first element of j index
				neighbors.append(sol[0:j] + [sol[j]+1] + sol[j+1:])
			if sol[j]<domain[j][1] and sol[j]>domain[j][0]:
				neighbors.append(sol[0:j]+[sol[j]-1] + sol[j+1:])
				
		current=costf(sol)
		best=current

		for j in range(len(neighbors)):
			cost = costf(neighbors[j])
			if cost < best:
				best=cost
				sol=neighbors[j]

		if best == current:
			break;

	return sol	

#Simulated annlealing optimisation
def annealingoptimize(domain,costf,T=10000.0,cool=0.95,step=1):
	#Initialize the values randomly
	vec=[float(random.randint(domain[i][0],domain[i][1])) for i in range(len(domain))]

	#While the temperature value is greater than 0.1 the optimization continues to loop

	while T>0.1:
		#Choose one of the indices
		i = random.randint(0,len(domain)-1)

		#Choose a direction to change in
		dir = random.randint(-step,step)

		# Create a new list with one of the values changed
		vecb=vec[:]
		vecb[i] += dir #randomly step up or down for chosen index

		#Check values are within bounds

		if vecb[i]<domain[i][0]: vecb[i]=domain[i][0]
		elif vecb[i]>domain[i][1]:vecb[i]=domain[i][1]

		# Calculate the current cost and new cost
		ea =costf(vec)
		eb =costf(vecb)
		p=pow(math.e,(-eb-ea)/T)

		#Is it better or does it make the probability cutoff?
		if(eb<ea or random.random()<p):
			vec=vecb

		#Decrease the temperature variable
		T=T*cool
	return vec

#Using a genetic algorithm optimization process, through a mixture of mutation and crossover methods

def geneticoptimize(domain,costf,popsize=50,step=1,mutprob=0.2,elite=0.2,maxiter=100):
	#Mutation operation
	def mutate(vec):
		i = random.randint(0,len(domain)-1)
		if random.random()<0.5 and vec[i]>domain[i][0]:
			return vec[0:i]+[vec[i] -step] + vec[i+1:]
		elif vec[i]<domain[i][1]:
			return vec[0:i]+[vec[i] -step] + vec[i+1:]

	#Crossover operation
	def crossover (r1, r2):
		i=random.randint(1,len(domain)-2)
		return r1[0:i] +r2[i:]

	#Build the intializaion process
	pop=[]
	for i in range(popsize):
		vec=[random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
		pop.append(vec)
		print vec

	#How many winners do we selection from each population
	topelite = int(elite*popsize)

	#Main loop
	for i in range(maxiter):
		#Calculate the score for every item in the pop and rank
		scores=[(costf(v),v) for v in pop]
		scores.sort()
		ranked =[v for (s,v) in scores]

		#Start with the pure winners
		pop=ranked[0:topelite]

		#Add mututated and bred forms of the winners
		while len(pop)<popsize:
			if random.random() < mutprob:
				#Mutate
				c=random.randint(0,topelite)
				pop.append(mutate(ranked[c]))
			else:
				#Crossover
				c1=random.randint(0,topelite)
				c2=random.randint(0,topelite)
				pop.append(crossover(ranked[c1],ranked[c2]))
		#Print current best score
		print scores[0][0]
	return scores[0][1]


			








