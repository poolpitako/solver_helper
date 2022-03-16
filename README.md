# Solver helper

![SolverHelperBackground](https://user-images.githubusercontent.com/78830419/158482372-ea31d119-8311-4d33-818f-c34dc253c34f.png)


## 1
User creates a USDC -> yvUSDC order through the website and signs the tx.

## 2
Driver polls the orderbook for orders

## 3
Driver sends solvable_orders to all solvers

## 4
Yearn solver knows how to solve USDC -> yvUSDC and returns a solvable solution

## 5
Driver sends the solution to the Settlement contract on chain

## 6
Settlement contract execute the action which is:
 - Send usdc from the user to the `SolvableHelper` contract
 - Calls `multiSend()` in `SolvableHelper` contract

## 7 + 8
`SolvableHelper` in the `multiSend()` logic approves usdc on the yvUSDC vault and deposit() minting yvTokens.

## 9
Minted yvUSDC are sent to the settlement contract, finishing the trade

