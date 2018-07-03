using Android.Media;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Xamarin.Forms;
using YoutubeExplode;
using YoutubeExplode.Models;

namespace YoutubeMusicPlayer
{
	public partial class MainPage : ContentPage
	{
        YoutubeClient YClient { get; set; }
        ContentPage PlayingPage;

		public MainPage()
		{
			InitializeComponent();

            YClient = new YoutubeClient();
		}

        public async void OnButtonPress(object sender, EventArgs args)
        {
            var id = Input.Text;
            // "PLNoB-hcIcvVd68WVqZGjWivuFgVgf5VVV"
            var playlist = await YClient.GetPlaylistAsync(id);

            PlayingPage = new Playing(YClient, playlist);
            await Navigation.PushModalAsync(PlayingPage);
        }
    }
}
