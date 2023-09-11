TG_TOKEN = 'your_tg_token'
TG_ID = 0 

DATA = {
    'ethereum'      : {'rpc': 'https://rpc.ankr.com/eth', 'scan': 'https://etherscan.io/tx', 'token': 'ETH', 'chain_id': 1},

    'optimism'      : {'rpc': 'https://rpc.ankr.com/optimism', 'scan': 'https://optimistic.etherscan.io/tx', 'token': 'ETH', 'chain_id': 10},

    'bsc'           : {'rpc': 'https://rpc.ankr.com/bsc', 'scan': 'https://bscscan.com/tx', 'token': 'BNB', 'chain_id': 56},

    'polygon'       : {'rpc': 'https://rpc.ankr.com/polygon', 'scan': 'https://polygonscan.com/tx', 'token': 'MATIC', 'chain_id': 137},

    'polygon_zkevm' : {'rpc': 'https://zkevm-rpc.com', 'scan': 'https://zkevm.polygonscan.com/tx', 'token': 'ETH', 'chain_id': 1101},

    'arbitrum'      : {'rpc': 'https://rpc.ankr.com/arbitrum', 'scan': 'https://arbiscan.io/tx', 'token': 'ETH', 'chain_id': 42161},

    'avalanche'     : {'rpc': 'https://rpc.ankr.com/avalanche', 'scan': 'https://snowtrace.io/tx', 'token': 'AVAX', 'chain_id': 43114},

    'fantom'        : {'rpc': 'https://rpc.ankr.com/fantom', 'scan': 'https://ftmscan.com/tx', 'token': 'FTM', 'chain_id': 250},

    'nova'          : {'rpc': 'https://nova.arbitrum.io/rpc', 'scan': 'https://nova.arbiscan.io/tx', 'token': 'ETH', 'chain_id': 42170},

    'zksync'        : {'rpc': 'https://mainnet.era.zksync.io', 'scan': 'https://explorer.zksync.io/tx', 'token': 'ETH', 'chain_id': 324},
    
    'celo'          : {'rpc': 'https://1rpc.io/celo', 'scan': 'https://celoscan.io/tx', 'token': 'CELO', 'chain_id': 42220},

    'gnosis'        : {'rpc': 'https://rpc.ankr.com/gnosis', 'scan': 'https://gnosisscan.io/tx', 'token': 'xDAI', 'chain_id': 100},

    'core'          : {'rpc': 'https://rpc.coredao.org', 'scan': 'https://scan.coredao.org/tx', 'token': 'CORE', 'chain_id': 1116},

    'harmony'       : {'rpc': 'https://api.harmony.one', 'scan': 'https://explorer.harmony.one/tx', 'token': 'ONE', 'chain_id': 1666600000},

    'moonbeam'      : {'rpc': 'https://rpc.ankr.com/moonbeam', 'scan': 'https://moonscan.io/tx', 'token': 'GLMR', 'chain_id': 1284},

    'moonriver'     : {'rpc': 'https://moonriver.public.blastapi.io', 'scan': 'https://moonriver.moonscan.io/tx', 'token': 'MOVR', 'chain_id': 1285},

    'linea'         : {'rpc': 'https://rpc.linea.build', 'scan': 'https://lineascan.build/tx', 'token': 'ETH', 'chain_id': 59144},

    'base'          : {'rpc': 'https://mainnet.base.org', 'scan': 'https://basescan.org/tx', 'token': 'ETH', 'chain_id': 8453},
}
