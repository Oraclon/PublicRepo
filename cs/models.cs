using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp2
{
    
    public class RangeItem
    {
        public int min { get; set; }
        public int max { get; set; }
    }
    public class SecondTest
    {
        public int[] price { get; set; } = new int[0];
        public int[] rooms { get; set; } = new int[0];
        public int[] floor { get; set; } = new int[0];
        public int[] amenity { get; set; } = new int[0];
    }

    public class MainTest
    {
        public SecondTest stest = new SecondTest();
        public string prop1
        {
            set
            {
                if (!string.IsNullOrEmpty(value))
                    stest.price = value.SplitStringFilter();
            }
            get
            {
                return stest.price == null ? string.Empty : string.Join(",", stest.price);
            }
        }
        public string prop2
        {
            set
            {
                if (!string.IsNullOrEmpty(value))
                    stest.rooms = value.SplitStringFilter();
            }
            get
            {
                return stest.rooms == null ? string.Empty : string.Join(",", stest.rooms);
            }
        }
        public string prop3
        {
            set
            {
                if (!string.IsNullOrEmpty(value))
                    stest.floor = value.SplitStringFilter();
            }
            get
            {
                return stest.floor == null ? string.Empty : string.Join(",", stest.floor);
            }
        }
        public string prop4
        {
            set
            {
                if (!string.IsNullOrEmpty(value))
                    stest.amenity = value.SplitStringFilter();
            }
            get
            {
                return stest.amenity == null ? string.Empty : string.Join(",", stest.amenity);
            }
        }
    }
    
    public class PropertyItem
    {
        public PropertyItem(Random rand)
        {
            amenity = rand.Next(1, 10);
            rooms = rand.Next(1, 6);
            floor = rand.Next(1, 12);

            int amenitiesSize = rand.Next(1, 10);
            amenities = Enumerable.Range(0, amenitiesSize).Select(x => rand.Next(1, 20)).ToArray();
        }
        public int price { get; set; }
        public int floor { get; set; }
        public int rooms { get; set; }
        public int amenity { get; set; }
        public int[] amenities { get; set; }
    }
    public class SearchResult
    {
        public int resultsCount { get; set; }
        private List<PropertyItem> _tmp = new List<PropertyItem>();
        public List<PropertyItem> resultsList { get { return _tmp; } set { _tmp = value; resultsCount = value.Count; } }
    }
}
