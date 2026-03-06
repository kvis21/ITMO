using System.Runtime.InteropServices;

namespace CSConsoleApp
{
    public static class Program
    {
        public static void Main()
        {
            var currentDirectory = System.IO.Directory.GetCurrentDirectory();
            var filePath = System.IO.Directory.GetFiles(currentDirectory, "*.csv").First();

            IReadOnlyList<MovieCredit> movieCredits = null;
            try
            {
                var parser = new MovieCreditsParser(filePath);
                movieCredits = parser.Parse(); // Тип переменной теперь IReadOnlyList<MovieCredit>
            }
            catch (Exception exc)
            {
                Console.WriteLine("Не удалось распарсить csv");
                Environment.Exit(1);
            }
            var top10Actors = movieCredits
                                .SelectMany(movie => movie.Cast) 
                                .GroupBy(castMember => castMember.Name) 
                                .Select(group => new
                                {
                                    ActorName = group.Key,
                                    MovieCount = group.Count() 
                                })
                                .OrderByDescending(actor => actor.MovieCount) 
                                .Take(10); 

            Console.WriteLine(string.Join(Environment.NewLine, top10Actors.Select(a => $"{a.ActorName} - {a.MovieCount}")));
            
            var sampleCast = movieCredits.SelectMany(movie => movie.Cast).First();
            var properties = sampleCast.GetType().GetProperties();

            Console.WriteLine("\nКомпактный вывод всех полей:");
            var castToShow = movieCredits.SelectMany(movie => movie.Cast).Take(3);
            foreach (var castMember in castToShow)
            {
                var line = string.Join("; ", properties.Select(p => 
                    $"{p.Name}={p.GetValue(castMember)}"));
                Console.WriteLine(line);
            }



        }
    }
}