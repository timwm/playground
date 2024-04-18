## linear search:
Scan through the array from beginning to end, looking for x

## Selection sort
```txt
Consider sorting n numbers stored in array A[1:n] by first finding the smallest
element of A[1:n] and exchanging it with the element in A[1]. Then find the
smallest element of A[2:n], and exchange it with A[2]. Then find the smallest
element of A[3:n], and exchange it with A[3]. Continue in this manner for the
first n - 1 elements of A.
```

## 2.3.1 merge sort
```txt
In each step, it sorts a subarray A[p:r], starting with the entire array A[1:n] and
recursing down to smaller and smaller subarrays. Here is how merge sort operates:
Divide the subarray A[p:r] to be sorted into two adjacent subarrays, each of half
the size. To do so, compute the midpoint q of A[p:r] (taking the average of p
and r), and divide A[p:r] into subarrays A[p:q] and A[q + 1 :r].
Conquer by sorting each of the two subarrays A[p:q] and A[q + 1 :r] recursively
using merge sort.
Combine by merging the two sorted subarrays A[p:q] and A[q + 1 :r] back into
A[p:r], producing the sorted answer.
```

## 2-2 Bubblesort
It works by repeatedly swapping adjacent elements that are out of order