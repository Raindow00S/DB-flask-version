# 将数据库查询结果转化为所需要的格式，用于这个功能的函数

# 传入一行个人信息，转为属性名-属性值一一对应的字典
def wrap_info(info,identity):
    if identity == 'student':
        attr = ["学号", "姓名", "院系", "专业", "年级"]
    elif identity == 'faculty':
        attr = ["职工号", "姓名", "职称"]
    else:
        attr = ["职工号", "姓名"]
    info_dict = dict(zip(attr, info))
    return info_dict

# 传入多行课题组信息（元组列表），加入属性名列表作为第一个元素
def wrap_groups(groups):
    attr = ["所属教师","编号","名称","类型"]
    groups.insert(0,attr)
    return groups

# 传入一行课题组信息（元组），加入属性名列表作为第一个元素
def wrap_one_group(group):
    # print("wrap_one_group参数："+str(group))
    attr = ["所属教师","编号","名称","类型"]
    group_dict = dict(zip(attr, group))
    return group_dict