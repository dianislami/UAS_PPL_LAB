import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from coins.models import Coin
from portfolio.models import Portfolio, Transaction
from django.contrib.auth.models import User
from django.db import models

@login_required(login_url='admin_login')
def admin_dashboard(request):
    # Ambil pengguna admin untuk seed data demo jika daftar SQLite kosong/tidak ada
    admin_user = User.objects.filter(username='admin').first()
    if admin_user and Portfolio.objects.filter(user=admin_user).count() == 0 and Coin.objects.count() > 0:
        btc = Coin.objects.filter(symbol='BTC').first()
        eth = Coin.objects.filter(symbol='ETH').first()
        sol = Coin.objects.filter(symbol='SOL').first()
        
        if btc:
            Portfolio.objects.get_or_create(user=admin_user, coin=btc, defaults={'amount': 0.45, 'avg_buy_price': 58000.0})
            Transaction.objects.get_or_create(user=admin_user, coin_symbol='BTC', type='BUY', amount=0.45, price=58000.0, date_str='May 25, 2026', status='Completed')
        if eth:
            Portfolio.objects.get_or_create(user=admin_user, coin=eth, defaults={'amount': 2.80, 'avg_buy_price': 2900.0})
            Transaction.objects.get_or_create(user=admin_user, coin_symbol='ETH', type='BUY', amount=2.80, price=2900.0, date_str='May 22, 2026', status='Completed')
        if sol:
            Portfolio.objects.get_or_create(user=admin_user, coin=sol, defaults={'amount': 15.0, 'avg_buy_price': 125.00})
            Transaction.objects.get_or_create(user=admin_user, coin_symbol='SOL', type='BUY', amount=15.0, price=125.00, date_str='May 20, 2026', status='Completed')

    # Kartu Statistik
    total_coins = Coin.objects.count()
    total_transactions = Transaction.objects.count()
    
    # Total nilai portofolio
    all_holdings = Portfolio.objects.all()
    total_portfolio_value = sum(h.amount * h.coin.price for h in all_holdings)
    
    total_users = User.objects.count()
    
    # Log aktivitas terbaru (5 transaksi terbaru di DB)
    recent_transactions = Transaction.objects.all().order_by('-id')[:5]
    
    # Ringkasan data koin
    all_coins = Coin.objects.all().order_by('rank')
    
    # Serialisasi data untuk bagan mini ChartJS (distribusi koin database)
    symbols = [coin.symbol for coin in all_coins[:6]]
    prices = [coin.price for coin in all_coins[:6]]
    
    admin_chart_data = {
        'labels': symbols,
        'prices': prices
    }
    admin_chart_json = json.dumps(admin_chart_data)

    return render(request, 'dashboard/admin_dashboard.html', {
        'coins': all_coins,
        'total_coins': total_coins,
        'total_transactions': total_transactions,
        'total_portfolio_value': total_portfolio_value,
        'total_users': total_users,
        'recent_transactions': recent_transactions,
        'admin_chart_json': admin_chart_json
    })

@login_required(login_url='admin_login')
def add_new_coin(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        symbol = request.POST.get('symbol', '').strip().upper()
        
        try:
            price = float(request.POST.get('price', 0.0))
            change_24h = float(request.POST.get('change_24h', 0.0))
        except (ValueError, TypeError):
            price = 0.0
            change_24h = 0.0
            
        market_cap = request.POST.get('market_cap', '').strip() or '$100.0 Million'
        volume_24h = request.POST.get('volume_24h', '').strip() or '$10.0 Million'
        circulating_supply = request.POST.get('circulating_supply', '').strip() or '10.0M'
        max_supply = request.POST.get('max_supply', '').strip() or 'Unlimited'
        
        try:
            rank = int(request.POST.get('rank', 1))
        except (ValueError, TypeError):
            rank = Coin.objects.count() + 1
            
        description = request.POST.get('description', '').strip() or 'No description provided.'
        
        # Hasilkan garis tren simulasi untuk sparkline visual
        spark_list = [price * 0.91, price * 1.04, price * 0.95, price * 1.02, price]
        sparkline_data = json.dumps(spark_list)
        
        if name and symbol and price > 0:
            Coin.objects.create(
                name=name,
                symbol=symbol,
                price=price,
                change_24h=change_24h,
                market_cap=market_cap,
                volume_24h=volume_24h,
                circulating_supply=circulating_supply,
                max_supply=max_supply,
                rank=rank,
                description=description,
                sparkline_data=sparkline_data
            )
            
    return redirect('admin_dashboard')

@login_required(login_url='admin_login')
def edit_coin(request, coin_id):
    coin = get_object_or_404(Coin, id=coin_id)
    if request.method == 'POST':
        coin.name = request.POST.get('name', '').strip()
        coin.symbol = request.POST.get('symbol', '').strip().upper()
        
        try:
            coin.price = float(request.POST.get('price', 0.0))
            coin.change_24h = float(request.POST.get('change_24h', 0.0))
        except (ValueError, TypeError):
            pass
            
        coin.market_cap = request.POST.get('market_cap', '').strip() or '$100.0 Million'
        coin.volume_24h = request.POST.get('volume_24h', '').strip() or '$10.0 Million'
        coin.circulating_supply = request.POST.get('circulating_supply', '').strip() or '10.0M'
        coin.max_supply = request.POST.get('max_supply', '').strip() or 'Unlimited'
        
        try:
            coin.rank = int(request.POST.get('rank', 1))
        except (ValueError, TypeError):
            pass
            
        coin.description = request.POST.get('description', '').strip() or 'No description provided.'
        
        # Sesuaikan sparkline sederhana agar sesuai dengan harga yang diperbarui
        try:
            prices = json.loads(coin.sparkline_data)
            if prices and len(prices) > 0:
                prices[-1] = coin.price
                coin.sparkline_data = json.dumps(prices)
            else:
                raise Exception()
        except Exception:
            spark_list = [coin.price * 0.91, coin.price * 1.04, coin.price * 0.95, coin.price * 1.02, coin.price]
            coin.sparkline_data = json.dumps(spark_list)
            
        coin.save()
        return redirect('admin_dashboard')
        
    return render(request, 'dashboard/edit_coin.html', {
        'coin': coin
    })

@login_required(login_url='admin_login')
def delete_coin(request, coin_id):
    coin = get_object_or_404(Coin, id=coin_id)
    if request.method == 'POST':
        coin.delete()
        return redirect('admin_dashboard')
    return render(request, 'dashboard/delete_confirm.html', {
        'coin': coin
    })

@login_required(login_url='admin_login')
def admin_transactions(request):
    txs = Transaction.objects.all().order_by('-id')
    
    # Filters
    search_query = request.GET.get('search', '').strip()
    if search_query:
        txs = txs.filter(
            models.Q(user__username__icontains=search_query) | 
            models.Q(coin_symbol__icontains=search_query)
        )
        
    coin_filter = request.GET.get('coin', '').strip()
    if coin_filter:
        txs = txs.filter(coin_symbol=coin_filter)
        
    user_filter = request.GET.get('user', '').strip()
    if user_filter:
        txs = txs.filter(user__username=user_filter)
        
    # Enriched data untuk Admin
    enriched_txs = []
    for t in txs:
        coin = Coin.objects.filter(symbol=t.coin_symbol).first()
        live_price = coin.price if coin else t.price
        current_value = t.amount * live_price
        profit_loss = current_value - (t.amount * t.price)
        
        enriched_txs.append({
            'id': t.id,
            'username': t.user.username,
            'coin_name': coin.name if coin else t.coin_symbol,
            'coin_symbol': t.coin_symbol,
            'amount': t.amount,
            'buy_price': t.price,
            'current_value': current_value,
            'profit_loss': profit_loss,
            'date': t.date_str,
            'type': t.type
        })
        
    # Dropdowns list
    all_coins_symbols = Coin.objects.values_list('symbol', flat=True).distinct()
    all_users = User.objects.values_list('username', flat=True).distinct()
    
    return render(request, 'dashboard/admin_transactions.html', {
        'transactions': enriched_txs,
        'all_coins': all_coins_symbols,
        'all_users': all_users,
        'search_query': search_query,
        'selected_coin': coin_filter,
        'selected_user': user_filter
    })

@login_required(login_url='admin_login')
def delete_transaction(request, tx_id):
    tx = get_object_or_404(Transaction, id=tx_id)

    coin = Coin.objects.filter(symbol=tx.coin_symbol).first()
    if coin:
        holding = Portfolio.objects.filter(user=tx.user, coin=coin).first()
        if holding:
            if tx.type == 'BUY':
                old_amount = holding.amount - tx.amount
                if old_amount > 0:
                    total_cost = holding.amount * holding.avg_buy_price
                    tx_cost = tx.amount * tx.price
                    remaining_cost = max(0.0, total_cost - tx_cost)
                    holding.avg_buy_price = remaining_cost / old_amount
                    holding.amount = old_amount
                    holding.save()
                else:
                    holding.delete()
            elif tx.type == 'SELL':
                holding.amount = holding.amount + tx.amount
                holding.save()
                
    tx.delete()
    return redirect('admin_transactions')
