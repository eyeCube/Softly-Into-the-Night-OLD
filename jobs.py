'''
    jobs.py
'''

from const import *

'''JOBITEMS = {
CLS_ATHLETE     : 
CLS_CHEMIST     : 
CLS_DEPRIVED     : 
CLS_ENGINEER     : 
CLS_POLITICIAN     : 
CLS_JANITOR     : 
CLS_SECURITY     : 
CLS_PILOT     : 
CLS_RIOTPOLICE     : 
CLS_SOLDIER     : 
    }'''

JOBS = {
    # KG, $$$: mass, money
    #Access keys:
    #S  level of security clearance
    #Keys:
        #J  janitor's closets
        #C  computer closets
        #K  key to the city
        #P  hangar access
        #L  lab access
    #stats: additional stat bonuses or nerfs
    #skills: starting skills
#ID                KG, $$$$,S|Key--------stats---------------skills
CLS_ATHLETE     : (80, 300, 0,'', {'msp':20,'dfn':4,'carry':15,},(SKL_ATHLET,),),
CLS_CHEMIST     : (60, 500, 2,'L',{'hpmax':-5,'mpmax':5,},(SKL_CHEMIS,),),
CLS_DEPRIVED    : (40, 0,   0,'', {'hpmax':-5,'mpmax':-5,'atk':-5,},(),),
CLS_ENGINEER    : (60, 500, 0,'C',{'hpmax':5,'carry':10,},(SKL_ENGINR,),),
CLS_POLITICIAN  : (60, 1000,3,'K',{'hpmax':-5,'mpmax':-5,},(SKL_PERSUA),),
CLS_JANITOR     : (60, 100, 0,'J',{},(),),
CLS_SECURITY    : (60, 300, 4,'', {'atk':3,},(),),
CLS_PILOT       : (60, 500, 0,'P',{'sight':10,},(SKL_PILOT,),),
CLS_RIOTPOLICE  : (60, 300, 3,'', {'hpmax':5,'mpmax':-5,'atk':3,'asp':10,},(SKL_FIGHTR,),),
CLS_SOLDIER     : (60, 300, 1,'', {'hpmax':10,'mpmax':-5,'atk':5,'asp':15,'msp':10,'carry':20,},(SKL_HEAVY,SKL_GUNS,),),),
CLS_THIEF       : (60, 1000,0,'', {'mpmax':-5,'dfn':2,'msp':10,'carry':15,},(SKL_SNEAK,),),
CLS_TECHNICIAN  : (60, 500, 1,'', {'mpmax':5,},(SKL_TECH,),),
CLS_SMUGGLER    : (60, 1000,0,'', {'hpmax':5,'carry':10,},(SKL_PERSUA,SKL_GUNS,),),
    }


def getMass(jobID): #int
    return JOBS[jobID][0]
def getMoney(jobID): #int
    return JOBS[jobID][1]
def getClearance(jobID): #int- security clearance level
    return JOBS[jobID][2]
def getKey(jobID): #char
    return JOBS[jobID][3]
def getStats(jobID): #dict of stat bonuses
    return JOBS[jobID][4]
def getSkills(jobID): #tuple of flag values
    return JOBS[jobID][5]
















    
