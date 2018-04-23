'''
For a given source string and a target string, you should output the first index(from 0) of target string in source string.
If target does not exist in source, just return -1.
'''

class Solution:
    '''
    Solution1: O(n2)
    '''
    def strStr1(self, source, target):
         # Solution1: O(nm)
        # When target is Null
        if target is None:
            return -1
        
        # When target is empty string
        if not target:
            return 0
        
        #When source is empty string
        if not source:
            return -1
            
        #the source index is from 0 to len(source) - len(target)    
        for i in range(len(source) - len(target) + 1):
            for j in range(len(target)):
                if source[i+j] != target[j]:
                    break
                # When jump out of the loop, still need to check if condition satisfies
                if j == len(target) - 1:
                    return i
        
        return -1
        
    '''
    Solution2: Using Robin-Karp Algorithm
    '''
    def strStr(self, source, target):
        if source is None or target is None:
            return -1
        
        if target == '':
            return 0
        
        n, m = len(source), len(target) 
        targetHash, sourceHash, base = 0, 0, 10**6
        
        # 计算哈希过程：
        # 当前哈希值进位 + 当前位置的arcii码的值，取模到base空间（为了防止数字过大）
        for i in range(m):
            targetHash = (targetHash * 31 + ord(target[i])) % base
        
        # abc
        # 97 * 31^2 + 31 * 16 + 99 
           
        # source: aabcd
        # target: bcd
        for j in range(n):
            sourceHash = (sourceHash * 31 + ord(source[j])) % base
            #如果不够足够位数就继续计算原串的hash
            if j < m - 1:
                continue
            
            #如果超过了目标串的长度，那么要重新调整元串儿中的子串的哈希
            if j > m - 1:
                sourceHash = (sourceHash - ord(source[j - m]) * 31 ** m) % base
            
            # 进行hash比较和字符串双重比较，因为我们之前有取模到base空间，所以双重比较很有必要
            if sourceHash == targetHash and source[j - m + 1:j + 1] == target:
                return j - m + 1
        
        return -1

'''
算法武器：Rabin-karp将字符串映射成整型作比较，化简时间复杂度到O(1)
解法一：O(n2)
第一个for循环遍历所有可能的起点，起点下标的最大值计算公式是：
len(source) - len(target)
因为range不包括最后一个元素，所以我们要把起点下标的最大值+1
第二个for循环是遍历目标串中的每一个字符，注意和源串作比较
解法二：O(n)
将字符串转化为整型数值，将字符串的比较转化为整数的比较，是复杂度从O(m) 降低到O(1)
注意使用字符串到整数映射过程中我们使用了base，有很小的可能性会发生冲突，即两个不同的字符串映射到了同一个整数造成targetHash == sourceHash, 所以在比较这部分时我们需要双重验证一下，再使用字符串比较一下以确保算法的绝对正确性。

引用自网络：
http://www.cnblogs.com/golove/p/3234673.html
Rabin-Karp 算法（字符串快速查找）
　　Go 语言的 strings 包（strings.go）中用到了 Rabin-Karp 算法。Rabin-Karp 算法是基于这样的思路：即把字符串看作是字符集长度进制的数，由数值的比较结果得出字符串的比较结果。
　　朴素的字符串匹配算法为什么慢？因为它太健忘了，前一次匹配的信息其实有部分可以应用到后一次匹配中去，而朴素的字符串匹配算法只是简单的把这个信息扔掉，从头再来，因此，浪费了时间。好好的利用这些信息，自然可以提高运行速度。
　　由于完成两个字符串的比较需要对其中包含的字符进行逐个比较，所需的时间较长，而数值比较则一次就可以完成，那么我们首先把“搜索词”中各个字符的“码点值”通过计算，得出一个数值（这个数值必须可以表示出字符的前后顺序，而且可以随时去掉某个字符的值，可以随时添加一个新字符的值），然后对“源串”中要比较的部分进行计算，也得出一个数值，对这两个数值进行比较，就能判断字符串是否匹配。对两个数值进行比较，速度比简单的字符串比较快很多。
　　比如我们要在源串 "9876543210520" 中查找 "520"，因为这些字符串中只有数字，所以我们可以使用字符集 {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'} 来表示字符串中的所有元素，并且将各个字符映射到数字 0～9，然后用 M 表示字符集中字符的总个数，这里是 10，那么我们就可以将搜索词 "520" 转化为下面的数值：
("5"的映射值 * M + "2"的映射值) * M + "0"的映射值 = (5 * 10 + 2) * 10 + 0 = 520
　　当然，如果“搜索词”很长，那么计算出来的这个数值就会很大，这时我们可以选一个较大的素数对其取模，用取模后的值作为“搜索词”的值。
　　分析一下这个数值：520，它可以代表字符串 "520"，其中:
代表字符 "5" 的部分是“ "5"的映射值 * (M 的 n - 1 次方) = 5 * (10 的 2 次方) = 500”
代表字符 "2" 的部分是“ "2"的映射值 * (M 的 n - 2 次方) = 2 * (10 的 1 次方) = 20”
代表字符 "0" 的部分是“ "0"的映射值 * (M 的 n - 3 次方) = 0 * (10 的 0 次方) = 0”
（n 代表字符串的长度）
　　我们可以随时减去其中一个字符的值，也可以随时添加一个字符的值。
　　“搜索词”计算好了，那么接下来计算“源串”，取“源串”的前 n 个字符（n 为“搜索词”的长度）"987"，按照同样的方法计算其数值：
("9"的映射值 * M + "8"的映射值) * M + "7"的映射值 = (9 * 10 + 8) * 10 + 7 = 987
　　然后将该值与搜索词的值进行比较即可。
　　比较发现 520 与 987 不相等，则说明 "520" 与 "987" 不匹配，则继续向下寻找，这时候该如何做呢？下一步应该比较 "520" 跟 "876" 了，那么我们如何利用前一步的信息呢？首先我们把 987 减去代表字符 "9" 的部分：
987 - ("9"的映射值 * (M 的 n - 1 次方)) = 987 - (9 * (10 的 2 次方)) = 987 - 900 = 87
　　然后再乘以 M（这里是 10），再加上 "6" 的映射值，不就成了 876 了么：
87 * M + "6"的映射值 = 87 * 10 + 6 = 876
　　当然了，由于采用了取模操作，当两个数值相等时，未必是真正的相等，我们需要进行一次细致的检查（再进行一次朴素的字符串比较）。若不匹配，则可以排除掉。继续下一步。
　　如果我们要在 ASCII 字符集范围内查找“搜索词”，由于 ASCII 字符集中有 128 个字符，那么 M 就等于 128，比如我们要在字符串 "abcdefg" 中查找 "cde"，那么我们就可以将搜索词 "cde" 转化为“("c"的码点 * M + "d"的码点) * M + "e"的码点 = (99 * 128 + 100) * 128 + 101 = 1634917”这样一个数值。
　　分析一下这个数值：1634917，它可以代表字符串 "cde"，其中：
代表字符 "c" 的部分是“ "c"的码点 * (M 的 n - 1 次方) = 99 * (128 的 2 次方) = 1622016”
代表字符 "d" 的部分是“ "d"的码点 * (M 的 n - 2 次方) = 100 * (128 的 1 次方) = 12800”
代表字符 "e" 的部分是“ "e"的码点 * (M 的 n - 3 次方) = 101 * (128 的 0 次方) = 101”
（n 代表字符串的长度）
　　我们可以随时减去其中一个字符的值，也可以随时添加一个字符的值。
　　“搜索词”计算好了，那么接下来计算“源串”，取“源串”的前 n 个字符（n 为“搜索词”的长度）"abc"，按照同样的方法计算其数值：
("a"的码点 * M + "b"的码点) * M + "c"的码点 = (97 * 128 + 98) * 128 + 99 = 1601891
　　然后将该值与“搜索词”的值进行比较即可。
　　比较发现 1634917 与 1601891 不相等，则说明 "cde" 与 "abc" 不匹配，则继续向下寻找，下一步应该比较 "cde" 跟 "bcd" 了，那么我们如何利用前一步的信息呢？首先去掉 "abc" 的数值中代表 a 的部分：
(1601891 - "a"的码点 * (M 的 n - 1 次方)) = (1601891 - 97 * (128 的 2 次方)) = 12643
　　然后再将结果乘以 M（这里是 128），再加上 "d" 的码点值不就成了 "bcd" 的值了吗：
12643 * 128 + "d"的码点 = 1618304 + 100 = 1618404
　　这样就可以继续比较 "cde" 和 "bcd" 是否匹配，以此类推。
　　如果我们要在 Unicode 字符集范围内查找“搜索词”，由于 Unicode 字符集中有 1114112 个字符，那么 M 就等于 1114112，而 Go 语言中使用 16777619 作为 M 的值，16777619 比 1114112 大（更大的 M 值可以容纳更多的字符，这是可以的），而且 16777619 是一个素数。这样就可以使用上面的方法计算 Unicode 字符串的数值了。进而可以对 Unicode 字符串进行比较了。
　　其实 M 可以理解为进位值，比如 10 进制就是 10，128 进制就是 128，16777619 进制就是 16777619。
'''