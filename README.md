# test-tarantool-index
Explore tarantool db features including differeces with usage of tree and hash indexes.

We use [*Tarantool DB*](https://www.tarantool.io/) at my current project very extensively and with high load (hundreds of millions records in RAM).
The idea behind this test is to understand better whether there is a benefit of using hash based index vs tree based index.

There is an interesting comment on the topic could be found here on [Konstantin Osipov's page](http://kostja.github.io/misc/2017/02/23/tarantool-data-structures.html):
```
In fact, our tree performs so well that sometimes we don’t even understand what’s faster, a hash or the B+*-tree in Tarantool
1.6. According to our measurements, a hash is still some 30-40% faster, but it’s a mere 40% gain given the logarithmic
complexity of our tree against the constant complexity of a hash: this logarithm is expressed in terms of only 2 or 3 cache
line lookups, whereas a hash may have an average value of 2 cache line lookups. This is another manifestation of the fact that
for an in-memory database, the cost is defined not through regular operations, but rather in terms of how well a particular
data structure works with the cache.
```
