##一种新的计算表达式方法
我们熟悉的计算表达式方法主要是通过栈或者二叉树来计算。我这个方法也是通过二叉树来做的，但跟以往生成树的方法有所不同。  
以前的方法是在构建树的同时，还需要判断计算优先级。在树建好后通过中序遍历或者转化成后缀表达式来计算表达式的值。我这个方法跟传统方法有所区别。  
算法步骤：
1. 先算出所有运算符的优先级；
2. 把所有数字当成叶子节点，从底层节点到root建立树；
3. 根据优先级从高到低，先从叶子节点建立高优先级的子树,建立树的时候顺便计算该表达式的值；
4. 如果运算符涉及到的数字已经被别的树（A树）占有，就把A树当作它的子树，用A树的值来计算；
5. 树建立完成后也同时完成了计算，根节点的值就是表达式的值。

待完善：
1. 目前只支持一位数四则运算