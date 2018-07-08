def tx_execute_before(from, to, value, gasLimit, gasPrice, data) :
    # 1. check `from` can pay upfront cost
    balance = getBalance(from)
    assert balance >= value + gasLimit * gasPrice

    # 2. substract upfront cost(tx.value + tx.gasLimit * tx.gasPrice)
    substractBalance(from, balance - value - gasLimit * gasPrice)

    # 3. execute EVM
    executeVM(from, to, value, gasLimit, gasPrice, data)

    # 4. collect refunded gas
    addBalance(from, gasRemained * gasPrice)

def tx_execute_after(from, to, value, gasLimit, gasPrice, data) :
    # 0. get delegatee, execute EVM
    delegatee = staminaContract.delegatee(to)

    # 1. case where delegatee exist
    if delegatee:
        # 1-1. if `to` has delegatee check upfront cost(only gasLimit * gasPrice)
        assert staminaContract.balanceOf(delegatee) >= gasLimit * gasPrice

        # 1-2. subtract upfront cost(only gasLimit * gasPrice) from delegatee
        staminaContract.subtractBalance(delegatee, gasLimit * gasPrice)

        # 1-3. substract upfront cost(only value)
        substractBalance(from, value)

        # 1-4. execute EVM
        executeVM(from, to, value, gasLimit, gasPrice, data)

        # 1-5. collect refunded gas to delegatee
        staminaContract.addBalance(delegatee, gasRemained * gasPrice)

    # 2. case where delegatee does not exist
    else:
        # Execute tx tranditional way
        tx_execute_before(from, to, value, gasLimit, gasPrice, data)
