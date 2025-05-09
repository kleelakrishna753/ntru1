import numpy as np
from padding.padding import padding_encode, padding_decode

def test_padding_round_trip():
    original = np.array([1, 2, 3, 4])
    block_size = 8
    padded = padding_encode(original, block_size)
    recovered = padding_decode(padded, block_size)
    assert np.all(recovered == original)

