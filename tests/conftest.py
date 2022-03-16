import pytest


@pytest.fixture
def owner(accounts):
    yield accounts[0]


@pytest.fixture
def rando(accounts):
    yield accounts[1]


@pytest.fixture
def usdc_whale(accounts):
    yield accounts.at("0x55FE002aefF02F77364de339a1292923A15844B8", True)


@pytest.fixture
def usdc(Contract):
    yield Contract("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")


@pytest.fixture
def yvusdc(Contract):
    yield Contract("0xa354F35829Ae975e850e23e9615b11Da1B3dC4DE")


@pytest.fixture
def settlement(Contract):
    yield Contract("0x9008D19f58AAbD9eD0D60971565AA8510560ab41")


@pytest.fixture
def solver_helper(SolverHelper, owner, settlement):
    yield SolverHelper.deploy(settlement, {"from": owner})
