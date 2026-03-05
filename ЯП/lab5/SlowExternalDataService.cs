public class SlowExternalDataService : IExternalDataService
{
    public async Task<string> GetUserDataAsync(int userId)
    {
        Console.WriteLine($"[{DateTime.Now:HH:mm:ss.fff}] GetUserDataAsync: Начало выполнения");
        await Task.Delay(2000);
        string result = $"Данные пользователя {userId}";
        Console.WriteLine($"[{DateTime.Now:HH:mm:ss.fff}] GetUserDataAsync: Завершено");
        return result;
    }

    public async Task<string> GetUserOrdersAsync(int userId)
    {
        Console.WriteLine($"[{DateTime.Now:HH:mm:ss.fff}] GetUserOrdersAsync: Начало выполнения");
        await Task.Delay(3000);
        string result = $"Заказы пользователя {userId}";
        Console.WriteLine($"[{DateTime.Now:HH:mm:ss.fff}] GetUserOrdersAsync: Завершено");
        return result;
    }

    public async Task<string> GetAdsAsync()
    {
        Console.WriteLine($"[{DateTime.Now:HH:mm:ss.fff}] GetAdsAsync: Начало выполнения");
        await Task.Delay(1000);
        string result = "Рекламный контент";
        Console.WriteLine($"[{DateTime.Now:HH:mm:ss.fff}] GetAdsAsync: Завершено");
        return result;
    }
}
