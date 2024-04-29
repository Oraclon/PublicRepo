
import math
import random as r
import flower_data
from tqdm import trange

fl=flower_data
epochs,lr=5000,.3
ci,ch,co=2,14,3

wihi=[[r.random() for _ in range(ci)]
    for _ in range(ch)]
bihi=[0 for _ in range(ch)]

wh1h2=[[r.random() for _ in range(ch)]
    for _ in range(ch)]
bh1h2=[0 for _ in range(ch)]

wh2o=[[r.random() for _ in range(ch)]
    for _ in range(co)]
bh2o=[0 for _ in range(co)]

def softmax(pr):
    m=max(pr)
    temp=[math.exp(p-m) for p in pr]
    total=sum(temp)
    return [t / total for t in temp]

def relu_act(predictions):
    activation=[[max(0,p) for p in pred]
        for pred in predictions]
    return activation

def tr(ar):
    return list(zip(*ar))

def predict(weights,biases,inputs):
    prediction=[[sum([w*i for w,i in zip(we,inp)])+bia
        for we,bia in zip(weights,biases)]
        for inp in inputs]
    return prediction

def test(a):
    s=f"{len(a)} {len(a[0])}"
    print(s)
    exit()

def update_weights(weight,
    weight_delta_transposed,
    inputs,
    bias,
    bias_delta):
    for i in range(len(weight_delta_transposed)):
        for w in range(len(weight_delta_transposed[0])):
weight[i][w]-=lr*weight_delta_transposed[i][w]/len(inputs)
        bias[i]-=lr*bias_delta[i]/len(inputs)

def log_loss(ac,ta):
    losses=[-t * math.log(a) - (1-t)
        *math.log(1-a)
        for a,t in zip(ac,ta)]
    return sum(losses)

t=trange(0,epochs)
for _ in t:
    pred_h1=predict(wihi,bihi,fl.inputs)
    act_h1=relu_act(pred_h1)
    pred_h2=predict(wh1h2,bh1h2,act_h1)
    act_h2=relu_act(pred_h2)
    pred_o=predict(wh2o,bh2o,act_h2)
    act_o=[softmax(p) for p in pred_o]

    #cost=sum([log_loss(a,t) for a,t in zip(act_o,fl.targets)])/len(fl.targets)

    message=f"Training: {_}/{epochs} "
    t.set_description(message)
    t.refresh()
    error_do=[[a-t for a,t in zip(ac,ta)]
        for ac, ta in zip(act_o,fl.targets)]
    wh2ot=tr(wh2o)
    error_dh2=[[sum([d*w for d,w in zip(deltas, weights)])
        *(0 if p<=0 else 1)
        for weights,p in zip(wh2ot,pred)]
        for deltas, pred in zip(error_do,pred_h2)]
    wh1h2t=tr(wh1h2)
    error_dh1=[[sum([d*w for d,w in zip(deltas, weights)])
        *(0 if p<=0 else 1)
        for weights,p in zip(wh1h2t,pred)]
        for deltas,pred in zip(error_dh2,pred_h1)]

    error_dot=tr(error_do)
    act_h2t=tr(act_h2)
    wh2od=[[sum([e*a for e,a in zip(er,ac)])
        for er in error_dot]
        for ac in act_h2t]
    bh2od=[sum([e for e in er])
        for er in error_dot]

    error_dh2t=tr(error_dh2)
    act_h1t=tr(act_h1)
    wh1h2d=[[sum([e*a for e,a in zip(er,ac)])
        for er in error_dh2t]
        for ac in act_h1t]
    bh1h2d=[sum([e for e in er])
        for er in error_dh2t]

    error_dh1t=tr(error_dh1)
    inputs_t=tr(fl.inputs)
    wihid=[[sum([e*a for e,a in zip(er,ac)])
        for er in error_dh1t]
        for ac in inputs_t]
    bihid=[sum([e for e in er])
        for er in error_dh1t]

    wh2odt=tr(wh2od)
    update_weights(wh2o,wh2odt,fl.inputs,bh2o,bh2od)
    wh1h2dt=tr(wh1h2d)
    update_weights(wh1h2,wh1h2dt,fl.inputs,bh1h2,bh1h2d)
    wihidt=tr(wihid)
    update_weights(wihi,wihidt,fl.inputs,bihi,bihid)

pred_h1=predict(wihi,bihi,fl.test_inputs)
act_h1=relu_act(pred_h1)
pred_h2=predict(wh1h2,bh1h2,act_h1)
act_h2=relu_act(pred_h2)
pred_o=predict(wh2o,bh2o,act_h2)
act_o=[softmax(p) for p in pred_o]

correct=0
for a,t in zip(act_o, fl.test_targets):
    if a.index(max(a))==t.index(max(t)):
        correct+=1

print(f"CORRECT:{correct}/{len(act_o)} | Confident: {correct/len(act_o):%}")
