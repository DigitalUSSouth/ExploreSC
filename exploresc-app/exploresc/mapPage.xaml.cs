using System;
using System.Collections.Generic;

using Xamarin.Forms;

namespace exploresc
{
    public partial class mapPage : ContentPage
    {
        public mapPage()
        {

            InitializeComponent();
            var web_view = mainWebView;

            var source = new UrlWebViewSource
            {
                Url = DependencyService.Get<IBaseUrl>().Get() + "/index.html"
                // = "https://www.digitalussouth.org/"
            };
            web_view.Source = source;
            web_view.Navigating += (s, e) =>
            {
                if (e.Url.StartsWith("https://www.google.com"))
                {
                    try
                    {
                        var uri = new Uri(e.Url);
                        Device.OpenUri(uri);
                    }
                    catch (Exception)
                    {
                    }

                    e.Cancel = true;
                }
            };

        }
    }
}
