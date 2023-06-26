# Rabbit less than secret protocol (LTS)

This code is designed based on Rabbit paper.

The code implements LTS prtocol as in figure 6.

Input: two secret shared values [x], [y]

Output:[w]_p=x<y

https://eprint.iacr.org/2021/119.pdf

## Installation

To install the code follow the instructions
```
1- Install MPSPDZ library at https://github.com/data61/MP-SPDZ.
2- mv rabbit.mpc MP-SPDZ/Programs/Source
```

## Usage
This is only used to benchmark LTS protocol as follows:

We set x=2, y=10

x<y must equal 1 since 2<10.

We set number of comparsions (count=100).

All thes values can be changed in rabbit.mpc file.

1- To compile the code run: 
    
    ./compile.py -F 40 rabbit
2- To run the code for P(OT) locally use:
    
    Scripts/mascot.sh rabbit

2- To run the code for P(HE) locally use:
    
    Scripts/highgear.sh rabbit

Note the above above scripts can be used to benchmark communication accurately. However, to gain acurrate run-time benchmark then it requires to have two different machines. For that please follow the instructions on how to run MPSPDZ on differnet machines and follow the following instructions:

1- For P(OT) run for mahcine 0 and 1 consecutively:

    ./mascot-party.x 0 rabbit -pn 19755 -h localhost -N 2
    ./mascot-party.x 1 rabbit -pn 19755 -h localhost -N 2
2- For P(HE) run for mahcine 0 and 1 consecutively:

    ./highgear-party.x 0 rabbit -pn 15093 -h localhost -N 2
    ./highgear-party.x 1 rabbit -pn 15093 -h localhost -N 2
