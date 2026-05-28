import json
from coins.models import Coin, Article

def seed_all():
    if Coin.objects.exists():
        return
        
    initial_coins = [
        {
            'name': 'Bitcoin',
            'symbol': 'BTC',
            'price': 64231.50,
            'change_24h': 2.45,
            'market_cap': '$1.26 Trillion',
            'volume_24h': '$28.4 Billion',
            'circulating_supply': '19.69M BTC',
            'max_supply': '21.00M BTC',
            'rank': 1,
            'description': 'Bitcoin is the world\'s first decentralized digital currency. It functions as a store of value and exchange medium with absolutely secure block cryptography.',
            'sparkline_data': json.dumps([62100, 62450, 62800, 62400, 63100, 63800, 64231])
        },
        {
            'name': 'Ethereum',
            'symbol': 'ETH',
            'price': 3452.80,
            'change_24h': -0.82,
            'market_cap': '$415.2 Billion',
            'volume_24h': '$14.1 Billion',
            'circulating_supply': '120.1M ETH',
            'max_supply': 'Unlimited',
            'rank': 2,
            'description': 'Ethereum is a decentralized open-source blockchain network supporting advanced smart contract execution and distributed application layers.',
            'sparkline_data': json.dumps([3520, 3500, 3480, 3490, 3460, 3440, 3452.80])
        },
        {
            'name': 'Solana',
            'symbol': 'SOL',
            'price': 145.22,
            'change_24h': 5.24,
            'market_cap': '$65.3 Billion',
            'volume_24h': '$3.8 Billion',
            'circulating_supply': '446.5M SOL',
            'max_supply': 'Unlimited',
            'rank': 3,
            'description': 'Solana is a high-speed web scale open infrastructure designed to support fast decentralized dApps with optimized throughput and minimal fees.',
            'sparkline_data': json.dumps([136, 138, 140, 139, 142, 144, 145.22])
        },
        {
            'name': 'Ripple',
            'symbol': 'XRP',
            'price': 0.524,
            'change_24h': 0.12,
            'market_cap': '$28.9 Billion',
            'volume_24h': '$850.4 Million',
            'circulating_supply': '55.3B XRP',
            'max_supply': '100.0B XRP',
            'rank': 4,
            'description': 'XRP is a fast distributed blockchain architecture specializing in cross-border settlements, global institutional liquidity, and instant low-cost transfers.',
            'sparkline_data': json.dumps([0.522, 0.521, 0.523, 0.524, 0.523, 0.524, 0.524])
        },
        {
            'name': 'Cardano',
            'symbol': 'ADA',
            'price': 0.354,
            'change_24h': -1.75,
            'market_cap': '$12.5 Billion',
            'volume_24h': '$340.2 Million',
            'circulating_supply': '35.6B ADA',
            'max_supply': '45.0B ADA',
            'rank': 5,
            'description': 'Cardano is a proof-of-stake platform driven by scientific research protocols, emphasizing sustainability, secure peer reviews, and transaction scalability.',
            'sparkline_data': json.dumps([0.362, 0.360, 0.358, 0.359, 0.355, 0.353, 0.354])
        }
    ]

    for coin_data in initial_coins:
        Coin.objects.create(**coin_data)

    initial_articles = [
        {
            'title': 'The Roadmap to Ethereum 2.5: Scaling the Next Layer',
            'category': 'Technology',
            'time_ago': '4 hours ago',
            'image_alt': 'Blockchain graphics',
            'content': 'Ethereum developers confirm active tests on layer-2 performance indexes aiming to reduce computational overhead. Scaling parameters on rollups successfully bypassed previous validation speed constraints.'
        },
        {
            'title': 'Global Regulation Paradigms: Institutional Safety Frameworks',
            'category': 'Regulation',
            'time_ago': '1 day ago',
            'image_alt': 'Gavel over glowing tablet',
            'content': 'Financial regulatory authorities release cooperative blueprints to establish standard transactional safeguards. De-risking strategies are set to enforce identity assurance for cross-border smart assets.'
        },
        {
            'title': 'Solana Decentralization index outpaces Previous Benchmarks',
            'category': 'Market Analysis',
            'time_ago': '2 days ago',
            'image_alt': 'Bull market chart',
            'content': 'Analysts report substantial progress in validator diversity across Solana networks. Staking distributions have shifted significantly, lowering the concentration of single validator group dominance.'
        }
    ]

    for art_data in initial_articles:
        Article.objects.create(**art_data)
