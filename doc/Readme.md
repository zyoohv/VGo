#智能反应系统建模


*	部队

|&nbsp;|01|02|03|04|05|06|07|
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|A|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|B|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|C|&nbsp;|&nbsp;|+|#|+|&nbsp;|&nbsp;|
|D|&nbsp;|&nbsp;|#|P|#|&nbsp;|&nbsp;|
|E|&nbsp;|&nbsp;|+|#|+|&nbsp;|&nbsp;|
|F|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|G|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|

> 'P' : 部队 & 移动范围 & 攻击范围

> '#' : 移动范围 & 攻击范围

> '+' : 攻击范围

部队属性：

> 'a' : 攻击力，每秒造成a点伤害

> 'b' : 血量

> 规定：先移动，后攻击

进阶属性：

1、增加兵种：狙击手。血量为1，无法移动，伤害高，射程远


*	地图

|&nbsp;|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|A|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|B|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|C|&nbsp;|A|A|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|D|&nbsp;|A|x|x|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|E|&nbsp;|&nbsp;|&nbsp;|x|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|F|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|x|&nbsp;|&nbsp;|D|&nbsp;|&nbsp;|&nbsp;|
|G|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|x|x|$|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|H|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|x|x|x|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|I|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|J|&nbsp;|&nbsp;|&nbsp;|x|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|K|&nbsp;|&nbsp;|x|x|D|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|L|&nbsp;|&nbsp;|x|$|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|D|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|
|M|&nbsp;|&nbsp;|x|x|x|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|$|$|&nbsp;|&nbsp;|&nbsp;|
|N|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|


> 'x' : 禁止移动位置

> '$' : 守方资源点，1血量

> 'A' : 攻击方部队

> 'D' : 防守方部队

地图属性：

> 1&nbsp;地图不变。因为作为防守方，地图显然是已知且不变的。（暂定）

> 2&nbsp;随时感知地图所有信息，包括敌我部队位置及状况。我们假设地图信息的输入来自另外的专门负责扫视的系统，这样面对欺诈、隐身等情况我们就可以愉快的甩锅辣。

由以上地图自然情况（包括资源点）作为全局情况，即不计入状态向量内，我们可以用两组集合来表示一个状态

$$  <攻军1-位置1，攻军2-位置2……> ,  <守军1-位置1，守军2-位置2……> $$


进阶属性：

1、增加道具：地雷，你懂的

2、增加环境：丛林。降低攻击距离，移动速度考虑需要降，比如可移动格子数降为4
