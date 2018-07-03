using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Android.Media;
using YoutubeExplode.Models; 
using Xamarin.Forms;
using Xamarin.Forms.Xaml;
using YoutubeExplode.Models.MediaStreams;
using YoutubeExplode;
using System.Threading;

namespace YoutubeMusicPlayer
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class Playing : ContentPage
    {
        public YoutubeClient YClient { get; set; }
        public Playlist CurrentPlaylist { get; set; }
        public MediaPlayer CurrentMedia { get; set; }
        public int Index { get; set; }

        object Lock = new object();
        CancellationTokenSource Source = new CancellationTokenSource();

        public Playing(YoutubeClient yclient, Playlist playlist)
        {
            InitializeComponent();
            YClient = yclient;
            CurrentPlaylist = playlist;
            CurrentMedia = new MediaPlayer();
            Index = 0;

            SetArt();
            PlayNextSongInPlayList(Source.Token);
        }

        protected override bool OnBackButtonPressed()
        {
            YClient = null;
            CurrentPlaylist = null;
            CurrentMedia.Reset();
            CurrentMedia.Dispose();
            Lock = null;
            Source = null;
            base.OnBackButtonPressed();
            return true;
        }

        public async void OnButton_Prev(object sender, EventArgs args)
        {
            if (Index - 2 < 0)
                return;
            Index -= 2;

            RunWithCancellation();
        }

        public async void OnButton_Play(object sender, EventArgs args)
        {
            if (CurrentMedia.IsPlaying)
                CurrentMedia.Pause();
            else
                CurrentMedia.Start();
        }

        public async void OnButton_Next(object sender, EventArgs args)
        {
            if (Index >= CurrentPlaylist.Videos.Count)
                return;

            RunWithCancellation();
        }

        private void RunWithCancellation()
        {
            lock (Lock)
            {
                if (Source != null)
                    Source.Cancel();
                Source = new CancellationTokenSource();
            }

            SetArt();
            var token = Source.Token;
            var t = Task.Run(() =>
            {
                CurrentMedia.Reset();
                token.ThrowIfCancellationRequested();
                PlayNextSongInPlayList(token);
            }, token);
        }

        private void SetArt()
        {
            Art.Source = CurrentPlaylist.Videos[Index].Thumbnails.MediumResUrl;
        }

        public void PlayNextSongInPlayList(CancellationToken ct)
        {
            var item = CurrentPlaylist.Videos[Index++];
            var result = YClient.GetVideoMediaStreamInfosAsync(item.Id).GetAwaiter().GetResult();
            ct.ThrowIfCancellationRequested();
            var url = result.Audio.WithHighestBitrate().Url;
            CurrentMedia.SetDataSource(url);
            CurrentMedia.Prepare();
            CurrentMedia.Start();
        }
    }
}