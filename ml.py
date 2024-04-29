import math;

#region [Data]
red: list[float]   = [ 1, 0, 0 ];
green: list[float] = [ 0, 1, 0 ];
blue: list[float]  = [ 0, 0, 1 ];

inputs: list[list[float]]  = [
    (0.0000, 0.0000), (0.2778, 0.2500), (0.2778, 0.9375), (0.9167, 0.6563),
    (0.4167, 0.2500), (0.3611, 0.3438), (0.3333, 0.4063), (0.9722, 0.3750),
    (0.0833, 0.3438), (0.6389, 0.3438), (0.4167, 0.6875), (0.7500, 0.6875),
    (0.0833, 0.1875), (0.9167, 0.5313), (0.1389, 0.2500), (0.8333, 0.6250),
    (0.8056, 0.6250), (0.1944, 1.0000), (0.8333, 0.5625), (0.4167, 1.0000),
    (1.0000, 0.6875), (0.4722, 0.6563), (0.3611, 0.5625), (0.4722, 0.8438),
    (0.1667, 0.3125), (0.4167, 0.9375), (0.3611, 0.9688), (0.9167, 0.3438),
    (0.0833, 0.0313), (0.3333, 0.8750)];

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
epochs: int = 100;
learning_rate: float = .1;
#endregion

def Softmax(predictions: list[float]) -> list[float]:
    m:     float = max(predictions);
    tmp:   list[float] = [math.exp(p-m) for p in predictions];
    total: float = sum(tmp);
    return [t / total for t in tmp];

def LogLoss(activations: list[float], targets: list[float]) -> float:
    losses: list[float] = [-t * math.log(a) - (1 - t) * math.log(1 - a)
                for a,t in zip(activations, targets)];
    return sum(losses);

for epoch in range(epochs):
    pred = [[sum([w*i for w,i in zip(we, inp)])+ bi
        for we, bi in zip(weights, biases)]
        for inp in inputs];
    act  = [Softmax(p) for p in pred];
    cost = sum([LogLoss(ac, ta) for ac, ta in zip(act, targets)]) / len(act);

    errors_d = [[a - t for a,t in zip(ac, ta)] for ac, ta in zip(act, targets)];
    inputsT  = list(zip(*inputs));
    errordT  = list(zip(*errors_d));

    weightD  = [[sum([e * i for e,i in zip(err, inp)]) 
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
