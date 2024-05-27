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
