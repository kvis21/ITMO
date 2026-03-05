public interface IExternalDataService
{
    Task<string> GetUserDataAsync(int userId);
    Task<string> GetUserOrdersAsync(int userId);
    Task<string> GetAdsAsync();
}

public class PagePayload
{
    public string? UserData { get; set; }
    public string? OrderData { get; set; }
    public string? AdData { get; set; }

    public override string ToString()
    {
        return $"--- Агрегированный результат --- \nПользователь: {UserData}\nЗаказы: {OrderData}\nРеклама: {AdData}\n-----------------";
    }
}

public interface IPageAggregator
{
    Task<PagePayload> LoadPageDataSequentialAsync(int userId);
    Task<PagePayload> LoadPageDataParallelAsync(int userId);
}