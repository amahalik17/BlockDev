// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    
    // this will get initialized to 0!
    uint256 favoriteNumber;
    bool favoriteBool;
    
    struct People {
        uint256 favoriteNumber;
        string name;
    }
    
    People[] public people;
    
    mapping(string => uint256) public nameToFavNum;
    
    //People public person = People({favoriteNumber: 2, name: "Aaron"});
    
    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }
    
    // view, pure
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }
    
    // 2 ways of storing memory are (storage and memory)
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavNum[_name] = _favoriteNumber;
    }
    
    
}
