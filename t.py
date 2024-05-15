#region [Main]
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MLV3
{
    public class Grad2
    {
        public double[] w { get; set; }
        public double b { get; set; }
    }
    public class MLLayer2
    {
        #region [Constructor and Variables]
        public MLLayer2(Model md, int nd, Activation act = Activation.Default, Optimizer opt = Optimizer.Default)
        {
            model      = md;
            nodeslen   = nd;
            activation = act;
            optimizer  = opt;
            nodes = new Dictionary<int, MLNode2>();
            _BuildNodes();
        }
        #region [Variables]
        #region [Internal Variables]
        int nodeid { get; set; }
        int nodeslen { get; set; }
        Model model { get; set; }
        Activation activation { get; set; }
        Optimizer optimizer { get; set; }
        Dictionary<int, MLNode2> nodes { get; set; }
        #endregion
        #region [Public Variables]
        public double[][] layeractivations { get; set; }
        public double[][] layerdeltas      { get; set; }
        #endregion
        #endregion
        #endregion
        #region [Public Methods]
        public void LayerTrain(double[][] inputs)
        {
            double[][] tmpactivs = new double[nodeslen][];
            for (nodeid = 0; nodeid < nodeslen; nodeid++)
            {
                nodes[nodeid].NodeTrain(inputs);
                tmpactivs[nodeid] = nodes[nodeid].activations;
            }
            layeractivations = tmpactivs.Transposer();
        }
        public void LayerDeltas(double[][] pders, double[][] respect)
        {
            double[][] deltas = new double[nodeslen][];
            for (nodeid = 0; nodeid < nodeslen; nodeid++)
            {
                nodes[nodeid].NodeLDeltas(pders, respect);
                deltas[nodeid] = nodes[nodeid].deltas;
            }
            layerdeltas = deltas.Transposer();
        }
        public void LayerUpdate()
        {
            for (nodeid = 0; nodeid < nodeslen; nodeid++)
            {
                nodes[nodeid].NodeUpdate();
            }
        }
        #endregion
        #region [Private Methods]
        private void _BuildNodes()
        {
            for (nodeid = 0; nodeid < nodeslen; nodeid++)
            {
                nodes.Add(nodeid, new MLNode2(model, activation, optimizer));
            }
        }
        #endregion
    }
    public class MLNode2
    {
        #region [Contructor and Variables]
        public MLNode2(Model md, Activation act = Activation.Default, Optimizer opt = Optimizer.Default)
        {
            activation = act;
            optimizer  = opt;
            model = md;
        }
        #region [Variables]
        Grad2 grad { get; set; } = new Grad2();
        Model model          { get; set; }
        Activation activation       { get; set; }
        Optimizer optimizer         { get; set; }
        public double[] activations { get; set; }
        public double[] derivatives { get; set; }
        public double[] deltas      { get; set; }
        public double[][] wDeltas   { get; set; }
        public bool ready           { get; set; } = false;
        public int featureid        { get; set; }
        #endregion
        #endregion
        #region [Public Methods]
        #region [Evaluation]
        public PredResult NodeEvaluate(double[] features)
        {
            PredResult pred = new PredResult();
            double[] calculations = new double[features.Length];
            for (int i = 0; i < features.Length; i++)
            {
                calculations[i] = grad.w[i] * features[i];
            }
            double prediction = calculations.Sum() + grad.b;

            switch (activation)
            {
                case Activation.Tanh:
                    pred.activation = Math.Tanh(prediction);
                    pred.actDeriv = 1 - Math.Pow(pred.activation, 2);
                    break;
                case Activation.Sigmoid:
                    pred.activation = 1 / (1 + Math.Exp(-prediction));
                    pred.actDeriv = pred.activation * (1 - pred.activation);
                    break;
                case Activation.SoftMax:
                    pred.activation = Math.Exp(prediction);
                    pred.actDeriv = -1;
                    break;
            }
            return pred;
        }
        #endregion
        #region [Training]
        public void NodeTrain(double[][] inputs)
        {
            if (!ready)
                _BuildGrad(inputs[0]);

            double[] tmp_acts = new double[inputs.Length];
            double[] tmp_ders = new double[inputs.Length];
            for (int i = 0; i < inputs.Length; i++)
            {
                PredResult pred = NodeEvaluate(inputs[i]);
                tmp_acts[i] = pred.activation;
                tmp_ders[i] = pred.actDeriv;
            }
            activations = tmp_acts;
            derivatives = tmp_ders;
        }
        public void NodeLDeltas(double[][] pders, double[][] respect)
        {
            double[] tmpdeltas = new double[pders.Length];
            for (int i = 0; i < tmpdeltas.Length; i++)
            {
                tmpdeltas[i] = pders[i].Length > 1 ? pders[i].Sum() / pders.Length : pders[i][0];
            }
            NodeDeltas(tmpdeltas, respect);
        }
        public void NodeDeltas(double[] pders, double[][] respect)
        {
            double[] dgda = new double[derivatives.Length];
            for (int i = 0; i < dgda.Length; i++)
            {
                double dg = pders[i];
                double da = derivatives[i];
                dgda[i] = dg * da;
            }
            deltas = dgda;
            _NodeWDeltas(respect);
        }
        public void NodeUpdate()
        {
            for (featureid = 0; featureid < wDeltas.Length; featureid++)
            {
                double oldw = grad.w[featureid] - _GetDGDW();
                grad.w[featureid] = oldw;
            }
            double oldb = grad.b - _GetDGDB();
            grad.b = oldb;
        }
        #endregion
        #endregion
        #region [Private Methods]
        private double _GetDGDB()
        {
            double[] calcs = new double[deltas.Length];
            for (int i = 0; i < calcs.Length; i++)
            {
                calcs[i] = deltas[i] * model.learning;
            }
            return calcs.Sum() / calcs.Length;
        }
        private double _GetDGDW()
        {
            double[] calcs = new double[deltas.Length];
            for (int i = 0; i < calcs.Length; i++)
            {
                calcs[i] = wDeltas[featureid][i] * model.learning;
            }
            return calcs.Sum() / calcs.Length;
        }
        private void _NodeWDeltas(double[][] respect)
        {
            double[][] respt = respect.Transposer();
            double[][] dgdw = new double[respt.Length][];
            for (int i = 0; i < dgdw.Length; i++)
            {
                double[] dws = new double[deltas.Length];
                for (int j = 0; j < dws.Length; j++)
                {
                    double da = deltas[j];
                    double dw = respt[i][j];
                    dws[j] = da * dw;
                }
                dgdw[i] = dws;
            }
            wDeltas = dgdw;
        }
        private void _BuildGrad(double[] features)
        {
            Random rand = new Random();
            grad.w = Enumerable.Range(0, features.Length).Select(x => rand.NextDouble()).ToArray();
            ready = true;
        }
        #endregion
    }
    public class Node : NodeStorage
    {
        #region Constructor and Variables
        public Node(Model md, Activation act, Optimizer opt)
        {
            model = md;
            actType = act;
            optimizer = opt;
        }
        public Model model { get; set; }
        public double[][] softmaxDers { get; set; }
        public Gradient grad;
        public Activation actType { get; set; }
        public Optimizer optimizer { get; set; }
        #endregion



        private void _GetWDeltasV2(double[][] respect)
        {
            double[][] calculations = new double[respect.Length][];
            for (int i = 0; i < respect.Length; i++)
            {
                double da = deltas[i];
                double[] dw = respect[i];
                double[] tmp = new double[dw.Length];
                for (int j = 0; j < tmp.Length; j++)
                {
                    tmp[j] = da * dw[j];
                }
                calculations[i] = tmp;
            }
            wDeltas = calculations.Transposer();
        }
        public void SoftmaxDeltas(double[] lossDerivatives, double[][] respectTo)
        {
            double[] calculations = new double[lossDerivatives.Length];
            for (int i = 0; i < calculations.Length; i++)
            {
                double dg = lossDerivatives[i];
                double[] da = softmaxDers[i];
                double[] tmp = new double[da.Length];
                for (int j = 0; j < da.Length; j++)
                {
                    tmp[j] = dg * da[j];
                }
                calculations[i] = tmp.Sum();
            }
            deltas = calculations;
            _GetWDeltasV2(respectTo);
        }

        #region Node Common
        private void _BuildGrad(double[][] inputs)
        {
            storageInps = inputs;
            grad.gradInps = inputs;
            for (featureId = 0; featureId < featuresLen; featureId++)
            {
                grad.w[featureId] = model.rand.NextDouble() - .5;
            }
            grad.isReady = true;
        }
        private void _GetWDeltas(double[][] respectTo)
        {
            double[][] respT = DA.Transposer(respectTo);
            for (featureId = 0; featureId < featuresLen; featureId++)
            {
                double[] tmpWDelta = new double[dataLen];
                double[] tmpWDeltaPow = new double[dataLen];
                double[] wFeatures = respT[featureId];

                for (itemId = 0; itemId < dataLen; itemId++)
                {
                    double delta = deltas[itemId];
                    double wFeat = wFeatures[itemId];
                    tmpWDelta[itemId] = delta * wFeat;
                    tmpWDeltaPow[itemId] = Math.Pow(delta * wFeat, 2);
                }
                wDeltas[featureId] = tmpWDelta;
                wDeltasPow[featureId] = tmpWDeltaPow;
            }
        }
        private double _GetJW(bool isPow = false)
        {
            if (!isPow)
                return wDeltas[featureId].Calculate(model.learning) / dataLen;
            else
                return wDeltasPow[featureId].Sum() / dataLen;
        }
        private double _GetJ(bool isPow = false)
        {
            if (!isPow)
                return deltas.Calculate(model.learning) / dataLen;
            else
                return deltasPow.Sum() / dataLen;
        }
        #endregion

        #region Node Update
        private void Default()
        {
            for (featureId = 0; featureId < featuresLen; featureId++)
            {
                //double old_w = grad.w[featureId] - model.learning * _GetJW();
                double old_w = grad.w[featureId] - _GetJW();
                grad.w[featureId] = old_w;
            }
            double old_b = grad.b - _GetJ();
            grad.b = old_b;
        }
        private void Momentum()
        {
            for (featureId = 0; featureId < featuresLen; featureId++)
            {
                double old_vdw = model.b1 * grad.vdw[featureId] + (1 - model.b1) * _GetJW();
                grad.vdw[featureId] = old_vdw;
                double tmp_w = grad.w[featureId] - model.learning * grad.vdw[featureId];
                grad.w[featureId] = tmp_w;
            }
            double old_vdb = model.b1 * grad.vdb + (1 - model.b1) * _GetJ();
            grad.vdb = old_vdb;
            double tmp_b = grad.b - model.learning * grad.vdb;
            grad.b = tmp_b;
        }
        private void RmsProp()
        {
            for (featureId = 0; featureId < featuresLen; featureId++)
            {
                double old_sdw = model.b2 * grad.sdw[featureId] + (1 - model.b2) * _GetJW(true);
                grad.sdw[featureId] = old_sdw;
                double tmp_w = grad.w[featureId] - model.learning * _GetJW() / Math.Sqrt(grad.sdw[featureId]);
                grad.w[featureId] = tmp_w;
            }
            double old_sdb= model.b2 * grad.sdb + (1 - model.b2) *_GetJ(true);
            grad.sdb = old_sdb;
            double tmp_b = grad.b - model.learning * _GetJ() / Math.Sqrt(grad.sdb);
            grad.b = tmp_b;
        }
        private void Adam()
        {
            for (featureId = 0; featureId < featuresLen; featureId++)
            {
                double old_vdw = model.b1 * grad.vdw[featureId] + (1 - model.b1) * _GetJW();
                double old_sdw = model.b2 * grad.sdw[featureId] + (1 - model.b2) * _GetJW(true);
                grad.vdw[featureId] = old_vdw;
                grad.sdw[featureId] = old_sdw;
                double vdw_c = grad.vdw[featureId] / (1 - Math.Pow(model.b1, dataLen));
                double sdw_c = grad.sdw[featureId] / (1 - Math.Pow(model.b2, dataLen));
                double tmp_w = grad.w[featureId] - model.learning * vdw_c / (Math.Sqrt(sdw_c) + model.e);
                grad.w[featureId] = tmp_w;
            }
            double old_vdb = model.b1 * grad.vdb + (1 - model.b1) * _GetJ();
            double old_sdb = model.b2 * grad.sdb + (1 - model.b2) * _GetJ(true);
            grad.vdb = old_vdb;
            grad.sdb = old_sdb;
            double vdb_c = grad.vdb / (1 - Math.Pow(model.b1, dataLen));
            double sdb_c = grad.sdb / (1 - Math.Pow(model.b2, dataLen));
            double tmp_b = grad.b - model.learning * vdb_c / (Math.Sqrt(sdb_c) + model.e);
            grad.b = tmp_b;
        }
        public void Update()
        {
            switch(optimizer)
            {
                case Optimizer.Default:
                    Default();
                    break;
                case Optimizer.Momentum:
                    Momentum();
                    break;
                case Optimizer.RmsProp:
                    RmsProp();
                    break;
                case Optimizer.Adam:
                    Adam();
                    break;
            }
        }
        #endregion

        #region Node Deltas
        public void LayerDeltas(double[][] layerLossDerivs, double[][] respectTo)
        {
            double[][] pdersT = layerLossDerivs.Transposer();
            double[] tmpCalcs = new double[pdersT.Length];
            for (int i = 0; i < tmpCalcs.Length; i++)
            {
                double tmp = pdersT[i].Sum() / pdersT[i].Length;
                double delta = tmp * activationDerivs[i];
                deltas[i] = delta;
                deltasPow[i] = Math.Pow(delta, 2);
            }
            _GetWDeltas(respectTo);
            var x = 20;
            //double[][] tmpCalcs = new double[layerLossDerivs.Length][];
            //for (int arrId = 0; arrId < layerLossDerivs.Length; arrId++)
            //{
            //    double[] tmpDeltaCalcs = new double[layerLossDerivs[0].Length];
            //    for (int i = 0; i < layerLossDerivs[arrId].Length; i++)
            //    {
            //        tmpDeltaCalcs[i] = layerLossDerivs[arrId][i] * activationDerivs[i];
            //    }
            //    tmpCalcs[arrId] = tmpDeltaCalcs;
            //}

            //double[][] tmpT = DA.Transposer(tmpCalcs);
            //for(int i = 0; i < tmpT.Length; i++)
            //{
            //    double[] item = tmpT[i];
            //    double res = item.Length > 1 ? item.Sum() / item.Length : item[0];
            //    deltas[i] = res;
            //    deltasPow[i] = Math.Pow(res, 2);
            //}
            //_GetWDeltas(respectTo);
        }
        public void Deltas(double[] lossDerivs, double[][] respectTo)
        {
            for (itemId = 0; itemId < dataLen; itemId++)
            {
                double lossDeriv = lossDerivs[itemId];
                double actDeriv = activationDerivs[itemId];
                deltas[itemId] = lossDeriv * actDeriv;
                deltasPow[itemId] = Math.Pow(lossDeriv * actDeriv, 2);
            }
            _GetWDeltas(respectTo);
        }
        #endregion

        #region Node Train and Predict
        public PredResult Predict(double[] input)
        {
            PredResult prediction = new PredResult();
            double[] featureCalcs = new double[featuresLen];
            for (featureId = 0; featureId < featuresLen; featureId++)
            {
                featureCalcs[featureId] = grad.w[featureId] * input[featureId];
            }

            double pred = featureCalcs.Sum() + grad.b;

            switch(actType)
            {
                case Activation.Default:
                    prediction.activation = pred;
                    prediction.actDeriv = 1;
                    break;
                case Activation.ReLU:
                    prediction.activation = pred <= 0 ? 0 : pred;
                    prediction.actDeriv = prediction.activation <= 0 ? 0 : 1;
                    break;
                case Activation.Tanh:
                    prediction.activation = Math.Tanh(pred);
                    prediction.actDeriv = 1 - Math.Pow(prediction.activation, 2);
                    break;
                case Activation.Sigmoid:
                    prediction.activation = 1 / (1 + Math.Exp(-pred));
                    prediction.actDeriv = prediction.activation * (1 - prediction.activation);
                    break;
                case Activation.SoftMax:
                    prediction.activation = Math.Exp(-pred);
                    prediction.actDeriv = -1;
                    break;
            }

            return prediction;
        }
        public void Train(double[][] inputs)
        {
            if (!grad.isReady)
                _BuildGrad(inputs);
            for (itemId = 0; itemId < dataLen; itemId++)
            {
                PredResult pred = Predict(inputs[itemId]);
                activations[itemId] = pred.activation;
                activationDerivs[itemId] = pred.actDeriv;
            }
        }
        #endregion
    }
}

#endregion
import random as r;
import math;

class Activ:
    def __init__(self):
        self.activation: list[float] = [];
        self.derivative: list[float] = [];
    def Calculate(self, activation: list[float]):
        self._ApplySoftmax(activation);
        self._CalculateDerivative();
    def _ApplySoftmax(self, activation: list[float]):
        self.activation = [x/sum(activation) for x in activation];
    def _CalculateDerivative(self):
        result: list[float] = [];
        for i, i1 in enumerate(self.activation):
            calcs: list[float] = [];
            for j, i2 in enumerate(self.activation):
                if(i == j):
                    calcs.append(i1*(1-i2));
                else:
                    calcs.append(-i1*i2);
            # result.append(calcs);
            result.append(sum(calcs));
        # self.derivative = [sum(x) for x in list(zip(*result))];
        self.derivative = result;
class Grad:
    def __init__(self):
        self.w: list[float] = [];
        self.b: float = 0;
class Node:
    def __init__(self):
        self.ready:       bool = False;
        self.grad:        Grad = Grad();
        self.activations: list[float] = [];
        self.derivatives: list[float] = [];
        self.deltas:      list[float] = [];
        self.wdeltas:     list[float] = [];
        self.a = 2.2;
    def __BuildGrad(self, input: list[float]):
        self.grad.w = [r.random() for _ in range(len(input))];
        self.ready = True;
    def NodePredict(self, input: list[float]):
        calculations: list[float] = [];
        for fid, feature in enumerate(input):
            calculations.append(self.grad.w[fid] * feature);
        pred: float = sum(calculations) + self.grad.b;
        return math.exp(pred);
    def NodeTrain(self, inputs: list[list[float]]):
        if not self.ready:
            self.__BuildGrad(inputs[0]);
        tmp: list[float] = []
        for input in inputs:
            tmp.append(self.NodePredict(input));
        self.activations = tmp;
    def NodeDeltas(self, ders: list[float], respect: list[list[float]]):
        self.deltas = [pd*cd for pd, cd in zip(ders, self.derivatives)];
        inputsT = list(zip(*respect));
        calcs: list[float] = [];
        for id, inp in enumerate(inputsT):
            tmp = [de*i for de,i in zip(self.deltas, inp)];
            calcs.append(tmp);
        self.wdeltas = calcs;
    def NodeUpdate(self):
        for i in range(len(self.grad.w)):
            # tmpw = self.grad.w[i] - 0.4 * (sum(self.wdeltas[i]));
            tmpw = self.grad.w[i] - self.a * (sum(self.wdeltas[i])/len(self.deltas));
            self.grad.w[i] = tmpw;
        # tmpb = self.grad.b - 0.4 * (sum(self.deltas));
        tmpb = self.grad.b - self.a * (sum(self.deltas)/len(self.deltas));
        self.grad.b = tmpb;
class Data:
    def __init__(self, input: list[float], target: list[float]):
        self.inputs:  list[float] = input;
        self.targets: list[float] = target;

def ApplySoftmax(activations: list[list[float]]):
    actT: list[list[float]] = list(zip(*activations));
    activations: list[Activ] = [];
    for activation in actT:
        a: Activ = Activ();
        a.Calculate(activation);
        activations.append(a);
    return activations;
def LossCalculation(acts: list[float], targets: list[float]):
    # calcs: list[float] = [-math.log(a) if t == 1 else -math.log(1-a) for a,t in zip(acts, targets)];
    # calcs: list[float] = [pow(a-t,2) for a,t in zip(acts, targets)];
    calcs: list[float] = [-t*math.log(a) for a,t in zip(acts, targets)];
    res = sum(calcs) / len(calcs);
    return res;
def LossDerivatives(acts: list[float], tars: list[float]):
    # calcs: list[float] = [-1/a if t == 1 else 1/(1-a) for a,t in zip(acts, tars)];
    # calcs: list[float] = [2*(a-t) for a,t in zip(acts, tars)];
    calcs: list[float] = [-t/a for a,t in zip(acts, tars)];
    return calcs;

setosa:     list[float] = [0,0,1];
versicolor: list[float] = [0,1,0];
virginica:  list[float] = [1,0,0];
inputs: list[float] = [
    [5.1,3.5,1.4,0.2],
    [4.9,3.0,1.4,0.2],
    [4.7,3.2,1.3,0.2],
    [4.6,3.1,1.5,0.2],
    [5.0,3.6,1.4,0.2],
    [5.4,3.9,1.7,0.4],
    [4.6,3.4,1.4,0.3],
    [5.0,3.4,1.5,0.2],
    [4.4,2.9,1.4,0.2],
    [4.9,3.1,1.5,0.1],
    [5.4,3.7,1.5,0.2],
    [4.8,3.4,1.6,0.2],
    [4.8,3.0,1.4,0.1],
    [4.3,3.0,1.1,0.1],
    [5.8,4.0,1.2,0.2],
    [5.7,4.4,1.5,0.4],
    [5.4,3.9,1.3,0.4],
    [5.1,3.5,1.4,0.3],
    [5.7,3.8,1.7,0.3],
    [5.1,3.8,1.5,0.3],
    [5.4,3.4,1.7,0.2],
    [5.1,3.7,1.5,0.4],
    [4.6,3.6,1.0,0.2],
    [5.1,3.3,1.7,0.5],
    [4.8,3.4,1.9,0.2],
    [5.0,3.0,1.6,0.2],
    [5.0,3.4,1.6,0.4],
    [5.2,3.5,1.5,0.2],
    [5.2,3.4,1.4,0.2],
    [4.7,3.2,1.6,0.2],
    [4.8,3.1,1.6,0.2],
    [5.4,3.4,1.5,0.4],
    [5.2,4.1,1.5,0.1],
    [5.5,4.2,1.4,0.2],
    [4.9,3.1,1.5,0.1],
    [5.0,3.2,1.2,0.2],
    [5.5,3.5,1.3,0.2],
    [4.9,3.1,1.5,0.1],
    [4.4,3.0,1.3,0.2],
    [5.1,3.4,1.5,0.2],
    [5.0,3.5,1.3,0.3],
    [4.5,2.3,1.3,0.3],
    [4.4,3.2,1.3,0.2],
    [5.0,3.5,1.6,0.6],
    [5.1,3.8,1.9,0.4],
    [4.8,3.0,1.4,0.3],
    [5.1,3.8,1.6,0.2],
    [4.6,3.2,1.4,0.2],
    [5.3,3.7,1.5,0.2],
    [5.0,3.3,1.4,0.2],
    [7.0,3.2,4.7,1.4],
    [6.4,3.2,4.5,1.5],
    [6.9,3.1,4.9,1.5],
    [5.5,2.3,4.0,1.3],
    [6.5,2.8,4.6,1.5],
    [5.7,2.8,4.5,1.3],
    [6.3,3.3,4.7,1.6],
    [4.9,2.4,3.3,1.0],
    [6.6,2.9,4.6,1.3],
    [5.2,2.7,3.9,1.4],
    [5.0,2.0,3.5,1.0],
    [5.9,3.0,4.2,1.5],
    [6.0,2.2,4.0,1.0],
    [6.1,2.9,4.7,1.4],
    [5.6,2.9,3.6,1.3],
    [6.7,3.1,4.4,1.4],
    [5.6,3.0,4.5,1.5],
    [5.8,2.7,4.1,1.0],
    [6.2,2.2,4.5,1.5],
    [5.6,2.5,3.9,1.1],
    [5.9,3.2,4.8,1.8],
    [6.1,2.8,4.0,1.3],
    [6.3,2.5,4.9,1.5],
    [6.1,2.8,4.7,1.2],
    [6.4,2.9,4.3,1.3],
    [6.6,3.0,4.4,1.4],
    [6.8,2.8,4.8,1.4],
    [6.7,3.0,5.0,1.7],
    [6.0,2.9,4.5,1.5],
    [5.7,2.6,3.5,1.0],
    [5.5,2.4,3.8,1.1],
    [5.5,2.4,3.7,1.0],
    [5.8,2.7,3.9,1.2],
    [6.0,2.7,5.1,1.6],
    [5.4,3.0,4.5,1.5],
    [6.0,3.4,4.5,1.6],
    [6.7,3.1,4.7,1.5],
    [6.3,2.3,4.4,1.3],
    [5.6,3.0,4.1,1.3],
    [5.5,2.5,4.0,1.3],
    [5.5,2.6,4.4,1.2],
    [6.1,3.0,4.6,1.4],
    [5.8,2.6,4.0,1.2],
    [5.0,2.3,3.3,1.0],
    [5.6,2.7,4.2,1.3],
    [5.7,3.0,4.2,1.2],
    [5.7,2.9,4.2,1.3],
    [6.2,2.9,4.3,1.3],
    [5.1,2.5,3.0,1.1],
    [5.7,2.8,4.1,1.3],
    [6.3,3.3,6.0,2.5],
    [5.8,2.7,5.1,1.9],
    [7.1,3.0,5.9,2.1],
    [6.3,2.9,5.6,1.8],
    [6.5,3.0,5.8,2.2],
    [7.6,3.0,6.6,2.1],
    [4.9,2.5,4.5,1.7],
    [7.3,2.9,6.3,1.8],
    [6.7,2.5,5.8,1.8],
    [7.2,3.6,6.1,2.5],
    [6.5,3.2,5.1,2.0],
    [6.4,2.7,5.3,1.9],
    [6.8,3.0,5.5,2.1],
    [5.7,2.5,5.0,2.0],
    [5.8,2.8,5.1,2.4],
    [6.4,3.2,5.3,2.3],
    [6.5,3.0,5.5,1.8],
    [7.7,3.8,6.7,2.2],
    [7.7,2.6,6.9,2.3],
    [6.0,2.2,5.0,1.5],
    [6.9,3.2,5.7,2.3],
    [5.6,2.8,4.9,2.0],
    [7.7,2.8,6.7,2.0],
    [6.3,2.7,4.9,1.8],
    [6.7,3.3,5.7,2.1],
    [7.2,3.2,6.0,1.8],
    [6.2,2.8,4.8,1.8],
    [6.1,3.0,4.9,1.8],
    [6.4,2.8,5.6,2.1],
    [7.2,3.0,5.8,1.6],
    [7.4,2.8,6.1,1.9],
    [7.9,3.8,6.4,2.0],
    [6.4,2.8,5.6,2.2],
    [6.3,2.8,5.1,1.5],
    [6.1,2.6,5.6,1.4],
    [7.7,3.0,6.1,2.3],
    [6.3,3.4,5.6,2.4],
    [6.4,3.1,5.5,1.8],
    [6.0,3.0,4.8,1.8],
    [6.9,3.1,5.4,2.1],
    [6.7,3.1,5.6,2.4],
    [6.9,3.1,5.1,2.3],
    [5.8,2.7,5.1,1.9],
    [6.8,3.2,5.9,2.3],
    [6.7,3.3,5.7,2.5],
    [6.7,3.0,5.2,2.3],
    [6.3,2.5,5.0,1.9],
    [6.5,3.0,5.2,2.0],
    [6.2,3.4,5.4,2.3],
    [5.9,3.0,5.1,1.8]
]
targets: list[list[float]] = [
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    setosa,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    versicolor,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica,
    virginica
];

data: list[Data] = [Data(i,t) for i,t in zip(inputs, targets)];
[r.shuffle(data) for _ in range(10)];
batches: list[list[Data]] = [data[x:x+32] for x in [x for x in range(0, len(data), 32)]]
pass

node1: Node = Node();
node2: Node = Node();
node3: Node = Node();
loss = 0;
for epoch in range(1000):
    for batch in batches:
        inps: list[list[float]] = [x.inputs for x in batch];
        tars: list[list[float]] = [x.targets for x in batch];

        nodes: list[Node] = [node1, node2, node3];
        [node.NodeTrain(inps) for node in nodes];
        res: list[Activ] = ApplySoftmax([node.activations for node in nodes]);
        acts: list[list[float]] = [x.activation for x in res];
        ders: list[list[float]] = [x.derivative for x in res];
        loss = sum([LossCalculation(act, tar) for act, tar in zip(acts, tars)])/len(tars);
        # loss = sum([LossCalculation(act, tar) for act, tar in zip(acts, tars)])/(2*len(tars));
        ldersT = list(zip(*[LossDerivatives(act, tar) for act, tar in zip(acts, tars)]));
        #region [Update Node Activations/Derivatives]
        actsT = list(zip(*acts));
        dersT = list(zip(*ders));
        for nid, node in enumerate(nodes):
            node.activations = actsT[nid];
            node.derivatives = dersT[nid];
        #endregion
        #region [Update Node Deltas]
        for nid, node in enumerate(nodes):
            node.NodeDeltas(ldersT[nid], inps)
        #endregion
        #region [Update Node]
        for nid, node in enumerate(nodes):
            node.NodeUpdate()
        #endregion
    print(loss)
    pass
