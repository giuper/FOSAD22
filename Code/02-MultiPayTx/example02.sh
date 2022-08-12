#!/bin/bash


accountDir="./Accounts"
account1=${accountDir}/P1
account2=${accountDir}/P2
account3=${accountDir}/P3

txDir="./TX"
unsignedTX=${txDir}/"MultiPay.utx"
unsignedWithPKTX=${txDir}/"MultiPayWithPK.utx"
signedTX=${txDir}/"MultiPay.stx"

GOAL=../../../goal
NODEDIR=../../../testnet

echo "Creating a 2 out of 3 multisig account"
python3 createMultiAddr.py ${account1} ${account2} ${account3} 
read

mkdir -p ${txDir}
echo "Creating a multisig TX"
python3 multiPayTXComplete.py ${account1} ${account2} ${account3} ${account1} ${account2} ${account3} ~/node/testnet


echo "Inspecting the transactions"
read

echo "Inspecting the Unsigned Transaction"
${GOAL} clerk inspect ${unsignedTX} -d ${NODEDIR}
read

echo "Inspecting the Unsigned Transaction with PK"
${GOAL} clerk inspect ${unsignedWithPKTX} -d ${NODEDIR}
read

echo "Inspecting the Signed Transaction"
${GOAL} clerk inspect ${signedTX} -d ${NODEDIR}
read
