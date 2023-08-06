import re
PATRON_HASH_USDT_BET20=re.compile(r"0x[0-9A-fa-f]{64}")
PATRON_HASH_USDT_TRC20=re.compile(r"[0-9A-fa-f]{64}")
PATRON_WALLET_USDT_BET20=re.compile(r"^0x[a-fA-F0-9]{40}$")
PATRON_WALLET_USDT_TRC20=re.compile(r"^[a-zA-Z0-9]{34}$")
def esUnHashCorrectoEnTransaccion_USDT_BET20(supuestoHash):
    return re.match(PATRON_HASH_USDT_BET20,supuestoHash) is not None
def esUnHashCorrectoEnTransaccion_USDT_TRC20(supuestoHash):
    return re.match(PATRON_HASH_USDT_TRC20,supuestoHash) is not None

def esUnaWalletCorrectaoEnTransaccion_USDT_BET20(supuestaWallet):
    return re.match(PATRON_WALLET_USDT_BET20, supuestaWallet) is not None
def esUnaWalletCorrectaoEnTransaccion_USDT_TRC20(supuestaWallet):
    return re.match(PATRON_WALLET_USDT_TRC20, supuestaWallet) is not None