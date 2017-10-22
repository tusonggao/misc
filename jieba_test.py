import jieba

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print "Full Mode:", "/ ".join(seg_list) #全模式

seg_list = jieba.cut("他来到了网易杭研大厦") #默认是精确模式
print ", ".join(seg_list)
#
seg_list = jieba.cut("小明硕士毕业于中国科学院计算所，后在日本京都大学深造") 
print ", ".join(seg_list)


