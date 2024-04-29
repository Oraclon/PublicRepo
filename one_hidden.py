import math
import random as r

inputs = [(0.0000, 0.3929), (0.5484, 0.7500), (0.0645, 0.5714), (0.5806, 0.5714),
    (0.2258, 0.8929), (0.4839, 0.2500), (0.3226, 0.2143), (0.7742, 0.8214),
    (0.4516, 0.5000), (0.4194, 0.0357), (0.4839, 0.2500), (0.3226, 0.7143),
    (0.5806, 0.5000), (0.5484, 0.1071), (0.6129, 0.6429), (0.6774, 0.1786),
    (0.2258, 0.8214), (0.7419, 0.1429), (0.6452, 1.0000), (0.8387, 0.2500),
    (0.9677, 0.3214), (0.3226, 0.4643), (0.3871, 0.5357), (0.3548, 0.1429),
    (0.3548, 0.6429), (0.1935, 0.4643), (0.4516, 0.3929), (0.4839, 0.6071),
    (0.6129, 0.6786), (0.2258, 0.6071), (0.5161, 0.3214), (0.5484, 0.6786),
    (0.3871, 0.8571), (0.6452, 0.6071), (0.1935, 0.3929), (0.6452, 0.3929),
    (0.6774, 0.4643), (0.3226, 0.2857), (0.7419, 0.7143), (0.7419, 0.3214),
    (1.0000, 0.3929), (0.8065, 0.3929), (0.1935, 0.5000), (0.1613, 0.8214),
    (0.2903, 0.9286), (0.3548, 0.0000), (0.2903, 0.6786), (0.5484, 0.9643),
    (0.4194, 0.1786), (0.2581, 0.2500), (0.3226, 0.7143), (0.5161, 0.3929),
    (0.2903, 0.6429), (0.5484, 0.9286), (0.2581, 0.3214), (0.0968, 0.5000),
    (0.6129, 0.7857), (0.0968, 0.3214), (0.6452, 0.9286), (0.8065, 0.7500)]

purple = (1, 0, 0)
orange = (0, 1, 0)
green = (0, 0, 1)

targets = [purple, orange, purple, orange, green, purple, purple, green, orange,
    purple, purple, green, orange, purple, orange, purple, green, purple, green,
    purple, purple, orange, orange, purple, orange, purple, orange, orange, orange,
    green, orange, orange, green, orange, purple, orange, orange, purple, orange,
    orange, purple, orange, green, green, green, purple, green, green, purple, purple,
    green, orange, green, green, purple, purple, green, purple, green, green]

test_inputs = [(0.0000, 0.3929), (0.0645, 0.5714), (0.0968, 0.3214),
    (0.0968, 0.5000), (0.2581, 0.3214), (0.1935, 0.4643), (0.2581, 0.2500),
    (0.1935, 0.3929), (0.3226, 0.2143), (0.4839, 0.2500), (0.3226, 0.4643),
    (0.3871, 0.5357), (0.3548, 0.6429), (0.4516, 0.5000), (0.4516, 0.3929),
    (0.5161, 0.3929), (0.5484, 0.7500), (0.6129, 0.6786), (0.5161, 0.3214),
    (0.5484, 0.6786), (0.1935, 0.5000), (0.2258, 0.6071), (0.3226, 0.7143),
    (0.2903, 0.6786), (0.3226, 0.7143), (0.2258, 0.8214), (0.2903, 0.6429),
    (0.6129, 0.7857), (0.7742, 0.8214), (0.8065, 0.7500)]

test_targets = [purple, purple, purple, purple, purple, purple, purple, purple,
    purple, purple, orange, orange, orange, orange, orange, orange, orange, orange,
    orange, orange, green, green, green, green, green, green, green, green, green, green]
ic,hc,oc=2,4,3


wih=[[0.1,-0.2],[-0.3,0.25],[0.12,0.23],[-0.11,-0.22]]
who=[[0.2,0.17,0.3,-0.11],[0.3,-0.4,0.5,-0.22],[0.12,0.23,0.15,0.33]]
bih=[0.2,0.34,0.21,0.44]
bho=[0.3,0.29,0.37]
epochs,lr=4000,0.4

def softmax(pr):
    m=max(pr)
    temp=[math.exp(p-m) for p in pr]
    total=sum(temp)
    return [t / total for t in temp]

def log_loss(ac,ta):
    losses=[-t * math.log(a) - (1-t)
        *math.log(1-a)
        for a,t in zip(ac,ta)]
    return sum(losses)

def tr(ar):
    return list(zip(*ar))

def rd():
    return r.random()-.5

for _ in range(epochs):
    pred_h1=[[sum([w*i for w,i in zip(weights,inp)])+bias
        for weights,bias in zip(wih,bih)]
        for inp in inputs]
    act_h1=[[max(0,p) for p in pred]
        for pred in pred_h1]
    pred_o=[[sum([w*i for w,i in zip(weights,inp)])+bias
        for weights,bias in zip(who,bho)]
        for inp in act_h1]
    act_o=[softmax(p) for p in pred_o]

    error_do=[[a-t for a,t in zip(ac,ta)]
        for ac, ta in zip(act_o,targets)]

    whot=tr(who)
    error_dh1=[[sum([d*w for d,w in zip(deltas,weights)])
        *(0 if p<=0 else 1)
            for weights,p in zip(whot,pred)]
            for deltas,pred in zip(error_do,pred_h1)]

    error_dot=tr(error_do)
    act_h1t=tr(act_h1)
    whod=[[sum([d*a for d,a in zip(deltas,act)])
        for deltas in error_dot]
        for act in act_h1t]
    bhod=[sum([d for d in deltas])
        for deltas in error_dot]

    error_dh1t=tr(error_dh1)
    inputst=tr(inputs)
    wihd=[[sum([d*w for d,w in zip(deltas,act)])
        for deltas in error_dh1t]
        for act in inputst]
    bihd=[sum([d for d in deltas])
        for deltas in error_dh1t]

    whodt=tr(whod)
    for i in range(len(whodt)):
        for w in range(len(whodt[0])):
            who[i][w]-=lr*whodt[i][w]/len(inputs)
        bho[i]-=lr*bhod[i]/len(inputs)

    wihdt=tr(wihd)
    for i in range(len(wihdt)):
        for w in range(len(wihdt[0])):
            wih[i][w]-=lr*wihdt[i][w]/len(inputs)
        bih[i]-=lr*bihd[i]/len(inputs)


pih=[[sum([w*i for w,i in zip(we,inp)])+b
    for we,b in zip(wih,bih)]
    for inp in test_inputs]
aih=[[max(0,p) for p in pred]
    for pred in pih]
pho=[[sum([w*i for w,i in zip(we,inp)])+b
    for we,b in zip(who,bho)]
    for inp in aih]
aho=[softmax(p) for p in pho]

correct=0
for a,t in zip(aho,test_targets):
    if a.index(max(a))==t.index(max(t)):
        correct+=1
    print(f"CORRECT:{correct}/{len(test_targets)} | PERS:{correct/len(test_targets):%}")
