using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Xamarin.Forms;
using Xamarin.Forms.Xaml;
using YoutubeExplode.Models;
using YoutubeMusicPlayer.Components;

namespace YoutubeMusicPlayer
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class SongList : ContentPage
    {
        private Playing PlayingView;
        private List<CellClass> Items;

        public SongList(Playlist playlist, Playing playingView)
        {
            InitializeComponent();
            PlayingView = playingView;
            Items = playlist.Videos.Select((o, Index) => new CellClass { Title = o.Title, Image = GetLowestResImageUrl(o), Index = Index }).ToList();
            SongListView.ItemsSource = Items;
            SetSelectedItem(PlayingView.Index);
        }

        public void SetSelectedItem(int index)
        {
            SongListView.BeginRefresh();
            SongListView.SelectedItem = Items[index - 1];
            SongListView.EndRefresh();
        }

        public void ScrollToIndex(int index)
            => SongListView.ScrollTo(Items[index - 1], ScrollToPosition.Start, false);

        private static string GetLowestResImageUrl(Video o)
            => o.Thumbnails.LowResUrl ?? (o.Thumbnails.MediumResUrl ?? o.Thumbnails.HighResUrl);

        protected override bool OnBackButtonPressed()
        {
            Navigation.PopModalAsync();
            base.OnBackButtonPressed();
            return true;
        }

        private async void OnListItemTap(object sender, EventArgs args)
        {
            var imageCell = sender as IndexImageCell;
            PlayingView.Index = imageCell.ListIndex;
            PlayingView.RunWithCancellation();
        }

        private class CellClass
        {
            public string Title { get; set; }
            public string Image { get; set; }
            public int Index { get; set; }
        }
    }
}