using Xamarin.Forms;

namespace exploresc
{
    public partial class explorescPage : ContentPage
    {
        public explorescPage()
        {
            InitializeComponent();
            var web_view = webView1;
            var htmlSource = new HtmlWebViewSource();
            htmlSource.Html = @"<html><body>
  <h1>Xamarin.Forms</h1>
  <p>Welcome to WebView.</p>
  </body></html>";
            var source = new UrlWebViewSource
            {
                Url = DependencyService.Get<IBaseUrl>().Get() + "/index.html"
            };
            web_view.Source = source;

        }
    }
    public interface IBaseUrl { string Get(); }

}
