# Pseudo Bitcoin

### Installation
* Install the prerequisites
```
pip install -r requirements.txt
```
### How to use
```
python3 args.py createwallet
python3 args.py createblockchain -a [address]
python3 args.py createwallet
python3 args.py send -from [address] -to [address] -a [amount]
python3 args.py getbalance -a [address]
python3 args.py printchain
python3 args.py printblock -h [height]
```
### Todo
- [x] Prototype
- [x] Persistence
- [x] Transaction-basic
- [x] Address
- [x] Transaction-advanced
- [ ] Network
