def tx_execute_before(from, to, value, gasLimit, gasPrice, data) :
    # 1. check `from` can pay upfront cost
    balance = getBalance(from)
    assert balance >= value + gasLimit * gasPrice

    # 2. substract upfront cost(tx.value + tx.gasLimit * tx.gasPrice)
    substractBalance(from, balance - value - gasLimit * gasPrice)

    # 3. execute EVM
    executeVM(from, to, value, gasLimit, gasPrice, data)

    # 4. collect refunded gas
    addBalance(from, remainedGas * gasPrice)

# "delegatee" is optional field in transaction
def tx_execute_after(from, to, value, gasLimit, gasPrice, data, delegatee=none):
    # 1. check if delegatee passed or not
    if delegatee:
        # 1-1. check if delegatee` is registered in staminaContract
        if staminaContract.delegatee(to):
            # 1-1-1. check if `delegatee` can pay upfront cost(only gasLimit * gasPrice)
            assert staminaContract.balanceOf(delegatee) >= gasLimit * gasPrice

            # 1-1-2. check if `from` can pay upfront cost(only value)
            assert getBalance(from) >= value

            # 1-1-3. substract upfront cost(only gasLimit * gasPrice) from `delegatee`
            staminaContract.substractBalance(delegatee, gasLimit * gasPrice)

            # 1-1-4. substract upfront cost(only value) from `from`
            substractBalance(from, value)

            # 1-1-5. execute EVM
            executeVM(from, to, value, gasLimit, gasPrice, data)

            # 1-1-6. collect refunded gas
            staminaContract.addBalance(delegatee, remainedGas * gasPrice)

        # 1-2 case where delegatee is not registered
        else:
            # "delegatee" account is in transaction but does not registered to staminaContract
            raise # throw if `delegatee` is not registered

    # 2. transaction without delegatee. same logic as original version
    else:
        return tx_execute_before(from, to, value, gasLimit, gasPrice, data)
