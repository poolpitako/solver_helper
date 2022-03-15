// SPDX-License-Identifier: AGPL-3.0
pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

import {
    SafeERC20,
    SafeMath,
    IERC20,
    Address
} from "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";

contract SolverHelper {
    using SafeERC20 for IERC20;
    using Address for address;
    using SafeMath for uint256;

    address public owner;
    address public pendingOwner;
    address public settlement;

    constructor(address _settlement) public {
        owner = msg.sender;
        settlement = _settlement;
    }

    function setSettlement(address _settlement) external {
        require(msg.sender == owner);
        settlement = _settlement;
    }

    function setPendingOwner(address _pendingOwner) external {
        require(msg.sender == owner);
        pendingOwner = _pendingOwner;
    }

    function acceptOwnership() external {
        require(msg.sender == pendingOwner);
        owner = pendingOwner;
    }


    // function robbed from https://etherscan.io/address/0x40A2aCCbd92BCA938b02010E17A5b8929b49130D#code
    function multiSend(bytes memory transactions) public payable {
      require(msg.sender == settlement);

      // solhint-disable-next-line no-inline-assembly
      assembly {
          let length := mload(transactions)
          let i := 0x20
          for {
              // Pre block is not used in "while mode"
          } lt(i, length) {
              // Post block is not used in "while mode"
          } {
              // First byte of the data is the operation.
              // We shift by 248 bits (256 - 8 [operation byte]) it right since mload will always load 32 bytes (a word).
              // This will also zero out unused data.
              let operation := shr(0xf8, mload(add(transactions, i)))
              // We offset the load address by 1 byte (operation byte)
              // We shift it right by 96 bits (256 - 160 [20 address bytes]) to right-align the data and zero out unused data.
              let to := shr(0x60, mload(add(transactions, add(i, 0x01))))
              // We offset the load address by 21 byte (operation byte + 20 address bytes)
              let value := mload(add(transactions, add(i, 0x15)))
              // We offset the load address by 53 byte (operation byte + 20 address bytes + 32 value bytes)
              let dataLength := mload(add(transactions, add(i, 0x35)))
              // We offset the load address by 85 byte (operation byte + 20 address bytes + 32 value bytes + 32 data length bytes)
              let data := add(transactions, add(i, 0x55))
              let success := 0
              switch operation
                  case 0 {
                      success := call(gas(), to, value, data, dataLength, 0, 0)
                  }
                  // This version does not allow delegatecalls
                  case 1 {
                      revert(0, 0)
                  }
              if eq(success, 0) {
                  revert(0, 0)
              }
              // Next entry starts at 85 byte + data length
              i := add(i, add(0x55, dataLength))
            }
        }
    }
}
