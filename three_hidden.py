import math
import random as r
from tqdm import trange
import flower_data as fl

epochs,lr=5000,0.2

w_in_h1=[[r.random() for _ in range(2)]
    for _ in range(4)]
b_in_h1=[0 for _ in range(4)]

w_h1_h2=[[r.random() for _ in range(4)]
    for _ in range(8)]
b_h1_h2=[0 for _ in range(8)]

w_h2_h3=[[r.random() for _ in range(8)]
    for _ in range(4)]
b_h2_h3=[0 for _ in range(4)]

w_h3_o=[[r.random() for _ in range(4)]
    for _ in range(3)]
b_h3_o=[0 for _ in range(3)]

def predict(weights,biases,inputs):
    prediction=[[sum([w*i for w,i in zip(we,inp)])+bia
        for we,bia in zip(weights,biases)]
        for inp in inputs]
    return prediction

def relu_act(predictions):
    activation=[[max(0,p) for p in pred]
        for pred in predictions]
    return activation

def softmax(pr):
    m=max(pr)
    temp=[math.exp(p-m) for p in pr]
    total=sum(temp)
    return [t/total for t in temp]

def log_loss(ac,ta):
    losses=[-t * math.log(a)-(1-t)
        *math.log(1-a) for a,t in zip(ac,ta)]
    return sum(losses)

def tr(ar):
    return list(zip(*ar))

t=trange(epochs,leave=True)
for _ in t:
    pred_h1=[[sum([w*i for w,i in zip(weights,inp)])+bias
        for weights, bias in zip(w_in_h1,b_in_h1)]
        for inp in fl.inputs]
    act_h1=[[max(0,p) for p in pred]
        for pred in pred_h1]

    pred_h2=[[sum([w*i for w,i in zip(weights,inp)])+bias
        for weights,bias in zip(w_h1_h2,b_h1_h2)]
        for inp in act_h1]
    act_h2=[[max(0,p) for p in pred]
        for pred in pred_h2]

    pred_h3=[[sum([w*i for w,i in zip(weights,inp)])+bias
        for weights,bias in zip(w_h2_h3,b_h2_h3)]
        for inp in act_h2]
    act_h3=[[max(0,p) for p in pred]
        for pred in pred_h3]

    pred_o=[[sum([w*i for w,i in zip(weights,inp)])+bias
        for weights,bias in zip(w_h3_o,b_h3_o)]
        for inp in act_h3]
    act_o=[softmax(p) for p in pred_o]

    error_do=[[a-t for a,t in zip(act,ta)]
        for act, ta in zip(act_o, fl.targets)]

    cost=sum([log_loss(a,t) for a,t in zip(act_o,fl.targets)])/len(act_o)
    message=f"{round(cost,5)}"
    t.set_description(message)
    if cost<=0.12:
        break

    wh3ot=tr(w_h3_o)
    error_dh3=[[sum([d*w for d,w in zip(de,we)])
        *(0 if p<=0 else 1)
        for we,p in zip(wh3ot,pred)]
        for de,pred in zip(error_do,pred_h3)]

    wh2h3t=tr(w_h2_h3)
    error_dh2=[[sum([d*w for d,w in zip(deltas,weights)])
        *(0 if p<=0 else 1)
        for weights,p in zip(wh2h3t,pr)]
        for deltas,pr in zip(error_dh3,pred_h2)]

    wh1h2t=tr(w_h1_h2)
    error_dh1=[[sum([d*w for d,w in zip(deltas,weights)])
        *(0 if p<=0 else 1)
        for weights,p in zip(wh1h2t,pr)]
        for deltas,pr in zip(error_dh2,pred_h1)]

    #griadient output->hidden3
    error_dot=tr(error_do)
    act_h3t=tr(act_h3)
    wh3od=[[sum([d*a for d,a in zip(de,ac)])
        for de in error_dot]
        for ac in act_h3t]
    bh3od=[sum([d for d in de])
        for de in error_dot]

    error_dh3t=tr(error_dh3)
    act_h2t=tr(act_h2)
    wh3h2d=[[sum([d*a for d,a in zip(de,ac)])
        for de in error_dh3t]
        for ac in act_h2t]
    bh3h2d=[sum([d for d in de])
        for de in error_dh3t]

    error_dh2t=tr(error_dh1)
    act_h1t=tr(act_h1)
    wh1h2d=[[sum([d*a for d,a in zip(de,ac)])
        for de in error_dh2t]
        for ac in act_h1t]
    bh1h2d=[sum([d for d in de])
        for de in error_dh2t]

    error_dh1t=tr(error_dh1)
    inputs_t=tr(fl.inputs)
    winh1d=[[sum([d*a for d,a in zip(de,ac)])
        for de in error_dh1t]
        for ac in inputs_t]
    binh1d=[sum([d for d in de])
        for de in error_dh1t]

    wh3odt=tr(wh3od)
    for i in range(len(wh3odt)):
        for w in range(len(wh3odt[0])):
            w_h3_o[i][w]-=lr*wh3odt[i][w]/len(fl.inputs)
        b_h3_o[i]-=lr*bh3od[i]/len(fl.inputs)

    wh2h3dt=tr(wh3h2d)
    for i in range(len(wh2h3dt)):
        for w in range(len(wh2h3dt[0])):
            w_h2_h3[i][w]-=lr*wh2h3dt[i][w]/len(fl.inputs)
        b_h2_h3[i]-=lr*bh3h2d[i]/len(fl.inputs)

    wh1h2dt=tr(wh1h2d)
    for i in range(len(wh1h2dt)):
        for w in range(len(wh1h2dt[0])):
            w_h1_h2[i][w]-=lr*wh1h2dt[i][w]/len(fl.inputs)
        b_h1_h2[i]-=lr*bh1h2d[i]/len(fl.inputs)

    winh1dt=tr(winh1d)
    for i in range(len(winh1dt)):
        for w in range(len(winh1dt[0])):
            w_in_h1[i][w]-=lr*winh1dt[i][w]/len(fl.inputs)
        b_in_h1[i]-=lr*binh1d[i]/len(fl.inputs)

pred_h1=predict(w_in_h1,b_in_h1,fl.test_inputs)
act_h1=relu_act(pred_h1)
pred_h2=predict(w_h1_h2,b_h1_h2,act_h1)
act_h2=relu_act(pred_h2)
pred_h3=predict(w_h2_h3,b_h2_h3,act_h2)
act_h3=relu_act(pred_h3)
pred_o=predict(w_h3_o,b_h3_o,act_h3)
act_o=[softmax(p) for p in pred_o]

correct=0
for a,t in zip(act_o, fl.test_targets):
    if a.index(max(a))==t.index(max(t)):
        correct+=1

print(f"CORRECT:{correct}/{len(act_o)} | Confident: {correct/len(act_o):%}")
