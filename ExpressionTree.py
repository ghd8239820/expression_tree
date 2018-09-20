# 初始优先级
base_priority = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2
}


class ExpressionTreeNode(object):
    '''
    树节点对象
    op：运算符
    value：值
    parent：父节点
    children：子节点
    '''
    children = []
    parent = None

    def __init__(self, value=None, children=None, parent=None, op=None):
        self.value = value
        self.children = children
        self.parent = parent
        self.op = op


def __calculate_priority(expr:str):
    '''
    遍历表达式，计算出所有运算符的优先级
    :param expr:
    :return:
    '''
    op_locations = []  # 运算符的位置
    op_priority = []  # 运算符的优先级
    for idx, c in enumerate(expr):
        if not c.isdigit() and c is not '(' and c is not ')':
            op_locations.append((idx,c))
            op_priority.append([base_priority[c], c, idx])   # [优先级,运算符,表达式中的位置]
    priority = 0
    for index, c in enumerate(expr):
        if c == '(':
            priority += 1
        if c == ')':
            priority -= 1
        if c.isdigit and c is not '(' and c is not ')':
            # 计算这个运算符的优先级
            i = -1  # 在数组中的位置
            for k, op in enumerate(op_locations):
                if op[0] == index:
                    i = k
            # print(i)
            if i > -1:
                op_priority[i][0] += priority
            # print('给 %s 增加优先级 %d' % (op_priority[i][1], priority))
    print('运算符优先级：[优先级，运算符，位置]')
    print(op_priority)
    return op_priority


def __get_biggest_priority(op_priority:list):
    '''
    获取优先值最高的运算符
    :param op_priority:
    :return:
    '''
    big = 0
    for priority in op_priority:
        if priority[0] > big:
            big = priority[0]
    return big


def __get_priority_by_pri(op_priority:list, pri:int):
    '''
    根据优先级获取运算符
    :param op_priority:
    :param pri:
    :return:
    '''
    ans = []
    for priority in op_priority:
        if priority[0] == pri:
            ans.append(priority)
    return ans


def __find_ancestor(node:ExpressionTreeNode):
    '''
    找到一个节点的祖先
    :param node:
    :return:
    '''
    if node.parent is None:
        return node
    else:
        return __find_ancestor(node.parent)


def __find_children(leaves: list, priority):
    '''
    工具函数
    找到运算符左右两边的数并计算。如果：
    1：旁边不是数字，继续往外围找
    2：旁边的数字已经有了父节点，找到它的祖先节点作为孩子节点。
    :param leaves:
    :param priority:
    :return:
    '''
    pri, operator, index = priority[0], priority[1], priority[2]  # 优先级，运算符，位置
    #  一个运算符只可以有两个数相乘，后面的过程会合并优先级相同、运算符相同的节点，会出现多个儿子节点
    left_child_idx = index - 1
    right_child_idx = index + 1
    while leaves[left_child_idx] == 'x':
        left_child_idx -= 1
    l_child = __find_ancestor(leaves[left_child_idx])
    while leaves[right_child_idx] == 'x':
        right_child_idx += 1
    r_child = __find_ancestor(leaves[right_child_idx])
    return [l_child, r_child]


def __merge(pri:int, node_list:list):
    '''
    整合优先级、运算符相同的节点，将他们放在一个节点下面
    这里只处理了加法合并的那一层，并没有普及到所有运算，不过原理是一样的，将优先级、运算符号一样的节点合并起来，父节点的值是他们根据运算符号加起来的值
    :param priority:
    :param children:
    :return:
    '''
    if pri == 1:
        value = 0
        for node in node_list:
            value += node.value
        parent_node = ExpressionTreeNode(op=node_list[0].op)
        parent_node.children = node_list
        for node in node_list:
            node.parent = parent_node
        parent_node.value = value
        parent_node.parent = None
        return parent_node


def __make_relate_between_nodes(parent: ExpressionTreeNode, children: list):
    '''
    链接子节点和父节点，并将计算值存到父节点value中
    :param parent:
    :param children:
    :return:
    '''
    for child in children:
        child.parent = parent
    parent.children = children
    if parent.op == '+':
        value = 0
        for child in children:
            value += child.value
        parent.value = value
    if parent.op == '-':
        value = children[0].value
        for x in range(1, len(children)):
            value -= children[x].value
        parent.value = value
    if parent.op == '*':
        value = children[0].value
        for x in range(1, len(children)):
            value = value * children[x].value
        parent.value = value
    if parent.op == '/':
        value = children[0].value
        for x in range(1, len(children)):
            value = value / children[x].value
        parent.value = value
    return parent


def __shuffle_node_list(node_list:list):
    '''
    将不符合合并条件的node剔除出去
    :param node_list:
    :return:
    '''
    pass


def create_expression_tree(expr: str):
    '''
    根据表达式创建树并运算
    :param expr:
    :return:
    '''
    priority = __calculate_priority(expr)
    #  从叶子节点开始创建树
    leaves = []
    for idx, c in enumerate(expr):
        leaves.append(ExpressionTreeNode(int(c))) if c.isdigit() else leaves.append('x')
    pri = __get_biggest_priority(op_priority=priority)
    #  按照优先级一层一层往上建
    while pri > 0:
        ops = __get_priority_by_pri(op_priority=priority, pri=pri)
        for op in ops:
            children = __find_children(leaves=leaves, priority=op)
            parent_node = ExpressionTreeNode(op=op[1], parent=None)
            __make_relate_between_nodes(parent=parent_node, children=children)
        pri -= 1
        #  这里只处理了加法合并的那一层，并没有普及到所有运算，不过原理是一样的，将优先级、运算符号一样的节点合并起来，
        #  父节点的值是他们根据运算符号加起来的值
        # pri -= 1
        # if pri == 1:
        #     node = __merge(pri=1, node_list=pri_node_list)
        #     return node
    for leaf in leaves:
        if type(leaf) == ExpressionTreeNode:
            return __find_ancestor(leaf)


if __name__ == '__main__':
    root = create_expression_tree('(1+2)+(5*6-7)+3/4')
    print('计算结果：'+ str(root.value))
    print('第二层节点：')
    print(root.children)
    print('第二层节点符号')
    for child in root.children:
        print(child.op)

