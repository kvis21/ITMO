namespace CSConsoleApp.Heroes
{
    class Knight : Hero
    {
        public bool Block = false;
        public Knight() : base("Knight", 150, 20, 10) { }


        public override void TakeDamage(int damage)
        {
            ApplySpecialAbility();
            if (Block)
            {
                Block = false;
                Console.WriteLine($"{Name} blocked the attack!");
                return;
            }

            HP -= damage;

            if (HP < 0)
                HP = 0;

            Console.WriteLine($"{Name} takes {damage} damage! Remaining HP: {HP}");
        }

        public override void ApplySpecialAbility(params Hero[] hero)
        {
            Block = new Random().NextDouble() >= 0.5 ? true : false;
        }
    }
}