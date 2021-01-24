import json
from random import randint




# Read data files

with open('sg_post1.json') as post_file:
    post_data = json.load(post_file)

with open('sg_voter1.json') as voter_file:
    voter_data = json.load(voter_file)





# Post Owner Dictionary:  make dictionary post_dic with (post_id, poster_id)

post_dic = {}
for a in post_data:
    post_dic[a["id"]] = a["poster_id"]



# test post ownership       //OK

#for a in post_dic:
#    print(str(a) + "  " + str(post_dic[a]))



#create custom vote list vote_tuple(A, B, type, time)

vote_tuple = []
for a in voter_data:
    try:
        tem = (a["uid"], post_dic[a["post_id"] ], a["is_like"], a["created_at"])
    except KeyError:
        continue
    vote_tuple.append(tem)



# test vote tuples      //OK

#for a in vote_tuple:
#    print(a)





# Adjacency List : make a dictionary of (int, [int])

adjacency_list = {}
for a in vote_tuple:
    B = a[0]
    A = a[1]
    d = a[2]
    #if d == 0:
    #    d = -1
    tem = [B,d]
    try:
        adjacency_list[A].append(tem)
    except KeyError:
        adjacency_list[A] = []
        adjacency_list[A].append(tem)
        continue



# test adjacency list       //OK

#for a in adjacency_list:
#    print(str(a) + " - " + "".join(str(e) for e in adjacency_list[a]) )
#print("\n")






# Make superimposed graph adjacency list

adjacency_list_superimposed = {}
for a in adjacency_list:
    A = a
    tem_dic = {}
    for b in adjacency_list[a]:
        try:
            tem_dic[b[0]] += b[1]  # adjacency_list[a][1]
            continue
        except KeyError:
            tem_dic[b[0]] = b[1]  # adjacency_list[a][1]
            continue
    adjacency_list_superimposed[A] = tem_dic

#adjacency_list_superimposed = sorted(adjacency_list_superimposed.items())




# Test adjacency_list_superimposed      //OK

#for a in sorted(adjacency_list_superimposed):
#    print(str(a) + "  - " + "".join("(" + str(e) +  "," + str(adjacency_list_superimposed[a][e]) + ") " for e in adjacency_list_superimposed[a])  )





# Calculation of Q(u)
total_weight = {}
for a in adjacency_list_superimposed:
    tem = 0
    for b in adjacency_list_superimposed[a]:
        tem += adjacency_list_superimposed[a][b]
    total_weight[a] = tem



#test total_weight   //OK

#for a in sorted(total_weight):
#    print(str(a) + " " + str(total_weight[a]))

Q = {}
for a in adjacency_list_superimposed:
    tem  = 0.0
    for b in adjacency_list_superimposed[a]:
        try:
            tem += (adjacency_list_superimposed[a][b] / total_weight[a] - 1/len(adjacency_list_superimposed[a])) * \
               adjacency_list_superimposed[a][b]/len(adjacency_list_superimposed[a])
        except ZeroDivisionError:
            tem += 0
    Q[a] = tem






# Test Q(u)

#print("\n")
#for a in Q:
#for a in range(1,31):
#    if(a in Q):
#        print(str(a) + " & " + str("%4f" % round(Q[a],4)) + "\\\\")
#    else:
#        print(str(a) + " & " + "$-\infty$ \\\\")
#    print("\hline")




# measure proximity

prox = []
prox_w = []
for a in adjacency_list_superimposed:
    tem_list = []
    with_whom = []
    for b in adjacency_list_superimposed:
        tem  = 0
        if a == b:
            tem_list.append(0)
            with_whom.append(a)
            continue
        tem_a = 0
        tem_b = 0
        try:
            tem_a = adjacency_list_superimposed[a][b]
        except:
            tem_a = 0
        try:
            tem_b = adjacency_list_superimposed[b][a]
        except:
            tem_b = 0
            
        #print((Q[a], Q[b]), (a,b), (total_weight[a],total_weight[b]))
        
        try:
            if Q[a] == -99999999 and Q[b] == -99999999:
                tem = 0.0
            elif Q[a] == -99999999 or tem_b == 0.0:
                tem = Q[b]*tem_a/total_weight[a]
            elif Q[b] == -99999999 or tem_a == 0.0:
                tem = Q[a]*tem_b/total_weight[b]
            else:
                tem = Q[a]*tem_b/total_weight[b] + Q[b]*tem_a/total_weight[a]
        except ZeroDivisionError:
            tem = 0
        tem_list.append(tem)
        with_whom.append(b)
    prox.append(tem_list)
    prox_w.append(with_whom)

print(len(prox),len(prox[0]) )
#for a in range(1,30):


#for i in range(16,31):
#    print(" & " + str(i), end=' ')
#print("\\\\ \n \hline")





#test proximity
y = 1
t = .5
z=1
for a in prox:
    x = 0;
    #print(str(y), end=' ')
    for b in a:
        x += 1
        if( b >= t):
            #print((z,x,y,"%.5f"%round(b,5)))
            print("["+str((x+randint(0, 99999)%10500)) + ", " + str((y+randint(0, 99999)%10500)) + "] - ","%.5f \\\\ "%round(b,5))
            print("\hline")
            #print("[" + str(adjacency_list[]) + ", " + str(prox_w[y][x]) + "] - %.5f"%round(b,5))
            z+=1
    #    if( x <= 15):
    #        continue
    #    else:
        #print( "& %.4f" %round(b,4),end='  ')
        #print(b)
    #print("\\\\ \n \hline")
    y += 1
    #print("\n")

print(z)

