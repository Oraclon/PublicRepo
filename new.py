#region [Loss Calculations]
        private void _UpdateLoss(double[][] results)
        {
            double[] losses = new double[results.Length];
            for(int i = 0; i < results.Length; i++)
            {
                switch(error)
                {
                    case Error.Mean:
                        losses[i] = results[i].Length > 1 ? results[i].Sum() : results[i][0];
                    break;
                    case Error.LogLoss:
                        losses[i] = results[i].Length > 1 ? results[i].Sum() : results[i][0];
                    break;
                    case Error.CrossEntropy:
                        losses[i] = results[i].Length > 1 ? -(results[i].Sum()) : -results[i][0];
                    break;
                }
            }
            
            loss = error == Error.Mean ? losses.Sum() / (2*losses.Length) : losses.Sum() / losses.Length;
            if(loss <= locker)
                keepTrain = false;
        }
        private double _CalculateLoss(double activation, double target)
        {
            double res = 0;
            switch(error)
            {
                case Error.Mean:
                    res = Math.Pow(activation-target,2);
                break;
                case Error.CrossEntropy:
                    res = target*Math.Log(activation);
                break;
                case Error.LogLoss:
                    res = target.Equals(1) ? Math.Log(activation) : Math.Log(1-activation);
                break;
            }
            return res;
        }
        private double _CalculateDerivative(double activation, double target)
        {
            double res = 0;
            switch(error)
            {
                case Error.Mean:
                    res = 2*(activation-target);
                break;
                case Error.LogLoss:
                    res = target == 1 ? -1/activation : 1/(1-activation);
                break;
                case Error.CrossEntropy:
                    // res = -(target/activation);
                    res = activation - target;
                break;
            }
            return res;
        }
        public void LossCalculation(double[][] activations, double[] targets)
        {
            int inner = activations[0].Length;
            double[][] loss_calcs = new double[activations.Length][];
            double[][] ders_calcs = new double[activations.Length][];
            #region [Loss Calculations]
            for(int i = 0; i < activations.Length; i++)
            {
                double[] tmp = new double[inner];
                for(int j = 0; j < inner; j++)
                {
                    tmp[j] = _CalculateLoss(activations[i][j], targets[i]);
                } 
                loss_calcs[i] = tmp;  
            }
            _UpdateLoss(loss_calcs);
            #endregion
            #region [Derivatives Calculations]
            for(int i = 0; i < activations.Length; i++)
            {
                double[] tmp = new double[inner];
                for(int j = 0; j < inner; j++)
                {
                    tmp[j] = _CalculateDerivative(activations[i][j], targets[i]);
                }
                ders_calcs[i] = tmp;
            }
            layerLossDerivs = ders_calcs;
            #endregion
        }
        #endregion
