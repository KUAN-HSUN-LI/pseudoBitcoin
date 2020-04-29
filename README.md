# Pseudo Bitcoin

### Installation
* prerequisites
    ```
    click
    ecdsa
    click-shell
    ```
* Install the prerequisites
    ```
    pip install -r requirements.txt
    ```
### How to use
```
$ python3 args.py -n [name]
cmd> createwallet
cmd> createblockchain -a [address]
cmd> createwallet
cmd> getwallets
cmd> send -from [address] -to [address] -a [amount]
cmd> getbalance -a [address]
cmd> printchain
cmd> printblock -h [height]
```
### Todo
- [x] Prototype
- [x] Persistence
- [x] Transaction-basic
- [x] Address
- [x] Transaction-advanced
- [ ] Network
