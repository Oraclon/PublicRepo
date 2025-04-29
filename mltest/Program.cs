using DevTests2.Datastructure;
using DevTests2.src.System.Datastructure;
using static System.Formats.Asn1.AsnWriter;

public class MLItem
{
    public double[] input;
    public double target;
}

public static class MLHelpers
{ 
    public static MLItem[] GetTestSamples()
    {
        MLItem[] samples = new MLItem[4];
        samples[0] = new MLItem();
        samples[0].input = new double[]
        {
            0,0.42,0,0,
            0.33,0,0,0.12,
            0,0,0.4,0,
            0,0.2,0,0

        };
        samples[0].target = 1;

        samples[1] = new MLItem();
        samples[1].input = new double[] 
        {
            0,0,0.2,0,
            0.2,0,0,0.4,
            0,0.2,0,0,
            0,0,0.2,0,
        };
        samples[1].target = 0;

        samples[2] = new MLItem();
        samples[2].input = new double[]
        {
            0,0,0.2,0,
            0,0.2,0,0,
            0.2,0,0,0.2,
            0,0,0.2,0,
        };
        samples[2].target = 1;

        samples[3] = new MLItem();
        samples[3].input = new double[]
        {
            0,0.2,0,0,
            0,0,0.2,0,
            0.2,0,0,0.2,
            0,0.2,0,0,
        };
        samples[3].target = 0;

        return samples;
    }
}

public class Test
{
    public Test()
    {
        double[] kSlopes = { .2, .2, -.5, .3, .6, .2, -.3, 0, -.4 };
        kernel = new Datastructure<double>();
        kernel.InsertArrayOnDataItemsLst(kSlopes);
    }
    
    public double[] kbiases = { .5, .2, .5, .6 };
    public double[] nodeSlopes = { .1, .23, .12, -.4 };
    public double nodeBias = .2;

    double target = 1;
    double a = .2;
    int epochs = 100;
    double e = 0;
    double g = 0;

    public Datastructure<double> kernel;
    public (double, double[]) CalculateLoss(double[] activations, MLItem[] samples)
    {
        double[] calculations = new double[activations.Length];
        double[] derivatives  = new double[activations.Length];
        
        for (int i = 0; i < calculations.Length; i++)
        {
            //calculations[i] = Math.Pow(activations[i] - samples[i].target, 2);
            //derivatives[i]  = 2 * (activations[i] - samples[i].target);
            calculations[i] = samples[i].target == 1 ? -Math.Log(activations[i]) : -Math.Log(1 - activations[i]);
            derivatives[i] = samples[i].target == 1 ? -1 / (activations[i]) : 1 / (1 - activations[i]);
        }

        return (calculations.Average(), derivatives);
    }
    public void Train(MLItem[] items)
    {
        #region Variables
        double[][][] convMultWith = new double[items.Length][][];
        double[][] convActivations = new double[items.Length][];
        double[][] convDerivatives = new double[items.Length][];

        double[] nodeMultWith = new double[items.Length];
        double[] nodeActivations = new double[items.Length];
        double[] nodeDerivatives = new double[items.Length];
        #endregion
        #region Train
        for (int sample = 0; sample < items.Length; sample++)
        {
            double[] sampleInput = items[sample].input;
            ConvDatastructure conv = new ConvDatastructure();
            conv.InsertArrayOnDataItemsArr(sampleInput);
            conv.ApplyKernelOnSample(kernel);

            double[] cy = conv.calcsSummed.Select((c, i) => c + kbiases[i]).ToArray();
            convActivations[sample] = cy.Select(pred=> pred > 0 ? pred : 0).ToArray();
            convDerivatives[sample] = cy.Select(pred=> pred > 0 ? 1.0 : 0).ToArray();
            convMultWith[sample] = conv.multipliedWith;

            double ny = nodeSlopes.Select((s, i) => s * convActivations[sample][i]).Sum() + nodeBias;
            nodeActivations[sample] = 1 / (1 + Math.Exp(-ny));
            nodeDerivatives[sample] = nodeActivations[sample] * (1 - nodeActivations[sample]);
        }
        #endregion
        #region Loss Calculation
        (double loss, double[] lossDerivatives) calc = CalculateLoss(nodeActivations, items);
        g = calc.loss;
        #endregion
        #region Node Gradient
        double[] nodeDB = new double[nodeDerivatives.Length];
        double[][] nodeDw = new double[nodeDerivatives.Length][];
        double[][] nodeDCA = new double[nodeDerivatives.Length][];
        for (int i = 0; i < nodeDB.Length; i++)
            nodeDB[i] = nodeDerivatives[i] * calc.lossDerivatives[i];
        for (int i = 0; i < nodeDw.Length; i++)
        {
            double selectedGradient = nodeDB[i];
            double[] selectedNodeDerivative = convActivations[i];
            double[] result = new double[selectedNodeDerivative.Length];
            for (int j = 0; j < selectedNodeDerivative.Length; j++)
                result[j] = selectedGradient * selectedNodeDerivative[j];
            nodeDw[i] = result;

            double[] dcaCalculations = new double[nodeSlopes.Length];
            for (int j = 0; j < nodeSlopes.Length; j++)
                dcaCalculations[j] = selectedGradient * nodeSlopes[j];
            nodeDCA[i] = dcaCalculations;
        }

        #region Propagate Slopes
        for (int slope = 0; slope < nodeSlopes.Length; slope++)
            nodeSlopes[slope] = nodeSlopes[slope] - a * nodeDw.Select(x => x[slope]).Average();
        nodeBias = nodeBias - a * nodeDB.Average();
        #endregion
        #endregion
        #region Conv Gradient
        double[][] convDB = new double[convDerivatives.Length][];
        double[][] convDW = new double[convDerivatives.Length][];
        for (int der = 0; der < convDB.Length; der++)
        {
            double[] selectedConvDerivative = convDerivatives[der];
            double[] selectedNodeDCA = nodeDCA[der];
            double[] calculation = new double[selectedNodeDCA.Length];
            for (int element = 0; element < selectedNodeDCA.Length; element++)
                calculation[element] = selectedConvDerivative[element] * selectedNodeDCA[element];
            convDB[der] = calculation;

            double[][] multWith = convMultWith[der];
            double[] dwCalcs = new double[kernel.dataItemsLst.Count];
            for (int feature = 0; feature < kernel.dataItemsLst.Count; feature++)
            {
                double[] selectedMultipliedWith = multWith.Select(x => x[feature]).ToArray();
                double[] tmp = new double[selectedMultipliedWith.Length];
                for (int element = 0; element < tmp.Length; element++)
                    tmp[element] = selectedMultipliedWith[element] * calculation[element];
                dwCalcs[feature] = tmp.Sum();
            }
            convDW[der] = dwCalcs;
        }
        #region Conv Propagate
        for (int k = 0; k < kernel.dataItemsLst.Count; k++)
            kernel.dataItemsLst[k] = kernel.dataItemsLst[k] - a * convDW.Select(x => x[k]).Average();
        for (int b = 0; b < kbiases.Length; b++)
            kbiases[b] = kbiases[b] - a * convDB.Select(x => x[b]).Average();
        #endregion
        #endregion
    }
}
public class Program
{
    public static void Main(string[] args)
    {
        MLItem[] testSamples = MLHelpers.GetTestSamples();

        Test t = new Test();
        int epochs = 10000;
        for(int epoch = 0; epoch < epochs; epoch++)
            t.Train(testSamples);

        double[][] evalSamples = new double[][] {
            new double[] 
            {
                .2,0,0,0.2,
                0,0,0.2,0,
                0,0.2,0,0,
                0.2,0,0,0
            },
            new double[]
            {
                0.2,0,0,0,
                0,0.2,0,0,
                0,0,0.2,0,
                .2,0,0,0.2
            },
            new double[]
            {
                0,0,0,0,
                0,0,0,0,
                0.2,0,0,0,
                0,0.2,0,0
            },
            new double[]
            {
                0,0,0.2,0,
                0,0,0,0.2,
                0,0,0,0,
                0,0,0,0,
            }
        };

        for (int sample = 0; sample < evalSamples.Length; sample++)
        {
            ConvDatastructure econv = new ConvDatastructure();
            econv.InsertArrayOnDataItemsArr(evalSamples[sample]);
            econv.ApplyKernelOnSample(t.kernel);
            double[] econvCalcs = econv.calcsSummed.Select((calc, i) => calc + t.kbiases[i]).ToArray();
            double[] econvActs = econvCalcs.Select(x => x > 0 ? x : 0).ToArray();
            double enodeCalcs = t.nodeSlopes.Select((slope, idx) => slope * econvActs[idx]).Sum() + t.nodeBias;
            double enodeAct = 1 / (1 + Math.Exp(-enodeCalcs));
        }
    }
}
