public class PageAggregatorService : IPageAggregator
{
    private readonly IExternalDataService _externalService;

    public PageAggregatorService(IExternalDataService externalService)
    {
        _externalService = externalService;
    }

    public async Task<PagePayload> LoadPageDataSequentialAsync(int userId)
    {
        Console.WriteLine("=== ПОСЛЕДОВАТЕЛЬНАЯ ЗАГРУЗКА ===");
        
        var userData = await _externalService.GetUserDataAsync(userId);
        var orderData = await _externalService.GetUserOrdersAsync(userId);
        var adData = await _externalService.GetAdsAsync();

        return new PagePayload
        {
            UserData = userData,
            OrderData = orderData,
            AdData = adData
        };
    }

    public async Task<PagePayload> LoadPageDataParallelAsync(int userId)
    {
        Console.WriteLine("=== ПАРАЛЛЕЛЬНАЯ ЗАГРУЗКА ===");
        
        var userTask = _externalService.GetUserDataAsync(userId);
        var ordersTask = _externalService.GetUserOrdersAsync(userId);
        var adsTask = _externalService.GetAdsAsync();

        await Task.WhenAll(userTask, ordersTask, adsTask);

        return new PagePayload
        {
            UserData = userTask.Result,
            OrderData = ordersTask.Result,
            AdData = adsTask.Result
        };
    }
}