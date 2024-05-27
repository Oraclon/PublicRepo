public static int[] KernelById(this int id, int size, int dimention)
    {
        int[] positions = new int[(int)Math.Pow(size, 2)];
        int key = 0;
        int multiplier = 0;

        for (int outter = 0; outter < size; outter++)
        {
            for (int i = 0; i < size; i++)
            {
                var pos = 0;
                if (multiplier.Equals(0))
                    pos = id + i;
                else
                    pos = id + dimention * multiplier + i;

                positions[key] = pos;
                key++;
            }
            multiplier++;
        }
        return positions;
    }
    public static double[] ApplyPooling(this double[] pixels, int poolsize = 2, PoolMethod method = PoolMethod.MaxPool)
    {
        #region [Loop Controls]
        int key = 0;
        #endregion
        #region [Sizes]
        int dimention = (int)Math.Sqrt(pixels.Length);
        int new_size = (dimention - poolsize) + 1;
        int loop_size = (int)Math.Pow(new_size, 2);
        #endregion
        #region [Apply Pooling]
        for (int i = 0; i < loop_size; i++)
        {
            int[] kernel = i.KernelById(poolsize, dimention);
        }
        #endregion
        return new double[2];
    }
public static double[] ApplyPadding(this double[] pixels, int padding = 1)
    {
        #region [Loop Controls]
        int key = 0;
        int inner_counter = 0;
        #endregion
        #region [Sizes]
        int tmp_size  = (int)(Math.Sqrt(pixels.Length) + (padding * 2));
        int loop_size = (int)Math.Pow(tmp_size, 2);
        #endregion
        #region [To Return]
        double[] padded = new double[loop_size];
        #endregion
        #region [Apply Padding]
        for (int i = 0; i < loop_size; i += tmp_size)
        {
            for (int j = i; j < (i + tmp_size); j++)
            {
                if ((i == 0) || (i == loop_size - tmp_size))
                {
                    Enumerable.Range(0, tmp_size).ToList().ForEach(x =>
                    {
                        padded[key] = 0;
                        key++;
                    });
                    break;
                }
                if (j % tmp_size == 0 || (j + padding) % tmp_size == 0) { padded[key] = 0; key++; }
                else
                {
                    padded[key] = pixels[inner_counter];
                    key++;
                    inner_counter++;
                }
            }
        }
        #endregion

        return padded;
    }
