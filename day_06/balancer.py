#!/usr/bin/env python
# coding: utf-8
""" """
import typing as t

import attr
import click


@attr.s(frozen=True)
class Memory(object):
    banks: t.Tuple[int, ...] = attr.ib()

    def balance(self) -> 'Memory':
        mem = list(self.banks)
        num_banks = len(self.banks)

        # Find the amount of blocks to balance - remove them from that bank.
        blocks_to_balance = max(mem)
        bank_pointer = mem.index(blocks_to_balance)
        mem[bank_pointer] = 0

        # Rebalance
        balance_rounds = 0
        while blocks_to_balance > 0:
            # Advance the pointer.
            bank_pointer = (bank_pointer + 1) % num_banks
            mem[bank_pointer] += 1
            blocks_to_balance -= 1

        return Memory(
            banks=tuple(mem)
        )


def detect_loop(memory: Memory) -> int:
    """Find how many steps until we detect a loop."""
    arrangements_seen = set()
    balancer_rounds = 0

    while memory not in arrangements_seen:
        arrangements_seen.add(memory)
        memory = memory.balance()
        balancer_rounds += 1

    return balancer_rounds, memory


@click.group()
def balancer():
    """Balancing memory like they were spinning tops."""
    pass


@balancer.command()
@click.argument('memory_banks', type=click.File())
def distribute(memory_banks):
    banks = tuple(map(int, memory_banks.read().split()))
    memory = Memory(banks)

    steps, memory = detect_loop(memory)
    msg = f"Loop found after {steps} balance rounds."
    click.secho(msg, fg='green')


@balancer.command()
@click.argument('memory_banks', type=click.File())
def loop_size(memory_banks):
    banks = tuple(map(int, memory_banks.read().split()))
    memory = Memory(banks)

    _, memory = detect_loop(memory)
    loop_size, _ = detect_loop(memory)
    msg = f"Loop size is {loop_size}."
    click.secho(msg, fg='green')


def main():
    """Entrypoint."""
    balancer()


if __name__ == '__main__':
    main()
