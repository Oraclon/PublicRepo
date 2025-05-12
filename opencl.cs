//package: dotnet add package OpenCL.Net

using System;
using OpenCL.Net;

class Program
{
    static void Main()
    {
        ErrorCode error;
        Platform[] platforms = Cl.GetPlatformIDs(out error);
        if (error != ErrorCode.Success) throw new Exception("OpenCL not found");

        Device[] devices = Cl.GetDeviceIDs(platforms[0], DeviceType.Gpu, out error);
        if (error != ErrorCode.Success) throw new Exception("GPU not found");

        Context context = Cl.CreateContext(null, 1, devices, null, IntPtr.Zero, out error);
        CommandQueue queue = Cl.CreateCommandQueue(context, devices[0], (CommandQueueProperties)0, out error);

        string source = @"
        __kernel void add(__global const float* a, __global const float* b, __global float* result) {
            int id = get_global_id(0);
            result[id] = a[id] + b[id];
        }";

        Program clProgram = Cl.CreateProgramWithSource(context, 1, new[] { source }, null, out error);
        error = Cl.BuildProgram(clProgram, 0, null, string.Empty, null, IntPtr.Zero);
        Kernel kernel = Cl.CreateKernel(clProgram, "add", out error);

        int vectorSize = 1024;
        float[] a = new float[vectorSize];
        float[] b = new float[vectorSize];
        float[] result = new float[vectorSize];
        for (int i = 0; i < vectorSize; i++) {
            a[i] = i;
            b[i] = i * 2;
        }

        IMem<float> bufferA = Cl.CreateBuffer(context, MemFlags.CopyHostPtr | MemFlags.ReadOnly, a, out error);
        IMem<float> bufferB = Cl.CreateBuffer(context, MemFlags.CopyHostPtr | MemFlags.ReadOnly, b, out error);
        IMem<float> bufferResult = Cl.CreateBuffer(context, MemFlags.WriteOnly, vectorSize * sizeof(float), out error);

        Cl.SetKernelArg(kernel, 0, bufferA);
        Cl.SetKernelArg(kernel, 1, bufferB);
        Cl.SetKernelArg(kernel, 2, bufferResult);

        Event clevent;
        Cl.EnqueueNDRangeKernel(queue, kernel, 1, null, new[] { (IntPtr)vectorSize }, null, 0, null, out clevent);
        Cl.EnqueueReadBuffer(queue, bufferResult, Bool.True, IntPtr.Zero, result, 0, null, out clevent);

        Cl.Finish(queue);

        Console.WriteLine($"Result[0] = {result[0]}");
    }
}
