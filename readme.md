======== development ==========
run   . set_env.sh

======== db setup ========
pip install sqlalchemy
pip install alembic
alembic init migrations # this initiates generic template - single db, alembic list_templates list all templates
alembic revision -m 'initial_schema'

======== data source requirement ===========
Yahoo finance changed url and requires a cookie to connect

Alternative:
1. Google finance has informally provide 2 data download ways:
  1.1 one year data
  https://www.google.com/finance/historical?output=csv&q=[Symbol name]

  1.2 any time frame/resolution data but without date
  https://www.google.com/finance/getprices?i=86400&p=7d&f=d,o,h,l,c,v&df=cpct&q=IBM
  86400 is # of seconds for each period, p=7d is the whole time frame,

2. QuantQuote
  h

finviz channel up and 52 week up is a useful tool. triagnel ascending has high fpr 


会议纪要

2017年2月11日

  12月底开的账户

  抓底部反弹

    举例：TLT 美国国库券
      国库券能源周期长，要多等一段时间

    10%仓位 一次交易

    信号起点：
      TLT在Trump上台附近大跌，RSI跌至30以下
      大公司跌不会一直下，会有抢反弹机会，1%~2%反弹
      读wall street journal看哪家大跌

    信号跟踪：
      顺着BBAND往下走，RSI 30以下不要动，

    抓低点：
      BBAND不能斜着下，BBAND往前几个点开始变平，而且RSI往上走，过了30左右震荡区，开始动，如果MACD也开始往上走，可以开始买

    * 底部反弹和底部correction不同
      底部反弹是FA，需要放量大涨
      底部correction是TA

    * MACD变化最缓慢，RSI最灵敏

    找卖点：
      conservative的，可以找stochastic差别开始减小的点卖
      aggresive的，可以等MACD的差别开始缩小再卖
      BBAND的顶开始变平
      设保护单子要根据预期幅度，反方向运动多少才割肉，运动额度大概是预期涨幅的1/3 
      涨的话，设tracking stop

    * BBAND上沿往上的时候，不能short
    * 向上向下势头太猛的时候，最好不要马上动
    * 超买short的条件要严格很多，要Bollinger Percentage低，而且超买表明它的趋势已经很牛了，很难大幅回调，所以一般期望3%回调
    * 设保护单子要根据预期幅度，反方向运动多少才割肉，而且short很难，需要很谨慎，大涨后短期内最好不动，放量暴涨，跳空高开都不要动
    * 设screen 超跌，超买
    * VRX 今年要涨！卖put，成功率极其大，跌不下去了，就卖一周的put，错了赶紧卖


XIV    14号69块多  后来跌了
SPY               却继续涨

20 weekly line 一直向上， 
需要10周，15周，20周的观察
Close price要大多数时刻在20周线上


出入点
个体化，顺着10周线或者20周线往上走
如果很牛的股票，顺着10周线走，那么就在10周线作为支撑
如果一般的股票，顺着20周线走，那么就在20周周线作为支撑，
在支撑上面1-1.5%百分点就买
割肉在下面2-3%

trend出点需要做另外strategy

***
earning附近以当天计算
高开低走，
而且高开需要是过去26周的最高的2%附近，
***

MACD负值，而且负的比较厉害，跟前六个月的MACD最低负点比，至少50%


投资底部反弹和顶部调整，肯定是和weekly pattern相反的

10周







天然气   
1月份需求高峰    7月份需求低谷
但7月份会增加库存

可以库存，可以用来发电，可以贱卖，所以价格都是priced in

天然气contango很大，看每个月future的增加，增加多，则contango大





bollinger下沿要平，四到五天

MA一般不用，只用weekly来看大趋势


search rsi < 30 高于 70

底部往上走的就开始买


IBM三重顶


one cancel the other同时设买卖单
但conditional不能用这个，所以还是用conditional做


每天发trigger email
形式：cap> 20 B, RSI<30 or >70,    MACD是否开始走出？


出现收窄，走人，等趋势，走的点位在最近的低点

long position太多


price在20周线上，连续







Trigger_name  Index Avg_gain  Success_rate  Frequency selling point 5 subsequent trading days     
trigger_sporadic  dow30 -0.000104874  0.511909309 81155         
trigger_macd_up_trend dow30 0.002035418 0.543184885 1482    50% 70% 80% 100%
trigger_macd_down_trend ?               
trigger_rsi_up_trend  dow30 0.002454156 0.547149123 912 涨到32以上  涨到33以上      
trigger_rsi_down_trend  ?               
trigger_rsi_low dow30 0.00371812  0.540050345 15493         
trigger_rsi_high  dow30 -0.000656384  0.50575957  23092 delete        
trigger_bband_lowerflat dow30 -0.00015568 0.510647069 70348         
trigger_bband_upbreak dow30 0.00141547  0.546666667 300         
trigger_bband_downbreak dow30 0.003843089 0.496153846 260         
20 week MA                  
                  
                  
selling point rules fixed 5 trading dates     neither of them met         
conditional cut loss  1%      both of them met at the same day          
conditional get profit  2%      cut loss met          
  whichever comes first     get profit met          
                  
                  
                  
trigger date  10 trading date low and high                
                  
                  
稳住了之后某一天涨3到5个百分点                  
新规则：RSI跳涨                 
前几天都低于32，至少有一天低于30，但今天跳到32以上                  
MACD黑线上钩，macddiff减小                 
bollinger percent 往上反弹15% 当天  放到RSI一起           
commodity用MACD做                 
short correction的时候更要用MACD做                 
PSX反弹非常快                  
TSO炼油厂                  


出消息之后，放量高开低走，那么很大很大可能这个股票不好了
多看图，给出错误的地方，为什么错，哪些共性，怎么避免
weekly数据，给出trigger point，算的TA指标，需要确认对不对


如果上沿下沿是平的，而且touch了，很容易弹回去
Bollinger band宽，表示反弹幅度大，更好做

过去六个月最高点 touch的次数

10周二十周 都在增长 很重要



above 20 weekly MA for 10 weeks as buying trigger, and look forward 2 weeks to see success or not

AAPL for 10 years 
rule_stats(avg_gain=0.01115787941180584, success_rate=0.55, frequency=60)

Write a FUNCTION to decide
1% down or 2% up which comes first?
Use this as success rate

Touch 20 MA
20MA increase continuously
every week is above 20MA

only condition
20MA up constantly for 10 weeks
look for 5 weeks

csv file

touch peak 98% and up
look up CAT
daily data touch 1.5%
past 6 months
duration(last time touch ts - first time touch ts), relation to success rate

做以上两个长期趋势 下周六早一点发csv结果，举几个例子


测BNO，


FA 对turnover的企业看现金流

cash flow 总体指没有变卖资产的现金流（这个要注意手中的现金和负债总额的对比）。假如没有变卖资产，简单的就是实在的现金收入 - 现金支出

当然，还有一个非常重要，就是手中的资产（这个资产评估受油气价格影响）跟总负债对比，假如现在手中资产比负债多，一点问题都没有。假如现在手中资产比负债少，那么1，如果现金流是正的，只要不是liquidity问题（就是被人逼债）那么可以慢慢的把债还下来。2，如果现在流是负的，就看随着油气价格变化，多快现金流能够变成正的或者资产能够增值到多于负债。中心思想是能不能在未来把债务减下来（或者通过正的现金流或者通过卖资产），还有如果能够把债务减下来，还能给股东剩下多少



RSI>70可能要冲很久
这种情况用MACD确认向下判断空

RSI<30可能较快反弹
这种情况下MACD比较慢

看ER
10-q file
asset可作假，liability不可能作假
关键看的项目
total liability
total equity value (deficit)
total share num: WEIGHTED AVERAGE COMMON AND COMMON EQUIVALENT SHARES OUTSTANDING


refactor considerations:
1. 分离处理逻辑和处理对象
2. 分离处理对象和大规模数据
3. 分离处理结果和发送消息

单机for loop的局限：无法并行计算，for loop多了，不方便微操调试，会stuck在一个retry上很久，尤其当job涉及到对外communicate的时候，失败率是很高的，不能stuck在一个email很久，要允许其他email也能发送

用messaging pattern:
处理对象一类，处理逻辑一类，用celery queue来让他们相遇
处理对象的数据如果太大，就用数据库存储
maintain一个指标来看是否成功处理完毕
处理完的结果存放在一个地方（非mem，因为考虑多进程）
一旦确认都处理完，建立另一个queue来发送结果
发送结果给各个receipant，fail就retry，放到queue尾
maintain一个指标来看是否queue为空





周六早上发
10周线   15周连续向上，10周连续向上

中期趋势
股价突破200天均线


revenue increase per year
PE, EPS per year
seasonality


search 2 year 
跳空高开低开，至少5%，量至少是前20天均量的2倍


中期趋势

抢反弹





FA 怎么看ER
EBIDTA    就是收入，扣除了前期投资折旧和运营成本

EBIDTA是主要收入指标

对turnaround公司，EBIDTA会被manipulate，因为折旧费是一个公司操纵的东西

对turnaround公司，着重看cash flow和debt，还有主要的买卖资产
期限看一年，因为有的债是一年还一次

去年同期的手中cash多少，对比今年，表名 CASH FLOW DATA
去年同期的手中Principal amount of debt outstanding多少，对比今年
debt包含短期current和长期longterm还有stock deficit

interest expense很不规则，每个季度有很大区别，不建议看

比如CHK，6个月前有882million的cash，现在只有13million，
6个月前9989million的debt, 现在有9710 million
cash减少869million，但债务只减少279million
也就是说债务比cash减少的少很多，
实际有590million亏损



