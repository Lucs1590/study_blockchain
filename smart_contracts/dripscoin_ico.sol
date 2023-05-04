// ICO Dripscoin

pragma solidity ^0.4.11

contract dripscoin_ico {
    uint public max_dripscoins = 1000000;
    uint public usd_to_dripscoins = 1000;
    uint public total_dripscoins_bought = 0;

    mapping(address => uint) equity_dripscoins;
    mapping(address => uint) equity_usd;

    modifier can_buy_dripscoins(uint usd_invested) {
        require (usd_invested * usd_to_dripscoins + total_dripscoins_bought <= max_dripscoins);
        _;
    }

    function equity_in_dripscoins(address investor) external constant returns (uint) {
        return equity_dripscoins[investor];
    }

    function equity_in_usd(address investor) external constant returns (uint) {
        return equity_usd[investor];
    }

    function buy_dripscoins(address investor, uint usd_invested) external
    can_buy_dripscoins(usd_invested) {
        uint dripscoins_bought = usd_invested * usd_to_dripscoins;
        equity_dripscoins[investor] += dripscoins_bought;
        equity_usd[investor] = equity_dripscoins[investor] / 1000;
        total_dripscoins_bought += dripscoins_bought;
    }

    function sell_dripscoins(address investor, uint dripscoins_sold) external {
        equity_dripscoins[investor] -= dripscoins_sold;
        equity_usd[investor] = equity_dripscoins[investor] / 1000;
        total_dripscoins_bought -= dripscoins_sold;
    }

}