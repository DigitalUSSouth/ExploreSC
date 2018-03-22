using Xamarin.Forms;

namespace exploresc
{
    public partial class explorescPage : TabbedPage
    {
        public explorescPage()
        {
            InitializeComponent();
            /*var web_view = mainWebView;

            var source = new UrlWebViewSource
            {
                Url = DependencyService.Get<IBaseUrl>().Get() + "/index.html"
                // = "https://www.digitalussouth.org/"
            };
            web_view.Source = source;*/

        }
    }
    public interface IBaseUrl { string Get(); }

}
