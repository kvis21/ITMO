using CSConsoleApp.Items;

namespace CSConsoleApp.Heroes
{

    public abstract class Hero
    {
        private ItemSet ItemSet = new ItemSet(); 
        public string Name { get; set; }
        public int HP { get; set; }
        public int AttackPower { get; set; }
        public int Defense { get; set; }

        public Hero(string heroName, int hp, int attackPower, int defense)
        {
            if (string.IsNullOrWhiteSpace(heroName))
                throw new ArgumentException("Name cannot be null or empty.", nameof(heroName));
            var random = new Random();
            Name = heroName + $" #{random.Next(0, 1000)}";
            HP = hp;
            AttackPower = attackPower;
            Defense = defense ;
        }

        public virtual void Attack(Hero target)
        {
            int damage = AttackPower - target.Defense;

            if (damage < 0) damage = 0;

            target.TakeDamage(damage);

            Console.WriteLine($"{Name} attacks {target.Name} for {damage} damage!");
        }

        public virtual void TakeDamage(int damage)
        {
            HP -= damage;

            if (HP < 0)
                HP = 0;

            Console.WriteLine($"{Name} takes {damage} damage! Remaining HP: {HP}");
        }

        public virtual void Heal(int amount)
        {
            if (amount < 0)
                throw new ArgumentException("Heal amount cannot be negative.", nameof(amount));

            HP += amount;
            Console.WriteLine($"{Name} is healed by {amount}. Current HP: {HP}");
        }                                                   

        public abstract void ApplySpecialAbility(params Hero[] hero);

        public void EquipItem(Item item)
        {
            if (item != null)
            {
                ItemSet.EquipItem(item);
            }
        }
    }
}