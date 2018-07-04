using System;
using System.Collections.Generic;
using System.Text;
using Xamarin.Forms;

namespace YoutubeMusicPlayer.Components
{
    public class IndexImageCell : ImageCell
    {
        public static readonly BindableProperty ListIndexProperty =
              BindableProperty.Create("ListIndex", typeof(int), typeof(int), default(int));

        public int ListIndex
        {
            get { return (int)GetValue(ListIndexProperty); }
            set { SetValue(ListIndexProperty, value); }
        }
    }
}
