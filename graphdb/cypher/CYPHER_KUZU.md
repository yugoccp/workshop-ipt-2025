# Cypher Tutorial

If you're new to Cypher and just getting started with Kuzu, you're in the right place! This tutorial will guide you through the basics of
Cypher, including how to create nodes and relationships, and how to scan, copy and query your data
that's in a Kuzu database.

## Define a schema

The first step in getting your data into Kuzu is creating node and relationship tables.

## Ingest the data

The `COPY FROM` command is used to ingest data from various file formats into Kuzu. In this case,
the data is stored in CSV format, in the local directory `dataset`.

```bash
COPY PERSON FROM './dataset/node_person.csv';
COPY LOCATION FROM './dataset/node_locations.csv';
COPY SCHOOL FROM './dataset/node_schools.csv';
COPY HOBBY FROM './dataset/node_hobbies.csv';
COPY JOB FROM './dataset/node_jobs.csv';
COPY LIVES_IN FROM './dataset/rel_lives_in.csv';
COPY MARRIED_TO FROM './dataset/rel_married_to.csv';
COPY STUDIES_AT FROM './dataset/rel_studies_at.csv';
COPY PARENTS_OF FROM './dataset/rel_parents_of.csv';
COPY HAS_HOBBY FROM './dataset/rel_has_hobby.csv';
COPY WORKS_AS FROM './dataset/rel_works_as.csv';
COPY CHILD_OF FROM './dataset/rel_child_of.csv';
COPY SIBLING_OF FROM './dataset/rel_sibling_of.csv';
```
You should see messages in your terminal indicating how many tuples were copied into each table. An
example is shown below.

```
┌───────────────────────────────────────────────┐
│ result                                        │
│ STRING                                        │
├───────────────────────────────────────────────┤
│ 20 tuples have been copied to the User table. │
└───────────────────────────────────────────────┘
```

## MATCH

In Kuzu, a graph's nodes and relationships are stored in tables. The `MATCH` clause is used to
find nodes that match the pattern specified in the clause. All entities in the pattern are
returned via the `RETURN` clause.


### Match nodes

Let's say we want to match only `PERSON` nodes in the database. We can do this by specifying the label
in the `MATCH` clause.

```cypher
MATCH (a:PERSON) RETURN a.* LIMIT 3;
```
Note the `a.*` in the `RETURN` clause. This is a wildcard that returns all properties of the `PERSON`
node, regardless of how many properties there are.

```
┌─────────────┬──────────────────┬────────────┬──────────────────────────────────────────────────┐
│ a.person_id │ a.name           │ a.birthDate│ a.description                                    │
│ INT64       │ STRING           │ DATE       │ STRING                                           │
├─────────────┼──────────────────┼────────────┼──────────────────────────────────────────────────┤
│ 1           │ John Smith       │ 1980-01-15 │ A versatile software engineer with a pas...      │
│ 2           │ Jane Doe         │ 1992-08-22 │ A compassionate doctor dedicated to ...          │
│ 3           │ Peter Jones      │ 1975-05-30 │ An inspiring teacher with a knack for...         │
└─────────────┴──────────────────┴────────────┴──────────────────────────────────────────────────┘
```

You can also match nodes across multiple node tables, as shown below. However, it only makes sense to do this
when there exists a common property between the two tables.

```cypher
MATCH (a:PERSON:LOCATION) RETURN * LIMIT 3;
```

### Match a relationship pattern

You can match a relationship pattern by specifying the relationship in the `MATCH` clause.
In the below example, we match the `LIVES_IN` relationship between a `PERSON` node and a `LOCATION` node.

```cypher
MATCH (a:PERSON)-[r:LIVES_IN]->(b:LOCATION) RETURN a.name, b.name LIMIT 3;
```
```
┌──────────────┬──────────────┐
│ a.name       │ b.name       │
│ STRING       │ STRING       │
├──────────────┼──────────────┤
│ John Smith   │ New York     │
│ Jane Doe     │ San Francisco│
│ Peter Jones  │ London       │
└──────────────┴──────────────┘
```
The person named `John Smith` lives in `New York`.

### Match on all nodes and relationships

If you want to match on an arbitrary node or relationship in the database, you can use the `MATCH` clause without any label
in the pattern.

```cypher
// Ask for all nodes and relationships in the database
MATCH (a)-[b]->(c) RETURN * LIMIT 3;
```
```
┌──────────────────────────────────┬──────────────────────────────────┬──────────────────────────────────┐
│ a                                │ c                                │ b                                │
│ NODE                             │ NODE                             │ REL                              │
├──────────────────────────────────┼──────────────────────────────────┼──────────────────────────────────┤
│ {_ID: 0:0, _LABEL: PERSON, pe... │ {_ID: 1:0, _LABEL: LOCATION, ... │ (0:0)-{_LABEL: LIVES_IN, _ID:...   │
│ {_ID: 0:1, _LABEL: PERSON, pe... │ {_ID: 1:1, _LABEL: LOCATION, ... │ (0:1)-{_LABEL: LIVES_IN, _ID:...   │
│ {_ID: 0:2, _LABEL: PERSON, pe... │ {_ID: 1:2, _LABEL: LOCATION, ... │ (0:2)-{_LABEL: LIVES_IN, _ID:...   │
└──────────────────────────────────┴──────────────────────────────────┴──────────────────────────────────┘
```

An alternate way to do this would be to leave the node and relationship fields blank, but store the path in a variable `p` as shown below.

```cypher
// Ask for all paths in the database
MATCH p=()-[]->() RETURN p LIMIT 3;
```
Both the above queries return similar results.

:::caution[Note]
It's recommended to use a `LIMIT` clause after the `RETURN` clause to control the number of tuples
returned in the result. By default, the shell returns the top 20 tuples in the result table.
:::

### Match multiple patterns

You can combine multiple match clauses that each specify a particular pattern.

```cypher
MATCH (a:PERSON)-[:SIBLING_OF]->(b:PERSON),
      (a)-[:LIVES_IN]->(c:LOCATION),
      (b)-[:LIVES_IN]->(c:LOCATION)
RETURN
  a.name AS person1,
  b.name AS person2,
  c.name AS location
LIMIT 3;
```

The above query is the same as having written the following three match clauses one after the other.
```cypher
MATCH (a:PERSON)-[:SIBLING_OF]->(b:PERSON)
MATCH (a)-[:LIVES_IN]->(c:LOCATION)
MATCH (b)-[:LIVES_IN]->(c:LOCATION)
RETURN a.name, b.name, c.name LIMIT 3;
```
Instead of repeating the match clause, you can comma-separate the clauses as shown above.
The following result is returned.

```
┌───────────┬───────────┬──────────┐
│ person1   │ person2   │ location │
│ STRING    │ STRING    │ STRING   │
├───────────┼───────────┼──────────┤
│ John Smith│ Jane Doe  │ New York │
└───────────┴───────────┴──────────┘
```

### Match variable-length relationships

One of the most powerful features of Cypher is the ability to match variable-length relationships.
This is done using the Kleene star operator `*`. The following query aims to find all people that
are one or two hops (i.e., paths with 1 or 2 edges) away from a particular person through the `SIBLING_OF` relationship.

```cypher
MATCH (a:PERSON)-[:SIBLING_OF*1..2]->(b:PERSON)
WHERE a.name = 'John Smith'
RETURN a.name, b.name
LIMIT 5;
```
```
┌────────────┬──────────┐
│ a.name     │ b.name   │
│ STRING     │ STRING   │
├────────────┼──────────┤
│ John Smith │ Jane Doe │
└────────────┴──────────┘
```

The full Kleene star syntax has the form `*<low>..<high>`. In the above example, the lower bound was `1` and the upper bound was `2`,
and so we match any paths with one or two edges. Alternatively, we can do `*..<high>` in which case the lower bound defaults to `1`.
And, if we just want to match paths with an exact number of edges, we can simply do `*<len>` instead of specifying the same bound twice.

For example, if we want to find all people that are exactly two hops away, we can use the following query.

```cypher
MATCH (a:PERSON)-[:PARENTS_OF*2]->(b:PERSON)
WHERE a.name = 'Peter Jones'
RETURN a.name, b.name
LIMIT 5;
```
```
┌─────────────┬────────────┐
│ a.name      │ b.name     │
│ STRING      │ STRING     │
├─────────────┼────────────┤
│ Peter Jones │ Emily Davis│
└─────────────┴────────────┘
```

The above result is telling us that the person in column `b` is a grandchild of the person in column `a`.
We can verify if this is true by manually writing the following query without the `*` operator.

```cypher
MATCH (a:PERSON)-[:PARENTS_OF]->(x:PERSON)-[:PARENTS_OF]->(b:PERSON)
WHERE a.name = 'Peter Jones'
RETURN a.name, b.name;
```
```
┌─────────────┬────────────┐
│ a.name      │ b.name     │
│ STRING      │ STRING     │
├─────────────┼────────────┤
│ Peter Jones │ Emily Davis│
└─────────────┴────────────┘
```
Indeed, the same result is returned.

## DISTINCT

The `DISTINCT` clause is used to return unique tuples in the result. The following query returns all
people who have a job. No duplicates are returned.

```cypher
MATCH (p:PERSON)-[:WORKS_AS]->(j:JOB)
RETURN DISTINCT p.name
LIMIT 3;
```
```
┌─────────────┐
│ p.name      │
│ STRING      │
├─────────────┤
│ John Smith  │
│ Jane Doe    │
│ Peter Jones │
└─────────────┘
```

## OPTIONAL MATCH

The `OPTIONAL MATCH` clause is used to define a pattern to find in the database. The difference from a regular
`MATCH` is that if the system cannot match a pattern defined by `OPTIONAL MATCH`, it will set the values in
the variables defined only in the `OPTIONAL MATCH`, to NULL.
Depending on what the end goal is, returning nulls may or may not be acceptable, so use a conventional
`MATCH` if no nulls are desired.

```cypher
MATCH (p1:PERSON)
OPTIONAL MATCH (p2:PERSON)-[:MARRIED_TO]->(p1)
RETURN p1.name, p2.name
LIMIT 3;
```

```
┌─────────────┬───────────┐
│ p1.name     │ p2.name   │
│ STRING      │ STRING    │
├─────────────┼───────────┤
│ John Smith  │ Jane Doe  │
│ Jane Doe    │ John Smith│
│ Peter Jones │ NULL      │
└─────────────┴───────────┘
```

## WHERE

The `WHERE` clause allows you to specify predicates/constraints on a part of your query. The query
below shows how to filter the results to only include people whose birth date was before a
particular date.

```cypher
MATCH (a:PERSON)
WHERE a.birthDate < DATE('1980-01-01')
RETURN a.name, a.birthDate
LIMIT 3;
```
The date format in the `WHERE` predicate is specified in the format `YYYY-MM-DD`, as a string, and
transformed into a date object that can be compared with the `birthDate` property of the
`PERSON` node.

```
┌─────────────┬────────────┐
│ a.name      │ a.birthDate│
│ STRING      │ DATE       │
├─────────────┼────────────┤
│ Peter Jones │ 1975-05-30 │
└─────────────┴────────────┘
```

### WHERE EXISTS subquery

You can specify a subquery in a `WHERE` clause with the `EXISTS` keyword. The following query returns all people
who have at least one hobby.

```cypher
MATCH (p:PERSON)
WHERE EXISTS {
  MATCH (p)-[:HAS_HOBBY]->()
}
RETURN p.name
LIMIT 3;
```

```
┌────────────┐
│ p.name     │
│ STRING     │
├────────────┤
│ John Smith │
│ Jane Doe   │
│ Peter Jones│
└────────────┘
```

## Grouping and Aggregation

Cypher does not have an explicit `GROUP BY` clause. Instead, you can simply apply an aggregation function
in the `RETURN` clause and group by the specified property. The following query returns the total number of
people.

```cypher
MATCH (p:PERSON)
RETURN COUNT(p) AS num_people;
```

```
┌────────────┐
│ num_people │
│ INT64      │
├────────────┤
│ 10         │
└────────────┘
```
The following example shows how to group by the `location` and return the number of people living in each location.

```cypher
MATCH (p:PERSON)-[:LIVES_IN]->(l:LOCATION)
RETURN l.name, COUNT(p) AS num_people
LIMIT 3;
```

```
┌───────────────┬────────────┐
│ l.name        │ num_people │
│ STRING        │ INT64      │
├───────────────┼────────────┤
│ New York      │ 2          │
│ San Francisco │ 2          │
│ London        │ 2          │
└───────────────┴────────────┘
```

## ORDER BY

The `ORDER BY` clause is used to sort the results of a query. The following query returns all people
sorted in descending order of their birth date.

```cypher
MATCH (p:PERSON)
RETURN p.name, p.birthDate
ORDER BY p.birthDate DESC
LIMIT 3;
```
```
┌─────────────────┬────────────┐
│ p.name          │ p.birthDate│
│ STRING          │ DATE       │
├─────────────────┼────────────┤
│ Emily Davis     │ 2005-03-10 │
│ Michael Brown   │ 1998-11-02 │
│ Jessica Williams│ 1995-07-19 │
└─────────────────┴────────────┘
```

## WITH

The `WITH` clause is used to chain the results of one query to another. The example below shows how to
find the top 3 oldest people and then find the hobbies they have.

```cypher
MATCH (p:PERSON)
WITH p
ORDER BY p.birthDate ASC
LIMIT 3
MATCH (p)-[:HAS_HOBBY]->(h:HOBBY)
RETURN p.name AS oldest_person, h.name AS hobby;
```
Note the use of the `AS` keyword to rename the columns in the result.
```
┌───────────────┬───────────┐
│ oldest_person │ hobby     │
│ STRING        │ STRING    │
├───────────────┼───────────┤
│ Peter Jones   │ Reading   │
│ Peter Jones   │ Gardening │
│ John Smith    │ Painting  │
│ John Smith    │ Hiking    │
│ Jane Doe      │ Cooking   │
└───────────────┴───────────┘
```

## UNWIND

The `UNWIND` clause is used to unnest (i.e., explode) a list and return the elements as separate rows.
Consider that you have a list of names and you want to find their birth dates.

```cypher
UNWIND ["John Smith", "Jane Doe", "Peter Jones"] AS person_name
MATCH (p:PERSON {name: person_name})
RETURN p.name, p.birthDate;
```

```
┌─────────────┬────────────┐
│ p.name      │ p.birthDate│
│ STRING      │ DATE       │
├─────────────┼────────────┤
│ John Smith  │ 1980-01-15 │
│ Jane Doe    │ 1992-08-22 │
│ Peter Jones │ 1975-05-30 │
└─────────────┴────────────┘
```

## CASE

Cypher supports the `CASE` expression to handle conditional logic. The following query returns
the name of each person and a description of their age group.

```cypher
MATCH (p:PERSON)
RETURN p.name,
       CASE
           WHEN p.birthDate > DATE('2000-01-01') THEN '21st Century Born'
           ELSE '20th Century Born'
       END AS century_born
LIMIT 3;
```
```
┌────────────┬───────────────────┐
│ p.name     │ century_born      │
│ STRING     │ STRING            │
├────────────┼───────────────────┤
│ John Smith │ 20th Century Born │
│ Jane Doe   │ 20th Century Born │
│ Peter Jones│ 20th Century Born │
└────────────┴───────────────────┘
```
