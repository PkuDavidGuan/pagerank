> 09/30

Begin to do the pagerank homework.
- Dataset:
    - author: 2014/networks/author-citation-network-nonself.txt
    - paper: 2014/networks/paper-citation-network-nonself.txt
    - venue: 2014/networks/paper-citation-network-nonself.txt, 2014/acl-metadata.txt
- 对venue的特殊处理：
    - idea：venue节点之间的边权重是不同的，简单地按照同权计算，paperank效果可能略差。
- 下午5:30，吃饭，venueRank pagerank部分还没改
- 20:15，acl-metadata格式有问题，不能按照5行一个条目来读