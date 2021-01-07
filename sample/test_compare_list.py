from roughset import RoughSet as rs
k1 = [1,2,[3,4],[6,5]]
k2 = [2,[6,5],[4,3],1]
rs.list_to_set(k1)
rs.list_to_set(k2)
rs.compare_list(k1,k2)
