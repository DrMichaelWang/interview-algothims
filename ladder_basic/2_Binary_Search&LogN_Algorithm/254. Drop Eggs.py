'''
There is a building of n floors. If an egg drops from the k th floor or above, it will break. If it's dropped from any floor below, it will not break.

You're given two eggs, Find k while minimize the number of drops for the worst case. Return the number of drops in the worst case.

Example
Given n = 10, return 4.
Given n = 100, return 14.
'''
class Solution:
    # @param {int} n an integer
    # @return {int} an integer
    def dropEggs(self, n):
        # import math
        # x = int(math.sqrt(n * 2))
        x = 1
        while x * (x + 1) / 2 < n:
            x += 1
        return x

'''
算法武器：逻辑分析 + 实验分析

分析方法：先走实验用例，再尝试寻找解决方案。先具体后抽象

这是一道实验类型的题目，我们需要走几个实验的例子，然后我们就能够窥见其中的端倪。

问题分析1 http://www.cnblogs.com/grandyang/p/4762756.html
这道题说有100层楼，从N楼开始扔鸡蛋会碎，低于N楼扔不会碎，现在给我们两个鸡蛋，让我们找到N，并且最小化最坏情况。
因为只有两个鸡蛋，所以第一个鸡蛋应该是按一定的间距扔，比如10楼，20楼，30楼等等，比如10楼和20楼没碎，30楼碎了，那么第二个鸡蛋就要做线性搜索，分别尝试21楼，22楼，23楼等等直到鸡蛋碎了，就能找到临界点。那么我们来看下列两种情况：

假如临界点是9楼，那么鸡蛋1在第一次扔10楼碎掉，然后鸡蛋2依次遍历1到9楼，则总共需要扔10次。
假如临界点是100楼，那么鸡蛋1需要扔10次，到100楼时碎掉，然后鸡蛋2依次遍历91楼到100楼，总共需要扔19次。
所以上述方法的最坏情况是19次，那么有没有更少的方法呢，上面那个方法每多扔一次鸡蛋1，鸡蛋2的线性搜索次数最多还是10次，那么最坏情况肯定会增加，所以我们需要让每多扔一次鸡蛋1，鸡蛋2的线性搜索最坏情况减少1，这样恩能够保持整体最坏情况的平衡，那么我们假设鸡蛋1第一次在第X层扔，然后向上X-1层扔一次，然后向上X-2层扔，以此类推直到100层，那么我们通过下面的公式求出X：
X + (X-1) + (X-2) + ... + 1 = 100 -> X = 14
所以我们先到14楼，然后27楼，然后39楼，以此类推，最坏情况需要扔14次。
问题分析2 https://www.jiuzhang.com/qa/2711/
1.
举个例子，假如当前我们要解决的问题是100层楼，那么假如我们一开始按照10作为间距的话，如果n是9的话，我们就要扔一次第一个鸡蛋，扔9次第二个鸡蛋，也就是需要10次，但这个明显不是最坏的情况，如果n是99的话，我们就需要扔10次第一个鸡蛋，扔9次第二个鸡蛋，那么需要19次。这种情况就是最坏的情况，现在再反过来想，我们一开始以10作为间距真的是最优的解吗，很明显如果我们是以等间距扔第一个鸡蛋的话我们每一个区间的最坏查询情况都是不相等的，最坏的查询情况肯定是最后一个区间的最后一个数。

那么再想，如果我们能够让每一个区间的最坏查询次数都相等的话，最坏的查询就能够达到最优的方案，那么怎么才能达到这个条件呢。
仔细思考，查询到第二个区间的时候已经扔了一次第一个鸡蛋了，查询到第x个区间的时候已经扔了x-1次第一个鸡蛋了，所以显然如果我们等间距的话我们每一个区间的查询都要比前面一个区间多1次，所以我们可以每过一个区间把区间长度-1，这样就能够达到最佳的方案。
那么最大的那个区间怎么进行计算呢？
其实到这一步不难发现，这个最大区间就是我们要求的最坏的情况的查询数了。
n + (n-1) + (n-2)…… + 1 = N。
这样我们就可以用简单的循环来求得这个n。
'''