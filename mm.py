
public class LoopControls : IDisposable
{
    public int index_position  { get; set; } = -1;
    public int loop_multiplier { get; set; } = 1;
    public int loopid          { get; set; }

    public void UpdateLoopId(ImgProcessingConfig conf)
    {
        loopid = (conf.stride * (loop_multiplier * conf.img_dimention)) - conf.stride;
        loop_multiplier++;
    }
    public int GetIndexSavePosition()
    {
        index_position++;
        return index_position;
    }
    public void Dispose()
    {}
}
public class ImgProcessingConfig
{
    private int _origsize { get; set; }
    public PoolMethod poolmethod { get; set; } = PoolMethod.MaxPool;
    public int padding   { get; set; } = 0;
    public int stride    { get; set; } = 1;
    public int poolcount { get; set; } = 0;
    public int padcount  { get; set; } = 0;
    public Dictionary<int, double[]> kernels { get; set; } = new Dictionary<int, double[]>();
    public int original_size { get { return _origsize; } set { _origsize = value; img_dimention = (int)Math.Sqrt(value); } }
    public int img_dimention { get; set; }
    public int ker_dimention { get; set; }

    public void AddKernel(double[] kernel)
    {
        int key = kernels.Count();
        kernels.Add(key, kernel);
    }
    public int GetNewArraySize<T>(T kernel)
    {
        int kernelsize = 0;
        if (kernel is int)
            kernelsize = Convert.ToInt32(kernel);
        else
            kernelsize = (int)Math.Sqrt((kernel as double[]).Length);

        ker_dimention = kernelsize;
        return (int)Math.Pow(((img_dimention + (2 * padding) - ker_dimention) / stride) + 1, 2);
    }
}
