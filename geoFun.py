import math


def DetMatrix3x3(A,B,C):
    return A[0]*(B[1]*C[2]-B[2]*C[1])+ \
           A[1]*(B[2]*C[0]-B[0]*C[2])+ \
           A[2]*(B[0]*C[1]-B[1]*C[0])
           
       
         
def VertexAngle(a1,a2):
    if a1>a2:
        return a1-a2-(math.pi/2)
    else:
        return a1-a2+(math.pi/2)
        

def TwoPointsToVector(p1,p2): #([x1,y1],[x2,y2])
    vect={}
    vect['Module']=math.sqrt(math.pow(p2[0]-p1[0],2)+math.pow(p2[1]-p1[1],2))

    deltaX=p2[0]-p1[0]
    deltaY=p2[1]-p1[1]
    
    degree=math.atan2(deltaY,deltaX)
        
    if degree<0:
        degree=(math.pi*2)+degree
        
    vect['Degree']=degree
        
    return vect
    
           
def CircleFrom3Points(p1,p2,p3):#([x1,y1],[x2,y2],[x3,y3])consecutivi
 
    a=[0,0,0]
    b=[0,0,0]
    c=[0,0,0]
    d=[0,0,0]
     
    a[0]=p1[0]
    b[0]=p1[1]
    c[0]=1
    d[0]=math.pow(p1[0],2)+math.pow(p1[1],2)

    a[1]=p2[0]
    b[1]=p2[1]
    c[1]=1
    d[1]=math.pow(p2[0],2)+math.pow(p2[1],2)

    a[2]=p3[0]
    b[2]=p3[1]
    c[2]=1
    d[2]=math.pow(p3[0],2)+math.pow(p3[1],2)

    DetM=DetMatrix3x3(a,b,c)
    DetA=DetMatrix3x3(d,b,c)
    DetB=DetMatrix3x3(a,d,c)
    DetC=DetMatrix3x3(a,b,d)

    Primo=DetA/DetM/2
    Secondo=DetB/DetM/2
    Terzo=DetC/DetM
    #print Primo
    #print Secondo
    #print Terzo

    circle={}
    circle['Center']=[Primo,Secondo] 
    vectp1=TwoPointsToVector(circle['Center'],p1)
    circle['Radius']=vectp1['Module']
    circle['P1Degree']=vectp1['Degree']
    circle['P2Degree']=TwoPointsToVector(circle['Center'],p2)['Degree']
    circle['P3Degree']=TwoPointsToVector(circle['Center'],p3)['Degree']
    circle['Direction']=TriangleDirection(p1,p2,p3)
    
    return circle
    
    
def TriangleDirection(p1,p2,p3):

    v1=TwoPointsToVector(p1,p2)
    v2=TwoPointsToVector(p2,p3)
    v3=TwoPointsToVector(p3,p1)
    delta_angle=[]

    delta_angle.append(VertexAngle(v1['Degree'],v2['Degree']))
    delta_angle.append(VertexAngle(v2['Degree'],v3['Degree']))
    delta_angle.append(VertexAngle(v3['Degree'],v1['Degree']))

    
    return (delta_angle[0]+delta_angle[1]+delta_angle[2])/(-math.pi/2)
    


def TriangleArea(p1,p2,p3):
    a=[p1[0],p1[1],1]
    b=[p2[0],p2[1],1]
    c=[p3[0],p3[1],1]
    area=0.5*DetMatrix3x3(a,b,c)
    return area
    
       
def TranslateNodes(n,x,y):
    t=[]
    for i in n :
        t.append([i[0]+x,i[1]+y])
    return t
  

def RotateNodes(n,alfa,p):
    r=[]
    for i in n :
        v=TwoPointsToVector(p,i)
        ra=v['Degree']+alfa
        r.append([p[0]+v['Module']*math.cos(ra),p[1]+v['Module']*math.sin(ra)])
    return r                


def EllipsisPath(a,b,s):
    ra=float(a/2)
    rb=float(b/2)
    n=[[ra,0]]
    p=[]
    d=math.pi/s*2
    for i in range(1,s):
        n.append([ra*math.cos(d*i),rb*math.sin(d*i)])
        p.append(['line',i-1,i])
    p.append(['line',s-1,0])
    
    return {"nodes":n,"path":p}

   
def ShapeArea(nodes,paths):
    area=0
    return area

     
def ShapePerimeter(nodes,paths):
    perimeter=0
    return perimeter
