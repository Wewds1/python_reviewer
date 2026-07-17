# Capstone Project — Enterprise Banking System

## What you're building

A multi-account banking system: customers who can hold multiple accounts, different account types with different rules, transactions that are logged and auditable, and custom exceptions enforcing every business rule (no overdrafts on savings, no negative balances, no transferring more than you have). This is the project that exercises essentially everything in Module 2 at once, and it's built as a proper multi-file package, following genuine enterprise project structure, not a single script.

As with the Module 1 capstone, I'm not handing you finished code. This one has more moving parts than the client records manager did, so we'll move through six milestones, and I'll review your work at the end of each before you continue. Design mistakes in a banking system's class structure are exactly the kind of thing that's cheap to fix on paper and expensive to fix after fifteen classes depend on the flawed version, so slowing down here is deliberate, not busywork.

## UML class diagram

```
                    «abstract»
                 ┌─────────────────┐
                 │      Account        │
                 ├─────────────────┤
                 │ - __balance: float     │
                 │ - account_number: str   │
                 │ - owner: Customer        │
                 ├─────────────────┤
                 │ + deposit(amount)          │
                 │ + withdraw(amount)  «abstract»│
                 │ + balance: float (property)     │
                 └────────┬────────┘
                           │
            ┌──────────────┼──────────────┐
            │                              │
   ┌────────▼────────┐          ┌────────▼────────┐
   │  SavingsAccount      │          │  CheckingAccount      │
   ├─────────────────┤          ├─────────────────┤
   │ - monthly_limit: int    │          │ - overdraft_limit: float  │
   ├─────────────────┤          ├─────────────────┤
   │ + withdraw(amount)         │          │ + withdraw(amount)          │
   └─────────────────┘          └─────────────────┘

┌───────────────┐    1        *   ┌───────────────┐
│    Customer        │◇────────────────│     Account        │   (aggregation — a Customer
├───────────────┤                 └───────────────┘    doesn't own the account's
│ - name: str          │                                       lifecycle exclusively;
│ - customer_id: str      │                                       accounts could be
├───────────────┤                                       transferred between customers)
│ + open_account(type)      │
│ + total_balance(): float    │
└───────────────┘

┌───────────────┐    1        *   ┌───────────────┐
│    Account         │◆────────────────│   Transaction       │   (composition — a
├───────────────┤                 ├───────────────┤   Transaction record belongs
│ - _transactions: list   │                 │ - amount: float         │   entirely to the account
└───────────────┘                 │ - timestamp: datetime    │   it happened on)
                                   │ - transaction_type: str   │
                                   └───────────────┘
```

Notice the two different relationship types deliberately used here: `Customer` to `Account` is aggregation (a customer's accounts could, in principle, be reassigned or closed independently), while `Account` to `Transaction` is composition (a transaction record has no meaning or existence outside the specific account it happened on). Getting this distinction right in your actual implementation, not just the diagram, is one of the things I'll be checking closely at Milestone 3.

## Package structure

```
banking-system/
├── main.py
├── requirements.txt
├── README.md
├── banking/
│   ├── __init__.py
│   ├── accounts.py       # Account (abstract), SavingsAccount, CheckingAccount
│   ├── customer.py        # Customer
│   ├── transaction.py      # Transaction
│   ├── exceptions.py        # InsufficientFundsError, AccountLimitError, etc.
│   ├── bank.py                # Bank — top-level coordinator, manages all customers/accounts
│   └── cli.py                   # menu-driven interface
└── tests/
    └── manual_test_checklist.md
```

## Feature list

- Create customers, each able to hold multiple accounts
- Open both `SavingsAccount` and `CheckingAccount` types for a given customer
- Deposit and withdraw, with each account type enforcing its own rules (savings: limited withdrawals per month; checking: overdraft allowed up to a limit)
- Transfer funds between two accounts, which should internally be a withdrawal from one and a deposit into another, atomically, either both succeed or neither does
- Every account maintains its own transaction history as a composed list of `Transaction` objects
- A `Bank` class coordinating everything: creating customers, opening accounts, looking up an account by number, generating a simple statement for any account
- Custom exceptions for every real business rule violation: insufficient funds, exceeding the savings withdrawal limit, exceeding a checking account's overdraft limit, opening an account for a nonexistent customer
- A menu-driven CLI tying it all together

## Milestone 1: exceptions and the abstract Account base

Start with `exceptions.py`: a base `BankingError`, and specific subclasses `InsufficientFundsError`, `WithdrawalLimitExceededError`, and `OverdraftLimitExceededError`. Then build the abstract `Account` class in `accounts.py`, using the `abc` module properly, following Lesson 9. `balance` should be a read-only property backed by a private `__balance` attribute (Lesson 6), `deposit()` should be concrete and shared, `withdraw()` should be abstract, since each account type enforces genuinely different rules.

Deliverable: `accounts.py` with the abstract `Account` class and the exception hierarchy, plus a short script proving `Account()` can't be instantiated directly, and that `Account.balance` genuinely has no public setter.

## Milestone 2: concrete account types

Build `SavingsAccount` and `CheckingAccount`, each inheriting from `Account` and correctly implementing `withdraw()` with their own specific rule, exactly as shown in Lesson 11's `SavingsAccount`/`CheckingAccount` example. Use `super().__init__()` correctly in both. Get the validation genuinely right: a `SavingsAccount` should track withdrawals in a way that could reasonably reset monthly (a simple counter is fine for this project; you don't need real date logic), and `CheckingAccount` should correctly compute whether a withdrawal would exceed its overdraft limit.

Deliverable: both concrete classes, plus test code demonstrating a successful and a rejected withdrawal for each account type, using the custom exceptions from Milestone 1.

## Milestone 3: Transaction and composition

Build `Transaction` in `transaction.py`: a simple class recording an amount, a type (`"deposit"`, `"withdrawal"`, `"transfer_in"`, `"transfer_out"`), and a timestamp. Wire `Account` to maintain a private `_transactions` list, appending a new `Transaction` record every time `deposit()` or `withdraw()` succeeds, composition, exactly as diagrammed above. Add a method `statement()` to `Account` that returns a formatted summary of every transaction.

Deliverable: an account that correctly logs every successful operation, and rejects logging anything for a failed operation (a withdrawal that raises `InsufficientFundsError` should NOT appear in the transaction history).

## Milestone 4: Customer and aggregation

Build `Customer` in `customer.py`: holds a name, an id, and a list of `Account` objects (aggregation, since accounts could conceivably be reassigned, and a `Customer` doesn't create `Account` instances internally the way `Account` creates its own `Transaction` records). Add a method `total_balance()` summing across every account the customer holds, and `open_account(account_type, ...)` that constructs and attaches a new account.

Deliverable: a `Customer` who can hold both a `SavingsAccount` and a `CheckingAccount` simultaneously, with `total_balance()` correctly summing both.

## Milestone 5: Bank and transfers

Build `Bank` in `bank.py`: the top-level coordinator, holding a collection of `Customer` objects, capable of looking up any account by its account number across every customer, and implementing `transfer(from_account_number, to_account_number, amount)`. This is the trickiest logic in the whole project: a transfer must withdraw from the source and deposit into the destination as a single logical operation, if the withdrawal fails (insufficient funds, limit exceeded), the deposit must never happen at all. Think carefully about the order of operations that guarantees this.

Deliverable: `Bank.transfer()`, with test code demonstrating both a successful transfer between two different customers' accounts, and a correctly rejected transfer that leaves both accounts completely untouched.

## Milestone 6: the CLI and polish

Build `cli.py` and wire everything together in `main.py`: create customers, open accounts, deposit, withdraw, transfer, and print a statement, all through a menu loop, catching every custom exception with a clear message rather than a raw traceback. Go back through the whole system looking for edge cases: what happens transferring an account to itself, what happens with a zero or negative amount anywhere, what happens looking up an account number that doesn't exist. Fix what you find.

## Suggested git commits

```
1. project skeleton and package structure
2. exception hierarchy
3. abstract Account base with property-based balance
4. SavingsAccount implementation and tests
5. CheckingAccount implementation and tests
6. Transaction class
7. wire Account to log transactions via composition
8. Customer class with account aggregation
9. Bank class: customer and account management
10. Bank.transfer() — atomic withdrawal and deposit
11. CLI menu loop
12. wire CLI to Bank, end-to-end working app
13. edge case fixes: self-transfer, zero amounts, invalid lookups
14. README and manual test checklist
```

## Manual testing checklist

- Does creating a `SavingsAccount` and immediately withdrawing more than the balance correctly raise `InsufficientFundsError`, with the balance unchanged afterward?
- Does exceeding a `SavingsAccount`'s monthly withdrawal count correctly raise `WithdrawalLimitExceededError`?
- Does a `CheckingAccount` correctly allow a withdrawal that dips into the overdraft limit, and correctly reject one that exceeds it?
- After a failed withdrawal attempt, is the account's transaction history unchanged, no phantom record for the failed attempt?
- Does `Bank.transfer()` leave both accounts completely untouched when the withdrawal side fails?
- Does `Customer.total_balance()` correctly sum across every account type the customer holds?
- Does attempting to instantiate the abstract `Account` class directly still correctly raise `TypeError`?

## Refactoring opportunities

Once the system works end to end, look specifically for any place a concrete class name appears where an abstraction should be used instead, is `Bank` referencing `SavingsAccount` or `CheckingAccount` by name anywhere it shouldn't need to, when it could just work with any `Account`? Also look for any remaining `if isinstance(account, SavingsAccount): ... elif ...` branching anywhere in the CLI or `Bank`, that's a signal polymorphism should be doing that work instead, exactly the Lesson 8 pattern.

## Future enhancements

Once this feels solid, natural next directions include adding interest calculation as a scheduled operation on `SavingsAccount`, persisting the entire system to a real database instead of in-memory objects (which would mean introducing a proper `Repository` abstraction, directly following Lesson 9's pattern, so `Bank` never needs to know or care whether accounts live in memory, in SQLite, or somewhere else entirely), and adding a proper audit log as a separate composed object rather than folding logging concerns directly into `Account`.
