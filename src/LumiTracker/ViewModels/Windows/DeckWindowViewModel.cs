﻿using Wpf.Ui.Controls;

using LumiTracker.Config;
using LumiTracker.Models;
using System.Windows.Controls;
using LumiTracker.ViewModels.Pages;

#pragma warning disable CS8618

namespace LumiTracker.ViewModels.Windows
{
    public partial class DeckWindowViewModel : ObservableObject
    {
        // ui
        [ObservableProperty]
        private double _mainContentHeightRatio = 0.0;

        [ObservableProperty]
        private ScrollBarVisibility _VerticalScrollBarVisibility = ScrollBarVisibility.Hidden;

        [ObservableProperty]
        private SymbolRegular _toggleButtonIcon = SymbolRegular.ChevronUp48;

        [ObservableProperty]
        private bool _isShowing = false;

        // data
        [ObservableProperty]
        private CardList _myActionCardsPlayed;

        [ObservableProperty]
        private CardList _opActionCardsPlayed;

        [ObservableProperty]
        private CardList _myDeck;

        // controls
        [ObservableProperty]
        private bool _gameStarted = false;

        [ObservableProperty]
        private bool _gameNotStarted = true;
        partial void OnGameStartedChanged(bool oldValue, bool newValue)
        {
            GameNotStarted = !GameStarted;
        }

        [ObservableProperty]
        private int _round = 0;

        private GameWatcher _gameWatcher;

        private DeckViewModel _deckViewModel;

        public DeckWindowViewModel(GameWatcher gameWatcher, DeckViewModel deckViewModel)
        {
            _gameWatcher   = gameWatcher;
            _deckViewModel = deckViewModel;

            _gameWatcher.GameStarted        += OnGameStarted;
            _gameWatcher.MyActionCardPlayed += OnMyActionCardPlayed;
            _gameWatcher.OpActionCardPlayed += OnOpActionCardPlayed;
            _gameWatcher.GameOver           += OnGameOver;
            _gameWatcher.RoundDetected      += OnRoundDetected;
            _gameWatcher.MyCardsDrawn       += OnMyCardsDrawn;
            _gameWatcher.MyCardsCreateDeck  += OnMyCardsCreateDeck;
            _gameWatcher.OpCardsCreateDeck  += OnOpCardsCreateDeck;
            _gameWatcher.UnsupportedRatio   += OnUnsupportedRatio;

            _gameWatcher.WindowWatcherExit  += OnWindowWatcherExit;

            Reset(gameStart: false);
        }

        private void Reset(bool gameStart)
        {
            MyActionCardsPlayed = new CardList(CardList.SortType.TimestampDescending);
            OpActionCardsPlayed = new CardList(CardList.SortType.TimestampDescending);
            Round = 0;
            GameStarted = gameStart;
            if (gameStart)
            {
                MyDeck = new CardList(Configuration.Get<string>("share_code"));
            }
            else
            {
                MyDeck = new ();
            }
        }

        private void UpdatePlayedActionCard(int card_id, bool is_op)
        {
            CardList ActionCardsPlayed = is_op ? OpActionCardsPlayed : MyActionCardsPlayed;
            ActionCardsPlayed.Add(card_id);
        }

        private void OnGameStarted()
        {
            Reset(gameStart: true);
        }

        private void OnMyActionCardPlayed(int card_id)
        {
            UpdatePlayedActionCard(card_id, is_op: false);
        }

        private void OnOpActionCardPlayed(int card_id)
        {
            UpdatePlayedActionCard(card_id, is_op: true);
        }

        private void OnGameOver()
        {
            Reset(gameStart: false);
        }

        private void OnRoundDetected(int round)
        {
            Round = round;
        }

        private void OnMyCardsDrawn(int[] card_ids)
        {
            MyDeck.Remove(card_ids, keep_zero: true);
        }

        private void OnMyCardsCreateDeck(int[] card_ids)
        {
            MyDeck.Add(card_ids);
        }

        private void OnOpCardsCreateDeck(int[] card_ids)
        {

        }

        private void OnUnsupportedRatio()
        {
            System.Windows.MessageBox.Show(
                $"{LocalizationSource.Instance["UnsupportedRatioWarning"]}\n{LocalizationSource.Instance["SupportedRatioInfo"]}", 
                $"{LocalizationSource.Instance["AppName"]}", 
                System.Windows.MessageBoxButton.OK, System.Windows.MessageBoxImage.Warning);
        }

        private void OnWindowWatcherExit()
        {
            Reset(gameStart: false);
        }

    }
}
