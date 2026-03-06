namespace CSConsoleApp.Items
{
    public abstract class Item
    {
        public string Name { get; protected set; }
        public ItemSlot Slot { get; protected set; }
        public int AttackBonus { get; protected set; }
        public int DefenseBonus { get; protected set; }
        public int HealBonus { get; protected set; }
        public string Description { get; protected set; }

        protected Item(string name, ItemSlot slot, int attackBonus = 0, int defenseBonus = 0, string description = "")
        {
            Name = name;
            Slot = slot;
            AttackBonus = attackBonus;
            DefenseBonus = defenseBonus;
            Description = description;
        }

        public abstract void Use();
        public abstract string GetSpecialEffect();

        public override string ToString()
        {
            return $"{Name} ({Slot}) - ATK: +{AttackBonus}, DEF: +{DefenseBonus} - {GetSpecialEffect()}";
        }
    }

    public enum ItemSlot
    {
        Weapon,
        Head,
        Body
    }
}