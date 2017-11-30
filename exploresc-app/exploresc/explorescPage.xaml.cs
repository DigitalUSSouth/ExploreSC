using Xamarin.Forms;

namespace exploresc
{
    public partial class explorescPage : ContentPage
    {
        public explorescPage()
        {
            InitializeComponent();
            var web_view = mainWebView;

            var source = new UrlWebViewSource
            {
                Url = DependencyService.Get<IBaseUrl>().Get() + "/index.html"
            };
            web_view.Source = source;

        }
    }
    public interface IBaseUrl { string Get(); }

}
