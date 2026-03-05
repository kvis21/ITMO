namespace CSConsoleApp.Items
{
    public class ItemSet
    {
        public Item Weapon { get; private set; }
        public Item Head { get; private set; }
        public Item Body { get; private set; }

        public bool EquipItem(Item item)
        {
            if (item == null)
                return false;

            switch (item.Slot)
            {
                case ItemSlot.Weapon:
                    Weapon = item;
                    return true;
                case ItemSlot.Head:
                    Head = item;
                    return true;
                case ItemSlot.Body:
                    Body = item;
                    return true;
                default:
                    return false;
            }
        }

        public bool UnequipItem(ItemSlot slot)
        {
            switch (slot)
            {
                case ItemSlot.Weapon:
                    if (Weapon != null)
                    {
                        Weapon = null;
                        return true;
                    }
                    break;
                case ItemSlot.Head:
                    if (Head != null)
                    {
                        Head = null;
                        return true;
                    }
                    break;
                case ItemSlot.Body:
                    if (Body != null)
                    {
                        Body = null;
                        return true;
                    }
                    break;
            }
            return false;
        }

        public Item GetItem(ItemSlot slot)
        {
            return slot switch
            {
                ItemSlot.Weapon => Weapon,
                ItemSlot.Head => Head,
                ItemSlot.Body => Body,
                _ => null
            };
        }

        public bool HasItem(ItemSlot slot)
        {
            return GetItem(slot) != null;
        }

        public int GetTotalAttackBonus()
        {
            int total = 0;
            total += Weapon?.AttackBonus ?? 0;
            total += Head?.AttackBonus ?? 0;
            total += Body?.AttackBonus ?? 0;
            return total;
        }

        public int GetTotalDefenseBonus()
        {
            int total = 0;
            total += Weapon?.DefenseBonus ?? 0;
            total += Head?.DefenseBonus ?? 0;
            total += Body?.DefenseBonus ?? 0;
            return total;
        }

        public int GetTotalHealBonus()
        {
            int total = 0;
            total += Weapon?.HealBonus ?? 0;
            total += Head?.HealBonus ?? 0;
            total += Body?.HealBonus ?? 0;
            return total;
        }

        public void Clear()
        {
            Weapon = null;
            Head = null;
            Body = null;
        }

        public IEnumerable<Item> GetAllItems()
        {
            var items = new List<Item>();
            if (Weapon != null) items.Add(Weapon);
            if (Head != null) items.Add(Head);
            if (Body != null) items.Add(Body);
            return items;
        }

        public override string ToString()
        {
            return $"Weapon: {Weapon?.Name ?? "None"}, Head: {Head?.Name ?? "None"}, Body: {Body?.Name ?? "None"}";
        }
    }
}