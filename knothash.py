def rotate_left(L, by):
    if by > len(L):
        by = by % len(L)
        
    return L[by:] + L[:by] if by > 0 else rotate_right(L, -by)

def rotate_right(L, by):
    if by > len(L):
        by = by % len(L)
        
    return L[-by:] + L[:-by] if by > 0 else rotate_left(L, -by) 


class KnotHash(object):
    
    def __init__(self, knot, lengths):
        self.current_index = 0
        self.skip_size = 0
        self._knot = knot
        self.lengths = lengths
    
    def hash(self, rounds):
        self._do_hash_rounds(rounds)
        
        return self._knot
    
    def hex_hash(self, rounds, hash_step):
        
        self.hash(rounds)
        
        return self._compute_hexadecimal_hash(hash_step)
    
    def _do_hash_rounds(self, rounds):
        for _ in range(0, rounds):
            for i, length in enumerate(self.lengths):
                self._knot = self._reverse_section(length)
                self.current_index = self._compute_next_index(length)
                self.skip_size +=1                    
    
    def _compute_next_index(self, length):
        return (self.current_index + length + self.skip_size) % len(self._knot)
    
    def _reverse_section(self, length):     
    
        if self.current_index + length <= len(self._knot):
            return self._knot[:self.current_index] + list(reversed(self._knot[self.current_index:self.current_index+length])) + \
                   self._knot[self.current_index+length:]        
        else:              
            rotated = rotate_left(self._knot, self.current_index)
            
            after_reverse = list(reversed(rotated[:length]))
            
            combined = after_reverse + rotated[length:]
            
            rotated_back = rotate_right(combined, self.current_index)
            
            return rotated_back
    
    def _compute_hexadecimal_hash(self, hash_step):           
        dense_hash = [None] * hash_step
        for index, hash_index in enumerate(range(0, 256, hash_step)):
            dense_hash[index] = self._sparse_hash(hash_index, hash_step)
    
        return ''.join([format(d, '02x') for d in dense_hash])
    
    def _sparse_hash(self, hash_index, hash_step):       
        return reduce(lambda x, y: x^y, self._knot[hash_index:hash_index+hash_step])