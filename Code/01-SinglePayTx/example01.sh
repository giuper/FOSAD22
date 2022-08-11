#!/bin/bash

ACCOUNTDir="./Accounts"
SENDER=${ACCOUNTDir}"/sender"
RECEIVER=${ACCOUNTDir}"/receiver"

TXDir="./TX"
UNSIGNEDTX=${TXDir}"/Pay.utx"
SIGNEDTX=${TXDir}"/Pay.stx"
NODEDir="../../../testnet"

GOAL=../../../goal

mkdir -p ${ACCOUNTDir}
mkdir -p ${TXDir}

echo "Creating the sender account"
python3 createSingle.py ${SENDER}
read
clear -x

echo "Creating the receiver account"
python3 createSingle.py ${RECEIVER}
read
clear -x

echo "Executing a single sender payment transaction"
python3 payTX.py ${SENDER}.mnem ${RECEIVER}.addr ${NODEDir}
read
clear -x

echo "Inspecting the unsigned transaction"
${GOAL} clerk inspect ${UNSIGNEDTX} -d ${NODEDir}
read
clear -x

echo "Inspecting the signed transaction"
${GOAL} clerk inspect ${SIGNEDTX} -d ${NODEDir}
read


