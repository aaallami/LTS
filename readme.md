# Less Than Secret protocol (LTS+)

This code is designed based on LTS+ protocol.

Input: two secret shared values [x], [y]

Output:[w]_p=x<y

## Installation

To install the code follow the instructions
```
1- Install the MPSPDZ library at https://github.com/data61/MP-SPDZ.
2- mv mpc MP-SPDZ/Programs/Source

```

## Usage
This is only used to benchmark LTS protocol as follows:

We set x=2, y=10

x<y must equal 1 since 2<10.

We set the number of comparisons (count=100).

All these values can be changed in rabbit.mpc file.

1- To compile the code run: 
    
    ./compile.py -F 40 rabbit
2- To run the code for P(OT) locally use:
    
    Scripts/mascot.sh rabbit

2- To run the code for P(HE) locally use:
    
    Scripts/highgear.sh rabbit

Note the above scripts can be used to benchmark communication accurately. However, to gain an accurate run-time benchmark then it requires to have two different machines. Follow the instructions on how to run the code on different machines. For more information, we advise the reader to https://mp-spdz.readthedocs.io/en/latest/index.html.


1- Set the IP addresses in a MPSPDZ/HOST.txt file 

2- For P(OT) run for machines 0 and 1 consecutively:

    ./mascot-party.x 0 rabbit -ip HOSTS -N 2
    ./mascot-party.x 1 rabbit -ip HOSTS -N 2
3- For P(HE) run for machines 0 and 1 consecutively:

    ./highgear-party.x 0 rabbit -ip HOSTS -N 2
    ./highgear-party.x 1 rabbit -ip HOSTS -N 2
