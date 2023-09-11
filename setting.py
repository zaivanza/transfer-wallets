WALLETS_IN_BATCH    = 10 # сколько максимум кошельков в одном потоке (можно указать > чем кол-во кошельков, ошибки не будет)
RANDOM_WALLETS      = True # True если хочешь рандомизировать кошельки
TG_BOT_SEND         = False # True если хочешь отправлять результаты в тг-бота, указанного в data/data.py
RETRY               = 0 # кол-во доп попыток на трансфер
SLEEPING_TIME       = 1 # сколько будем спать между выводом монеты в одной сети. увеличивай если будут ошибки nonce too low

MIN_TRANSFER_AMOUNT = 0.1 # если amount будет меньше этого числа, выводить монету не будет
MIN_TRANSFER_USD    = 3 # в $, если amount * price будет меньше этого числа, выводить монету не будет

# erc20 токены добавлять сюда
ERC20_TOKENS = {
        'bsc': [
            '0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d', # USDC
            '0x55d398326f99059ff775485246999027b3197955', # USDT
            # '0xe9e7cea3dedca5984780bafc599bd69add087d56', # BUSD
            # '0xB0b84D294e0C75A6abe60171b70edEb2EFd14A1B', # SnBNB
            ],
        'arbitrum': [
            '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9', # USDT
            '0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8', # USDC
            # '0x6694340fc020c5e6b96567843da2df01b2ce1eb6', # STG
            # '0x912CE59144191C1204E64559FE8253a0e49E6548', # ARB
            '0xfc5a1a6eb076a2c7ad06ed22c90d7e710e35ad0a', # GMX
            ],
        # 'optimism': [
        #     '0x7f5c764cbc14f9669b88837ca1490cca17c31607', # USDC
        #     '0x4200000000000000000000000000000000000042', # OP
        #     '0x94b008aa00579c1307b0ef2c499ad98a8ce58e58', # USDT
        #     ],
        'polygon': [
            '0xc2132d05d31c914a87c6611c10748aeb04b58e8f', # USDT
            '0x2791bca1f2de4661ed88a30c99a7a9449aa84174', # USDC
            '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270', # WMATIC
            ],
        # 'avalanche': [
        #     '0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E', # USDT
        #     ],
        # 'ethereum': [
        #     '0xdac17f958d2ee523a2206206994597c13d831ec7', # USDT
        #     '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', # USDC
        #     '0xaf5191b0de278c7286d6c7cc6ab6bb8a73ba2cd6', # STG
        #     ],
        # 'zksync': [
        #     '', 
        #     ],
        # 'nova': [
        #     '', 
        #     ],
        # 'fantom': [
        #     '0x04068da6c83afcfa0e13ba15a6696662335d5b75', # USDC
        #     ],
        # 'polygon_zkevm': [
        #     '', 
        #     ],
        # 'celo': [
        #     '', 
        #     ],
        # 'gnosis': [
        #     '', 
        #     ],
        # 'harmony': [
        #     '', 
        #     ],
        'core': [
            '0x900101d06a7426441ae63e9ab3b9b0f63be145f1', # USDT
            ],
        # 'linea': [
        #     '', 
        #     ],
        # 'base': [
        #     '', 
        #     ],
    }

# закомментируй сеть если не хочешь с нее выводить eth (нативный) токен
ETH_TOKENS = [
    # "bsc",
    "arbitrum",
    # "optimism",
    "polygon",
    # "avalanche",
    # "ethereum",
    "zksync",
    # "nova",
    "fantom",
    "polygon_zkevm",
    # "celo",
    # "gnosis",
    # "harmony",
    "core",
    # "linea",
    "base",
]
    