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
            TestItem[] items = Enumerable.Range(0, 60).Select(x => new TestItem(rnd) { price = (int)(x + 1) }).ToArray();
            TestItem[] collection = new TestItem[0];

            MainTest t = new MainTest();
            //price
            t.prop1 = ",100";
            //floor
            t.prop2 = "1,";
            //rooms
            t.prop3 = "1,5";
            //amenity
            t.prop4 = "1,2";
            
            SecondTest filters = t.stest;
            //Search by price
            if(!filters.prop1.Length.Equals(0))
                collection = items.Where(x => CheckCondition(filters.prop1.ToRangeItem(), x.price)).ToArray();
            //Search by roof
            if (!filters.prop2.Length.Equals(0))
                collection = (collection.Any() ? collection : items).Where(x => CheckCondition(filters.prop2.ToRangeItem(), x.floor)).ToArray();
            //Search by rooms
            if (!filters.prop3.Length.Equals(0))
                collection = (collection.Any() ? collection : items).Where(x => CheckCondition(filters.prop3.ToRangeItem(), x.floor)).ToArray();
            //Search by amenity
            if (!filters.prop4.Length.Equals(0))
                collection = (collection.Any() ? collection : items).Where(x => filters.prop4.Contains(x.amenity)).ToArray();
        }
    }
}
