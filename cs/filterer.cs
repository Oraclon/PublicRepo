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
            TestItem[] items = Enumerable.Range(0, 100000).Select(x => new TestItem(rnd) { price = (int)(x + 1) }).OrderBy(x=> rnd.Next()).ToArray();
            TestItem[] collection = new TestItem[0];

            MainTest t = new MainTest();
            //price
            t.prop1 = "800,";
            //floor
            t.prop2 = "11,";
            //rooms
            t.prop3 = "2,";
            //amenity
            t.prop4 = "1,2,4,7";
            
            SecondTest filters = t.stest;
            //Search by price
            if(!filters.price.Length.Equals(0))
                collection = items.Where(x => CheckCondition(filters.price.ToRangeItem(), x.price)).ToArray();
            //Search by roof
            if (!filters.floor.Length.Equals(0))
                collection = (collection.Any() ? collection : items).Where(x => CheckCondition(filters.floor.ToRangeItem(), x.floor)).ToArray();
            //Search by rooms
            if (!filters.rooms.Length.Equals(0))
                collection = (collection.Any() ? collection : items).Where(x => CheckCondition(filters.rooms.ToRangeItem(), x.rooms)).ToArray();
            //Search by amenity (Not part of primary search thats why collection.any() removed)
            if (!filters.amenity.Length.Equals(0))
                collection = collection.Where(x => filters.amenity.Contains(x.amenity)).ToArray();
        }
    }
}
