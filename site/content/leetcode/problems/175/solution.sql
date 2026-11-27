-- Project only the four requested columns.
SELECT p.firstName, p.lastName, a.city, a.state
FROM Person AS p
LEFT JOIN Address AS a ON a.personId = p.personId
-- Sort by the source keys so the lesson can replay the same row order.
ORDER BY p.personId, a.addressId;
