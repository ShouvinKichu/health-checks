#reverse a string
# def rev_str(n):
#     rev = ''
#     for i in n:
#         rev = i+ rev
#     return rev

# print(rev_str("mango"))


#ISpalindrome
# def is_pal(s):
#     return s == s[::-1]
# print(is_pal("boob"))


# count freq
# names = ["alice", "brad", "collin", "brad", "dylan", "kim"]
# def hash_map(n):
#     count = {}
#     for i in n:
#         if i not in count:
#             count[i] = 1
#         else:
#             count[i] +=1
#     return count
# print(hash_map(names))


#find largest
# nums = [5,3,9,1,7]
# lar = nums[0]
# for num in nums:
#     if num > lar:
#         lar = num
# print(lar)

# nums = [10,20,40,30]
# fir = sec = float('-inf')
# for n in nums:
#     if n > fir:
#         sec = fir
#         fir = n
#     elif fir > n > sec:
#         sec = n
# print(sec)


#remove dups:
# nums = [1,2,2,3,4,4]
# print(list(set(nums)))


#fibo:
# def fibo(n):
#     a , b = 0 , 1
#     for _ in range(n):
#         print(a, end=" ")
#         a , b = b , a + b
# fibo(11)

