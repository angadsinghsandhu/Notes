# Combine Two Tables

Start with one row per person in `Person`. Find every row in `Address` with the same `personId` and return the person's first and last names alongside the city and state. A person without a matching address still contributes one row, with SQL `NULL` for both address columns. The primary keys are `Person.personId` and `Address.addressId`, so one person can have several address rows. The problem accepts any result row order. [Official problem and schema](https://leetcode.com/problems/combine-two-tables/)

The lesson inputs list the rows of `Person` first in `[personId, lastName, firstName]` order, followed by the rows of `Address` in `[addressId, personId, city, state]` order. JSON `null` represents SQL `NULL`.

## Work through the inputs

- **Missing and orphaned addresses.** Nia has no matching address. The output keeps her with two `NULL` values. Leo has a match, and an address for person 99 has no person to contribute a row.
- **Several addresses and repeated output.** Sam has three matching address IDs. Two have identical city and state values, so the same projected row appears twice. The third address has a stored `NULL` city and a known state. An address whose `personId` is `NULL` cannot match a person's ID.
- **An empty Person table.** Even with an address, there are no people to contribute rows. The result still has the four named columns.

## Preserve Person rows with a LEFT JOIN

Put `Person` to the left of `LEFT JOIN`. The `ON` condition uses the IDs because different people can share a name. For every joined row, `SELECT` picks the four requested columns. There is no `DISTINCT`, so addresses with different IDs and identical projected values retain their multiplicity.

The final `ORDER BY` uses the person and address primary keys so playback stays stable when fixture rows arrive in a different order. The IDs are available to the query even though they're absent from the returned columns. Each example shows one frame with the table returned by SQLite. Its highlighted source lines cover the projection, the preserved table, the join condition, and the display order.

## Why it works

Fix a person and count the address rows for which the `ON` condition is true. If the count is positive, SQL emits one joined row for each of those addresses, and the projection preserves all those rows. If the count is zero, a left join emits exactly one row for that person with every right-hand column set to `NULL`. Every result row belongs to a person in the left table, so an orphan address never appears on its own. An inner join would lose the person in the zero-match case.

For `P` people, `A` addresses, and `R` result rows, producing the output takes at least `O(R)` work. A nested-loop plan that scans all addresses for every person can spend `O(P × A)` looking for matches. With an index on `Address(personId, addressId)`, ordered lookups can find matches in `O(P log(A + 1) + R)` time under a B-tree lookup model. If the engine uses a separate comparison sort for display order, that adds up to `O(R log(R + 1))` time and `O(R)` sort storage. The exact work depends on the engine and query plan. The checker independently groups the fixture addresses by person ID and verifies the ordered table, including repeated rows and `NULL` values.
