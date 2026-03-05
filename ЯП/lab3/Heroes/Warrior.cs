namespace CSConsoleApp.Heroes
{
    class Warrior : Hero
    {
        public Warrior() : base("Warrior", 100, 30, 5) { }

        public override void Attack(Hero target)
        {
            ApplySpecialAbility(target);
            int damage = AttackPower - target.Defense;

            if (damage < 0) damage = 0;

            target.TakeDamage(damage);

            Console.WriteLine($"{Name} attacks {target.Name} for {damage} damage!");
        }

        public override void ApplySpecialAbility(params Hero[] hero)
        {
            if (new Random().NextDouble() >= 0.3) {
                foreach (var h in hero)
                {
                    h.Attack(h);
                }
                Console.WriteLine($"{Name} double attack!");
            }
        }
    }
}