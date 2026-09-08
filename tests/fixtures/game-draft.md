# 封印塔测试文案

虚构测试资源。节点绑定由已有游戏资源提供，以下仅为本批接入正文。

## tower.need_stones
角色：西洛
条件：月石不足3枚；{missing}为还缺的数量。
目标：nodes.need_stones.text
~~~~text
还差{missing}枚月石。等你找齐了，我再给你开门。
~~~~

## tower.leave
类型：玩家选项
目标：nodes.leave.text
~~~~text
再去找找
~~~~

## tower.goodbye
角色：西洛
目标：nodes.goodbye.text
~~~~text
好，我就在这里。
~~~~

## ui.overwrite.title
目标：ui.overwrite.title
~~~~text
覆盖存档
~~~~

## ui.overwrite.body
目标：ui.overwrite.body
~~~~text
当前手动存档将被替换。
自动存档不受影响。
~~~~

## ui.overwrite.confirm
目标：ui.overwrite.confirm
~~~~text
覆盖
~~~~

## ui.overwrite.cancel
目标：ui.overwrite.cancel
~~~~text
取消
~~~~

## ui.stones
目标：ui.stones
~~~~text
月石：{count}/3
~~~~
