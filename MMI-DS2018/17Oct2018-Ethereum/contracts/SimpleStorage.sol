pragma solidity ^0.4.24;

contract SimpleStorage {
  uint public voteYes;
  uint public voteNo;

  function vote(bool yes) public{
    if(yes)
      ++voteYes;
    else
      ++voteNo;
  }
}
