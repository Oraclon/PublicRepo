using System;
using System.Collections.Generic;
using System.Linq;

namespace ConsoleApp2
{
    public enum ValueType
    {
        Price,
        Floor,
        Room
    }
    public static class FilterHelpers
    {
        public static bool CheckCondition(RangeItem range, int value)
        {
            return ((range.min > 0 && value >= range.min) && (range.max > 0 && value <= range.max)) || (range.min == 0 && value <= range.max) || (value >= range.min && range.max == 0);
        }
        public static bool CheckForAmenityInList(this int[] propertyAmenities, int[] filterAmenities)
        {
            bool response = false;
            for (int i = 0; i < propertyAmenities.Length; i++)
            {
                if (filterAmenities.Contains(propertyAmenities[i]))
                {
                    response = true;
                    break;
                }
            }
            return response;
        }
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
        public static List<PropertyItem> ApplyRangeFilter(this List<PropertyItem> items, RangeItem filter, ValueType type)
        {
            List<PropertyItem> collection = new List<PropertyItem>();
            for (int x = 0; x < items.Count; x++)
            {
                PropertyItem item = items[x];
                switch (type)
                {
                    case ValueType.Price:
                            if (CheckCondition(filter, item.price)) collection.Add(item);
                        break;
                    case ValueType.Room:
                            if (CheckCondition(filter, item.rooms)) collection.Add(item);
                        break;
                    case ValueType.Floor:
                            if (CheckCondition(filter, item.floor)) collection.Add(item);
                        break;
                }
            }
            return collection;
        }
        public static List<PropertyItem> ApplyAmenityFilter(this List<PropertyItem> items, int[] filterAmeniies)
        {
            List<PropertyItem> collection = new List<PropertyItem>();
            for (int x = 0; x < items.Count; x++)
                if (items[x].amenities.CheckForAmenityInList(filterAmeniies))
                    collection.Add(items[x]);
            return collection;
        }
    }
}
