from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from coins.models import Coin
from .models import Portfolio, Transaction
from datetime import datetime

def get_target_user(request):

    if request.user.is_authenticated:
        return request.user
    user = User.objects.filter(username='admin').first()
    if not user:
        user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.first()
    if not user:
        # Buat superuser 'admin' secara otomatis jika tidak ada
        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    return user

def get_session_portfolio(request):

    if 'portfolio_assets' not in request.session:
        # Seed kepemilikan default dalam sesi pengguna
        btc = Coin.objects.filter(symbol='BTC').first()
        eth = Coin.objects.filter(symbol='ETH').first()
        
        request.session['portfolio_assets'] = [
            {
                'coin_id': btc.id if btc else 1,
                'coin_name': 'Bitcoin',
                'symbol': 'BTC',
                'amount': 0.24,
                'avg_buy_price': 62000.00
            } if btc else {},
            {
                'coin_id': eth.id if eth else 2,
                'coin_name': 'Ethereum',
                'symbol': 'ETH',
                'amount': 1.50,
                'avg_buy_price': 3200.00
            } if eth else {},
        ]
        
    if 'portfolio_transactions' not in request.session:
        request.session['portfolio_transactions'] = [
            {
                'date': 'May 24, 2026',
                'coin_symbol': 'BTC',
                'type': 'BUY',
                'amount': 0.15,
                'price': 63500.00,
                'status': 'Completed'
            },
            {
                'date': 'May 22, 2026',
                'coin_symbol': 'ETH',
                'type': 'BUY',
                'amount': 1.05,
                'price': 3300.00,
                'status': 'Completed'
            },
        ]
    return request.session['portfolio_assets'], request.session['portfolio_transactions']

def portfolio_dashboard(request):
    is_guest = not request.user.is_authenticated
    target_user = get_target_user(request)
    
    # Muat catatan database pengguna alih-alih sesi
    user_portfolio = Portfolio.objects.filter(user=target_user)
    user_txs = Transaction.objects.filter(user=target_user).order_by('-id')
    
    total_valuation = 0.0
    portfolio_list = []
    
    for item in user_portfolio:
        live_val = item.amount * item.coin.price
        total_valuation += live_val
        portfolio_list.append({
            'coin_id': item.coin.id,
            'coin_name': item.coin.name,
            'symbol': item.coin.symbol,
            'amount': item.amount,
            'avg_buy_price': item.avg_buy_price,
            'live_price': item.coin.price,
            'live_value': live_val,
            'pnl_percentage': item.profit_loss_percentage,
            'pnl_value': item.profit_loss_value,
        })
        
    txs_list = []
    for tx in user_txs:
        txs_list.append({
            'date': tx.date_str,
            'coin_symbol': tx.coin_symbol,
            'type': tx.type,
            'amount': tx.amount,
            'price': tx.price,
            'status': tx.status
        })
        
    # Hitung portofolio lanjutan
    total_cost = 0.0
    for item in portfolio_list:
        total_cost += item['amount'] * item['avg_buy_price']
        
    total_profit_loss = total_valuation - total_cost
    
    best_asset = None
    worst_asset = None
    if portfolio_list:
        best_asset = max(portfolio_list, key=lambda x: x['pnl_percentage'])
        worst_asset = min(portfolio_list, key=lambda x: x['pnl_percentage'])
        
    total_transactions_count = len(txs_list)
    
    # Siapkan detail untuk Chart.js
    chart_labels = [item['symbol'] for item in portfolio_list]
    chart_allocations = [round(item['live_value'], 2) for item in portfolio_list]
    chart_pnls = [round(item['pnl_value'], 2) for item in portfolio_list]
    chart_amounts = [item['amount'] for item in portfolio_list]
    
    # Bagan garis pertumbuhan 7 hari simulasi
    if total_valuation > 0:
        ratios = [0.88, 0.92, 0.90, 0.95, 1.02, 0.97, 1.00]
        growth_timeline = [round(total_valuation * r, 2) for r in ratios]
    else:
        growth_timeline = [0.0] * 7
        
    import json
    chart_data = {
        'labels': chart_labels,
        'allocations': chart_allocations,
        'pnls': chart_pnls,
        'amounts': chart_amounts,
        'growth_timeline': growth_timeline
    }
    chart_data_json = json.dumps(chart_data)
        
    return render(request, 'portfolio/portfolio.html', {
        'portfolio': portfolio_list,
        'transactions': txs_list,
        'total_valuation': total_valuation,
        'total_profit_loss': total_profit_loss,
        'best_asset': best_asset,
        'worst_asset': worst_asset,
        'total_transactions_count': total_transactions_count,
        'chart_data_json': chart_data_json,
        'is_guest': is_guest,
        'target_user': target_user
    })

def add_to_portfolio(request):
    if request.method != 'POST':
        return redirect('portfolio_dashboard')
        
    coin_id = request.POST.get('coin_id')
    try:
        amount = float(request.POST.get('amount', 0.0))
        price = float(request.POST.get('price', 0.0))
    except (TypeError, ValueError):
        amount = 0.0
        price = 0.0
        
    if amount <= 0 or price <= 0:
        return redirect('portfolio_dashboard')
        
    coin = get_object_or_404(Coin, id=coin_id)
    target_user = get_target_user(request)
    
    # Tambah atau perbarui Database secara langsung
    holding, created = Portfolio.objects.get_or_create(user=target_user, coin=coin)
    if created:
        holding.amount = amount
        holding.avg_buy_price = price
    else:
        new_amount = holding.amount + amount
        holding.avg_buy_price = ((holding.amount * holding.avg_buy_price) + (amount * price)) / new_amount
        holding.amount = new_amount
    holding.save()
    
    # Simpan log transaksi secara langsung
    Transaction.objects.create(
        user=target_user,
        coin_symbol=coin.symbol,
        type='BUY',
        amount=amount,
        price=price,
        date_str=datetime.now().strftime('%b %d, %Y'),
        status='Completed'
    )
        
    return redirect('portfolio_dashboard')
