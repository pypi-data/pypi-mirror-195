# Restricted Partition

A restricted partition is the subset of an integer partition with only partitions at
or below a certain length.

~~~python
from restricted_partition import iter_partition

iter_partition(5)

# [1, 1, 1, 1, 1]
# [1, 1, 1, 2]
# [1, 1, 3]
# [1, 2, 2]
# [1, 4]
# [2, 3]
# [5]

iter_partition(5, 3)

# [1, 1, 3]
# [1, 2, 2]
# [1, 4]
# [2, 3]
# [5]
~~~

Uses the accel_asc algorithm (thank you, Jerome Kelleher), so it is pretty speedy in pure Python.

I found the algorithm at https://jeromekelleher.net/generating-integer-partitions.html.
