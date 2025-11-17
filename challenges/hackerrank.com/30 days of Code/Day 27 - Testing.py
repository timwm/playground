import random


class TestDataEmptyArray:
    def get_array(self):
        return list()


class TestDataUniqueValues:
    def get_array(self):
        length = random.randint(2, 100)
        # Set of values between [0, 100]
        arr = set([random.randint(0, int(random.random() * 100)) for i in range(length)])
        while len(arr) < length:
            arr.add(random.randint(0, 100))
       
        return list(arr)

    def get_expected_result(self):
        random.randint(0, 100)


class TestDataExactlyTwoDifferentMinimums:
    def __init__(self):
        self.min = random.randint(0, 100)
        self.data = list()

    def get_array(self):
        start = self.min + 1
        length = random.randint(2, 100)
        # Set of values between [start, start + 100]
        mset = set([random.randint(start, start + int(random.random() * 100)) for i in range(length)])
        while len(mset) < length:
            mset.add(random.randint(0, 100))
        # Make sure we have at least self.min in the set
        mset.add(self.min)
        
        self.data = list(mset)
        self.data.append(self.min)

        random.shuffle(self.data)
        
        return self.data

    def get_expected_result(self):
        return self.data.index(self.min)


def minimum_index(seq):
    if len(seq) == 0:
        raise ValueError("Cannot get the minimum value index from an empty sequence")
    min_idx = 0
    for i in range(1, len(seq)):
        if seq[i] < seq[min_idx]:
            min_idx = i
    return min_idx


def TestWithEmptyArray():
    try:
        seq = TestDataEmptyArray.get_array()
        result = minimum_index(seq)
    except ValueError as e:
        pass
    else:
        assert False


def TestWithUniqueValues():
    seq = TestDataUniqueValues.get_array()
    assert len(seq) >= 2

    assert len(list(set(seq))) == len(seq)

    expected_result = TestDataUniqueValues.get_expected_result()
    result = minimum_index(seq)
    assert result == expected_result


def TestiWithExactyTwoDifferentMinimums():
    seq = TestDataExactlyTwoDifferentMinimums.get_array()
    assert len(seq) >= 2
    tmp = sorted(seq)
    assert tmp[0] == tmp[1] and (len(tmp) == 2 or tmp[1] < tmp[2])

    expected_result = TestDataExactlyTwoDifferentMinimums.get_expected_result()
    result = minimum_index(seq)
    assert result == expected_result

TestWithEmptyArray()
TestWithUniqueValues()
TestiWithExactyTwoDifferentMinimums()
print("OK")

