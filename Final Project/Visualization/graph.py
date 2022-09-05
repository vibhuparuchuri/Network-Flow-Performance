import pandas as pd
from matplotlib import pyplot as plt

def graphCSV():
        
    
    # load graph data into dataframes
    df = pd.read_csv('alekhyaRandomNodeBFS.csv',header = None)
    df1 = pd.read_csv('alekhyaRandomNodeDFS.csv',header = None)
    #df2 = pd.read_csv('ashwinRandomRange.csv',header = None)
    df3 = pd.read_csv('vibhuRandomNodeBFS.csv',header = None)
    df4 = pd.read_csv('vibhuRandomNodeDFS.csv',header = None)


    t = df[0]
    v = df[1]

    t1 = df1[0]
    v1 = df1[1]


    #t2 = df2[0]
    #v2 = df2[1]

    t3 = df3[0]
    v3 = df3[1]

    t4 = df4[0]
    v4 = df4[1]


    #plot the data
    plt.plot(t,v, label="Ford Fulkerson - BFS")
    plt.plot(t1,v1, label="Ford Fulkerson - DFS")
    #plt.plot(t2,v2, label="Pre Flow Push")
    plt.plot(t3,v3, label="Scaling Ford Fulkerson - BFS")
    plt.plot(t4,v4, label="Scaling Ford Fulkerson - DFS")

    #label the x and y axis
    plt.xlabel('Vertices')
    plt.ylabel('Execution Time (seconds)')

    #plot legend placement
    plt.legend(loc='best')

    #location of file
    plt.savefig("Figure_Random_6")

    #clear plot
    plt.clf()

        

graphCSV()



    



