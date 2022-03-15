import pytest


@pytest.fixture
def owner(accounts):
    yield accounts[0]


@pytest.fixture
def rando(accounts):
    yield accounts[1]


@pytest.fixture
def settlement(Contract):
    yield Contract("0x9008D19f58AAbD9eD0D60971565AA8510560ab41")


@pytest.fixture
def solver_helper(SolverHelper, owner, settlement):
    yield SolverHelper.deploy(settlement, {"from": owner})
