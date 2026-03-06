using CSConsoleApp.Heroes;

namespace CSConsoleApp
{
    static class Program
    {
        public static void Main(string[] args)
        {
            BattleManager battleManager = RegisterHeroes();
            foreach (Hero hero in battleManager.GetHeroes())
            {
                Console.WriteLine($"{hero.Name} - HP: {hero.HP}, Attack: {hero.AttackPower}, Defense: {hero.Defense}");
            }

            battleManager.StartBattle();
            Console.ReadKey();
        }

        public static BattleManager RegisterHeroes()
        {
            BattleManager battleManager = new BattleManager();
            battleManager.AddHero(new Knight());
            battleManager.AddHero(new Wizard());
            battleManager.AddHero(new Warrior());
            return battleManager;
        }
        
    }
}