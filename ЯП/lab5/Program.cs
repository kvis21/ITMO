using System;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        Console.WriteLine("ЛАБОРАТОРНАЯ РАБОТА: АСИНХРОННОЕ ПРОГРАММИРОВАНИЕ\n");
        
        var externalService = new SlowExternalDataService();
        var aggregator = new PageAggregatorService(externalService);
        
        int testUserId = 123;

        Console.WriteLine("1. ТЕСТИРОВАНИЕ ПОСЛЕДОВАТЕЛЬНОГО ПОДХОДА");
        var sequentialStopwatch = Stopwatch.StartNew();
        var sequentialResult = await aggregator.LoadPageDataSequentialAsync(testUserId);
        sequentialStopwatch.Stop();
        
        Console.WriteLine(sequentialResult);
        Console.WriteLine($"Время выполнения последовательного метода: {sequentialStopwatch.ElapsedMilliseconds} мс\n");

        Console.WriteLine("Ожидание 2 секунды...\n");
        await Task.Delay(2000);

        Console.WriteLine("2. ТЕСТИРОВАНИЕ ПАРАЛЛЕЛЬНОГО ПОДХОДА");
        var parallelStopwatch = Stopwatch.StartNew();
        var parallelResult = await aggregator.LoadPageDataParallelAsync(testUserId);
        parallelStopwatch.Stop();
        
        Console.WriteLine(parallelResult);
        Console.WriteLine($"Время выполнения параллельного метода: {parallelStopwatch.ElapsedMilliseconds} мс\n");

        Console.WriteLine("АНАЛИЗ РЕЗУЛЬТАТОВ:");
        Console.WriteLine($"Последовательный подход: {sequentialStopwatch.ElapsedMilliseconds} мс");
        Console.WriteLine($"Параллельный подход: {parallelStopwatch.ElapsedMilliseconds} мс");
        Console.WriteLine($"Экономия времени: {sequentialStopwatch.ElapsedMilliseconds - parallelStopwatch.ElapsedMilliseconds} мс");
        Console.WriteLine($"Ускорение в {sequentialStopwatch.ElapsedMilliseconds / (double)parallelStopwatch.ElapsedMilliseconds:F2} раза");

    }

}