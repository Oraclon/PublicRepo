def LogLoss(a:float, t:float) -> float:
    return -math.log(a) if t == 1 else -math.log(1-a);

def Deriv(a,t) -> float:
    res: float = 0;
    if t == 1:
        res = ((-1 / a) * (a * (1 - a)));
    else:
        res = ((-1 / (1 - a)) * (a * (a - 1)));
    return res;
    
import math;
import random as r;
#region [Node]
class Node:
    def __init__(self):
        self.learning = 0.4;
        self.w = [];
        self.b = 0;
        self.a = [];
        self.d = [];
    
    def _Predict(self, input: list[float]) -> None:
        calcs: list[float] = [];
        for featid in range(len(input)):
            calc = self.w[featid] * input[featid];
            calcs.append(calc);
        pred: float = sum(calcs) + self.b;
        # self.a.append(math.exp(pred));
        self.a.append(pred);


    def Train(self, inputs: list[list[float]]) -> list[float]:
        self.a = []
        for input in inputs:
            self._Predict(input);
        return self.a;

#endregion
#region [Data]
red: list[float]   = [ 1, 0, 0 ];
green: list[float] = [ 0, 1, 0 ];
blue: list[float]  = [ 0, 0, 1 ];

inputs: list[list[float]]  = [
    [0.0000, 0.0000], [0.2778, 0.2500], [0.2778, 0.9375], [0.9167, 0.6563],
    [0.4167, 0.2500], [0.3611, 0.3438], [0.3333, 0.4063], [0.9722, 0.3750],
    [0.0833, 0.3438], [0.6389, 0.3438], [0.4167, 0.6875], [0.7500, 0.6875],
    [0.0833, 0.1875], [0.9167, 0.5313], [0.1389, 0.2500], [0.8333, 0.6250],
    [0.8056, 0.6250], [0.1944, 1.0000], [0.8333, 0.5625], [0.4167, 1.0000],
    [1.0000, 0.6875], [0.4722, 0.6563], [0.3611, 0.5625], [0.4722, 0.8438],
    [0.1667, 0.3125], [0.4167, 0.9375], [0.3611, 0.9688], [0.9167, 0.3438],
    [0.0833, 0.0313], [0.3333, 0.8750]];

targets: list[list[float]] = [
    red, red, blue, green, 
    red, red, red, green, 
    red, green, blue, green, 
    red, green, red, green, 
    green, blue, green, blue, 
    green, blue, blue, blue, 
    red, blue, blue, green, 
    red, blue];
#endregion

#region [Gradient]
weights: list[list[float]] = [ [.1, .2], [.15, .25], [.18, .1] ];
biases: list[float] = [ .3, .4, .35 ];
nodes: list[Node] = [Node() for _ in range(3)];
for i, node in enumerate(nodes):
    node.w = weights[i];
    node.b = biases[i];

# weights: list[list[float]] = [[r.random() for _ in range(2)] for _ in range(3)];

epochs: int = 100;
learning_rate: float = .1;
#endregion
#region [Methods]
def Softmax(predictions: list[float]) -> list[float]:
    m:     float = max(predictions);
    tmp:   list[float] = [math.exp(p-m) for p in predictions];
    total: float = sum(tmp);
    return [t / total for t in tmp];

def LogLoss(activations: list[float], targets: list[float]) -> float:
    losses: list[float] = [-math.log(a) if t == 1 else -math.log(1-a)
                for a,t in zip(activations, targets)];
    # losses: list[float] = [-t * math.log(a) - (1 - t) * math.log(1 - a)
    #             for a,t in zip(activations, targets)];
    return sum(losses);
#endregion

def CalculateLossDerivs(activations: list[list[float]], targets: list[list[float]]):
    derivs: list[list[float]] = [];
    for activation, target in zip(activations, targets):
        calcs = [];
        for act, tar in zip(activation, target):
            calcs.append(-1 / act if tar == 1 else 1 / (1 - act));
        derivs.append(calcs);
    return derivs;

for epoch in range(epochs):
    preds = list(zip(*[x.Train(inputs) for x in nodes]));
    acts  = [Softmax(x) for x in preds];
    pred = [[sum([w*i for w,i in zip(we, inp)])+ bi
        for we, bi in zip(weights, biases)]
        for inp in inputs];
    act  = [Softmax(p) for p in pred];
    cost = sum([LogLoss(ac, ta) for ac, ta in zip(act, targets)]) / len(act);

    errors_d2 = CalculateLossDerivs(acts, targets);
    errors_d = [[ (-1 / a) if t == 1 else (1 / ( 1 - a )) for a,t in zip(ac, ta)] for ac, ta in zip(act, targets)];
    # errors_d = [[a - t for a,t in zip(ac, ta)] for ac, ta in zip(act, targets)];

    inputsT  = list(zip(*inputs));
    errordT  = list(zip(*errors_d));

    #region [Experimental]
    # #region [deltas]
    # der = [];
    # for e in errors_d:
    #     der.append(sum(e));
    # #endregion
    # #region [wDeltas]
    # weightDEXP = [];
    # for inp in inputsT:
    #     errs = []
    #     for err in errordT:
    #         calcs = [];
    #         for e,i in zip(err, inp):
    #             calcs.append(e*i);
    #         errs.append(calcs);
    #     weightDEXP.append(errs);
    
    # dw = [];
    # for x in weightDEXP:
    #     tmp = []
    #     for inps in list(zip(*x)):
    #         tmp.append(sum(inps));
    #     dw.append(tmp);
    # #endregion
    # #region [Update Grad]
    # for i in range(len(weights[0])):
    #     for j in range(len(weights)):
    #         weights[i][j] = weights[i][j] - learning_rate * sum(dw[i]) / len(targets);
    #     biases[i] = biases[i] - learning_rate * sum(der) /len(targets);
    # #endregion
    # z =20;
    #endregion

    weightD  = [[ sum([e * i for e,i in zip(err, inp)])
            for err in errordT]
            for inp in inputsT];
    biasesD  = [sum([e for e in errors]) 
            for errors in errordT];

    weightDT = list(zip(*weightD));
    for i in range(len(weightDT)):
        for j in range(len(weightDT[0])):
            weights[i][j] = weights[i][j] - learning_rate * weightDT[i][j] / len(targets);
        biases[i] = biases[i] - learning_rate * biasesD[i] / len(targets);
    print(cost)
    x=10;
