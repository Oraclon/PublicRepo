using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp2
{
    public class TestItem
    {
        public int value { get; set; }
        public int amenity { get; set; }
    }
    public class RangeItem
    {
        public int min { get; set; }
        public int max { get; set; }
    }
    public class SecondTest
    {
        public int[] prop1 { get; set; } = new int[0];
        public int[] prop2 { get; set; } = new int[0];
        public int[] prop3 { get; set; } = new int[0];
        public int[] prop4 { get; set; } = new int[0];
    }
public class MainTest
{
    public SecondTest stest = new SecondTest();
    public string prop1
    {
        set
        {
            if (!string.IsNullOrEmpty(value))
                stest.prop1 = value.SplitStringFilter();
        }
        get
        {
            return stest.prop1 == null ? string.Empty : string.Join(",", stest.prop1);
        }
    }
    public string prop2
    {
        set
        {
            if (!string.IsNullOrEmpty(value))
                stest.prop2 = value.SplitStringFilter();
        }
        get
        {
            return stest.prop2 == null ? string.Empty : string.Join(",", stest.prop2);
        }
    }
    public string prop3
    {
        set
        {
            if (!string.IsNullOrEmpty(value))
                stest.prop3 = value.SplitStringFilter();
        }
        get
        {
            return stest.prop3 == null ? string.Empty : string.Join(",", stest.prop3);
        }
    }
    public string prop4
    {
        set
        {
            if (!string.IsNullOrEmpty(value))
                stest.prop4 = value.SplitStringFilter();
        }
        get
        {
            return stest.prop4 == null ? string.Empty : string.Join(",", stest.prop4);
        }
    }
}
public static class Helpers
{
    public static int[] SplitStringFilter(this string input)
    {
        string[] splittedElements = input.Split(",");
        return splittedElements.Select(x => string.IsNullOrEmpty(x) ? (int)0 : Convert.ToInt16(x)).ToArray();
    }
    public static RangeItem ToRangeItem(this int[] value)
    {
        RangeItem item = new RangeItem();
        item.min = value[0];
        item.max = value[1];
        return item;
    }
}
}
