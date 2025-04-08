using System;
using System.Collections.Generic;
using System.Linq;

namespace ConsoleApp2
{
    class Program
    {
        
         static void Main(string[] args)
        {
            Random rnd = new Random();
            List<PropertyItem> items = Enumerable.Range(0, 1000).Select(x => new PropertyItem(rnd) { price = (int)(x + 1) }).OrderBy(x=> rnd.Next()).ToList();
            PropertyItem[] collection = new PropertyItem[0];

            MainTest t = new MainTest();
            //price
            t.prop1 = "800,900";
            //floor
            t.prop2 = "4,";
            //rooms
            t.prop3 = "2,";
            //amenity
            t.prop4 = "4,7,8,9";
            
            SecondTest filters = t.stest;

            SearchResult result = new SearchResult();
            //Filter by price
            if (!filters.price.Length.Equals(0))
                result.resultsList = items.ApplyRangeFilter(filters.price.ToRangeItem(), ValueType.Price);
            if (!filters.floor.Length.Equals(0))
                result.resultsList = (result.resultsList.Any() ? result.resultsList : items).ApplyRangeFilter(filters.floor.ToRangeItem(), ValueType.Floor);
            if (!filters.rooms.Length.Equals(0))
                result.resultsList = (result.resultsList.Any() ? result.resultsList : items).ApplyRangeFilter(filters.rooms.ToRangeItem(), ValueType.Room);
            if (!filters.amenity.Length.Equals(0))
                result.resultsList = result.resultsList.ApplyAmenityFilter(filters.amenity);
        }
    }
}
