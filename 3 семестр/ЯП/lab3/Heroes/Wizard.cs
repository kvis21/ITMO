namespace CSConsoleApp.Heroes
{
    public sealed class Wizard : Hero
    {
        public Wizard() : base("Wizard", 70, 40, 0) { }

        public override void TakeDamage(int damage)
        {
            
            HP -= damage;

            if (HP < 0) {
                HP = 0;
            } else {
                ApplySpecialAbility();
            }

            Console.WriteLine($"{Name} takes {damage} damage! Remaining HP: {HP}");
        }

        public override void ApplySpecialAbility(params Hero[] heroes)
        {
            int healAmount = new Random().Next(15, 26);
            this.Heal(healAmount);
        }

    }
}