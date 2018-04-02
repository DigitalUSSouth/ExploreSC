using System;
using System.Collections.Generic;

using Xamarin.Forms;
using Plugin.Geolocator;

namespace exploresc
{
    public partial class mapPage : ContentPage
    {
        public mapPage()
        {

            InitializeComponent();
            var web_view = mainWebView;


            //locator.PositionChanged += (sender, e) => {
                //var position = e.Position;
                //web_view.Eval(string.Format("updateMap({0}, {1})", position.Latitude, position.Longitude));
                //latitudeLabel.Text = position.Latitude;
                //longitudeLabel.Text = position.Longitude;
            //};

            //Debug.WriteLine("Position Status: {0}", position.Timestamp);
            //Debug.WriteLine("Position Latitude: {0}", position.Latitude);
            //Debug.WriteLine("Position Longitude: {0}", position.Longitude);


            var source = new UrlWebViewSource
            {
                Url = DependencyService.Get<IBaseUrl>().Get() + "/index.html"
                // = "https://www.digitalussouth.org/"
            };
            web_view.Source = source;
            web_view.Navigating += async (s, e) =>
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
                if (e.Url.EndsWith("getLoc"))
                {
                    try
                    {
                        var locator = CrossGeolocator.Current;

                        var position = await locator.GetPositionAsync(TimeSpan.FromSeconds(2));

                        web_view.Eval(string.Format("updateMap({0}, {1})", position.Latitude, position.Longitude));
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
