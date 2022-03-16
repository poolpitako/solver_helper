import pytest
import brownie
from gnosis.safe.multi_send import MultiSendOperation, MultiSendTx

def test_multisend(solver_helper, settlement, usdc, usdc_whale, yvusdc):
    usdc.transfer(settlement, 1_000 * 1e6, {"from": usdc_whale})

    # Create the ms tx to be executed in the Solverhelper
    txs = []

    # 1) approve the token to be used by the vault
    input1 = usdc.approve.encode_input(yvusdc, 2**256-1)
    txs.append(MultiSendTx(MultiSendOperation.CALL, usdc.address, 0, input1))

    # 2) Deposit the usdc into the vault and send to the settlement contract
    input2 = yvusdc.deposit.encode_input(2**256-1, settlement)
    txs.append(MultiSendTx(MultiSendOperation.CALL, yvusdc.address, 0, input2))

    # Combine all the txs
    encoded_multisend_data = b"".join([x.encoded_data for x in txs])

    # send usdc from settlement to solver_helper
    usdc.transfer(solver_helper, usdc.balanceOf(settlement), {"from": settlement})
    assert usdc.balanceOf(solver_helper) >= 1_000 * 1e6

    solver_helper.multiSend(encoded_multisend_data, {"from": settlement})
    assert yvusdc.balanceOf(settlement) > 0
