using System;
using System.Collections.Generic;
using System.Linq;

namespace ConsoleApp2
{
    class Program
    {
        static bool CheckCondition(RangeItem range, int value)
        {
            return ((range.min > 0 && value >= range.min) && (range.max > 0 && value <= range.max)) || (range.min == 0 && value <= range.max) || (value >= range.min && range.max == 0);
        }
        static void Main(string[] args)
        {
            Random rnd = new Random();
            TestItem[] items = Enumerable.Range(0, 3200000).Select(x => new TestItem() { value = (int)(x + 1), amenity = rnd.Next(12) }).ToArray();
            TestItem[] collection = new TestItem[0];

            MainTest t = new MainTest();
            t.prop1 = "600,700";
            t.prop2 = "1,";
            t.prop3 = "1,5";
            t.prop4 = "1,2";
            
            SecondTest filters = t.stest;
            if(!filters.prop1.Length.Equals(0))
                collection = items.Where(x => CheckCondition(filters.prop1.ToRangeItem(), x.value)).ToArray();
            if(!filters.prop4.Length.Equals(0))
                collection = (collection.Any() ? collection : items).Where(x => filters.prop4.Contains(x.amenity)).ToArray();
        }
    }
}
