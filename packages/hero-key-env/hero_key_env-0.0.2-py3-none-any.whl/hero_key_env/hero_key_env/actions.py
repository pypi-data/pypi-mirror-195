# Author: xuejinlin
# Date: 2023/3/7 16:17


# 角度
angle = [i * 3 for i in list(range(121))]
# 力度
depth = list(range(11))
#操作类型: 0: 点击,  1: 滑动,  2: 释放
handle_type = [0,1,2]

# jn1_1_10_2:  技能1 滑动, 角度, 力度

# 移动操作 0
move_handle = ['noop']
for a in angle:
    for d in depth:
        move_handle.append("move_" + str(a) + "_" + str(d))

# 技能操作 1
skill_type = ['skill0','skill1','skill2','skill3',"skill4",'skill5','skilltt','skillbb','skillzhs','skillhc','skillhf','skilljg','skillct','skilljh']
skill_handle = []
# 技能操作: 点击
for st in skill_type:
    skill_handle.append(st + '_click')
    skill_handle.append('noop')
# 技能操作: 滑动
for st in skill_type:
    for a in angle:
        for d in depth:
            skill_handle.append(st + '_slide_' + str(a) + '_'+ str(d))
#技能操作: 加点 2
skill_upgrade_handle = ['noop']
skill_upgrade_type = ['skill1','skill2','skill3',"skill4"]
for st in skill_upgrade_type:
    skill_upgrade_handle.append(st+"_upgrade")

# 3指操作 3
threez_handle = ['noop']
for a in angle:
    for d in depth:
        threez_handle.append("threez_"+ str(a) + '_' + str(d))

# 购买装备 4
shopping_handle = ['noop','shopping1','shopping2']

# 小地图 5
map_handel = ['noop']
# 点击/滑动
map_handle_type = [0,1]
for mht in map_handle_type:
    for a in angle:
        for d in depth:
            map_handel.append('map_' + str(mht) + '_' + str(a) + '_' + str(d))

# print("move_handle_size: ",len(move_handle))
# print("skill_handle_size: ",len(skill_handle))
# print("skill_handle_upgrade_size: ",len(skill_upgrade_handle))
# print("threez_handle_size: ",len(threez_handle))
# print("shopping_handle_size: ",len(shopping_handle))
# print("map_handel_size: ",len(map_handel))