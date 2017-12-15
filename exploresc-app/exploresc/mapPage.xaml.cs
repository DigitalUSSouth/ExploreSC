using System;
using System.Collections.Generic;

using Xamarin.Forms;

namespace exploresc
{
    public partial class mapPage : ContentPage
    {
        int count = 0;

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

        }

        public void OnButtonClicked(object sender, EventArgs args)
        {
            count++;

            ((Button)sender).Text =
                String.Format("{0} click{1}!", count, count == 1 ? "" : "s");
        }
    }
}
