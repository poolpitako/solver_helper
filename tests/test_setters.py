import pytest
import brownie
from brownie import ZERO_ADDRESS


def test_init_values(solver_helper, owner, settlement):
    assert solver_helper.owner() == owner
    assert solver_helper.settlement() == settlement
    assert solver_helper.pendingOwner() == ZERO_ADDRESS


def test_set_owner(solver_helper, owner, rando):
    with brownie.reverts():
        solver_helper.setPendingOwner(rando, {"from": rando})

    solver_helper.setPendingOwner(rando, {"from": owner})
    assert solver_helper.pendingOwner() == rando

    with brownie.reverts():
        solver_helper.acceptOwnership({"from": owner})

    solver_helper.acceptOwnership({"from": rando})
    assert solver_helper.owner() == rando
