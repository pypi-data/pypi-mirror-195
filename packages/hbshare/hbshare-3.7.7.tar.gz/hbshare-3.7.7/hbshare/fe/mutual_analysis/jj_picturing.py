# -*- coding:utf-8 -*-
import pandas as pd
from hbshare.fe.XZ import db_engine
from hbshare.fe.XZ import functionality
from hbshare.fe.mutual_analysis import  holdind_based as hb
import numpy as np
import datetime

util=functionality.Untils()
hbdb=db_engine.HBDB()
localdb=db_engine.PrvFunDB().engine
ia=hb.Industry_analysis()
plot=functionality.Plot(700,350)
ind_map=dict(zip(['股份制银行',
 '房地产开发',
 '软件开发',
 '环境治理',
 '一般零售',
 '轨交设备',
 '电池',
 '基础建设',
 '玻璃玻纤',
 '黑色家电',
 '摩托车及其他',
 '农产品加工',
 '光学光电子',
 '消费电子',
 '水泥',
 '汽车服务',
 '饰品',
 '电力',
 '医药商业',
 '汽车零部件',
 '通信设备',
 'IT服务',
 '综合',
 '通用设备',
 '装修建材',
 '房地产服务',
 '炼化及贸易',
 '工业金属',
 '其他电子',
 '专业工程',
 '计算机设备',
 '航运港口',
 '航空机场',
 '医疗服务',
 '贸易',
 '化学制药',
 '电视广播',
 '工程机械',
 '证券',
 '白色家电',
 '电网设备',
 '生物制品',
 '家电零部件',
 '燃气',
 '农化制品',
 '多元金融',
 '化学纤维',
 '化学原料',
 '中药',
 '酒店餐饮',
 '铁路公路',
 '旅游及景区',
 '造纸',
 '地面兵装',
 '个护用品',
 '教育',
 '出版',
 '照明设备',
 '军工电子',
 '商用车',
 '环保设备',
 '煤炭开采',
 '航空装备',
 '化学制品',
 '白酒',
 '乘用车',
 '自动化设备',
 '林业',
 '广告营销',
 '医疗美容',
 '物流',
 '保险',
 '房屋建设',
 '冶钢原料',
 '金属新材料',
 '元件',
 '小金属',
 '包装印刷',
 '家居用品',
 '影视院线',
 '数字媒体',
 '饲料',
 '特钢',
 '普钢',
 '医疗器械',
 '种植业',
 '休闲食品',
 '焦炭',
 '纺织制造',
 '非白酒',
 '养殖业',
 '能源金属',
 '工程咨询服务',
 '渔业',
 '专用设备',
 '专业连锁',
 '饮料乳品',
 '塑料',
 '通信服务',
 '食品加工',
 '电机',
 '油气开采',
 '贵金属',
 '橡胶',
 '服装家纺',
 '城商行',
 '非金属材料',
 '小家电',
 '互联网电商',
 '厨卫电器',
 '装修装饰',
 '半导体',
 '化妆品',
 '游戏',
 '光伏设备',
 '风电设备',
 '油服工程',
 '其他电源设备',
 '文娱用品',
 '调味发酵品',
 '农业综合',
 '电子化学品',
 '其他家电',
 '动物保健',
 '专业服务',
 '农商行',
 '航天装备',
 '体育',
 '航海装备',
 '网络服务',
 '有色金属冶炼与加工',
 '电气设备',
 '环保工程及服务',
 '家用轻工',
 '建筑装饰',
 '建筑材料',
 '金属制品',
 '计算机应用',
 '石油化工',
 '其他采掘',
 '传媒',
 '铁路运输',
 '酒店',
 '电源设备',
 '稀有金属',
 '金属非金属新材料',
 '互联网传媒',
 '畜禽养殖',
 '国有大型银行',
 '旅游零售',
 '本地生活服务'],['银行',
 '房地产',
 '计算机',
 '环保',
 '商贸零售',
 '机械设备',
 '电力设备',
 '建筑装饰',
 '建筑材料',
 '家用电器',
 '汽车',
 '农林牧渔',
 '电子',
 '电子',
 '建筑材料',
 '汽车',
 '纺织服饰',
 '公用事业',
 '医药生物',
 '汽车',
 '通信',
 '计算机',
 '综合',
 '机械设备',
 '建筑材料',
 '房地产',
 '石油石化',
 '有色金属',
 '电子',
 '建筑装饰',
 '计算机',
 '交通运输',
 '交通运输',
 '医药生物',
 '商贸零售',
 '医药生物',
 '传媒',
 '机械设备',
 '非银金融',
 '家用电器',
 '电力设备',
 '医药生物',
 '家用电器',
 '公用事业',
 '基础化工',
 '非银金融',
 '基础化工',
 '基础化工',
 '医药生物',
 '社会服务',
 '交通运输',
 '社会服务',
 '轻工制造',
 '国防军工',
 '美容护理',
 '社会服务',
 '传媒',
 '家用电器',
 '国防军工',
 '汽车',
 '环保',
 '煤炭',
 '国防军工',
 '基础化工',
 '食品饮料',
 '汽车',
 '机械设备',
 '农林牧渔',
 '传媒',
 '美容护理',
 '交通运输',
 '非银金融',
 '建筑装饰',
 '钢铁',
 '有色金属',
 '电子',
 '有色金属',
 '轻工制造',
 '轻工制造',
 '传媒',
 '传媒',
 '农林牧渔',
 '钢铁',
 '钢铁',
 '医药生物',
 '农林牧渔',
 '食品饮料',
 '煤炭',
 '纺织服饰',
 '食品饮料',
 '农林牧渔',
 '有色金属',
 '建筑装饰',
 '农林牧渔',
 '机械设备',
 '商贸零售',
 '食品饮料',
 '基础化工',
 '通信',
 '食品饮料',
 '电力设备',
 '石油石化',
 '有色金属',
 '基础化工',
 '纺织服饰',
 '银行',
 '基础化工',
 '家用电器',
 '商贸零售',
 '家用电器',
 '建筑装饰',
 '电子',
 '美容护理',
 '传媒',
 '电力设备',
 '电力设备',
 '石油石化',
 '电力设备',
 '轻工制造',
 '食品饮料',
 '农林牧渔',
 '电子',
 '家用电器',
 '农林牧渔',
 '社会服务',
 '银行',
 '国防军工',
 '社会服务',
 '国防军工',
 '信息服务',
 '有色金属',
 '机械设备',
 '公用事业',
 '轻工制造',
 '建筑建材',
 '建筑建材',
 '钢铁',
 '信息服务',
 '化工',
 '采掘',
 '信息服务',
 '交通运输',
 '休闲服务',
 '电气设备',
 '有色金属',
 '有色金属',
 '传媒',
 '农林牧渔',
 '银行',
 '商贸零售',
 '社会服务']))


class old_version:
    @staticmethod
    def industry_pic(jjdm,jjjc,th1=0.5,th2=0.5,show_num=20,if_percentage=True):

        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_industry_property_new",con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_industry_property_new where jjdm='{0}' and asofdate='{1}' "\
            .format(jjdm,latest_date)
        industry_p=pd.read_sql(sql,con=localdb).rename(columns={'cen_ind_1':'一级行业集中度',
                                                                'ratio_ind_1':'一级行业换手率',
                                                                'cen_ind_2': '二级行业集中度',
                                                                'ratio_ind_2': '二级行业换手率',
                                                                'cen_ind_3': '三级行业集中度',
                                                                'ratio_ind_3': '三级行业换手率',
                                                                'industry_num':'行业暴露数',
                                                                'top5': '前五大行业',
                                                                'longtou_med':'龙头占比(时序中位数)',
                                                                'longtou_mean': '龙头占比(时序均值)',
                                                                'longtou_med_rank': '龙头占比(时序中位数)排名',
                                                                'longtou_mean_rank': '龙头占比(时序均值)排名',
                                                                'cen_theme':'主题集中度',
                                                                'ratio_theme':'主题换手率'
                                                                })
        industry_p[['龙头占比(时序均值)','龙头占比(时序中位数)']]=industry_p[['龙头占比(时序均值)','龙头占比(时序中位数)']]/100
        float_col_list=industry_p.columns.tolist()
        float_col_list.remove('jjdm')
        float_col_list.remove('asofdate')
        float_col_list.remove('前五大行业')


        industry_detail_df_list=[]
        class_name_list=['yjxymc','ejxymc','sjxymc']
        name_map=dict(zip([ 'zsbl_mean', 'ROE_mean', 'NETASSETPS_mean',
           'DIVIDENDRATIO_mean', 'OPERCASHFLOWPS_mean', 'TOTALMV_mean', 'PE_mean',
           'PB_mean', 'PEG_mean', 'EPS_mean', 'NETPROFITGROWRATE_mean',
           'OPERATINGREVENUEYOY_mean', 'longtou_zjbl_for_ind_mean', 'zsbl_med',
           'ROE_med', 'NETASSETPS_med', 'DIVIDENDRATIO_med', 'OPERCASHFLOWPS_med',
           'TOTALMV_med', 'PE_med', 'PB_med', 'PEG_med', 'EPS_med',
           'NETPROFITGROWRATE_med', 'OPERATINGREVENUEYOY_med',
           'longtou_zjbl_for_ind_med', 'jjdm', 'zsbl_mean_rank', 'ROE_mean_rank',
           'NETASSETPS_mean_rank', 'DIVIDENDRATIO_mean_rank',
           'OPERCASHFLOWPS_mean_rank', 'TOTALMV_mean_rank', 'PE_mean_rank',
           'PB_mean_rank', 'PEG_mean_rank', 'EPS_mean_rank',
           'NETPROFITGROWRATE_mean_rank', 'OPERATINGREVENUEYOY_mean_rank',
           'longtou_zjbl_for_ind_mean_rank', 'zsbl_med_rank', 'ROE_med_rank',
           'NETASSETPS_med_rank', 'DIVIDENDRATIO_med_rank',
           'OPERCASHFLOWPS_med_rank', 'TOTALMV_med_rank', 'PE_med_rank',
           'PB_med_rank', 'PEG_med_rank', 'EPS_med_rank',
           'NETPROFITGROWRATE_med_rank', 'OPERATINGREVENUEYOY_med_rank',
           'longtou_zjbl_for_ind_med_rank', 'growth_mean_rank', 'value_mean_rank',
           'growth_med_rank', 'value_med_rank'],['占持仓比例(时序均值)','净资产收益率(时序均值)',
                                                 '每股净资产与价格比率(时序均值)','股息率(时序均值)',
                                                 '经营现金流与价格比率(时序均值)','总市值(时序均值)',
                                                 'PE(时序均值)','PB(时序均值)','PEG(时序均值)',
                                                 '每股收益与价格比率(时序均值)','净利润增长率(时序均值)',
                                                 '主营业务增长率(时序均值)','行业龙头占比(时序均值)',
                                                 '占持仓比例(时序中位数)','净资产收益率(时序中位数)',
                                                 '每股净资产与价格比率(时序中位数)','股息率(时序中位数)',
                                                 '经营现金流与价格比率(时序中位数)','总市值(时序中位数)',
                                                 'PE(时序中位数)','PB(时序中位数)','PEG(时序中位数)',
                                                 '每股收益与价格比率(时序中位数)','净利润增长率(时序中位数)',
                                                 '主营业务增长率(时序中位数)','行业龙头占比(时序中位数)',
                                                 'jjdm','占持仓比例(时序均值)排名','净资产收益率(时序均值)排名',
                                                 '每股净资产与价格比率(时序均值)排名','股息率(时序均值)排名',
                                                 '经营现金流与价格比率(时序均值)排名','总市值(时序均值)排名',
                                                 'PE(时序均值)排名','PB(时序均值)排名','PEG(时序均值)排名',
                                                 '每股收益与价格比率(时序均值)排名','净利润增长率(时序均值)排名',
                                                 '主营业务增长率(时序均值)排名','行业龙头占比(时序均值)排名',
                                                 '占持仓比例(时序中位数)排名','净资产收益率(时序中位数)排名',
                                                 '每股净资产与价格比率(时序中位数)排名','股息率(时序中位数)排名',
                                                 '经营现金流与价格比率(时序中位数)排名','总市值(时序中位数)排名',
                                                 'PE(时序中位数)排名','PB(时序中位数)排名','PEG(时序中位数)排名',
                                                 '每股收益与价格比率(时序中位数)排名','净利润增长率(时序中位数)排名',
                                                 '主营业务增长率(时序中位数)排名','行业龙头占比(时序中位数)排名',
                                                 '综合成长属性(时序均值)排名','综合价值属性(时序均值)排名','综合成长属性(时序中位数)排名',
                                                 '综合价值属性(时序中位数)排名','asofdate']))

        sql=" select * from hbs_industry_financial_stats where ENDDATE>='{0}' and ENDDATE<='{1}'"\
            .format(str(int(latest_date[0:4])-3)+latest_date[4:6],latest_date[0:6])
        industry_financial_info=pd.read_sql(sql,con=localdb)

        industry_financial_info[['ROE','NETPROFITGROWRATE',
                                 'OPERATINGREVENUEYOY','DIVIDENDRATIO']]=industry_financial_info[['ROE','NETPROFITGROWRATE',
                                 'OPERATINGREVENUEYOY','DIVIDENDRATIO']]/100

        industry_financial_info_mean=industry_financial_info\
            .groupby('industry_name').median().rename(columns={
            "ROE":"行业净资产收益率","EPS":"行业每股收益比股价","OPERCASHFLOWPS":"行业经营现金流与价格比率",
            "NETPROFITGROWRATE":"行业净利润增长率","OPERATINGREVENUEYOY":"行业主营业务增长率",
            "NETASSETPS":"行业每股净资产与价格比率","DIVIDENDRATIO":"行业股息率","AVERAGEMV":"行业平均市值","TOTALMV":"行业总市值",
            "PE":"行业PE","PB":"行业PB","PEG":"行业PEG"})
        industry_financial_info_med=industry_financial_info\
            .groupby('industry_name').median().rename(columns={
            "ROE":"行业净资产收益率","EPS":"行业每股收益比股价","OPERCASHFLOWPS":"行业经营现金流与价格比率",
            "NETPROFITGROWRATE":"行业净利润增长率","OPERATINGREVENUEYOY":"行业主营业务增长率",
            "NETASSETPS":"行业每股净资产与价格比率","DIVIDENDRATIO":"行业股息率","AVERAGEMV":"行业平均市值","TOTALMV":"行业总市值",
            "PE":"行业PE","PB":"行业PB","PEG":"行业PEG"})

        industry_financial_info=pd.merge(industry_financial_info_mean,industry_financial_info_med,
                                         how='inner',left_index=True,right_index=True)

        industry_financial_info.columns=industry_financial_info.columns.str.replace('TOP',"")
        industry_financial_info.columns = industry_financial_info.columns.str.replace('TOP', "")
        industry_financial_info.columns = industry_financial_info.columns.str.replace('MV', "市值")
        industry_financial_info.columns = industry_financial_info.columns.str.replace('%', "分位数")
        industry_financial_info.columns = industry_financial_info.columns.str.replace('_x', "(时序均值)")
        industry_financial_info.columns = industry_financial_info.columns.str.replace('_y', "(时序中位数)")
        industry_financial_info.reset_index(inplace=True)

        theme_weight=pd.DataFrame()
        for i in range(3):
            latest_date = pd.read_sql(
                "select max(asofdate) as asofdate from hbs_industry_property_{0}_industry_level".format(i+1), con=localdb)['asofdate'][0]

            sql = "SELECT * from hbs_industry_property_{2}_industry_level where jjdm='{0}' and asofdate='{1}' " \
                .format(jjdm, latest_date,i+1)
            temp_ind_detail=pd.read_sql(sql, con=localdb).rename(columns=name_map)
            temp_ind_detail.rename(columns={class_name_list[i]:'行业名称'},inplace=True)
            temp_ind_detail=temp_ind_detail.sort_values('占持仓比例(时序均值)', ascending=False).iloc[0:show_num]
            temp_ind_detail[['行业龙头占比(时序均值)', '行业龙头占比(时序中位数)',
                             '净资产收益率(时序均值)','股息率(时序均值)','净利润增长率(时序均值)',
                             '主营业务增长率(时序均值)','净资产收益率(时序中位数)','股息率(时序中位数)',
                             '净利润增长率(时序中位数)', '主营业务增长率(时序中位数)']] = temp_ind_detail[['行业龙头占比(时序均值)', '行业龙头占比(时序中位数)',
                             '净资产收益率(时序均值)','股息率(时序均值)','净利润增长率(时序均值)',
                             '主营业务增长率(时序均值)','净资产收益率(时序中位数)','股息率(时序中位数)',
                             '净利润增长率(时序中位数)', '主营业务增长率(时序中位数)']] / 100

            temp_ind_detail=pd.merge(temp_ind_detail,industry_financial_info,
                                     how='left',left_on='行业名称',right_on='industry_name')

            temp_ind_detail=temp_ind_detail[['行业名称', '占持仓比例(时序均值)',
           '占持仓比例(时序均值)排名',
            '综合价值属性(时序均值)排名','综合成长属性(时序均值)排名',
            '行业龙头占比(时序均值)', '行业龙头占比(时序均值)排名',
           '主营业务增长率(时序均值)','主营业务增长率(时序均值)排名','行业主营业务增长率(时序均值)',
            '净利润增长率(时序均值)','净利润增长率(时序均值)排名','行业净利润增长率(时序均值)',
           '净资产收益率(时序均值)','净资产收益率(时序均值)排名','行业净资产收益率(时序均值)',
           '每股净资产与价格比率(时序均值)', '每股净资产与价格比率(时序均值)排名','行业每股净资产与价格比率(时序均值)',
          '每股收益与价格比率(时序均值)', '每股收益与价格比率(时序均值)排名','行业每股收益比股价(时序均值)',
           '经营现金流与价格比率(时序均值)','经营现金流与价格比率(时序均值)排名','行业经营现金流与价格比率(时序均值)',
           '股息率(时序均值)', '股息率(时序均值)排名','行业股息率(时序均值)',
            'PE(时序均值)', 'PE(时序均值)排名','行业PE(时序均值)',
            'PB(时序均值)', 'PB(时序均值)排名','行业PB(时序均值)',
            'PEG(时序均值)', 'PEG(时序均值)排名','行业PEG(时序均值)',
     '总市值(时序均值)','总市值(时序均值)排名', '行业平均市值(时序均值)','25分位数市值(时序均值)','50分位数市值(时序均值)', '75分位数市值(时序均值)',
                                             '90分位数市值(时序均值)','asofdate',
                                             '占持仓比例(时序中位数)', '占持仓比例(时序中位数)排名','综合价值属性(时序中位数)排名',
                                             '综合成长属性(时序中位数)排名','行业龙头占比(时序中位数)', '行业龙头占比(时序中位数)排名',
                                             '主营业务增长率(时序中位数)', '主营业务增长率(时序中位数)排名',
                                             '净利润增长率(时序中位数)', '净利润增长率(时序中位数)排名','行业净利润增长率(时序中位数)',
                                             '净资产收益率(时序中位数)', '净资产收益率(时序中位数)排名','行业净资产收益率(时序中位数)',
                                             '每股净资产与价格比率(时序中位数)', '每股净资产与价格比率(时序中位数)排名','行业每股净资产与价格比率(时序中位数)',
                                             '每股收益与价格比率(时序中位数)','每股收益与价格比率(时序中位数)排名','行业每股收益比股价(时序中位数)',
                                             '经营现金流与价格比率(时序中位数)', '经营现金流与价格比率(时序中位数)排名','行业经营现金流与价格比率(时序中位数)',
                                             '股息率(时序中位数)', '股息率(时序中位数)排名','行业股息率(时序中位数)',
                                             'PE(时序中位数)','PE(时序中位数)排名','行业PE(时序中位数)',
                                             'PB(时序中位数)','PB(时序中位数)排名','行业PB(时序中位数)',
                                             'PEG(时序中位数)','PEG(时序中位数)排名','行业PEG(时序中位数)',
                                             '总市值(时序中位数)', '总市值(时序中位数)排名',
                                             '行业平均市值(时序中位数)', '25分位数市值(时序中位数)', '50分位数市值(时序中位数)', '75分位数市值(时序中位数)',
                                             '90分位数市值(时序中位数)'
                                             ]]

            ind_detial_float_col=temp_ind_detail.columns.tolist()
            ind_detial_float_col.sort()
            for col in ['总市值(时序中位数)','总市值(时序中位数)排名',
     '总市值(时序均值)','总市值(时序均值)排名', '行业平均市值(时序中位数)','25分位数市值(时序中位数)',
                        '50分位数市值(时序中位数)', '75分位数市值(时序中位数)', '90分位数市值(时序中位数)','行业平均市值(时序均值)','25分位数市值(时序均值)',
                        '50分位数市值(时序均值)', '75分位数市值(时序均值)', '90分位数市值(时序均值)','asofdate','行业名称',
                        'PE(时序中位数)','PE(时序均值)','PEG(时序中位数)','PEG(时序均值)',
                        'PB(时序中位数)','PB(时序均值)','行业PE(时序中位数)','行业PB(时序中位数)','行业PEG(时序中位数)','行业PE(时序均值)','行业PB(时序均值)','行业PEG(时序均值)']:
                ind_detial_float_col.remove(col)
            if(i==0):
                theme_weight=temp_ind_detail[['行业名称', '占持仓比例(时序均值)']]
            if(if_percentage):
                for col in ind_detial_float_col:
                    temp_ind_detail[col]=temp_ind_detail[col].map("{:.2%}".format)
            industry_detail_df_list.append(temp_ind_detail )


        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_industry_shift_property_new",con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_industry_shift_property_new where jjdm='{0}' and asofdate='{1}' "\
            .format(jjdm,latest_date)
        industry_sp=pd.read_sql(sql,con=localdb).set_index('项目名').fillna(0)
        ind_sp_float_col_list=industry_sp.columns.tolist()
        ind_sp_float_col_list.remove('jjdm')
        ind_sp_float_col_list.remove('asofdate')


        #generate the label:
        if(industry_p['一级行业集中度'][0]>th1 and industry_p['一级行业换手率'][0]>th2):
            industry_p['一级行业类型']='博弈'
        elif(industry_p['一级行业集中度'][0]>th1 and industry_p['一级行业换手率'][0]<th2):
            industry_p['一级行业类型'] = '专注'
        elif(industry_p['一级行业集中度'][0]<th1 and industry_p['一级行业换手率'][0]>th2):
            industry_p['一级行业类型'] = '轮动'
        elif(industry_p['一级行业集中度'][0]<th1 and industry_p['一级行业换手率'][0]<th2):
            industry_p['一级行业类型'] = '配置'


        if(industry_p['二级行业集中度'][0]>th1 and industry_p['二级行业换手率'][0]>th2):
            industry_p['二级行业类型']='博弈'
        elif(industry_p['二级行业集中度'][0]>th1 and industry_p['二级行业换手率'][0]<th2):
            industry_p['二级行业类型'] = '专注'
        elif(industry_p['二级行业集中度'][0]<th1 and industry_p['二级行业换手率'][0]>th2):
            industry_p['二级行业类型'] = '轮动'
        elif(industry_p['二级行业集中度'][0]<th1 and industry_p['二级行业换手率'][0]<th2):
            industry_p['二级行业类型'] = '配置'

        if(industry_p['三级行业集中度'][0]>th1 and industry_p['三级行业换手率'][0]>th2):
            industry_p['三级行业类型']='博弈'
        elif(industry_p['三级行业集中度'][0]>th1 and industry_p['三级行业换手率'][0]<th2):
            industry_p['三级行业类型'] = '专注'
        elif(industry_p['三级行业集中度'][0]<th1 and industry_p['三级行业换手率'][0]>th2):
            industry_p['三级行业类型'] = '轮动'
        elif(industry_p['三级行业集中度'][0]<th1 and industry_p['三级行业换手率'][0]<th2):
            industry_p['三级行业类型'] = '配置'

        if (industry_p['主题集中度'][0] > th1 and industry_p['主题换手率'][0] > th2):
            industry_p['主题类型'] = '博弈'
        elif (industry_p['主题集中度'][0] > th1 and industry_p['主题换手率'][0] < th2):
            industry_p['主题类型'] = '专注'
        elif (industry_p['主题集中度'][0] < th1 and industry_p['主题换手率'][0] > th2):
            industry_p['主题类型'] = '轮动'
        elif (industry_p['主题集中度'][0] < th1 and industry_p['主题换手率'][0] < th2):
            industry_p['主题类型'] = '配置'
        if(if_percentage):
            for col in float_col_list:
                industry_p[col]=industry_p[col].map("{:.2%}".format)
            for col in ind_sp_float_col_list[0:int(len(ind_sp_float_col_list)/2)]:
                industry_sp.loc[industry_sp.index!='切换次数',col]=\
                    industry_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
            for col in ind_sp_float_col_list[int(len(ind_sp_float_col_list)/2):]:
                industry_sp[col]=\
                    industry_sp[col].astype(float).map("{:.2%}".format)

        industry_p['基金简称']=[jjjc]
        # industry_p_old['基金简称']=[jjjc]

        #theme picture
        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from hbs_theme_shift_property_new", con=localdb)['asofdate'][0]

        sql = "SELECT * from hbs_theme_shift_property_new where jjdm='{0}' and asofdate='{1}' " \
            .format(jjdm, latest_date)
        theme_sp = pd.read_sql(sql, con=localdb).set_index('项目名').fillna(0)

        theme_sp_float_col_list = theme_sp.columns.tolist()
        theme_sp_float_col_list.remove('jjdm')
        theme_sp_float_col_list.remove('asofdate')

        if (if_percentage):
            for col in theme_sp_float_col_list[0:int(len(theme_sp_float_col_list) / 2)]:
                theme_sp.loc[theme_sp.index != '切换次数', col] = \
                    theme_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
            for col in theme_sp_float_col_list[int(len(theme_sp_float_col_list) / 2):]:
                theme_sp[col] = \
                    theme_sp[col].astype(float).map("{:.2%}".format)

        theme_weight=pd.merge(theme_weight,ia.ind2thememap,
                              how='left',left_on='行业名称',right_on='industry_name').drop('industry_name',axis=1)
        theme_weight=theme_weight.groupby('theme').sum().T.reset_index(drop=True)
        for col in theme_weight.columns:
            theme_weight[col] = \
                theme_weight[col].astype(float).map("{:.2%}".format)

        industry_p=pd.concat([industry_p,theme_weight],axis=1)
        theme_p=industry_p[['jjdm','基金简称','主题类型','主题集中度', '主题换手率','大金融', '消费', 'TMT',
           '周期', '制造', 'asofdate']]
        theme_sp = theme_sp[['Total_rank',
                             '大金融_rank', '消费_rank', 'TMT_rank', '周期_rank', '制造_rank',
                             'Total', '大金融', '消费', 'TMT', '周期', '制造', 'asofdate']]
        theme_sp.reset_index(inplace=True)


        industry_p=industry_p[['jjdm','基金简称','一级行业类型','一级行业集中度', '一级行业换手率','前五大行业','龙头占比(时序均值)',
           '龙头占比(时序中位数)', '龙头占比(时序均值)排名', '龙头占比(时序中位数)排名','二级行业类型','二级行业集中度', '二级行业换手率',
                               '三级行业类型','三级行业集中度', '三级行业换手率','asofdate']]

        industry_sp=industry_sp[['Total_rank', '农林牧渔_rank',
           '基础化工_rank', '钢铁_rank', '有色金属_rank', '电子_rank', '家用电器_rank',
           '食品饮料_rank', '纺织服饰_rank', '轻工制造_rank', '医药生物_rank', '公用事业_rank',
           '交通运输_rank', '房地产_rank', '商贸零售_rank', '社会服务_rank', '综合_rank',
           '建筑材料_rank', '建筑装饰_rank', '电力设备_rank', '国防军工_rank', '计算机_rank',
           '传媒_rank', '通信_rank', '银行_rank', '非银金融_rank', '汽车_rank', '机械设备_rank',
           '煤炭_rank', '石油石化_rank', '环保_rank', '美容护理_rank','Total', '农林牧渔', '基础化工', '钢铁', '有色金属', '电子', '家用电器', '食品饮料', '纺织服饰',
           '轻工制造', '医药生物', '公用事业', '交通运输', '房地产', '商贸零售', '社会服务', '综合', '建筑材料',
           '建筑装饰', '电力设备', '国防军工', '计算机', '传媒', '通信', '银行', '非银金融', '汽车', '机械设备',
           '煤炭', '石油石化', '环保', '美容护理','asofdate']]
        industry_sp.reset_index(inplace=True)

        return industry_p,industry_sp,theme_p,theme_sp,industry_detail_df_list

    @staticmethod
    def style_pic(jjdm,jjjc,fre,th1=0.5,th2=0.5,if_percentage=True):

        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from nav_style_property_value where fre='{0}'"
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from nav_style_property_value where jjdm='{0}' and fre='{1}' and asofdate='{2}' "\
            .format(jjdm,fre,latest_date)
        value_p=pd.read_sql(sql,con=localdb).rename(columns={'shift_ratio_rank':'换手率排名',
                                                             'centralization_rank':'集中度排名',
                                                             '成长_mean':'成长暴露排名',
                                                             '价值_mean':'价值暴露排名',
                                                             '成长_abs_mean': '成长绝对暴露',
                                                             '价值_abs_mean': '价值绝对暴露',
                                                             'manager_change':'经理是否未变更',
                                                             'shift_ratio':'换手率',
                                                             'centralization':'集中度',
                                                             'fre':'回归周期',
                                                             })


        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_style_property "
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_style_property where jjdm='{0}' and asofdate='{1}' "\
            .format(jjdm,latest_date)
        value_p_hbs=pd.read_sql(sql,con=localdb).rename(columns={'cen_lv':'集中度(持仓)',
                                                                 'shift_lv':'换手率(持仓)',
                                                                 '成长':'成长绝对暴露(持仓)',
                                                                 '价值':'价值绝对暴露(持仓)',
                                                                 'cen_lv_rank':'集中度排名(持仓)',
                                                                 'shift_lv_rank':'换手率排名(持仓)',
                                                                 '成长_rank':'成长暴露排名(持仓)',
                                                                 '价值_rank':'价值暴露排名(持仓)',})


        # generate the label for nav based :
        winning_value=value_p[['成长暴露排名','价值暴露排名']].T[value_p[['成长暴露排名','价值暴露排名']].T[0]
                                                     ==value_p[['成长暴露排名','价值暴露排名']].T.max()[0]].index[0]
        if(value_p['集中度排名'][0]>th1 and value_p['换手率排名'][0]>th2 ):
            value_p['风格类型']='博弈'
            value_p['风格偏好']=winning_value[0:2]
        elif(value_p['集中度排名'][0]>th1 and value_p['换手率排名'][0]<th2 ):
            value_p['风格类型'] = '专注'
            value_p['风格偏好'] = winning_value[0:2]
        elif(value_p['集中度排名'][0]<th1 and value_p['换手率排名'][0]>th2 ):
            value_p['风格类型'] = '轮动'
            value_p['风格偏好'] = '均衡'
        elif(value_p['集中度排名'][0]<th1 and value_p['换手率排名'][0]<th2 ):
            value_p['风格类型'] = '配置'
            value_p['风格偏好'] =  '均衡'

        value_p['基金简称']=jjjc
        value_p=value_p[['jjdm','基金简称','风格类型','风格偏好','换手率排名','集中度排名',
                         '成长暴露排名', '价值暴露排名','成长绝对暴露','价值绝对暴露' ,'经理是否未变更',
                         '换手率', '集中度','回归周期','asofdate']]

        # generate the label for hbs based :
        winning_value=value_p_hbs[['成长暴露排名(持仓)','价值暴露排名(持仓)']].T[value_p_hbs[['成长暴露排名(持仓)','价值暴露排名(持仓)']].T[0]
                                                     ==value_p_hbs[['成长暴露排名(持仓)','价值暴露排名(持仓)']].T.max()[0]].index[0]
        if(value_p_hbs['集中度排名(持仓)'][0]>th1 and value_p_hbs['换手率排名(持仓)'][0]>th2 ):
            value_p_hbs['风格类型']='博弈'
            value_p_hbs['风格偏好']=winning_value[0:2]
        elif(value_p_hbs['集中度排名(持仓)'][0]>th1 and value_p_hbs['换手率排名(持仓)'][0]<th2 ):
            value_p_hbs['风格类型'] = '专注'
            value_p_hbs['风格偏好'] = winning_value[0:2]
        elif(value_p_hbs['集中度排名(持仓)'][0]<th1 and value_p_hbs['换手率排名(持仓)'][0]>th2 ):
            value_p_hbs['风格类型'] = '轮动'
            value_p_hbs['风格偏好'] = '均衡'
        elif(value_p_hbs['集中度排名(持仓)'][0]<th1 and value_p_hbs['换手率排名(持仓)'][0]<th2 ):
            value_p_hbs['风格类型'] = '配置'
            value_p_hbs['风格偏好'] =  '均衡'

        value_p_hbs['基金简称']=jjjc
        value_p_hbs=value_p_hbs[['jjdm','基金简称','风格类型','风格偏好','集中度(持仓)', '换手率(持仓)',
                                 '成长绝对暴露(持仓)', '价值绝对暴露(持仓)', '集中度排名(持仓)',
           '换手率排名(持仓)', '成长暴露排名(持仓)', '价值暴露排名(持仓)', 'asofdate']]

        if(if_percentage):
            for col in ['集中度(持仓)', '换手率(持仓)', '成长绝对暴露(持仓)', '价值绝对暴露(持仓)', '集中度排名(持仓)',
               '换手率排名(持仓)', '成长暴露排名(持仓)', '价值暴露排名(持仓)']:
                value_p_hbs[col]=value_p_hbs[col].map("{:.2%}".format)

        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from nav_style_property_size where fre='{0}'"
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from nav_style_property_size where jjdm='{0}' and fre='{1}' and asofdate='{2}' "\
            .format(jjdm,fre,latest_date)
        size_p=pd.read_sql(sql,con=localdb).rename(columns={'shift_ratio_rank':'换手率排名',
                                                             'centralization_rank':'集中度排名',
                                                             '大盘_mean':'大盘暴露排名',
                                                             '中盘_mean':'中盘暴露排名',
                                                            '小盘_mean':'小盘暴露排名',
                                                            '大盘_abs_mean': '大盘绝对暴露',
                                                            '中盘_abs_mean': '中盘绝对暴露',
                                                            '小盘_abs_mean': '小盘绝对暴露',
                                                             'manager_change':'经理是否未变更',
                                                             'shift_ratio':'换手率',
                                                             'centralization':'集中度',
                                                             'fre':'回归周期',
                                                             })

        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_size_property "
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_size_property where jjdm='{0}' and asofdate='{1}' "\
            .format(jjdm,latest_date)
        size_p_hbs=pd.read_sql(sql,con=localdb).rename(columns={'cen_lv':'集中度(持仓)',
                                                                 'shift_lv':'换手率(持仓)',
                                                                 '大盘':'大盘绝对暴露(持仓)',
                                                                 '中盘':'中盘绝对暴露(持仓)',
                                                                 '小盘': '小盘绝对暴露(持仓)',
                                                                 'cen_lv_rank':'集中度排名(持仓)',
                                                                 'shift_lv_rank':'换手率排名(持仓)',
                                                                 '大盘_rank':'大盘暴露排名(持仓)',
                                                                 '中盘_rank':'中盘暴露排名(持仓)',
                                                                 '小盘_rank': '小盘暴露排名(持仓)',
                                                                })



        # generate the label for nav based :
        winning_size=[x[0] for x in size_p[['大盘暴露排名','中盘暴露排名','小盘暴露排名']].T[size_p[['大盘暴露排名','中盘暴露排名','小盘暴露排名']].T[0]>0.5].index.tolist()]
        winning_size=''.join(winning_size)

        if(size_p['集中度排名'][0]>th1 and size_p['换手率排名'][0]>th2 ):
            size_p['规模风格类型']='博弈'
            size_p['规模偏好']=winning_size
        elif(size_p['集中度排名'][0]>th1 and size_p['换手率排名'][0]<th2 ):
            size_p['规模风格类型'] = '专注'
            size_p['规模偏好'] = winning_size
        elif(size_p['集中度排名'][0]<th1 and size_p['换手率排名'][0]>th2 ):
            size_p['规模风格类型'] = '轮动'
            size_p['规模偏好'] = '均衡'
        elif(size_p['集中度排名'][0]<th1 and size_p['换手率排名'][0]<th2 ):
            size_p['规模风格类型'] = '配置'
            size_p['规模偏好'] ='均衡'

        size_p['基金简称']=jjjc
        size_p=size_p[['jjdm','基金简称','规模风格类型','规模偏好','换手率排名','集中度排名','大盘暴露排名',
                       '大盘绝对暴露','中盘暴露排名','中盘绝对暴露','小盘暴露排名','小盘绝对暴露', '经理是否未变更',
                         '换手率', '集中度','回归周期','asofdate']]

        # generate the label for hbs based :
        winning_size=[x[0] for x in size_p_hbs[['大盘暴露排名(持仓)','中盘暴露排名(持仓)','小盘暴露排名(持仓)']].T[size_p_hbs[['大盘暴露排名(持仓)','中盘暴露排名(持仓)','小盘暴露排名(持仓)']].T[0]>0.5].index.tolist()]
        winning_size=''.join(winning_size)

        if(size_p_hbs['集中度排名(持仓)'][0]>th1 and size_p_hbs['换手率排名(持仓)'][0]>th2 ):
            size_p_hbs['规模风格类型']='博弈'
            size_p_hbs['规模偏好']=winning_size
        elif(size_p_hbs['集中度排名(持仓)'][0]>th1 and size_p_hbs['换手率排名(持仓)'][0]<th2 ):
            size_p_hbs['规模风格类型'] = '专注'
            size_p_hbs['规模偏好'] = winning_size
        elif(size_p_hbs['集中度排名(持仓)'][0]<th1 and size_p_hbs['换手率排名(持仓)'][0]>th2 ):
            size_p_hbs['规模风格类型'] = '轮动'
            size_p_hbs['规模偏好'] = '均衡'
        elif(size_p_hbs['集中度排名(持仓)'][0]<th1 and size_p_hbs['换手率排名(持仓)'][0]<th2 ):
            size_p_hbs['规模风格类型'] = '配置'
            size_p_hbs['规模偏好'] ='均衡'

        size_p_hbs['基金简称']=jjjc
        size_p_hbs=size_p_hbs[['jjdm','基金简称','规模风格类型','规模偏好','集中度(持仓)', '换手率(持仓)', '大盘绝对暴露(持仓)', '中盘绝对暴露(持仓)', '小盘绝对暴露(持仓)',
           '集中度排名(持仓)', '换手率排名(持仓)', '大盘暴露排名(持仓)', '中盘暴露排名(持仓)', '小盘暴露排名(持仓)',
        'asofdate']]
        if (if_percentage):
            for col in ['集中度(持仓)', '换手率(持仓)', '大盘绝对暴露(持仓)', '中盘绝对暴露(持仓)', '小盘绝对暴露(持仓)',
               '集中度排名(持仓)', '换手率排名(持仓)', '大盘暴露排名(持仓)', '中盘暴露排名(持仓)', '小盘暴露排名(持仓)']:
                size_p_hbs[col]=size_p_hbs[col].map("{:.2%}".format)

        #shift property for nav based
        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from nav_shift_property_value where fre='{0}'"
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from nav_shift_property_value where jjdm='{0}' and asofdate='{1}' and fre='{2}' "\
            .format(jjdm,latest_date,fre)
        value_sp=pd.read_sql(sql,con=localdb).set_index('项目名').fillna(0)
        value_sp_float_col_list=value_sp.columns.tolist()
        value_sp_float_col_list.remove('jjdm')
        value_sp_float_col_list.remove('asofdate')
        value_sp_float_col_list.remove('fre')


        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from nav_shift_property_size where fre='{0}'"
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from nav_shift_property_size where jjdm='{0}' and asofdate='{1}' and fre='{2}' "\
            .format(jjdm,latest_date,fre)
        size_sp=pd.read_sql(sql,con=localdb).set_index('项目名').fillna(0)
        size_sp_float_col_list=size_sp.columns.tolist()
        size_sp_float_col_list.remove('jjdm')
        size_sp_float_col_list.remove('asofdate')
        size_sp_float_col_list.remove('fre')



        # shift property for hbs based
        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_shift_property_value"
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_shift_property_value where jjdm='{0}' and asofdate='{1}'  "\
            .format(jjdm,latest_date)
        value_sp_hbs=pd.read_sql(sql,con=localdb).set_index('项目名').fillna(0)
        value_sp_hbs_float_col_list=value_sp_hbs.columns.tolist()
        value_sp_hbs_float_col_list.remove('jjdm')
        value_sp_hbs_float_col_list.remove('asofdate')


        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_shift_property_size "
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_shift_property_size where jjdm='{0}' and asofdate='{1}' "\
            .format(jjdm,latest_date)
        size_sp_hbs=pd.read_sql(sql,con=localdb).set_index('项目名').fillna(0)
        size_sp_hbs_float_col_list=size_sp_hbs.columns.tolist()
        size_sp_hbs_float_col_list.remove('jjdm')
        size_sp_hbs_float_col_list.remove('asofdate')

        if (if_percentage):
            for col in ['换手率排名', '集中度排名', '成长暴露排名', '价值暴露排名',
                               '换手率', '集中度', ]:
                value_p[col]=value_p[col].map("{:.2%}".format)

            for col in ['换手率排名', '集中度排名', '大盘暴露排名', '中盘暴露排名','小盘暴露排名',
                               '换手率', '集中度', ]:
                size_p[col]=size_p[col].map("{:.2%}".format)


            for col in ['Total', '成长', '价值']:
                value_sp.loc[value_sp.index!='切换次数',col]=\
                    value_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
                value_sp_hbs.loc[value_sp_hbs.index!='切换次数',col]=\
                    value_sp_hbs.iloc[1:][col].astype(float).map("{:.2%}".format)
            for col in ['Total_rank', '成长_rank', '价值_rank']:
                value_sp[col]=\
                    value_sp[col].astype(float).map("{:.2%}".format)
                value_sp_hbs[col]=\
                    value_sp_hbs[col].astype(float).map("{:.2%}".format)

            for col in ['Total', '大盘', '中盘', '小盘']:
                size_sp.loc[size_sp.index!='切换次数',col]=\
                    size_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
                size_sp_hbs.loc[size_sp_hbs.index!='切换次数',col]=\
                    size_sp_hbs.iloc[1:][col].astype(float).map("{:.2%}".format)
            for col in ['Total_rank', '大盘_rank', '中盘_rank', '小盘_rank']:
                size_sp[col]=\
                    size_sp[col].astype(float).map("{:.2%}".format)
                size_sp_hbs[col]=\
                    size_sp_hbs[col].astype(float).map("{:.2%}".format)


        value_sp=value_sp[['Total_rank', '成长_rank', '价值_rank',
                           'Total', '成长', '价值','fre','asofdate']]
        value_sp_hbs=value_sp_hbs[['Total_rank', '成长_rank', '价值_rank',
                           'Total', '成长', '价值','asofdate']]
        size_sp = size_sp[['Total_rank','大盘_rank', '中盘_rank',
           '小盘_rank','Total', '大盘', '中盘', '小盘','fre','asofdate']]
        size_sp_hbs = size_sp_hbs[['Total_rank', '大盘_rank', '中盘_rank',
                           '小盘_rank', 'Total', '大盘', '中盘', '小盘', 'asofdate']]

        value_sp.reset_index(inplace=True)
        size_sp.reset_index(inplace=True)
        value_sp_hbs.reset_index(inplace=True)
        size_sp_hbs.reset_index(inplace=True)


        return  value_p,value_p_hbs,value_sp,value_sp_hbs, size_p,size_p_hbs,size_sp,size_sp_hbs

    @staticmethod
    def stock_trading_pci(jjdm,jjjc,ind_cen,th1=0.75,th2=0.25,th3=0.5,th4=0.5,th5=0.75,th6=0.5,if_percentage=True):

        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_holding_property "
            ,con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_holding_property where jjdm='{0}' and asofdate='{1}' "\
            .format(jjdm,latest_date)
        stock_p=pd.read_sql(sql,con=localdb)

        float_col=stock_p.columns.tolist()
        float_col.remove('jjdm')
        float_col.remove('asofdate')
        float_col.remove('持股数量')
        float_col.remove('PE')
        float_col.remove('PB')
        float_col.remove('ROE')
        float_col.remove('股息率')
        float_col.remove('PE_中位数')
        float_col.remove('PB_中位数')
        float_col.remove('ROE_中位数')
        float_col.remove('股息率_中位数')


        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_stock_trading_property "
            ,con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_stock_trading_property where jjdm='{0}' and asofdate='{1}' "\
            .format(jjdm,latest_date)
        stock_tp=pd.read_sql(sql,con=localdb)

        tp_float_col=stock_tp.columns.tolist()
        tp_float_col.remove('jjdm')
        tp_float_col.remove('平均持有时间(出重仓前)')
        tp_float_col.remove('平均持有时间(出持仓前)')
        tp_float_col.remove('asofdate')


        #generate the labels

        if(stock_p['个股集中度'][0]>th1 and stock_tp['平均持有时间(出持仓前)_rank'][0]>th1 ):
            stock_p['个股风格A']='专注'
        elif(stock_p['个股集中度'][0]>th1 and stock_tp['平均持有时间(出持仓前)_rank'][0]<th2 ):
            stock_p['个股风格A'] = '博弈'
        elif(stock_p['个股集中度'][0]<th2 and stock_tp['平均持有时间(出持仓前)_rank'][0]>th1 ):
            stock_p['个股风格A'] = '配置'
        elif(stock_p['个股集中度'][0]<th2 and stock_tp['平均持有时间(出持仓前)_rank'][0]<th2 ):
            stock_p['个股风格A'] = '轮动'
        else:
            stock_p['个股风格A'] = '无'


        if(stock_p['个股集中度'][0]>th1 and ind_cen<th6 ):
            stock_p['个股风格B']='自下而上'
        elif(stock_p['个股集中度'][0]<th6 and ind_cen>th1 ):
            stock_p['个股风格B'] = '自上而下'

        else:
            stock_p['个股风格B'] = '无'

        if(stock_p['个股集中度'][0]>th1 and stock_p['个股集中度'][0]-stock_p['hhi'][0]>0.05):
            stock_p['是否有尾仓(针对高个股集中基金)']='有尾仓'
        else:
            stock_p['是否有尾仓(针对高个股集中基金)'] = '无尾仓'

        if(stock_tp['左侧概率(出持仓前,半年线)_rank'][0]>th3 and stock_tp['左侧程度(出持仓前,半年线)'][0]>th4):
            stock_tp['左侧标签']='深度左侧'
        elif(stock_tp['左侧概率(出持仓前,半年线)_rank'][0]>th3 and stock_tp['左侧程度(出持仓前,半年线)'][0]<th4):
            stock_tp['左侧标签'] = '左侧'
        else:
            stock_tp['左侧标签'] = '无'

        lable=''
        if(stock_tp['新股概率(出持仓前)_rank'][0]>th5):
            lable+='偏好新股'
        if( stock_tp['次新股概率(出持仓前)_rank'][0]>th5):
            lable+='偏好次新股'
        stock_tp['新股次新股偏好']=lable

        if(if_percentage):
            for col in float_col:
                stock_p[col]= stock_p[col].map("{:.2%}".format)
            for col in tp_float_col:
                stock_tp[col] = stock_tp[col].map("{:.2%}".format)



        stock_p['基金简称'] = jjjc
        stock_tp['基金简称'] = jjjc

        stock_p=stock_p[['jjdm','基金简称','个股风格A','个股风格B','是否有尾仓(针对高个股集中基金)','个股集中度', 'hhi','持股数量',
                         '前三大', '前五大', '前十大', '平均仓位', '仓位换手率','PE_rank', 'PB_rank', 'ROE_rank', '股息率_rank', 'PE_中位数_rank',
           'PB_中位数_rank', 'ROE_中位数_rank', '股息率_中位数_rank','PE', 'PB', 'ROE', '股息率',
                         'PE_中位数', 'PB_中位数', 'ROE_中位数', '股息率_中位数','asofdate'
                         ]]
        stock_tp=stock_tp[['jjdm','基金简称','左侧标签', '新股次新股偏好','左侧概率(出重仓前,半年线)_rank', '左侧概率(出持仓前,半年线)_rank',
           '左侧概率(出重仓前,年线)_rank', '左侧概率(出持仓前,年线)_rank',
                           '平均持有时间(出重仓前)_rank', '平均持有时间(出持仓前)_rank','出重仓前平均收益率_rank',
           '出全仓前平均收益率_rank',
                           '新股概率(出重仓前)_rank','新股概率(出持仓前)_rank', '次新股概率(出重仓前)_rank', '次新股概率(出持仓前)_rank','平均持有时间(出重仓前)', '平均持有时间(出持仓前)', '出重仓前平均收益率', '出全仓前平均收益率',
           '左侧概率(出重仓前,半年线)', '左侧概率(出持仓前,半年线)', '左侧概率(出重仓前,年线)', '左侧概率(出持仓前,年线)',
           '左侧程度(出重仓前,半年线)', '左侧程度(出持仓前,半年线)', '左侧程度(出重仓前,年线)', '左侧程度(出持仓前,年线)',
           '新股概率(出重仓前)', '新股概率(出持仓前)', '次新股概率(出重仓前)', '次新股概率(出持仓前)','asofdate'
                           ]]

        return stock_p,stock_tp


    def save_pic_as_excel(self,jjdm_list):

        value_df_list=[pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),
                       pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]

        industry_df_list=[pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]

        stock_df_list=[pd.DataFrame(),pd.DataFrame()]

        for jjdm in jjdm_list:

            jjjc=hbdb.db2df("select jjjc from st_fund.t_st_gm_jjxx where jjdm='{0}'".format(jjdm),db='funduser')['jjjc'][0]

            value_pic=self.style_pic(jjdm,jjjc,fre='M')
            #value_p,value_p_hbs,value_sp,value_sp_hbs, size_p,size_p_hbs,size_sp,size_sp_hbs=style_pic(jjdm,jjjc,fre='M')
            for i in range(8):
                value_pic[i]['jjdm']=jjdm
                value_df_list[i]=pd.concat([value_df_list[i],value_pic[i]],axis=0)

            ind_pic=self.industry_pic(jjdm,jjjc)
            #industry_p,industry_sp,theme_p,theme_sp,industry_detail_df_list=industry_pic(jjdm,jjjc)
            for i in range(4):
                ind_pic[i]['jjdm']=jjdm
                industry_df_list[i] = pd.concat([industry_df_list[i], ind_pic[i]], axis=0)
            for j in range(len(ind_pic[4])):
                ind_pic[4][j]['jjdm']=jjdm
                ind_pic[4][j]['industry_level'] =j+1
                industry_df_list[4]=pd.concat([industry_df_list[4], ind_pic[4][j]], axis=0)

            stock_pic=self.stock_trading_pci(jjdm,jjjc,ind_cen=float(ind_pic[0]['一级行业集中度'][0].split('%')[0])/100)
            for i in range(2):
                stock_df_list[i] = pd.concat([stock_df_list[i], stock_pic[i]], axis=0)
            # stock_p,stock_tp=stock_trading_pci(jjdm,jjjc,ind_cen=float(industry_p['一级行业集中度'][0].split('%')[0])/100)

        writer=pd.ExcelWriter("风格画像.xlsx")
        value_df_list[1].to_excel(writer,sheet_name='成长价值画像_基于持仓',index=False)
        value_df_list[3].to_excel(writer, sheet_name='成长价值切换属性_基于持仓',index=False)
        value_df_list[0].to_excel(writer,sheet_name='成长价值画像_基于净值',index=False)
        value_df_list[2].to_excel(writer, sheet_name='成长价值切换属性_基于净值',index=False)

        value_df_list[5].to_excel(writer,sheet_name='大中小盘画像_基于持仓',index=False)
        value_df_list[7].to_excel(writer, sheet_name='大中小盘切换属性_基于持仓',index=False)
        value_df_list[4].to_excel(writer,sheet_name='大中小盘画像_基于净值',index=False)
        value_df_list[6].to_excel(writer, sheet_name='大中小盘切换属性_基于净值',index=False)
        writer.save()

        writer = pd.ExcelWriter("行业主题画像.xlsx")
        industry_df_list[0].to_excel(writer,sheet_name="行业画像",index=False)
        industry_df_list[1].to_excel(writer, sheet_name="行业切换属性",index=False)
        industry_df_list[2].to_excel(writer,sheet_name="主题画像",index=False)
        industry_df_list[3].to_excel(writer,sheet_name="主题切换属性",index=False)
        industry_df_list[4].to_excel(writer, sheet_name="细分行业画像", index=False)
        writer.save()

        writer = pd.ExcelWriter("个股交易画像.xlsx")
        stock_df_list[0].to_excel(writer,sheet_name='画像A',index=False)
        stock_df_list[1].to_excel(writer,sheet_name='画像B',index=False)
        writer.save()

def get_annotations(asset_allo_series):


        name_map=dict(zip(['NETPROFITGROWRATE_sj',
       'NETPROFITGROWRATE_ticker','PE_sj', 'PE_ticker','PE_FY1_sj','PE_FY1_ticker'],['三级行业净利增速','净利增速',
                                                                                     '三级行业PE','PE','三级行业预期PE','预期PE']))

        asset_allo_series.reset_index(inplace=True)
        x_length=len(asset_allo_series)
        asset_allo_series=asset_allo_series[asset_allo_series['PE_ticker'] != 0]
        annotations=[]
        # index_list = asset_allo_series.T.index.tolist()
        # index_list.reverse()

        for i in range(len(asset_allo_series)):
            asset=asset_allo_series.iloc[i]
            x_position=asset.name/x_length
            y_position=asset['sl']
            text=""
            for col in ['NETPROFITGROWRATE_sj',
       'NETPROFITGROWRATE_ticker']:
                text=text+name_map[col]+": "+str('{:.2%}'.format(asset[col]))+"<br />"
            for col in ['PE_sj', 'PE_ticker','PE_FY1_sj','PE_FY1_ticker']:
                text = text + name_map[col] + ": " + str(round(asset[col],2)) + "<br />"
            #, yanchor='middle'
            #xref='paper',
            #yref = "y1"
            # labeling the left_side of the plot
            # if(max_value>0):
            #     x_index=asset_allo_series[asset].nlargest(1).index[0]
            #     x_position=asset_allo_series.index.tolist().index(x_index)/np.max([(len(asset_allo_series.index)-1),1])
            #     y_position=(asset_allo_series.T.loc[index_list]*100).loc[asset:][x_index].sum()-(asset_allo_series.T*100).loc[asset][x_index]+(asset_allo_series.T*100).loc[asset][x_index]/2
            #     if(x_position==0):
            #         xanchor='left'
            #     elif(x_position==1):
            #         xanchor='right'
            #     else:
            #         xanchor='center'
            annotations.append(dict(xref='paper',yref = "y2",x=x_position, y=y_position,
                                    xanchor='center',yanchor='bottom',
                                    text=text,
                                    font=dict(family='Arial',
                                              size=12),
                                    showarrow=False))


        return annotations

def get_pic_from_localdb(jjdm,asofdate='20211231',if_percentage=True,show_num=None):

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_value_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_value_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    value_p=pd.read_sql(sql,con=localdb)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_value_p_hbs where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_value_p_hbs where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    value_p_hbs=pd.read_sql(sql,con=localdb)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_value_sp where type='nav_based' and asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_value_sp where {0} and asofdate='{1}' and type='nav_based' "\
        .format(jjdm,latest_date)
    value_sp=pd.read_sql(sql,con=localdb).drop('type',axis=1)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_value_sp where type='holding_based' and asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_value_sp where {0} and asofdate='{1}' and type='holding_based' "\
        .format(jjdm,latest_date)
    value_sp_hbs=pd.read_sql(sql,con=localdb).drop(['type','fre'],axis=1)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_size_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_size_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    size_p=pd.read_sql(sql,con=localdb)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_size_p_hbs where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_size_p_hbs where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    size_p_hbs=pd.read_sql(sql,con=localdb)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_size_sp where type='nav_based' and asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_size_sp where {0} and asofdate='{1}' and type='nav_based' "\
        .format(jjdm,latest_date)
    size_sp=pd.read_sql(sql,con=localdb)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_size_sp where type='holding_based' and asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_size_sp where {0} and asofdate='{1}' and type='holding_based' "\
        .format(jjdm,latest_date)
    size_sp_hbs=pd.read_sql(sql,con=localdb)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_industry_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_industry_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    industry_p=pd.read_sql(sql,con=localdb)

    float_col_list=industry_p.columns.tolist()
    float_col_list.remove('jjdm')
    float_col_list.remove('asofdate')
    float_col_list.remove('前五大行业')
    float_col_list.remove('二级行业前20大')
    float_col_list.remove('三级行业前20大')
    float_col_list.remove('基金简称')
    float_col_list.remove('一级行业类型')
    float_col_list.remove('二级行业类型')
    float_col_list.remove('三级行业类型')


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_theme_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_theme_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    theme_p=pd.read_sql(sql,con=localdb)


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_industry_sp where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_industry_sp where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    industry_sp=pd.read_sql(sql,con=localdb)
    ind_sp_float_col_list=industry_sp.columns.tolist()
    ind_sp_float_col_list.remove('jjdm')
    ind_sp_float_col_list.remove('asofdate')
    ind_sp_float_col_list.remove('项目名')

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_theme_sp where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_theme_sp where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    theme_sp=pd.read_sql(sql,con=localdb)
    theme_sp_float_col_list = theme_sp.columns.tolist()
    theme_sp_float_col_list.remove('jjdm')
    theme_sp_float_col_list.remove('asofdate')
    theme_sp_float_col_list.remove('项目名')

    latest_date = pd.read_sql(
        "select max(asofdate) as asofdate from hbs_ticker_contribution where asofdate<='{}'".format(asofdate),
        con=localdb)['asofdate'][0]
    sql = "SELECT * from hbs_ticker_contribution where  {0}  and asofdate='{1}' " \
        .format(jjdm, latest_date)
    tempdf = pd.read_sql(sql, con=localdb)[['jjdm','zqdm','CHINAMEABBR','contribution','asofdate']]
    tempdf = pd.merge(tempdf, theme_p[['jjdm', '基金简称']], how='left', on='jjdm')
    ticker_con=[]
    for jj in tempdf['jjdm'].unique():
        ticker_con.append(tempdf[tempdf['jjdm']==jj].reset_index(drop=True))
    ticker_con=pd.concat(ticker_con,axis=1)
    # ticker_con = pd.merge(ticker_con, theme_p[['jjdm', '基金简称']], how='left', on='jjdm')
    ticker_con['jjdm'] = ticker_con['基金简称']
    ticker_con.drop('基金简称', axis=1, inplace=True)

    industry_detail_df_list=[pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]
    industry_contribution_list=[pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]
    industry_contribution_perweight_list=[pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]
    industry_level=['yjxymc','ejxymc','sjxymc']
    for i in range(3):
        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from jjpic_industry_detail_{0}"
                .format(i+1), con=localdb)['asofdate'][0]
        sql = "SELECT * from jjpic_industry_detail_{2} where {0} and asofdate='{1}' " \
            .format(jjdm, latest_date,i+1)
        if(show_num is not None):
            temp_ind_detail=pd.read_sql(sql, con=localdb).sort_values(['jjdm','占持仓比例(时序均值)'],ascending=False)[0:show_num]
        else:
            temp_ind_detail = pd.read_sql(sql, con=localdb)

        if(i==0):

            #calculate the industry value and growth rank
            # industry_rank = temp_ind_detail.drop_duplicates(['行业名称'])
            # industry_rank[[ '行业PB(时序中位数)', '行业PE(时序中位数)']]=1/industry_rank[[ '行业PB(时序中位数)', '行业PE(时序中位数)']]
            # industry_rank[
            #     ['行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)', '行业净资产收益率(时序中位数)',
            #      '行业PB(时序中位数)', '行业PE(时序中位数)',
            #      '行业股息率(时序中位数)']] = industry_rank[['行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)', '行业净资产收益率(时序中位数)',
            #                                          '行业PB(时序中位数)', '行业PE(时序中位数)',
            #                                          '行业股息率(时序中位数)']].rank(method='min') / len(industry_rank)
            # industry_rank['行业综合成长排名'] = industry_rank[['行业净资产收益率(时序中位数)', '行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)']].mean(axis=1)
            # industry_rank['行业综合价值排名'] = industry_rank[['行业PB(时序中位数)','行业PE(时序中位数)','行业股息率(时序中位数)']].mean(axis=1)
            # industry_rank[['行业综合成长排名', '行业综合价值排名']] = industry_rank[['行业综合成长排名', '行业综合价值排名']].rank(method='min') / len(
            #     industry_rank)
            # value_industry = industry_rank[industry_rank['行业综合价值排名'] > industry_rank['行业综合成长排名']][
            #                      ['行业名称', '行业综合成长排名', '行业综合价值排名']].sort_values('行业综合价值排名')[-10:]
            # value_industry['行业类型']='价值'
            # growth_industry = industry_rank[industry_rank['行业综合成长排名'] > industry_rank['行业综合价值排名']][
            #                      ['行业名称', '行业综合成长排名', '行业综合价值排名']].sort_values('行业综合成长排名')[-10:]
            # growth_industry['行业类型'] = '成长'
            # industry_class=pd.concat([value_industry,growth_industry],axis=0)
            #
            # industry_rank=pd.merge(industry_rank[['行业名称']]
            #                        ,industry_class[['行业名称','行业类型']],
            #                        how='left',on='行业名称').fillna('无')
            industry_rank=pd.DataFrame()
            industry_rank['行业名称']=['交通运输', '银行', '公用事业', '钢铁', '石油石化', '家用电器', '建筑装饰', '房地产', '煤炭',
       '非银金融', '轻工制造', '美容护理', '电子', '电力设备', '食品饮料', '有色金属', '建筑材料',
       '基础化工', '国防军工', '医药生物', '环保', '社会服务', '纺织服饰', '商贸零售', '计算机', '通信',
       '农林牧渔', '传媒', '机械设备', '汽车']
            industry_rank['行业类型'] = ['价值', '价值', '价值', '价值', '价值', '价值', '价值', '价值', '价值', '价值', '成长',
       '成长', '成长', '成长', '成长', '成长', '成长', '成长', '成长', '成长', '无', '无',
       '无', '无', '无', '无', '无', '无', '无', '无']

            tempdf=temp_ind_detail
            tempdf=pd.merge(tempdf,industry_rank,how='left',on='行业名称')


            industry_class=tempdf.groupby(['jjdm','行业类型']).sum('占持仓比例(时序均值)')['占持仓比例(时序均值)'].reset_index()


            industry_class['一级行业策略']='无'
            industry_class.loc[(industry_class['占持仓比例(时序均值)'] > 0.45)&
                               (industry_class['行业类型']!="无"), '一级行业策略'] = \
            industry_class.loc[(industry_class['占持仓比例(时序均值)'] > 0.45)&
                               (industry_class['行业类型']!="无")]['行业类型']
            tempdf=pd.merge(tempdf.drop_duplicates('jjdm'),industry_class[industry_class['一级行业策略']!='无'][['jjdm','一级行业策略']],
                            how='left',on='jjdm')
            tempdf.loc[tempdf['一级行业策略'].isnull(),'一级行业策略']='无'
            tempdf=pd.merge(tempdf,industry_class.pivot_table('占持仓比例(时序均值)','jjdm','行业类型')
                            ,how='left',on='jjdm').rename(columns={'价值':'价值行业占比',
                                                                   '成长':'成长行业占比'})


            industry_p=pd.merge(industry_p,tempdf[['jjdm','一级行业策略', '成长行业占比',
       '价值行业占比']],how='left',on='jjdm')

        elif(i==1):

            #calculate the industry value and growth rank for secondary industry
            # industry_rank = temp_ind_detail.drop_duplicates(['行业名称'])
            # industry_rank['一级行业名称'] = [ind_map[x] for x in industry_rank['行业名称']]
            # industry_rank[[ '行业PB(时序中位数)', '行业PE(时序中位数)']]=1/industry_rank[[ '行业PB(时序中位数)', '行业PE(时序中位数)']]
            # industry_rank[['行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)', '行业净资产收益率(时序中位数)',
            #      '行业PB(时序中位数)', '行业PE(时序中位数)',
            #      '行业股息率(时序中位数)']] = industry_rank.groupby('一级行业名称').rank(method='min')[['行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)', '行业净资产收益率(时序中位数)',
            #      '行业PB(时序中位数)', '行业PE(时序中位数)',
            #      '行业股息率(时序中位数)']]
            #
            # industry_rank=pd.merge(industry_rank,
            #                        industry_rank.groupby('一级行业名称').count()['jjdm'].to_frame('count')
            #                        ,how='left',on='一级行业名称')
            # for col in ['行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)', '行业净资产收益率(时序中位数)',
            #      '行业PB(时序中位数)', '行业PE(时序中位数)',
            #      '行业股息率(时序中位数)']:
            #     industry_rank[col]=industry_rank[col]/industry_rank['count']
            #
            # industry_rank['行业综合成长排名'] = industry_rank[['行业净资产收益率(时序中位数)', '行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)']].mean(axis=1)
            # industry_rank['行业综合价值排名'] = industry_rank[['行业PB(时序中位数)','行业PE(时序中位数)','行业股息率(时序中位数)']].mean(axis=1)
            # industry_rank[['行业综合成长排名', '行业综合价值排名']] = industry_rank.groupby('一级行业名称').rank(method='min')[['行业综合成长排名', '行业综合价值排名']]
            # for col in ['行业综合成长排名', '行业综合价值排名']:
            #     industry_rank[col] = industry_rank[col] / industry_rank['count']
            #
            # value_industry=industry_rank[
            #     (industry_rank['行业综合价值排名'] > industry_rank['行业综合成长排名'])
            #     & (industry_rank['行业综合价值排名'] > 0.67)
            #     & (industry_rank['count'] > 1)]
            # value_industry['二级行业类型'] = '价值'
            #
            # growth_industry =industry_rank[
            #     (industry_rank['行业综合价值排名'] < industry_rank['行业综合成长排名'])
            #     & (industry_rank['行业综合成长排名'] > 0.67)
            #     & (industry_rank['count'] > 1)]
            # growth_industry['二级行业类型'] = '成长'
            # industry_class=pd.concat([value_industry,growth_industry],axis=0)
            #
            # industry_rank=pd.merge(industry_rank[['行业名称']]
            #                        ,industry_class[['行业名称','二级行业类型']],
            #                        how='left',on='行业名称').fillna('无')

            industry_rank=pd.DataFrame()
            industry_rank['行业名称']=['IT服务', '一般零售', '专业工程', '专业服务', '专业连锁', '专用设备', '个护用品', '中药'
                , '乘用车', '互联网电商', '休闲食品', '保险', '元件', '光伏设备', '光学光电子', '其他家电', '其他电子', '其他电源设备'
                , '养殖业', '军工电子', '农产品加工', '农化制品', '农商行', '出版', '动物保健', '包装印刷', '化妆品', '化学制品'
                , '化学制药', '化学原料', '化学纤维', '医疗器械', '医疗服务', '医疗美容', '医药商业', '半导体', '厨卫电器', '商用车'
                , '国有大型银行', '地面兵装', '城商行', '基础建设', '塑料', '多元金融', '家居用品', '家电零部件', '小家电', '小金属'
                , '工业金属', '工程咨询服务', '工程机械', '影视院线', '房地产开发', '房地产服务', '房屋建设', '摩托车及其他', '教育'
                , '数字媒体', '文娱用品', '旅游及景区', '旅游零售', '普钢', '服装家纺', '橡胶', '汽车服务', '汽车零部件', '油服工程'
                , '油气开采', '消费电子', '游戏', '炼化及贸易', '照明设备', '燃气', '物流', '特钢', '环保设备', '环境治理', '玻璃玻纤'
                , '生物制品', '电力', '电子化学品', '电机', '电池', '电网设备', '白色家电', '白酒', '种植业', '纺织制造', '股份制银行'
                , '能源金属', '自动化设备', '航天装备', '航空机场', '航空装备', '装修建材', '装修装饰', '计算机设备', '证券', '调味发酵品'
                , '贵金属', '贸易', '轨交设备', '软件开发', '通信设备', '通用设备', '造纸', '酒店餐饮', '金属新材料', '非白酒', '非金属材料'
                , '风电设备', '食品加工', '饮料乳品', '饰品', '饲料', '黑色家电', '冶钢原料', '广告营销', '水泥', '焦炭', '煤炭开采'
                , '电视广播', '综合', '航海装备', '航运港口', '通信服务', '铁路公路']
            industry_rank['二级行业类型'] =['无', '价值', '成长', '成长', '价值', '成长', '价值', '价值', '无', '无', '无'
                , '价值', '价值', '成长', '价值', '价值', '无', '价值', '成长', '成长', '无', '成长', '无', '价值', '价值'
                , '价值', '无', '成长', '无', '无', '价值', '成长', '无', '成长', '价值', '成长', '成长', '价值', '价值', '无'
                , '成长', '价值', '价值', '无', '成长', '无', '成长', '无', '无', '无', '成长', '无', '价值', '成长', '无', '无'
                , '成长', '成长', '无', '价值', '成长', '价值', '无', '无', '成长', '无', '成长', '无', '成长', '无', '价值'
                , '无', '成长', '成长', '成长', '无', '无', '无', '成长', '价值', '无', '无', '无', '无', '价值', '成长', '无'
                , '无', '无', '无', '无', '无', '无', '成长', '无', '无', '无', '成长', '无', '无', '成长', '价值', '无', '无'
                , '无', '价值', '价值', '无', '成长', '无', '价值', '价值', '价值', '无', '成长', '无', '无', '无', '无', '无'
                , '无', '价值', '无', '价值', '成长', '无', '价值']


            tempdf=temp_ind_detail
            tempdf=pd.merge(tempdf,industry_rank,how='left',on='行业名称')

            tempdf['成长综合排名']=tempdf[['主营业务增长率(时序中位数)排名','净利润增长率(时序中位数)排名','净资产收益率(时序中位数)排名']].mean(axis=1)
            tempdf[['PB(时序中位数)排名', 'PE(时序中位数)排名']]=1 - tempdf[['PB(时序中位数)排名', 'PE(时序中位数)排名']]
            tempdf['价值综合排名'] = tempdf[['PB(时序中位数)排名', 'PE(时序中位数)排名','股息率(时序中位数)排名']].mean(axis=1)


            tempdf['成长综合排名']=tempdf['成长综合排名']*tempdf['占持仓比例(时序均值)']
            tempdf['价值综合排名'] = tempdf['价值综合排名'] * tempdf['占持仓比例(时序均值)']

            industry_class=tempdf.groupby(['jjdm','二级行业类型']).sum('占持仓比例(时序均值)')['占持仓比例(时序均值)'].reset_index()

            #old version for calculating the 个股精选策略
            # tempdf['成长超额']=tempdf['成长超额']*tempdf['占持仓比例(时序均值)']
            # tempdf['价值超额'] = tempdf['价值超额'] * tempdf['占持仓比例(时序均值)']
            # # tempdf['行业综合成长排名']=tempdf['行业综合成长排名']*tempdf['占持仓比例(时序均值)']
            # # tempdf['行业综合价值排名'] = tempdf['行业综合价值排名'] * tempdf['占持仓比例(时序均值)']
            # tempdf['综合价值属性(时序均值)排名']=tempdf['综合价值属性(时序均值)排名']*tempdf['占持仓比例(时序均值)']
            # tempdf['综合成长属性(时序均值)排名'] = tempdf['综合成长属性(时序均值)排名'] * tempdf['占持仓比例(时序均值)']
            #
            # tempdf=tempdf.groupby('jjdm').sum()[['占持仓比例(时序均值)',
            #                                      '成长超额','价值超额','综合价值属性(时序均值)排名','综合成长属性(时序均值)排名']]
            # tempdf['成长超额']=tempdf['成长超额']/tempdf['占持仓比例(时序均值)']
            # tempdf['价值超额'] = tempdf['价值超额'] / tempdf['占持仓比例(时序均值)']
            # # tempdf['行业综合成长排名']=tempdf['行业综合成长排名']/tempdf['占持仓比例(时序均值)']
            # # tempdf['行业综合价值排名'] = tempdf['行业综合价值排名'] / tempdf['占持仓比例(时序均值)']
            # tempdf['综合价值属性(时序均值)排名']=tempdf['综合价值属性(时序均值)排名']/tempdf['占持仓比例(时序均值)']
            # tempdf['综合成长属性(时序均值)排名'] = tempdf['综合成长属性(时序均值)排名'] / tempdf['占持仓比例(时序均值)']
            #
            # tempdf['行业精选个股策略']=''
            # tempdf.loc[tempdf['成长超额']>=0.3,'行业精选个股策略']=tempdf.loc[tempdf['成长超额']>=0.3]['行业精选个股策略']+'精选成长,'
            # tempdf.loc[tempdf['成长超额'] <= -0.3, '行业精选个股策略'] = tempdf.loc[tempdf['成长超额'] <= -0.3]['行业精选个股策略'] + '避免成长,'
            # tempdf.loc[tempdf['价值超额']>=0.3,'行业精选个股策略']=tempdf.loc[tempdf['价值超额']>=0.3]['行业精选个股策略']+'精选价值,'
            # tempdf.loc[tempdf['价值超额'] <= -0.3, '行业精选个股策略'] = tempdf.loc[tempdf['价值超额'] <= -0.3]['行业精选个股策略'] + '避免价值,'
            # tempdf.loc[tempdf['行业精选个股策略']=='','行业精选个股策略']='无,'
            # tempdf['行业精选个股策略'] = [x[0:-1] for x in tempdf['行业精选个股策略']]

            #
            # tempvalue=(tempdf[['净资产收益率(时序中位数)', '主营业务增长率(时序中位数)', '净利润增长率(时序中位数)']].values-tempdf[
            #     ['行业净资产收益率(时序中位数)', '行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)']].values) / tempdf[
            #     ['行业净资产收益率(时序中位数)', '行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)']].values
            # tempvalue[tempvalue > 3] = 3
            # tempvalue[tempvalue < -3] = -3
            # tempdf['成长超额']=tempvalue.mean(axis=1)
            #
            # # tempdf[['PB(时序均值)','PE(时序均值)','PCF(时序均值)',
            # #         '行业PB(时序均值)','行业PE(时序均值)','行业PCF(时序均值)']]=1/tempdf[['PB(时序均值)','PE(时序均值)','PCF(时序均值)',
            # #         '行业PB(时序均值)','行业PE(时序均值)','行业PCF(时序均值)']]
            # tempvalue=pd.DataFrame(data= (tempdf[['PB(时序中位数)','PE(时序中位数)','PCF(时序中位数)','股息率(时序中位数)']].values-tempdf[
            #     ['行业PB(时序中位数)','行业PE(时序中位数)','行业PCF(时序中位数)','行业股息率(时序中位数)']].values) / tempdf[
            #     ['行业PB(时序中位数)','行业PE(时序中位数)','行业PCF(时序中位数)','行业股息率(时序中位数)']].values ,columns=['PB(时序中位数)','PE(时序中位数)',
            #                                            'PCF(时序中位数)','股息率(时序均值)'])
            #
            # tempvalue[['PB(时序中位数)','PE(时序中位数)','PCF(时序中位数)']]=-1*tempvalue[['PB(时序中位数)','PE(时序中位数)','PCF(时序中位数)']]
            #
            # tempvalue[tempvalue > 3] = 3
            # tempvalue[tempvalue < -3] = -3
            # tempdf['价值超额']=tempvalue.mean(axis=1)


            tempdf=tempdf.groupby('jjdm').sum()[['成长综合排名','价值综合排名']]
            tempdf['adjust_benchmark'] = tempdf[['成长综合排名', '价值综合排名']].sum(axis=1).values
            tempdf['成长综合排名']=tempdf['成长综合排名']/tempdf['adjust_benchmark']
            tempdf['价值综合排名'] = tempdf['价值综合排名'] / tempdf['adjust_benchmark']
            tempdf['行业精选个股策略']='无'
            tempdf.loc[tempdf['成长综合排名']-tempdf['价值综合排名']>=0.1,
                       '行业精选个股策略']='成长'
            tempdf.loc[tempdf['价值综合排名'] - tempdf['成长综合排名'] >= 0.1,
                       '行业精选个股策略'] = '价值'

            # tempdf['行业精选个股策略']=''
            # tempdf.loc[tempdf['成长超额']>=0.3,'行业精选个股策略']=tempdf.loc[tempdf['成长超额']>=0.3]['行业精选个股策略']+'精选成长,'
            # tempdf.loc[tempdf['成长超额'] <= -0.3, '行业精选个股策略'] = tempdf.loc[tempdf['成长超额'] <= -0.3]['行业精选个股策略'] + '避免成长,'
            # tempdf.loc[tempdf['价值超额']>=0.3,'行业精选个股策略']=tempdf.loc[tempdf['价值超额']>=0.3]['行业精选个股策略']+'精选价值,'
            # tempdf.loc[tempdf['价值超额'] <= -0.3, '行业精选个股策略'] = tempdf.loc[tempdf['价值超额'] <= -0.3]['行业精选个股策略'] + '避免价值,'
            # tempdf.loc[tempdf['行业精选个股策略']=='','行业精选个股策略']='无,'
            # tempdf['行业精选个股策略'] = [x[0:-1] for x in tempdf['行业精选个股策略']]

            industry_class['二级行业策略']='无'
            industry_class.loc[(industry_class['占持仓比例(时序均值)'] > 0.45)&
                               (industry_class['二级行业类型']!="无"), '二级行业策略'] = \
            industry_class.loc[(industry_class['占持仓比例(时序均值)'] > 0.45)&
                               (industry_class['二级行业类型']!="无")]['二级行业类型']
            tempdf=pd.merge(tempdf,industry_class[industry_class['二级行业策略']!='无'][['jjdm','二级行业策略']],
                            how='left',on='jjdm')
            tempdf.loc[tempdf['二级行业策略'].isnull(),'二级行业策略']='无'
            tempdf=pd.merge(tempdf,industry_class.pivot_table('占持仓比例(时序均值)','jjdm','二级行业类型')
                            ,how='left',on='jjdm').rename(columns={'价值':'二级价值行业占比',
                                                                   '成长':'二级成长行业占比'})


            industry_p = pd.merge(industry_p, tempdf[['jjdm', '行业精选个股策略', '二级行业策略', '二级价值行业占比', '二级成长行业占比',
                                                      '成长综合排名', '价值综合排名']],
                                  how='left', on='jjdm')
            industry_p = industry_p[
                ['jjdm', '基金简称', '一级行业类型', '一级行业集中度', '一级行业换手率', '前五大行业', '一级行业策略', '成长行业占比'
                    ,'价值行业占比','二级行业策略', '二级价值行业占比', '二级成长行业占比', '行业精选个股策略',
                 '成长综合排名', '价值综合排名', '龙头占比(时序均值)',
                 '龙头占比(时序中位数)', '龙头占比(时序均值)排名', '龙头占比(时序中位数)排名', '二级行业类型', '二级行业集中度',
                 '二级行业换手率', '三级行业类型', '三级行业集中度', '三级行业换手率',  '二级行业前20大',
                 '三级行业前20大', 'asofdate']]

        ind_detial_float_col = temp_ind_detail.columns.tolist()
        ind_detial_float_col.sort()
        for col in ['总市值(时序中位数)', '总市值(时序中位数)排名',
                    '总市值(时序均值)', '总市值(时序均值)排名', '行业平均市值(时序中位数)', '25分位数市值(时序中位数)',
                    '50分位数市值(时序中位数)', '75分位数市值(时序中位数)', '90分位数市值(时序中位数)', '行业平均市值(时序均值)', '25分位数市值(时序均值)',
                    '50分位数市值(时序均值)', '75分位数市值(时序均值)', '90分位数市值(时序均值)', 'asofdate', '行业名称',
                    'PE(时序中位数)', 'PE(时序均值)', 'PEG(时序中位数)', 'PEG(时序均值)','PCF(时序中位数)', 'PCF(时序均值)','行业PCF(时序均值)',
                    'PB(时序中位数)', 'PB(时序均值)', '行业PE(时序中位数)', '行业PB(时序中位数)', '行业PEG(时序中位数)', '行业PE(时序均值)', '行业PB(时序均值)',
                    '行业PEG(时序均值)','jjdm']:
            ind_detial_float_col.remove(col)

        industry_zjbl=temp_ind_detail.pivot_table('占持仓比例(时序均值)','行业名称','jjdm')
        industry_zjbl.rename(columns=dict(zip(theme_p['jjdm'].tolist()
                                              ,theme_p['基金简称'].tolist())),inplace=True)

        if (if_percentage):
            for col in ind_detial_float_col:
                temp_ind_detail[col] = temp_ind_detail[col].map("{:.2%}".format)
        industry_detail_df_list[i] = temp_ind_detail


        #get the industry contribution
        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from hbs_industry_contribution",
                 con=localdb)['asofdate'][0]
        sql = "SELECT * from hbs_industry_contribution where  {0} and industry_lv='{2}' and asofdate='{1}' " \
            .format(jjdm,latest_date,industry_level[i])
        industry_con=pd.read_sql(sql,con=localdb)
        industry_con=pd.merge(industry_con,theme_p[['jjdm','基金简称']],how='left',on='jjdm')
        industry_con['jjdm']=industry_con['基金简称']
        industry_con.drop('基金简称',axis=1,inplace=True)
        industry_con_temp=industry_con.pivot_table('contribution','industry_name','jjdm')
        for jj in industry_con_temp.columns:

            industry_con_temp=pd.merge(industry_con_temp,
                                       (industry_con[industry_con['jjdm'] == jj][['industry_name', '个股贡献']].set_index('industry_name').rename(columns={'个股贡献': jj + '个股贡献'})).drop_duplicates(),
                                       how='left',on='industry_name')

        industry_contribution_list[i]=industry_con_temp.reset_index()
        industry_contribution_perweight_list[i]=(industry_con_temp.sort_index()[industry_zjbl.columns]/industry_zjbl).reset_index()
    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_stock_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_stock_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    stock_p=pd.read_sql(sql,con=localdb)
    float_col=stock_p.columns.tolist()
    float_col.remove('jjdm')
    float_col.remove('asofdate')
    float_col.remove('持股数量')
    float_col.remove('PE')
    float_col.remove('PB')
    float_col.remove('ROE')
    float_col.remove('股息率')
    float_col.remove('PE_中位数')
    float_col.remove('PB_中位数')
    float_col.remove('ROE_中位数')
    float_col.remove('股息率_中位数')
    float_col.remove('基金简称')
    float_col.remove('个股风格A')
    float_col.remove('个股风格B')
    float_col.remove('是否有尾仓(针对高个股集中基金)')

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_stock_tp where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_stock_tp where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    stock_tp=pd.read_sql(sql,con=localdb)
    tp_float_col=stock_tp.columns.tolist()
    tp_float_col.remove('jjdm')
    tp_float_col.remove('平均持有时间(出重仓前)')
    tp_float_col.remove('平均持有时间(出持仓前)')
    tp_float_col.remove('asofdate')
    tp_float_col.remove('基金简称')
    tp_float_col.remove('左侧标签')
    tp_float_col.remove('新股次新股偏好')

    #update the industry label by ticker shift ratio
    industry_p = pd.merge(industry_p, stock_tp[['jjdm', '换手率_rank']],how='left',on='jjdm')
    industry_p.loc[(industry_p['一级行业类型']=='博弈')
                   &(industry_p['换手率_rank']<0.5),'一级行业类型']='博弈(被动)'
    industry_p.loc[(industry_p['一级行业类型']=='轮动')
                   &(industry_p['换手率_rank']<0.5),'一级行业类型']='轮动(被动)'
    industry_p.drop('换手率_rank',axis=1,inplace=True)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from nav_jj_ret_analysis where  asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from nav_jj_ret_analysis where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    jj_performance=pd.read_sql(sql,con=localdb).fillna(0)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from nav_hurst_index where  asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from nav_hurst_index where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    hurst=pd.read_sql(sql,con=localdb)
    hurst['业绩特征'] = '随机'
    hurst.loc[hurst['H'] <= 0.35,'业绩特征']='趋势反转'
    hurst.loc[hurst['H'] >= 0.65,'业绩特征']='趋势保持'

    jj_performance=pd.merge(jj_performance,hurst[['jjdm','业绩特征']],how='left',on='jjdm')

    jj_performance=jj_performance[['jjdm','业绩预期回归强度', '长期相对业绩表现', '相对业绩稳定性','业绩特征','month_rank_mean', 'month_rank_std', 'quarter_rank_mean',
       'quarter_rank_std', 'hy_rank_mean', 'hy_rank_std', 'yearly_rank_mean',
       'yearly_rank_std', 'ret_regress',
       'sharp_ratio', 'sharp_ratio_rank', 'downwards_ratio',
       'downwards_ratio_rank', 'sortino_ratio', 'sortino_ratio_rank',
       'max_drawback', 'max_drawback_rank', 'calmark_ratio',
       'calmark_ratio_rank', 'treynor_ratio', 'treynor_ratio_rank','moment','moment_rank',
       'asofdate']]
    performance_float_col=jj_performance.columns.tolist()
    performance_float_col.remove('jjdm')
    performance_float_col.remove('业绩预期回归强度')
    performance_float_col.remove('长期相对业绩表现')
    performance_float_col.remove('相对业绩稳定性')
    performance_float_col.remove('asofdate')
    performance_float_col.remove('业绩特征')

    #theme histroy data

    sql="SELECT * from hbs_theme_exp where  jjdm in ({0}) "\
        .format(util.list_sql_condition(value_p['jjdm'].astype(int).astype(str).tolist()))
    theme_exp=pd.read_sql(sql,con=localdb)
    theme_exp['jjdm']=[("000000"+x)[-6:] for x in theme_exp['jjdm']]
    theme_exp=pd.merge(theme_exp,theme_p[['jjdm','基金简称']],how='left',on='jjdm').drop('jjdm',axis=1)

    #get the secondary industry exp

    sql="SELECT jjdm,jsrq,ejxymc,zjbl from hbs_industry_class2_exp where  jjdm in ({0})"\
        .format(util.list_sql_condition(value_p['jjdm'].astype(str).tolist()))
    ind2_exp=pd.read_sql(sql,con=localdb)
    #remove the Ⅱ in the ejxymc
    ind2_exp['ejxymc']=[x.replace('Ⅱ','') for x in ind2_exp['ejxymc']]
    ind2_exp['jjdm']=[("000000"+x)[-6:] for x in ind2_exp['jjdm']]
    ind2_exp=pd.merge(ind2_exp,theme_p[['jjdm','基金简称']],how='left',on='jjdm').drop('jjdm',axis=1)



    #get the value and growth  exp

    sql="SELECT * from hbs_style_exp where  jjdm in ({0})"\
        .format(util.list_sql_condition(value_p['jjdm'].astype(str).tolist()))
    style_exp=pd.read_sql(sql,con=localdb)

    sql="SELECT * from hbs_size_exp where  jjdm in ({0})"\
        .format(util.list_sql_condition(value_p['jjdm'].astype(str).tolist()))
    size_exp=pd.read_sql(sql,con=localdb)

    style_exp = pd.merge(style_exp, theme_p[['jjdm', '基金简称']], how='left', on='jjdm').drop(['jjdm','jjzzc'], axis=1)
    size_exp = pd.merge(size_exp, theme_p[['jjdm', '基金简称']], how='left', on='jjdm').drop(['jjdm','jjzzc'], axis=1)


    if (if_percentage):
        for col in float_col_list:
            industry_p[col] = industry_p[col].map("{:.2%}".format)
        for col in ind_sp_float_col_list[0:int(len(ind_sp_float_col_list) / 2)]:
            industry_sp[col] = \
                industry_sp[col].astype(float).map("{:.2%}".format)
        for col in ind_sp_float_col_list[int(len(ind_sp_float_col_list) / 2):]:
            industry_sp.loc[industry_sp['项目名'] != '切换次数', col] = \
                industry_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
        for col in theme_sp_float_col_list[0:int(len(theme_sp_float_col_list) / 2)]:
            theme_sp[col] = \
                theme_sp[col].astype(float).map("{:.2%}".format)
        for col in theme_sp_float_col_list[int(len(theme_sp_float_col_list) / 2):]:
            theme_sp.loc[theme_sp['项目名'] != '切换次数', col] = \
                theme_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
        for col in ['主题集中度', '主题换手率', '大金融', '消费', 'TMT', '周期',
       '制造']:
            theme_p[col]=theme_p[col].map("{:.2%}".format)


        for col in ['集中度(持仓)', '换手率(持仓)', '成长绝对暴露(持仓)', '价值绝对暴露(持仓)', '集中度排名(持仓)',
           '换手率排名(持仓)', '成长暴露排名(持仓)', '价值暴露排名(持仓)']:
            value_p_hbs[col]=value_p_hbs[col].map("{:.2%}".format)
        for col in ['集中度(持仓)', '换手率(持仓)', '大盘绝对暴露(持仓)', '中盘绝对暴露(持仓)', '小盘绝对暴露(持仓)',
           '集中度排名(持仓)', '换手率排名(持仓)', '大盘暴露排名(持仓)', '中盘暴露排名(持仓)', '小盘暴露排名(持仓)']:
            size_p_hbs[col]=size_p_hbs[col].map("{:.2%}".format)
        for col in ['换手率排名', '集中度排名', '成长暴露排名', '价值暴露排名',
                           '换手率', '集中度', ]:
            value_p[col]=value_p[col].map("{:.2%}".format)
        for col in ['换手率排名', '集中度排名', '大盘暴露排名', '中盘暴露排名','小盘暴露排名',
                           '换手率', '集中度', ]:
            size_p[col]=size_p[col].map("{:.2%}".format)
        for col in ['Total', '成长', '价值']:
            value_sp.loc[value_sp['项目名']!='切换次数',col]=\
                value_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
            value_sp_hbs.loc[value_sp_hbs['项目名']!='切换次数',col]=\
                value_sp_hbs.iloc[1:][col].astype(float).map("{:.2%}".format)
        for col in ['Total_rank', '成长_rank', '价值_rank']:
            value_sp[col]=\
                value_sp[col].astype(float).map("{:.2%}".format)
            value_sp_hbs[col]=\
                value_sp_hbs[col].astype(float).map("{:.2%}".format)
        for col in ['Total', '大盘', '中盘', '小盘']:
            size_sp.loc[size_sp['项目名']!='切换次数',col]=\
                size_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
            size_sp_hbs.loc[size_sp_hbs['项目名']!='切换次数',col]=\
                size_sp_hbs.iloc[1:][col].astype(float).map("{:.2%}".format)
        for col in ['Total_rank', '大盘_rank', '中盘_rank', '小盘_rank']:
            size_sp[col]=\
                size_sp[col].astype(float).map("{:.2%}".format)
            size_sp_hbs[col]=\
                size_sp_hbs[col].astype(float).map("{:.2%}".format)

        for col in float_col:
            stock_p[col]= stock_p[col].map("{:.2%}".format)
        for col in tp_float_col:
            stock_tp[col] = stock_tp[col].map("{:.2%}".format)

        for col in performance_float_col:
            jj_performance[col] = jj_performance[col].map("{:.2%}".format)

    return value_p,value_p_hbs,value_sp,value_sp_hbs, size_p,size_p_hbs,size_sp,size_sp_hbs,\
           industry_p,industry_sp,theme_p,theme_sp,industry_detail_df_list,stock_p,\
           stock_tp,jj_performance,industry_contribution_list,ticker_con,theme_exp,ind2_exp\
        ,industry_contribution_perweight_list,style_exp,size_exp

def plot_picatlocal(jjdm):

    jjjc=hbdb.db2df("select jjjc from st_fund.t_st_gm_jjxx where jjdm='{0}'".format(jjdm),db='funduser')['jjjc'][0]

    jjdm_con="jjdm='{}'".format(jjdm)
    value_p, value_p_hbs, value_sp, value_sp_hbs, size_p, size_p_hbs, size_sp, size_sp_hbs, \
    industry_p, industry_sp, theme_p, theme_sp, industry_detail_df_list, stock_p, stock_tp,jj_performance=get_pic_from_localdb(jjdm_con,show_num=20)

    plot=functionality.Plot(2000,400)
    plot2=functionality.Plot(2000,100)

    print("%html <h3>行业画像</h3>")
    plot2.plotly_table(industry_p, 8000, 'asdf')
    plot.plotly_table(industry_sp, 6000, 'asdf')

    print("%html <h3>一级行业画像</h3>")
    plot.plotly_table(industry_detail_df_list[0][industry_detail_df_list[0].columns[0:45]],8000,'asdf')
    print("%html <h3>二级行业画像</h3>")
    plot.plotly_table(industry_detail_df_list[1][industry_detail_df_list[1].columns[0:45]],8000,'asdf')
    print("%html <h3>三级行业画像</h3>")
    plot.plotly_table(industry_detail_df_list[2][industry_detail_df_list[2].columns[0:45]],8000,'asdf')

    if(len(theme_p)>0):
        print("%html <h3>主题画像</h3>")
        plot2.plotly_table(theme_p, 2000, 'asdf')
        plot.plotly_table(theme_sp, 2000, 'asdf')
    else:
        print("%html <h3>主题画像暂无</h3>")


    print("%html <h3>风格画像_基于持仓</h3>")
    plot2.plotly_table(value_p_hbs, 2000, 'asdf')
    plot.plotly_table(value_sp_hbs, 2000, 'asdf')
    print("%html <h3>风格画像_基于净值</h3>")
    plot2.plotly_table(value_p, 2000, 'asdf')
    plot.plotly_table(value_sp, 2000, 'asdf')

    print("%html <h3>规模风格画像_基于持仓</h3>")
    plot2.plotly_table(size_p_hbs, 2000, 'asdf')
    plot.plotly_table(size_sp_hbs, 2000, 'asdf')
    print("%html <h3>规模风格画像_基于净值</h3>")
    plot2.plotly_table(size_p, 2000, 'asdf')
    plot.plotly_table(size_sp, 2000, 'asdf')


    print("%html <h3>个股交易画像</h3>")
    plot2.plotly_table(stock_p, 4000, 'asdf')
    plot2.plotly_table(stock_tp, 8000, 'asdf')

def industry_pic_all(jj_base_info,asofdate1,asofdate2,th1=0.5, th2=0.5,if_prv=False,fre='Q'):


    if(if_prv):

        if(fre=='M'):
            fre_table='_monthly'
        else:
            fre_table=''
        property_table='hbs_prv_industry_property{}_new'.format(fre_table)
        industry_level_table = 'hbs_prv_industry_property{}'.format(fre_table)
        ind_shift_property_table='hbs_prv_industry_shift_property'
        theme_shift_property_table='hbs_prv_theme_shift_property'
        ind_property_pic_table='jjpic_prv_industry_p{}'.format(fre_table)
        ind_shift_pic_table='jjpic_prv_industry_sp{}'.format(fre_table)
        theme_property_pic_table='jjpic_prv_theme_p{}'.format(fre_table)
        theme_shift_pic_table='jjpic_prv_theme_sp{}'.format(fre_table)
        industry_level_pic_table = 'jjpic_prv_industry_detail{}'.format(fre_table)
    else:
        property_table='hbs_industry_property_new'
        industry_level_table='hbs_industry_property'
        ind_shift_property_table='hbs_industry_shift_property_new'
        theme_shift_property_table='hbs_theme_shift_property_new'
        ind_property_pic_table='jjpic_industry_p'
        ind_shift_pic_table='jjpic_industry_sp'
        theme_property_pic_table='jjpic_theme_p'
        theme_shift_pic_table='jjpic_theme_sp'
        industry_level_pic_table='jjpic_industry_detail'

    # latest_date =str( pd.read_sql(
    #     "select max(asofdate) as asofdate from {0}".format(property_table), con=localdb)['asofdate'][0])
    latest_date=asofdate1
    sql = "SELECT * from {1} where asofdate='{0}' " \
        .format( latest_date,property_table)
    industry_p = pd.read_sql(sql, con=localdb).rename(columns={'cen_ind_1_rank': '一级行业集中度',
                                                               'ratio_ind_1_rank': '一级行业换手率',
                                                               'cen_ind_2_rank': '二级行业集中度',
                                                               'ratio_ind_2_rank': '二级行业换手率',
                                                               'cen_ind_3_rank': '三级行业集中度',
                                                               'ratio_ind_3_rank': '三级行业换手率',
                                                               'industry_num': '行业暴露数',
                                                               'top5': '前五大行业',
                                                               'top20_2': '二级行业前20大',
                                                               'top20_3': '三级行业前20大',
                                                               'longtou_med': '龙头占比(时序中位数)',
                                                               'longtou_mean': '龙头占比(时序均值)',
                                                               'longtou_med_rank': '龙头占比(时序中位数)排名',
                                                               'longtou_mean_rank': '龙头占比(时序均值)排名',
                                                               'cen_theme_rank': '主题集中度',
                                                               'ratio_theme_rank': '主题换手率'
                                                               })

    industry_p.drop(['cen_ind_1','cen_ind_2','cen_ind_3','cen_theme',
                     'ratio_ind_1','ratio_ind_2','ratio_ind_3','ratio_theme'],axis=1,inplace=True)
    industry_p[['龙头占比(时序均值)', '龙头占比(时序中位数)']] = industry_p[['龙头占比(时序均值)', '龙头占比(时序中位数)']] / 100
    float_col_list = industry_p.columns.tolist()
    float_col_list.remove('jjdm')
    float_col_list.remove('asofdate')
    float_col_list.remove('前五大行业')
    float_col_list.remove('二级行业前20大')
    float_col_list.remove('三级行业前20大')

    industry_detail_df_list = []
    class_name_list = ['yjxymc', 'ejxymc', 'sjxymc']
    name_map = dict(zip(['zsbl_mean', 'ROE_mean', 'PB_mean',
                         'DIVIDENDRATIO_mean', 'PCF_mean', 'TOTALMV_mean',
                         'PEG_mean', 'PE_mean', 'NETPROFITGROWRATE_mean',
                         'OPERATINGREVENUEYOY_mean', 'longtou_zjbl_for_ind_mean', 'zsbl_med',
                         'ROE_med', 'PB_med', 'DIVIDENDRATIO_med', 'PCF_med',
                         'TOTALMV_med', 'PEG_med', 'PE_med',
                         'NETPROFITGROWRATE_med', 'OPERATINGREVENUEYOY_med',
                         'longtou_zjbl_for_ind_med', 'jjdm', 'zsbl_mean_rank', 'ROE_mean_rank',
                         'PB_mean_rank', 'DIVIDENDRATIO_mean_rank',
                         'PCF_mean_rank', 'TOTALMV_mean_rank',  'PEG_mean_rank', 'PE_mean_rank',
                         'NETPROFITGROWRATE_mean_rank', 'OPERATINGREVENUEYOY_mean_rank',
                         'longtou_zjbl_for_ind_mean_rank', 'zsbl_med_rank', 'ROE_med_rank',
                         'PB_med_rank', 'DIVIDENDRATIO_med_rank',
                         'PCF_med_rank', 'TOTALMV_med_rank', 'PEG_med_rank', 'PE_med_rank',
                         'NETPROFITGROWRATE_med_rank', 'OPERATINGREVENUEYOY_med_rank',
                         'longtou_zjbl_for_ind_med_rank', 'growth_mean_rank', 'value_mean_rank',
                         'growth_med_rank', 'value_med_rank'], ['占持仓比例(时序均值)', '净资产收益率(时序均值)',
                                                                'PB(时序均值)', '股息率(时序均值)',
                                                                'PCF(时序均值)', '总市值(时序均值)',
                                                                 'PEG(时序均值)',
                                                                'PE(时序均值)', '净利润增长率(时序均值)',
                                                                '主营业务增长率(时序均值)', '行业龙头占比(时序均值)',
                                                                '占持仓比例(时序中位数)', '净资产收益率(时序中位数)',
                                                                'PB(时序中位数)', '股息率(时序中位数)',
                                                                'PCF(时序中位数)', '总市值(时序中位数)',
                                                                 'PEG(时序中位数)',
                                                                'PE(时序中位数)', '净利润增长率(时序中位数)',
                                                                '主营业务增长率(时序中位数)', '行业龙头占比(时序中位数)',
                                                                'jjdm', '占持仓比例(时序均值)排名', '净资产收益率(时序均值)排名',
                                                                'PB(时序均值)排名', '股息率(时序均值)排名',
                                                                'PCF(时序均值)排名', '总市值(时序均值)排名',
                                                                 'PEG(时序均值)排名',
                                                                'PE(时序均值)排名', '净利润增长率(时序均值)排名',
                                                                '主营业务增长率(时序均值)排名', '行业龙头占比(时序均值)排名',
                                                                '占持仓比例(时序中位数)排名', '净资产收益率(时序中位数)排名',
                                                                'PB(时序中位数)排名', '股息率(时序中位数)排名',
                                                                'PCF(时序中位数)排名', '总市值(时序中位数)排名',
                                                                 'PEG(时序中位数)排名',
                                                                'PE(时序中位数)排名', '净利润增长率(时序中位数)排名',
                                                                '主营业务增长率(时序中位数)排名', '行业龙头占比(时序中位数)排名',
                                                                '综合成长属性(时序均值)排名', '综合价值属性(时序均值)排名', '综合成长属性(时序中位数)排名',
                                                                '综合价值属性(时序中位数)排名', 'asofdate']))

    sql = " select * from hbs_industry_financial_stats where ENDDATE>='{0}' and ENDDATE<='{1}'" \
        .format(str(int(latest_date[0:4]) - 3) + latest_date[4:6], latest_date[0:6])
    industry_financial_info = pd.read_sql(sql, con=localdb)

    industry_financial_info[['ROE', 'NETPROFITGROWRATE',
                             'OPERATINGREVENUEYOY', 'DIVIDENDRATIO']] = industry_financial_info[
                                                                            ['ROE', 'NETPROFITGROWRATE',
                                                                             'OPERATINGREVENUEYOY',
                                                                             'DIVIDENDRATIO']] / 100

    industry_financial_info_mean = industry_financial_info \
        .groupby('industry_name').median().rename(columns={
        "ROE": "行业净资产收益率", "PE": "行业PE", "PCF": "行业PCF",
        "NETPROFITGROWRATE": "行业净利润增长率", "OPERATINGREVENUEYOY": "行业主营业务增长率",
        "PB": "行业PB", "DIVIDENDRATIO": "行业股息率", "AVERAGEMV": "行业平均市值", "TOTALMV": "行业总市值",
        "PEG": "行业PEG"})
    industry_financial_info_med = industry_financial_info \
        .groupby('industry_name').median().rename(columns={
        "ROE": "行业净资产收益率", "PE": "行业PE", "PCF": "行业PCF",
        "NETPROFITGROWRATE": "行业净利润增长率", "OPERATINGREVENUEYOY": "行业主营业务增长率",
        "PB": "行业PB", "DIVIDENDRATIO": "行业股息率", "AVERAGEMV": "行业平均市值", "TOTALMV": "行业总市值",
        "PEG": "行业PEG"})

    industry_financial_info = pd.merge(industry_financial_info_mean, industry_financial_info_med,
                                       how='inner', left_index=True, right_index=True)

    industry_financial_info.columns = industry_financial_info.columns.str.replace('TOP', "")
    industry_financial_info.columns = industry_financial_info.columns.str.replace('TOP', "")
    industry_financial_info.columns = industry_financial_info.columns.str.replace('MV', "市值")
    industry_financial_info.columns = industry_financial_info.columns.str.replace('%', "分位数")
    industry_financial_info.columns = industry_financial_info.columns.str.replace('_x', "(时序均值)")
    industry_financial_info.columns = industry_financial_info.columns.str.replace('_y', "(时序中位数)")
    industry_financial_info.reset_index(inplace=True)

    theme_weight = pd.DataFrame()
    for i in range(3):
        # latest_date = pd.read_sql(
        #     "select max(asofdate) as asofdate from {1}_{0}_industry_level".format(i + 1,industry_level_table),
        #     con=localdb)['asofdate'][0]
        latest_date=asofdate1
        sql = "SELECT * from {2}_{1}_industry_level where asofdate='{0}' " \
            .format(latest_date, i + 1,industry_level_table)
        temp_ind_detail = pd.read_sql(sql, con=localdb).rename(columns=name_map)
        temp_ind_detail.rename(columns={class_name_list[i]: '行业名称'}, inplace=True)

        temp_ind_detail[['行业龙头占比(时序均值)', '行业龙头占比(时序中位数)',
                         '净资产收益率(时序均值)', '股息率(时序均值)', '净利润增长率(时序均值)',
                         '主营业务增长率(时序均值)', '净资产收益率(时序中位数)', '股息率(时序中位数)',
                         '净利润增长率(时序中位数)', '主营业务增长率(时序中位数)']] = temp_ind_detail[['行业龙头占比(时序均值)', '行业龙头占比(时序中位数)',
                                                                                '净资产收益率(时序均值)', '股息率(时序均值)',
                                                                                '净利润增长率(时序均值)',
                                                                                '主营业务增长率(时序均值)', '净资产收益率(时序中位数)',
                                                                                '股息率(时序中位数)',
                                                                                '净利润增长率(时序中位数)',
                                                                                '主营业务增长率(时序中位数)']] / 100

        temp_ind_detail = pd.merge(temp_ind_detail, industry_financial_info,
                                   how='left', left_on='行业名称', right_on='industry_name')

        temp_ind_detail = temp_ind_detail[['jjdm','行业名称', '占持仓比例(时序均值)',
                                           '占持仓比例(时序均值)排名',
                                           '综合价值属性(时序均值)排名', '综合成长属性(时序均值)排名',
                                           '行业龙头占比(时序均值)', '行业龙头占比(时序均值)排名',
                                           '主营业务增长率(时序均值)', '主营业务增长率(时序均值)排名', '行业主营业务增长率(时序均值)',
                                           '净利润增长率(时序均值)', '净利润增长率(时序均值)排名', '行业净利润增长率(时序均值)',
                                           '净资产收益率(时序均值)', '净资产收益率(时序均值)排名', '行业净资产收益率(时序均值)',
                                           'PB(时序均值)', 'PB(时序均值)排名', '行业PB(时序均值)',
                                           'PE(时序均值)', 'PE(时序均值)排名', '行业PE(时序均值)',
                                           'PCF(时序均值)', 'PCF(时序均值)排名', '行业PCF(时序均值)',
                                           '股息率(时序均值)', '股息率(时序均值)排名', '行业股息率(时序均值)',
                                           'PEG(时序均值)', 'PEG(时序均值)排名', '行业PEG(时序均值)',
                                           '总市值(时序均值)', '总市值(时序均值)排名', '行业平均市值(时序均值)', '25分位数市值(时序均值)', '50分位数市值(时序均值)',
                                           '75分位数市值(时序均值)',
                                           '90分位数市值(时序均值)', 'asofdate',
                                           '占持仓比例(时序中位数)', '占持仓比例(时序中位数)排名', '综合价值属性(时序中位数)排名',
                                           '综合成长属性(时序中位数)排名', '行业龙头占比(时序中位数)', '行业龙头占比(时序中位数)排名',
                                           '主营业务增长率(时序中位数)', '主营业务增长率(时序中位数)排名','行业主营业务增长率(时序中位数)',
                                           '净利润增长率(时序中位数)', '净利润增长率(时序中位数)排名', '行业净利润增长率(时序中位数)',
                                           '净资产收益率(时序中位数)', '净资产收益率(时序中位数)排名', '行业净资产收益率(时序中位数)',
                                           'PB(时序中位数)', 'PB(时序中位数)排名', '行业PB(时序中位数)',
                                           'PE(时序中位数)', 'PE(时序中位数)排名', '行业PE(时序中位数)',
                                           'PCF(时序中位数)', 'PCF(时序中位数)排名', '行业PCF(时序中位数)',
                                           '股息率(时序中位数)', '股息率(时序中位数)排名', '行业股息率(时序中位数)',
                                           'PEG(时序中位数)', 'PEG(时序中位数)排名', '行业PEG(时序中位数)',
                                           '总市值(时序中位数)', '总市值(时序中位数)排名',
                                           '行业平均市值(时序中位数)', '25分位数市值(时序中位数)', '50分位数市值(时序中位数)', '75分位数市值(时序中位数)',
                                           '90分位数市值(时序中位数)'
                                           ]]

        ind_detial_float_col = temp_ind_detail.columns.tolist()
        ind_detial_float_col.sort()
        for col in ['总市值(时序中位数)', '总市值(时序中位数)排名',
                    '总市值(时序均值)', '总市值(时序均值)排名', '行业平均市值(时序中位数)', '25分位数市值(时序中位数)',
                    '50分位数市值(时序中位数)', '75分位数市值(时序中位数)', '90分位数市值(时序中位数)', '行业平均市值(时序均值)', '25分位数市值(时序均值)',
                    '50分位数市值(时序均值)', '75分位数市值(时序均值)', '90分位数市值(时序均值)', 'asofdate', '行业名称',
                    'PE(时序中位数)', 'PE(时序均值)', 'PEG(时序中位数)', 'PEG(时序均值)',
                    'PB(时序中位数)', 'PB(时序均值)', '行业PE(时序中位数)', '行业PB(时序中位数)', '行业PEG(时序中位数)', '行业PE(时序均值)', '行业PB(时序均值)',
                    '行业PEG(时序均值)']:
            ind_detial_float_col.remove(col)
        if (i == 0):
            theme_weight = temp_ind_detail[['jjdm','行业名称', '占持仓比例(时序均值)']]

        industry_detail_df_list.append(temp_ind_detail)

    # latest_date = pd.read_sql(
    #     "select max(asofdate) as asofdate from {0}".format(ind_shift_property_table), con=localdb)['asofdate'][0]

    latest_date = asofdate2
    sql = "SELECT * from {1} where  asofdate='{0}' " \
        .format(latest_date,ind_shift_property_table)
    industry_sp = pd.read_sql(sql, con=localdb).set_index('项目名').fillna(0)
    ind_sp_float_col_list = industry_sp.columns.tolist()
    ind_sp_float_col_list.remove('jjdm')
    ind_sp_float_col_list.remove('asofdate')


    # generate the label:
    industry_p['一级行业类型']='配置'
    industry_p['二级行业类型'] = '配置'
    industry_p['三级行业类型'] = '配置'
    industry_p['主题类型'] = '配置'
    for class_lv in ['一级行业','二级行业','三级行业','主题']:
        industry_p.loc[(industry_p[class_lv+'集中度']>th1)
                       &(industry_p[class_lv+'换手率'] > th2),class_lv+'类型']='博弈'
        industry_p.loc[(industry_p[class_lv+'集中度']>th1)
                       &(industry_p[class_lv+'换手率'] < th2),class_lv+'类型']='专注'
        industry_p.loc[(industry_p[class_lv+'集中度']<th1)
                       &(industry_p[class_lv+'换手率'] > th2),class_lv+'类型']='轮动'
        industry_p.loc[(industry_p[class_lv+'集中度']<th1)
                       &(industry_p[class_lv+'换手率'] < th2),class_lv+'类型']='配置'


    industry_p=pd.merge(industry_p,jj_base_info,how='left',on='jjdm').rename(columns={'jjjc':'基金简称'})

    # theme picture
    # latest_date = pd.read_sql(
    #     "select max(asofdate) as asofdate from {0}".format(theme_shift_property_table), con=localdb)['asofdate'][0]
    latest_date=asofdate2
    sql = "SELECT * from {1} where asofdate='{0}' " \
        .format(latest_date,theme_shift_property_table)
    theme_sp = pd.read_sql(sql, con=localdb).set_index('项目名').fillna(0)

    theme_sp_float_col_list = theme_sp.columns.tolist()
    theme_sp_float_col_list.remove('jjdm')
    theme_sp_float_col_list.remove('asofdate')

    theme_weight = pd.merge(theme_weight, ia.ind2thememap,
                            how='left', left_on='行业名称', right_on='industry_name').drop('industry_name', axis=1)
    theme_weight = theme_weight.groupby(['jjdm','theme']).sum().reset_index(level=0).T

    for theme in ia.theme_col:
        industry_p = pd.merge(industry_p,
                              theme_weight[theme].T,
                              how='left', on='jjdm').rename(columns={'占持仓比例(时序均值)':theme})


    theme_p = industry_p[['jjdm', '基金简称', '主题类型', '主题集中度', '主题换手率', '大金融', '消费', 'TMT',
                          '周期', '制造', 'asofdate']]
    theme_sp = theme_sp[['Total_rank',
                         '大金融_rank', '消费_rank', 'TMT_rank', '周期_rank', '制造_rank',
                         'Total', '大金融', '消费', 'TMT', '周期', '制造', 'jjdm','asofdate']]
    theme_sp.reset_index(inplace=True)

    industry_p = industry_p[['jjdm', '基金简称', '一级行业类型', '一级行业集中度', '一级行业换手率', '前五大行业','二级行业前20大','三级行业前20大', '龙头占比(时序均值)',
                             '龙头占比(时序中位数)', '龙头占比(时序均值)排名', '龙头占比(时序中位数)排名', '二级行业类型', '二级行业集中度', '二级行业换手率',
                             '三级行业类型', '三级行业集中度', '三级行业换手率', 'asofdate']]

    industry_sp = industry_sp[['Total_rank', '农林牧渔_rank',
                               '基础化工_rank', '钢铁_rank', '有色金属_rank', '电子_rank', '家用电器_rank',
                               '食品饮料_rank', '纺织服饰_rank', '轻工制造_rank', '医药生物_rank', '公用事业_rank',
                               '交通运输_rank', '房地产_rank', '商贸零售_rank', '社会服务_rank', '综合_rank',
                               '建筑材料_rank', '建筑装饰_rank', '电力设备_rank', '国防军工_rank', '计算机_rank',
                               '传媒_rank', '通信_rank', '银行_rank', '非银金融_rank', '汽车_rank', '机械设备_rank',
                               '煤炭_rank', '石油石化_rank', '环保_rank', '美容护理_rank', 'Total', '农林牧渔', '基础化工', '钢铁', '有色金属',
                               '电子', '家用电器', '食品饮料', '纺织服饰',
                               '轻工制造', '医药生物', '公用事业', '交通运输', '房地产', '商贸零售', '社会服务', '综合', '建筑材料',
                               '建筑装饰', '电力设备', '国防军工', '计算机', '传媒', '通信', '银行', '非银金融', '汽车', '机械设备',
                               '煤炭', '石油石化', '环保', '美容护理', 'jjdm','asofdate']]
    industry_sp.reset_index(inplace=True)

    #check if data already exist
    # sql="delete from {1} where asofdate={0}".format(industry_p['asofdate'][0],ind_property_pic_table)
    localdb.execute(sql)
    industry_p.to_sql(ind_property_pic_table,con=localdb,index=False,if_exists='append')

    sql="delete from {1} where asofdate={0}".format(industry_sp['asofdate'][0],ind_shift_pic_table)
    localdb.execute(sql)
    industry_sp.to_sql(ind_shift_pic_table, con=localdb, index=False, if_exists='append')

    sql="delete from {1} where asofdate={0}".format(theme_p['asofdate'][0],theme_property_pic_table)
    localdb.execute(sql)
    theme_p.to_sql(theme_property_pic_table, con=localdb, index=False, if_exists='append')

    sql="delete from {1} where asofdate={0}".format(theme_sp['asofdate'][0],theme_shift_pic_table)
    localdb.execute(sql)
    theme_sp.to_sql(theme_shift_pic_table, con=localdb, index=False, if_exists='append')

    for i in range(3):
        sql = "delete from {2}_{1} where asofdate={0}"\
            .format(industry_detail_df_list[i]['asofdate'][0],str(i+1),industry_level_pic_table)
        localdb.execute(sql)
        industry_detail_df_list[i].to_sql("{1}_{0}".format(str(i+1),industry_level_pic_table),
                                          con=localdb, index=False, if_exists='append')

    return industry_p[['jjdm','一级行业集中度']]

def style_pic_all(jj_base_info,asofdate,fre, th1=0.5, th2=0.5, if_percentage=True,if_prv=False,fre2='Q'):

    def label_style(df, cen_col, shift_col, style_col, bias_col, th1, th2):

        df[style_col] = '配置'
        df[bias_col] = '均衡'
        df.loc[(df[cen_col] > th1) & (df[shift_col] > th2), style_col] = '博弈'
        df.loc[(df[cen_col] > th1) & (df[shift_col] > th2), bias_col] = \
            df.loc[(df[cen_col] > th1) & (df[shift_col] > th2)]['winning_value']

        df.loc[(df[cen_col] > th1) & (df[shift_col] < th2), style_col] = '专注'
        df.loc[(df[cen_col] > th1) & (df[shift_col] < th2), bias_col] = \
            df.loc[(df[cen_col] > th1) & (df[shift_col] < th2)]['winning_value']

        df.loc[(df[cen_col] < th1) & (df[shift_col] > th2), style_col] = '轮动'
        df.loc[(df[cen_col] < th1) & (df[shift_col] > th2), bias_col] = '均衡'

        df.loc[(df[cen_col] < th1) & (df[shift_col] < th2), style_col] = '配置'
        df.loc[(df[cen_col] < th1) & (df[shift_col] < th2), bias_col] = '均衡'

        return df.drop('winning_value', axis=1)

    if(if_prv):
        if(fre2=='M'):
            fre_table='_monthly'
        else:
            fre_table=''
        nav_property_table='nav_prv_style_property'
        hbs_property_table='hbs_prv{}'.format(fre_table)
        nav_shift_table='nav_prv_shift_property'
        jjpic_table='jjpic_prv{}'.format(fre_table)
    else:
        nav_property_table='nav_style_property'
        hbs_property_table='hbs'
        nav_shift_table='nav_shift_property'
        jjpic_table='jjpic'

    if(not if_prv):
        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from {1}_value where fre='{0}'"
                .format(fre,nav_property_table), con=localdb)['asofdate'][0]

        sql = "SELECT * from {2}_value where fre='{0}' and asofdate='{1}' " \
            .format( fre, latest_date,nav_property_table)
        value_p = pd.read_sql(sql, con=localdb).rename(columns={'shift_ratio_rank': '换手率排名',
                                                                'centralization_rank': '集中度排名',
                                                                '成长_mean': '成长暴露排名',
                                                                '价值_mean': '价值暴露排名',
                                                                '成长_abs_mean': '成长绝对暴露',
                                                                '价值_abs_mean': '价值绝对暴露',
                                                                'manager_change': '经理是否未变更',
                                                                'shift_ratio': '换手率',
                                                                'centralization': '集中度',
                                                                'fre': '回归周期',
                                                                })

        # generate the label for nav based :
        value_p['max'] = value_p[['成长暴露排名', '价值暴露排名']].max(axis=1)
        value_p.loc[value_p['成长暴露排名'] == value_p['max'], 'winning_value'] = '成长'
        value_p.loc[value_p['价值暴露排名'] == value_p['max'], 'winning_value'] = '价值'
        value_p.drop('max', axis=1, inplace=True)

        value_p = label_style(value_p, '集中度排名', '换手率排名', '风格类型', '风格偏好', th1, th2)
        value_p = pd.merge(value_p, jj_base_info, how='left', on='jjdm').rename(columns={'jjjc': '基金简称'})
        value_p = value_p[['jjdm', '基金简称', '风格类型', '风格偏好', '换手率排名', '集中度排名',
                           '成长暴露排名', '价值暴露排名', '成长绝对暴露', '价值绝对暴露', '经理是否未变更',
                           '换手率', '集中度', '回归周期', 'asofdate']]

        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from {1}_size where fre='{0}'"
                .format(fre, nav_property_table), con=localdb)['asofdate'][0]

        sql = "SELECT * from {2}_size where fre='{0}' and asofdate='{1}' " \
            .format(fre, latest_date, nav_property_table)
        size_p = pd.read_sql(sql, con=localdb).rename(columns={'shift_ratio_rank': '换手率排名',
                                                               'centralization_rank': '集中度排名',
                                                               '大盘_mean': '大盘暴露排名',
                                                               '中盘_mean': '中盘暴露排名',
                                                               '小盘_mean': '小盘暴露排名',
                                                               '大盘_abs_mean': '大盘绝对暴露',
                                                               '中盘_abs_mean': '中盘绝对暴露',
                                                               '小盘_abs_mean': '小盘绝对暴露',
                                                               'manager_change': '经理是否未变更',
                                                               'shift_ratio': '换手率',
                                                               'centralization': '集中度',
                                                               'fre': '回归周期',
                                                               })

        # generate the label for nav based :
        size_p['winning_value'] = ''
        size_p.loc[size_p['大盘暴露排名'] > 0.5, 'winning_value'] = size_p.loc[size_p['大盘暴露排名'] > 0.5]['winning_value'] + '大'
        size_p.loc[size_p['中盘暴露排名'] > 0.5, 'winning_value'] = size_p.loc[size_p['中盘暴露排名'] > 0.5]['winning_value'] + '中'
        size_p.loc[size_p['小盘暴露排名'] > 0.5, 'winning_value'] = size_p.loc[size_p['小盘暴露排名'] > 0.5]['winning_value'] + '小'

        size_p = label_style(size_p, '集中度排名', '换手率排名', '规模风格类型', '规模偏好', th1, th2)

        size_p = pd.merge(size_p, jj_base_info, how='left', on='jjdm').rename(columns={'jjjc': '基金简称'})
        size_p = size_p[['jjdm', '基金简称', '规模风格类型', '规模偏好', '换手率排名', '集中度排名', '大盘暴露排名',
                         '大盘绝对暴露', '中盘暴露排名', '中盘绝对暴露', '小盘暴露排名', '小盘绝对暴露', '经理是否未变更',
                         '换手率', '集中度', '回归周期', 'asofdate']]

        # shift property for nav based
        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from {1}_value where fre='{0}'"
                .format(fre, nav_shift_table), con=localdb)['asofdate'][0]

        sql = "SELECT * from {2}_value where asofdate='{0}' and fre='{1}' " \
            .format(latest_date, fre, nav_shift_table)
        value_sp = pd.read_sql(sql, con=localdb).set_index('项目名').fillna(0)
        value_sp_float_col_list = value_sp.columns.tolist()
        value_sp_float_col_list.remove('jjdm')
        value_sp_float_col_list.remove('asofdate')
        value_sp_float_col_list.remove('fre')

        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from {1}_size where fre='{0}'"
                .format(fre, nav_shift_table), con=localdb)['asofdate'][0]

        sql = "SELECT * from {2}_size where asofdate='{0}' and fre='{1}' " \
            .format(latest_date, fre, nav_shift_table)
        size_sp = pd.read_sql(sql, con=localdb).set_index('项目名').fillna(0)
        size_sp_float_col_list = size_sp.columns.tolist()
        size_sp_float_col_list.remove('jjdm')
        size_sp_float_col_list.remove('asofdate')
        size_sp_float_col_list.remove('fre')

        # shift property for hbs based
        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from {0}_shift_property_value"
                .format(hbs_property_table), con=localdb)['asofdate'][0]

        sql = "SELECT * from {1}_shift_property_value where asofdate='{0}'  " \
            .format(latest_date, hbs_property_table)
        value_sp_hbs = pd.read_sql(sql, con=localdb).set_index('项目名').fillna(0)
        value_sp_hbs_float_col_list = value_sp_hbs.columns.tolist()
        value_sp_hbs_float_col_list.remove('jjdm')
        value_sp_hbs_float_col_list.remove('asofdate')

        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from {0}_shift_property_size "
                .format(hbs_property_table), con=localdb)['asofdate'][0]

        sql = "SELECT * from {1}_shift_property_size where asofdate='{0}' " \
            .format(latest_date, hbs_property_table)
        size_sp_hbs = pd.read_sql(sql, con=localdb).set_index('项目名').fillna(0)
        size_sp_hbs_float_col_list = size_sp_hbs.columns.tolist()
        size_sp_hbs_float_col_list.remove('jjdm')
        size_sp_hbs_float_col_list.remove('asofdate')

        if (if_percentage):
            for col in ['换手率排名', '集中度排名', '成长暴露排名', '价值暴露排名',
                        '换手率', '集中度', ]:
                value_p[col] = value_p[col].map("{:.2%}".format)

            for col in ['换手率排名', '集中度排名', '大盘暴露排名', '中盘暴露排名', '小盘暴露排名',
                        '换手率', '集中度', ]:
                size_p[col] = size_p[col].map("{:.2%}".format)

            for col in ['Total', '成长', '价值']:
                value_sp.loc[value_sp.index != '切换次数', col] = \
                    value_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
                value_sp_hbs.loc[value_sp_hbs.index != '切换次数', col] = \
                    value_sp_hbs.iloc[1:][col].astype(float).map("{:.2%}".format)
            for col in ['Total_rank', '成长_rank', '价值_rank']:
                value_sp[col] = \
                    value_sp[col].astype(float).map("{:.2%}".format)
                value_sp_hbs[col] = \
                    value_sp_hbs[col].astype(float).map("{:.2%}".format)

            for col in ['Total', '大盘', '中盘', '小盘']:
                size_sp.loc[size_sp.index != '切换次数', col] = \
                    size_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
                size_sp_hbs.loc[size_sp_hbs.index != '切换次数', col] = \
                    size_sp_hbs.iloc[1:][col].astype(float).map("{:.2%}".format)
            for col in ['Total_rank', '大盘_rank', '中盘_rank', '小盘_rank']:
                size_sp[col] = \
                    size_sp[col].astype(float).map("{:.2%}".format)
                size_sp_hbs[col] = \
                    size_sp_hbs[col].astype(float).map("{:.2%}".format)

        value_sp = value_sp[['jjdm', 'Total_rank', '成长_rank', '价值_rank',
                             'Total', '成长', '价值', 'fre', 'asofdate']]
        value_sp['type'] = 'nav_based'
        value_sp_hbs = value_sp_hbs[['jjdm', 'Total_rank', '成长_rank', '价值_rank',
                                     'Total', '成长', '价值', 'asofdate']]
        value_sp_hbs['type'] = 'holding_based'
        value_sp = pd.concat([value_sp, value_sp_hbs], axis=0)

        size_sp = size_sp[['jjdm', 'Total_rank', '大盘_rank', '中盘_rank',
                           '小盘_rank', 'Total', '大盘', '中盘', '小盘', 'fre', 'asofdate']]
        size_sp['type'] = 'nav_based'
        size_sp_hbs = size_sp_hbs[['jjdm', 'Total_rank', '大盘_rank', '中盘_rank',
                                   '小盘_rank', 'Total', '大盘', '中盘', '小盘', 'asofdate']]
        size_sp_hbs['type'] = 'holding_based'
        size_sp = pd.concat([size_sp, size_sp_hbs], axis=0)

        value_sp.reset_index(inplace=True)
        size_sp.reset_index(inplace=True)

        sql = "delete from {1}_value_p where asofdate='{0}'".format(value_p['asofdate'][0], jjpic_table)
        localdb.execute(sql)
        value_p.to_sql('{0}_value_p'.format(jjpic_table), con=localdb, index=False, if_exists='append')

        sql = "delete from {1}_size_p where asofdate='{0}'".format(size_p['asofdate'][0], jjpic_table)
        localdb.execute(sql)
        size_p.to_sql('{0}_size_p'.format(jjpic_table), con=localdb, index=False, if_exists='append')

        sql = "delete from {2}_value_sp where asofdate='{0}' or asofdate='{1}'" \
            .format(value_sp['asofdate'].unique()[0], value_sp['asofdate'].unique()[1], jjpic_table)
        localdb.execute(sql)
        value_sp.to_sql('{0}_value_sp'.format(jjpic_table), con=localdb, index=False, if_exists='append')

        sql = "delete from {2}_size_sp where asofdate='{0}' or asofdate='{1}'" \
            .format(size_sp['asofdate'].unique()[0], size_sp['asofdate'].unique()[1], jjpic_table)
        localdb.execute(sql)
        size_sp.to_sql('{0}_size_sp'.format(jjpic_table), con=localdb, index=False, if_exists='append')

    # latest_date = pd.read_sql(
    #     "select max(asofdate) as asofdate from {0}_style_property "
    #         .format(hbs_property_table), con=localdb)['asofdate'][0]

    latest_date=asofdate
    sql = "SELECT * from {1}_style_property where asofdate='{0}' " \
        .format(latest_date,hbs_property_table)
    value_p_hbs = pd.read_sql(sql, con=localdb).rename(columns={'cen_lv': '集中度(持仓)',
                                                                'shift_lv': '换手率(持仓)',
                                                                '成长': '成长绝对暴露(持仓)',
                                                                '价值': '价值绝对暴露(持仓)',
                                                                'cen_lv_rank': '集中度排名(持仓)',
                                                                'shift_lv_rank': '换手率排名(持仓)',
                                                                '成长_rank': '成长暴露排名(持仓)',
                                                                '价值_rank': '价值暴露排名(持仓)', })

    # generate the label for hbs based :
    value_p_hbs['max']=value_p_hbs[['成长绝对暴露(持仓)', '价值绝对暴露(持仓)']].max(axis=1)
    value_p_hbs.loc[value_p_hbs['成长绝对暴露(持仓)']==value_p_hbs['max'],'winning_value']='成长'
    value_p_hbs.loc[value_p_hbs['价值绝对暴露(持仓)'] == value_p_hbs['max'], 'winning_value'] = '价值'
    value_p_hbs.drop('max', axis=1, inplace=True)

    value_p_hbs = label_style(value_p_hbs, '集中度排名(持仓)', '换手率排名(持仓)',
                              '风格类型','风格偏好',th1,th2)

    value_p_hbs = pd.merge(value_p_hbs, jj_base_info, how='left', on='jjdm').rename(columns={'jjjc': '基金简称'})
    value_p_hbs = value_p_hbs[['jjdm', '基金简称', '风格类型', '风格偏好', '集中度(持仓)', '换手率(持仓)',
                               '成长绝对暴露(持仓)', '价值绝对暴露(持仓)', '集中度排名(持仓)',
                               '换手率排名(持仓)', '成长暴露排名(持仓)', '价值暴露排名(持仓)', 'asofdate']]

    if (if_percentage):
        for col in ['集中度(持仓)', '换手率(持仓)', '成长绝对暴露(持仓)', '价值绝对暴露(持仓)', '集中度排名(持仓)',
                    '换手率排名(持仓)', '成长暴露排名(持仓)', '价值暴露排名(持仓)']:
            value_p_hbs[col] = value_p_hbs[col].map("{:.2%}".format)

    # latest_date = pd.read_sql(
    #     "select max(asofdate) as asofdate from {0}_size_property "
    #         .format(hbs_property_table), con=localdb)['asofdate'][0]
    latest_date=asofdate
    sql = "SELECT * from {1}_size_property where  asofdate='{0}' " \
        .format(latest_date,hbs_property_table)
    size_p_hbs = pd.read_sql(sql, con=localdb).rename(columns={'cen_lv': '集中度(持仓)',
                                                               'shift_lv': '换手率(持仓)',
                                                               '大盘': '大盘绝对暴露(持仓)',
                                                               '中盘': '中盘绝对暴露(持仓)',
                                                               '小盘': '小盘绝对暴露(持仓)',
                                                               'cen_lv_rank': '集中度排名(持仓)',
                                                               'shift_lv_rank': '换手率排名(持仓)',
                                                               '大盘_rank': '大盘暴露排名(持仓)',
                                                               '中盘_rank': '中盘暴露排名(持仓)',
                                                               '小盘_rank': '小盘暴露排名(持仓)',
                                                               })


    # generate the label for hbs based :
    size_p_hbs['winning_value'] = ''
    size_p_hbs.loc[size_p_hbs['大盘绝对暴露(持仓)'] > 0.45, 'winning_value'] = size_p_hbs.loc[size_p_hbs['大盘绝对暴露(持仓)'] > 0.45]['winning_value'] + '大'
    size_p_hbs.loc[size_p_hbs['中盘绝对暴露(持仓)'] > 0.45, 'winning_value'] = size_p_hbs.loc[size_p_hbs['中盘绝对暴露(持仓)'] > 0.45]['winning_value'] + '中'
    size_p_hbs.loc[size_p_hbs['小盘绝对暴露(持仓)'] > 0.45, 'winning_value'] = size_p_hbs.loc[size_p_hbs['小盘绝对暴露(持仓)'] > 0.45]['winning_value'] + '小'
    size_p_hbs.loc[size_p_hbs['winning_value']=='','winning_value']=size_p_hbs.loc[size_p_hbs['winning_value']==''][['大盘绝对暴露(持仓)','中盘绝对暴露(持仓)','小盘绝对暴露(持仓)']].idxmax(axis=1).astype(str).str[0]

    size_p_hbs = label_style(size_p_hbs, '集中度排名(持仓)', '换手率排名(持仓)',
                             '规模风格类型', '规模偏好', th1, th2)

    size_p_hbs = pd.merge(size_p_hbs, jj_base_info, how='left', on='jjdm').rename(columns={'jjjc': '基金简称'})
    size_p_hbs = size_p_hbs[
        ['jjdm', '基金简称', '规模风格类型', '规模偏好', '集中度(持仓)', '换手率(持仓)', '大盘绝对暴露(持仓)', '中盘绝对暴露(持仓)', '小盘绝对暴露(持仓)',
         '集中度排名(持仓)', '换手率排名(持仓)', '大盘暴露排名(持仓)', '中盘暴露排名(持仓)', '小盘暴露排名(持仓)',
         'asofdate']]
    if (if_percentage):
        for col in ['集中度(持仓)', '换手率(持仓)', '大盘绝对暴露(持仓)', '中盘绝对暴露(持仓)', '小盘绝对暴露(持仓)',
                    '集中度排名(持仓)', '换手率排名(持仓)', '大盘暴露排名(持仓)', '中盘暴露排名(持仓)', '小盘暴露排名(持仓)']:
            size_p_hbs[col] = size_p_hbs[col].map("{:.2%}".format)

    # value_sp_hbs.reset_index(inplace=True)
    # size_sp_hbs.reset_index(inplace=True)

    #delete already exist data


    sql="delete from {1}_value_p_hbs where asofdate='{0}'".format(value_p_hbs['asofdate'][0],jjpic_table)
    localdb.execute(sql)
    value_p_hbs.to_sql('{0}_value_p_hbs'.format(jjpic_table), con=localdb, index=False, if_exists='append')


    sql="delete from {1}_size_p_hbs where asofdate='{0}'".format(size_p_hbs['asofdate'][0],jjpic_table)
    localdb.execute(sql)
    size_p_hbs.to_sql('{0}_size_p_hbs'.format(jjpic_table), con=localdb, index=False, if_exists='append')

def stock_trading_pci_all(jj_base_info,asofdate,ind_cen, th1=0.75,
                          th2=0.25, th3=0.5, th4=0.5, th5=0.75, th6=0.5, if_percentage=True):
    # latest_date = pd.read_sql(
    #     "select max(asofdate) as asofdate from hbs_holding_property "
    #     , con=localdb)['asofdate'][0]
    latest_date=asofdate
    sql = "SELECT * from hbs_holding_property where  asofdate='{0}' " \
        .format(latest_date)
    stock_p = pd.read_sql(sql, con=localdb)

    float_col = stock_p.columns.tolist()
    float_col.remove('jjdm')
    float_col.remove('asofdate')
    float_col.remove('持股数量')
    float_col.remove('PE')
    float_col.remove('PB')
    float_col.remove('ROE')
    float_col.remove('股息率')
    float_col.remove('PE_中位数')
    float_col.remove('PB_中位数')
    float_col.remove('ROE_中位数')
    float_col.remove('股息率_中位数')

    stock_p=pd.merge(stock_p,ind_cen,how='left',on='jjdm')

    # latest_date = pd.read_sql(
    #     "select max(asofdate) as asofdate from hbs_stock_trading_property "
    #     , con=localdb)['asofdate'][0]
    latest_date = asofdate
    sql = "SELECT * from hbs_stock_trading_property where asofdate='{0}' " \
        .format(latest_date)
    stock_tp = pd.read_sql(sql, con=localdb)
    stock_tp.columns=stock_tp.columns.str.replace("（","(")
    stock_tp.columns = stock_tp.columns.str.replace("）", ")")
    stock_tp['换手率']=stock_tp['换手率']/100
    tp_float_col = stock_tp.columns.tolist()
    tp_float_col.remove('jjdm')
    tp_float_col.remove('平均持有时间(出重仓前)')
    tp_float_col.remove('平均持有时间(出持仓前)')
    tp_float_col.remove('asofdate')

    # generate the labels

    stock_p['个股风格A'] = '无'
    stock_p['个股风格B'] = '无'
    stock_p['是否有尾仓(针对高个股集中基金)'] = '无尾仓'
    stock_tp['左侧标签'] = '无'
    stock_tp['新股次新股偏好']= ''


    stock_p.loc[(stock_p['个股集中度']>th1)&(stock_tp['换手率_rank'] < th1),
                '个股风格A']='专注'
    stock_p.loc[(stock_p['个股集中度']>th1)&(stock_tp['换手率_rank'] > th2),
                '个股风格A']='博弈'
    stock_p.loc[(stock_p['个股集中度']<th2)&(stock_tp['换手率_rank'] < th1),
                '个股风格A']='配置'
    stock_p.loc[(stock_p['个股集中度']<th2)&(stock_tp['换手率_rank'] > th2),
                '个股风格A']='轮动'
    stock_p.loc[(stock_p['个股集中度'] > th1)
                & (stock_p['一级行业集中度'] < th6),'个股风格B']='自下而上'
    stock_p.loc[(stock_p['个股集中度'] < th6)
                & (stock_p['一级行业集中度'] > th1),'个股风格B']='自上而上'
    stock_p.loc[(stock_p['个股集中度'] > th1)
                & (stock_p['个股集中度'] - stock_p['hhi'] > 0.05),'是否有尾仓(针对高个股集中基金)']='有尾仓'
    stock_tp.loc[(stock_tp['左侧概率(出持仓前,半年线)_rank'] > th3)
                 & (stock_tp['左侧程度(出持仓前,半年线)'] > th4),'左侧标签']='深度左侧'
    stock_tp.loc[(stock_tp['左侧概率(出持仓前,半年线)_rank'] > th3)
                 & (stock_tp['左侧程度(出持仓前,半年线)'] < th4),'左侧标签']='左侧'

    stock_tp.loc[(stock_tp['新股概率(出持仓前)_rank'] > th5),'新股次新股偏好']=\
        stock_tp[(stock_tp['新股概率(出持仓前)_rank'] > th5)]['新股次新股偏好']+'偏好新股'
    stock_tp.loc[(stock_tp['次新股概率(出持仓前)_rank'] > th5),'新股次新股偏好']=\
        stock_tp[(stock_tp['次新股概率(出持仓前)_rank'] > th5)]['新股次新股偏好']+'偏好次新股'
    stock_tp.loc[stock_tp['新股次新股偏好'] == '','新股次新股偏好']='无'


    if (if_percentage):
        for col in float_col:
            stock_p[col] = stock_p[col].map("{:.2%}".format)
        for col in tp_float_col:
            stock_tp[col] = stock_tp[col].map("{:.2%}".format)

    stock_p=pd.merge(stock_p,jj_base_info,how='left',on='jjdm').rename(columns={'jjjc':'基金简称'})
    # stock_p['基金简称'] = ''
    stock_tp = pd.merge(stock_tp, jj_base_info, how='left', on='jjdm').rename(columns={'jjjc': '基金简称'})
    # stock_tp['基金简称'] = ''

    stock_p = stock_p[['jjdm', '基金简称', '个股风格A', '个股风格B', '是否有尾仓(针对高个股集中基金)', '个股集中度', 'hhi', '持股数量',
                       '前三大', '前五大', '前十大', '平均仓位', '仓位换手率', 'PE_rank', 'PB_rank', 'ROE_rank', '股息率_rank',
                       'PE_中位数_rank',
                       'PB_中位数_rank', 'ROE_中位数_rank', '股息率_中位数_rank', 'PE', 'PB', 'ROE', '股息率',
                       'PE_中位数', 'PB_中位数', 'ROE_中位数', '股息率_中位数', 'asofdate'
                       ]]
    stock_tp = stock_tp[['jjdm', '基金简称', '左侧标签', '新股次新股偏好', '左侧概率(出重仓前,半年线)_rank', '左侧概率(出持仓前,半年线)_rank',
                         '左侧概率(出重仓前,年线)_rank', '左侧概率(出持仓前,年线)_rank','换手率_rank',
                         '平均持有时间(出重仓前)_rank', '平均持有时间(出持仓前)_rank', '出重仓前平均收益率_rank',
                         '出全仓前平均收益率_rank',
                         '新股概率(出重仓前)_rank', '新股概率(出持仓前)_rank', '次新股概率(出重仓前)_rank', '次新股概率(出持仓前)_rank', '平均持有时间(出重仓前)',
                         '平均持有时间(出持仓前)', '出重仓前平均收益率', '出全仓前平均收益率','换手率',
                         '左侧概率(出重仓前,半年线)', '左侧概率(出持仓前,半年线)', '左侧概率(出重仓前,年线)', '左侧概率(出持仓前,年线)',
                         '左侧程度(出重仓前,半年线)', '左侧程度(出持仓前,半年线)', '左侧程度(出重仓前,年线)', '左侧程度(出持仓前,年线)',
                         '新股概率(出重仓前)', '新股概率(出持仓前)', '次新股概率(出重仓前)', '次新股概率(出持仓前)', 'asofdate'
                         ]]

    sql="delete from jjpic_stock_p where asofdate='{}'".format(stock_p['asofdate'][0])
    localdb.execute(sql)
    stock_p.to_sql("jjpic_stock_p",con=localdb,index=False,if_exists='append')

    sql="delete from jjpic_stock_tp where asofdate='{}'".format(stock_tp['asofdate'][0])
    localdb.execute(sql)
    stock_tp.to_sql("jjpic_stock_tp", con=localdb, index=False, if_exists='append')

def save_entire_jjpic2db(asofdate1,asofdate2,if_prv=False,fre='Q'):
    if(if_prv):
        jj_base_info = hbdb.db2df("select jjdm,jjjc from st_hedge.t_st_jjxx",db='highuser')
    else:
        jj_base_info = hbdb.db2df("select jjdm,jjjc from st_fund.t_st_gm_jjxx", db='funduser')
    ind_cen=industry_pic_all(jj_base_info,asofdate1,asofdate2,if_prv=if_prv,fre=fre)
    stock_trading_pci_all(jj_base_info,asofdate2,ind_cen,if_percentage=False)
    style_pic_all(jj_base_info,asofdate2,fre='M', if_percentage=False,if_prv=if_prv,fre2=fre)


def save_pic_as_excelfromlocaldb(jjdm_list=None):

    import xlwings as xw

    if(jjdm_list is not None):
        jjdm_con="jjdm in ({})".format(util.list_sql_condition(jjdm_list))
    else:
        jjdm_con='1=1'


    value_p, value_p_hbs, value_sp, value_sp_hbs, size_p, size_p_hbs, size_sp, size_sp_hbs, \
    industry_p, industry_sp, theme_p, theme_sp, industry_detail_df_list, stock_p, stock_tp,\
    jj_performance,industry_contribution_list,ticker_con,theme_exp,ind2_exp\
        ,industry_contribution_perweight_list,style_exp,size_exp= \
        get_pic_from_localdb(jjdm_con)


    filename=r"E:\GitFolder\docs\池报告模板.xlsx"
    app = xw.App(visible=False)
    wb =app.books.open(filename)

    df_list=[industry_p, industry_sp, theme_p, theme_sp,
               industry_detail_df_list[0],industry_detail_df_list[1],industry_detail_df_list[2],
               value_p_hbs, value_sp_hbs, value_p, value_sp, size_p_hbs, size_sp_hbs, size_p, size_sp,
               stock_p,stock_tp,jj_performance,industry_contribution_list[0],
             industry_contribution_list[1],industry_contribution_list[2],ticker_con
        ,industry_contribution_perweight_list[0],industry_contribution_perweight_list[1],industry_contribution_perweight_list[2]]

    sheet_list=['行业画像','行业切换属性','主题画像','主题切换属性','细分行业画像_一级','细分行业画像_二级','细分行业画像_三级',
                '成长价值画像_基于持仓','成长价值切换属性_基于持仓','成长价值画像_基于净值','成长价值切换属性_基于净值',
                '大中小盘画像_基于持仓','大中小盘切换属性_基于持仓','大中小盘画像_基于净值','大中小盘切换属性_基于净值',
                '个股特征画像A','个股特征画像B','基金业绩画像','一级行业贡献','二级行业贡献','三级行业贡献','个股贡献'
        ,'一级行业单位贡献','二级行业单位贡献','三级行业单位贡献']

    newpath = r'E:\GitFolder\docs\私募股多持仓分析\pic_temp'
    ws = wb.sheets['主题画像']

    for pic in ws.pictures:
        pic.delete()
    upper_range =100
    x_position=len(theme_p)+3
    for jjjc in theme_exp['基金简称'].unique():
        data, layout = plot.plotly_area(100 * theme_exp[theme_exp['基金简称']==jjjc].set_index('jsrq').drop('基金简称',axis=1).T,
                                        '{}主题暴露时序'.format(jjjc), upper_range)
        plot.save_pic2local(data, layout, newpath + r"\{}主题暴露时序".format(jjjc))
        ws.pictures.add(newpath + r"\{}主题暴露时序.png".format(jjjc), left=ws.range('A{}'.format(int(x_position))).left, top=ws.range('A{}'.format(int(x_position))).top,
                        width=700, height=350)

        x_position+=30

    ws = wb.sheets['行业画像']
    x_position_list = ['A', 'O', 'AC', 'AQ', 'BE']
    ind2_exp['yjxymc']=[ind_map[x] for x in ind2_exp['ejxymc']]
    for pic in ws.pictures:
        pic.delete()
    x_position=len(theme_p)+3
    for jjjc in theme_exp['基金简称'].unique():
        i = 0
        top5_inds=industry_p.loc[industry_p['基金简称']==jjjc]['前五大行业'].values[0].split(',')
        for inds in top5_inds:
            upper_range =1.2 * ind2_exp.groupby(['基金简称','yjxymc','jsrq']).sum().loc[jjjc,inds.replace("'","")].max().values[0]
            data, layout = plot.plotly_area( (ind2_exp[(ind2_exp['基金简称']==jjjc)
                                                           &(ind2_exp['yjxymc']==inds.replace("'",""))]).pivot_table('zjbl','jsrq','ejxymc').fillna(0).T,
                                            '{0}_{1}_二级行业暴露时序'.format(jjjc,inds.replace("'","")), upper_range)
            plot.save_pic2local(data, layout, newpath + r"\{}二级行业暴露时序".format(jjjc))
            ws.pictures.add(newpath + r"\{}二级行业暴露时序.png".format(jjjc), left=ws.range('{0}{1}'
                                                                                     .format(x_position_list[i],int(x_position))).left, top=ws.range('{0}{1}'
                                                                                                                                                     .format(x_position_list[i],int(x_position))).top,
                            width=700, height=350)
            i+=1
        x_position += 30

    ws = wb.sheets['成长价值画像_基于持仓']
    for pic in ws.pictures:
        pic.delete()
    x_position=len(value_p_hbs)+3
    for jjjc in theme_exp['基金简称'].unique():
        data, layout = plot.plotly_area(style_exp[style_exp['基金简称']==jjjc].pivot_table('zjbl','jsrq','style_type').T,
                                        '{}风格暴露时序'.format(jjjc), 100)
        plot.save_pic2local(data, layout, newpath + r"\{}风格暴露时序".format(jjjc))
        ws.pictures.add(newpath + r"\{}风格暴露时序.png".format(jjjc), left=ws.range('A{0}'
                                                                               .format(int(x_position))).left
                        , top=ws.range('A{0}'.format(int(x_position))).top,width=700, height=350)

        x_position+=28

    ws = wb.sheets['大中小盘画像_基于持仓']
    for pic in ws.pictures:
        pic.delete()
    x_position=len(size_p_hbs)+3
    for jjjc in theme_exp['基金简称'].unique():
        data, layout = plot.plotly_area(size_exp[size_exp['基金简称']==jjjc].pivot_table('zjbl','jsrq','size_type').T,
                                        '{}规模暴露时序'.format(jjjc), 100)
        plot.save_pic2local(data, layout, newpath + r"\{}规模暴露时序".format(jjjc))
        ws.pictures.add(newpath + r"\{}规模暴露时序.png".format(jjjc), left=ws.range('A{0}'
                                                                               .format(int(x_position))).left
                        , top=ws.range('A{0}'.format(int(x_position))).top,width=700, height=350)

        x_position+=28

    ws = wb.sheets['前十大交易时序']
    ws.clear()
    for pic in ws.pictures:
        pic.delete()
    #get the top10 ticker adjusted trade history
    sql="select * from hbs_hld_sl_history where {0} and asofdate='{1}'"\
        .format(jjdm_con,value_p_hbs['asofdate'].unique()[0])
    trade_history=pd.read_sql(sql,con=localdb)
    trade_history=trade_history.sort_values(['jjdm', 'zqdm', 'trade_date'])
    trade_history[['ROE_yj',
       'NETPROFITGROWRATE_yj', 'OPERATINGREVENUEYOY_yj','EST_NET_PROFIT_YOY_yj', 'EST_OPER_REVENUE_YOY_yj', 'ROE_FY1_yj', 'ROE_ej', 'NETPROFITGROWRATE_ej',
       'OPERATINGREVENUEYOY_ej', 'EST_NET_PROFIT_YOY_ej', 'EST_OPER_REVENUE_YOY_ej', 'ROE_FY1_ej','ROE_sj',
       'NETPROFITGROWRATE_sj', 'OPERATINGREVENUEYOY_sj','EST_NET_PROFIT_YOY_sj', 'EST_OPER_REVENUE_YOY_sj', 'ROE_FY1_sj', 'ROE_ticker',
       'NETPROFITGROWRATE_ticker', 'OPERATINGREVENUEYOY_ticker', 'ROE_FY1_ticker',
       'EST_NET_PROFIT_YOY_ticker', 'EST_OPER_REVENUE_YOY_ticker'
       ]]=trade_history[['ROE_yj',
       'NETPROFITGROWRATE_yj', 'OPERATINGREVENUEYOY_yj','EST_NET_PROFIT_YOY_yj', 'EST_OPER_REVENUE_YOY_yj', 'ROE_FY1_yj', 'ROE_ej', 'NETPROFITGROWRATE_ej',
       'OPERATINGREVENUEYOY_ej', 'EST_NET_PROFIT_YOY_ej', 'EST_OPER_REVENUE_YOY_ej', 'ROE_FY1_ej','ROE_sj',
       'NETPROFITGROWRATE_sj', 'OPERATINGREVENUEYOY_sj','EST_NET_PROFIT_YOY_sj', 'EST_OPER_REVENUE_YOY_sj', 'ROE_FY1_sj', 'ROE_ticker',
       'NETPROFITGROWRATE_ticker', 'OPERATINGREVENUEYOY_ticker', 'ROE_FY1_ticker',
       'EST_NET_PROFIT_YOY_ticker', 'EST_OPER_REVENUE_YOY_ticker'
       ]]/100
    trade_history['ajduested_sl_change']=\
        trade_history[['jjdm','zqdm','adjuested_sl']].groupby(['jjdm','zqdm']).pct_change().fillna(0)

    y_position=0
    x_position_list=['A','O','AC','AQ','BE']

    for jjdm in jjdm_list:
        print(jjdm)
        tempdf=trade_history[trade_history['jjdm']==jjdm]
        top10_tickers=tempdf['zqdm'].unique().tolist()


        #calculate the sl change weight in all positive or negative change :
        tempdf=pd.concat([pd.merge(tempdf[tempdf['ajduested_sl_change'] > 0],
                        tempdf[tempdf['ajduested_sl_change'] > 0].groupby('zqdm').sum()['ajduested_sl_change'].to_frame('sumed_change_by_ticker'),how='left',on='zqdm'),
                          pd.merge(tempdf[tempdf['ajduested_sl_change'] < 0],
                                   tempdf[tempdf['ajduested_sl_change'] < 0].groupby('zqdm').sum()[
                                       'ajduested_sl_change'].to_frame('sumed_change_by_ticker'), how='left', on='zqdm'),
                          tempdf[tempdf['ajduested_sl_change']==0]
                          ],axis=0)

        tempdf=tempdf.sort_values(['jjdm', 'zqdm', 'trade_date']).reset_index(drop=True)
        tempdf['sl_change_weight']=0

        tempdf.loc[tempdf['ajduested_sl_change'] > 0,'sl_change_weight']=\
            tempdf[tempdf['ajduested_sl_change'] > 0]['ajduested_sl_change']/\
            tempdf[tempdf['ajduested_sl_change'] > 0]['sumed_change_by_ticker']
        tempdf.loc[tempdf['ajduested_sl_change'] < 0,'sl_change_weight']=\
            tempdf[tempdf['ajduested_sl_change'] < 0]['ajduested_sl_change']/\
            tempdf[tempdf['ajduested_sl_change'] < 0]['sumed_change_by_ticker']
        #calculated the weighed average buy and sell timing financial stats
        financial_col=[ 'ROE_yj',
       'NETPROFITGROWRATE_yj', 'OPERATINGREVENUEYOY_yj', 'PE_yj', 'PEG_yj',
       'EST_NET_PROFIT_YOY_yj', 'EST_OPER_REVENUE_YOY_yj', 'ROE_FY1_yj',
       'PE_FY1_yj', 'PEG_FY1_yj', 'ROE_rank_yj', 'NETPROFITGROWRATE_rank_yj',
       'OPERATINGREVENUEYOY_rank_yj', 'PE_rank_yj', 'PEG_rank_yj',
       'EST_NET_PROFIT_YOY_rank_yj', 'EST_OPER_REVENUE_YOY_rank_yj',
       'ROE_FY1_rank_yj', 'PE_FY1_rank_yj', 'PEG_FY1_rank_yj', 'ROE_ej',
       'NETPROFITGROWRATE_ej', 'OPERATINGREVENUEYOY_ej', 'PE_ej', 'PEG_ej',
       'EST_NET_PROFIT_YOY_ej', 'EST_OPER_REVENUE_YOY_ej', 'ROE_FY1_ej',
       'PE_FY1_ej', 'PEG_FY1_ej', 'ROE_rank_ej', 'NETPROFITGROWRATE_rank_ej',
       'OPERATINGREVENUEYOY_rank_ej', 'PE_rank_ej', 'PEG_rank_ej',
       'EST_NET_PROFIT_YOY_rank_ej', 'EST_OPER_REVENUE_YOY_rank_ej',
       'ROE_FY1_rank_ej', 'PE_FY1_rank_ej', 'PEG_FY1_rank_ej', 'ROE_sj',
       'NETPROFITGROWRATE_sj', 'OPERATINGREVENUEYOY_sj', 'PE_sj', 'PEG_sj',
       'EST_NET_PROFIT_YOY_sj', 'EST_OPER_REVENUE_YOY_sj', 'ROE_FY1_sj',
       'PE_FY1_sj', 'PEG_FY1_sj', 'ROE_rank_sj', 'NETPROFITGROWRATE_rank_sj',
       'OPERATINGREVENUEYOY_rank_sj', 'PE_rank_sj', 'PEG_rank_sj',
       'EST_NET_PROFIT_YOY_rank_sj', 'EST_OPER_REVENUE_YOY_rank_sj',
       'ROE_FY1_rank_sj', 'PE_FY1_rank_sj', 'PEG_FY1_rank_sj','ROE_ticker', 'NETPROFITGROWRATE_ticker',
       'OPERATINGREVENUEYOY_ticker', 'PE_ticker', 'PEG_ticker',
       'PE_FY1_ticker', 'PEG_FY1_ticker', 'ROE_FY1_ticker',
       'EST_NET_PROFIT_YOY_ticker', 'EST_OPER_REVENUE_YOY_ticker',
       'ROE_rank_ticker', 'NETPROFITGROWRATE_rank_ticker',
       'OPERATINGREVENUEYOY_rank_ticker', 'PE_rank_ticker', 'PEG_rank_ticker',
       'EST_NET_PROFIT_YOY_rank_ticker', 'EST_OPER_REVENUE_YOY_rank_ticker',
       'ROE_FY1_rank_ticker', 'PE_FY1_rank_ticker', 'PEG_FY1_rank_ticker']
        tempdf[[x + '_margin_change' for x in financial_col]]=tempdf.groupby(['jjdm','zqdm'])[financial_col].diff()
        financial_col=financial_col+[x + '_margin_change' for x in financial_col]
        for col in financial_col:
            tempdf[col+'_w']=tempdf[col]*tempdf['sl_change_weight']
        buy_timing=tempdf[tempdf['ajduested_sl_change'] > 0].groupby('zqdm').sum()[[x+'_w' for x in financial_col]+['sumed_change_by_ticker']].reset_index(drop=False)
        sell_timing=tempdf[tempdf['ajduested_sl_change'] < 0].groupby('zqdm').sum()[[x+'_w' for x in financial_col]+['sumed_change_by_ticker']].reset_index(drop=False)
        total_buy=0
        total_sell=0

        sell_timing.columns=['zqdm']+financial_col+['sumed_change_by_ticker']
        buy_timing.columns =['zqdm']+financial_col+['sumed_change_by_ticker']

        length_b=len(buy_timing)
        length_s = len(sell_timing)

        #get ticker chinese name
        sql="select zqdm,zqjc from st_ashare.t_st_ag_zqzb where zqdm in ({0}) and zqlb in (1,2)"\
            .format(util.list_sql_condition(top10_tickers))
        tempdf=pd.merge(tempdf,hbdb.db2df(sql,db='alluser'),how='left',on='zqdm')

        if(length_b>0):
            for n in range(length_b):
                total_buy += buy_timing.iloc[n][financial_col] * buy_timing.iloc[n][
                                  'sumed_change_by_ticker']
            buy_timing.loc[length_b] = total_buy / buy_timing['sumed_change_by_ticker'].sum()
            buy_timing.loc[length_b, 'zqdm'] = '买入平均'
            buy_timing = pd.merge(buy_timing, hbdb.db2df(sql, db='alluser'), how='left', on='zqdm')
            buy_timing.loc[buy_timing['zqjc'].notnull(), 'zqdm'] = buy_timing['zqjc'] + '_买入'
        else:
            buy_timing=[]

        if (length_s > 0):
            for n in range(length_s):
                total_sell += sell_timing.iloc[n][financial_col] * sell_timing.iloc[n][
                                  'sumed_change_by_ticker']


            sell_timing.loc[length_s] = total_sell / sell_timing['sumed_change_by_ticker'].sum()
            sell_timing.loc[length_s, 'zqdm'] = '平均卖出'
            sell_timing = pd.merge(sell_timing, hbdb.db2df(sql, db='alluser'), how='left', on='zqdm')
            sell_timing.loc[sell_timing['zqjc'].notnull(), 'zqdm'] = sell_timing['zqjc'] + '_卖出'
        else:
            sell_timing=[]

        trade_property=pd.concat([buy_timing, sell_timing], axis=0)
        trade_property.drop(['zqjc','sumed_change_by_ticker'],axis=1,inplace=True)

        tempdf.drop([x+'_w' for x in financial_col],axis=1,inplace=True)

        trade_property.columns=['证券简称', 'ROE_一级行业', '净利增速_一级行业', '主营收入增速_一级行业',
       'PE_一级行业', 'PEG_一级行业', '净利增速预期_一级行业', '主营收入增速预期_一级行业',
       'ROE预期_一级行业', 'PE预期_一级行业', 'PEG预期_一级行业', 'ROE_分位数_一级行业',
       '净利增速_分位数_一级行业', '主营收入增速_分位数_一级行业',
       'PE_分位数_一级行业', 'PEG_分位数_一级行业', '净利增速预期_分位数_一级行业',
       '主营收入增速预期_分位数_一级行业', 'ROE预期_分位数_一级行业', 'PE预期_分位数_一级行业',
       'PEG预期_分位数_一级行业', 'ROE_二级行业', '净利增速_二级行业',
       '主营收入增速_二级行业', 'PE_二级行业', 'PEG_二级行业', '净利增速预期_二级行业',
       '主营收入增速预期_二级行业', 'ROE预期_二级行业', 'PE预期_二级行业', 'PEG预期_二级行业',
       'ROE_分位数_二级行业', '净利增速_分位数_二级行业',
       '主营收入增速_分位数_二级行业', 'PE_分位数_二级行业', 'PEG_分位数_二级行业',
       '净利增速预期_分位数_二级行业', '主营收入增速预期_分位数_二级行业',
       'ROE预期_分位数_二级行业', 'PE预期_分位数_二级行业', 'PEG预期_分位数_二级行业', 'ROE_三级行业',
       '净利增速_三级行业', '主营收入增速_三级行业', 'PE_三级行业', 'PEG_三级行业',
       '净利增速预期_三级行业', '主营收入增速预期_三级行业', 'ROE预期_三级行业',
       'PE预期_三级行业', 'PEG预期_三级行业', 'ROE_分位数_三级行业', '净利增速_分位数_三级行业',
       '主营收入增速_分位数_三级行业', 'PE_分位数_三级行业', 'PEG_分位数_三级行业',
       '净利增速预期_分位数_三级行业', '主营收入增速预期_分位数_三级行业',
       'ROE预期_分位数_三级行业', 'PE预期_分位数_三级行业', 'PEG预期_分位数_三级行业', 'ROE_个股',
       '净利增速_个股', '主营收入增速_个股', 'PE_个股',
       'PEG_个股', 'PE预期_个股', 'PEG预期_个股', 'ROE预期_个股',
       '净利增速预期_个股', '主营收入增速预期_个股',
       'ROE_分位数_个股', '净利增速_分位数_个股',
       '主营收入增速_分位数_个股', 'PE_分位数_个股', 'PEG_分位数_个股',
       '净利增速预期_分位数_个股', '主营收入增速预期_分位数_个股',
       'ROE预期_分位数_个股', 'PE预期_分位数_个股', 'PEG预期_分位数_个股','ROE_一级行业_边际变动', '净利增速_一级行业_边际变动', '主营收入增速_一级行业_边际变动',
       'PE_一级行业_边际变动', 'PEG_一级行业_边际变动', '净利增速预期_一级行业_边际变动', '主营收入增速预期_一级行业_边际变动',
       'ROE预期_一级行业_边际变动', 'PE预期_一级行业_边际变动', 'PEG预期_一级行业_边际变动', 'ROE_分位数_一级行业_边际变动',
       '净利增速_分位数_一级行业_边际变动', '主营收入增速_分位数_一级行业_边际变动',
       'PE_分位数_一级行业_边际变动', 'PEG_分位数_一级行业_边际变动', '净利增速预期_分位数_一级行业_边际变动',
       '主营收入增速预期_分位数_一级行业_边际变动', 'ROE预期_分位数_一级行业_边际变动', 'PE预期_分位数_一级行业_边际变动',
       'PEG预期_分位数_一级行业_边际变动', 'ROE_二级行业_边际变动', '净利增速_二级行业_边际变动',
       '主营收入增速_二级行业_边际变动', 'PE_二级行业_边际变动', 'PEG_二级行业_边际变动', '净利增速预期_二级行业_边际变动',
       '主营收入增速预期_二级行业_边际变动', 'ROE预期_二级行业_边际变动', 'PE预期_二级行业_边际变动', 'PEG预期_二级行业_边际变动',
       'ROE_分位数_二级行业_边际变动', '净利增速_分位数_二级行业_边际变动',
       '主营收入增速_分位数_二级行业_边际变动', 'PE_分位数_二级行业_边际变动', 'PEG_分位数_二级行业_边际变动',
       '净利增速预期_分位数_二级行业_边际变动', '主营收入增速预期_分位数_二级行业_边际变动',
       'ROE预期_分位数_二级行业_边际变动', 'PE预期_分位数_二级行业_边际变动', 'PEG预期_分位数_二级行业_边际变动', 'ROE_三级行业_边际变动',
       '净利增速_三级行业_边际变动', '主营收入增速_三级行业_边际变动', 'PE_三级行业_边际变动', 'PEG_三级行业_边际变动',
       '净利增速预期_三级行业_边际变动', '主营收入增速预期_三级行业_边际变动', 'ROE预期_三级行业_边际变动',
       'PE预期_三级行业_边际变动', 'PEG预期_三级行业_边际变动', 'ROE_分位数_三级行业_边际变动', '净利增速_分位数_三级行业_边际变动',
       '主营收入增速_分位数_三级行业_边际变动', 'PE_分位数_三级行业_边际变动', 'PEG_分位数_三级行业_边际变动',
       '净利增速预期_分位数_三级行业_边际变动', '主营收入增速预期_分位数_三级行业_边际变动',
       'ROE预期_分位数_三级行业_边际变动', 'PE预期_分位数_三级行业_边际变动', 'PEG预期_分位数_三级行业_边际变动', 'ROE_个股_边际变动',
       '净利增速_个股_边际变动', '主营收入增速_个股_边际变动', 'PE_个股_边际变动',
       'PEG_个股_边际变动', 'PE预期_个股_边际变动', 'PEG预期_个股_边际变动', 'ROE预期_个股_边际变动',
       '净利增速预期_个股_边际变动', '主营收入增速预期_个股_边际变动',
       'ROE_分位数_个股_边际变动', '净利增速_分位数_个股_边际变动',
       '主营收入增速_分位数_个股_边际变动', 'PE_分位数_个股_边际变动', 'PEG_分位数_个股_边际变动',
       '净利增速预期_分位数_个股_边际变动', '主营收入增速预期_分位数_个股_边际变动',
       'ROE预期_分位数_个股_边际变动', 'PE预期_分位数_个股_边际变动', 'PEG预期_分位数_个股_边际变动']
        trade_property['基金名称']=value_p_hbs[value_p_hbs['jjdm'] == jjdm]['基金简称'].values[0]
        trade_property=trade_property[['基金名称','证券简称','ROE_个股_边际变动',
       '净利增速_个股_边际变动', '主营收入增速_个股_边际变动', 'PE_个股_边际变动',
       'PEG_个股_边际变动', 'PE预期_个股_边际变动', 'PEG预期_个股_边际变动', 'ROE预期_个股_边际变动',
       '净利增速预期_个股_边际变动', '主营收入增速预期_个股_边际变动','ROE_二级行业_边际变动', '净利增速_二级行业_边际变动',
       '主营收入增速_二级行业_边际变动', 'PE_二级行业_边际变动', 'PEG_二级行业_边际变动', '净利增速预期_二级行业_边际变动',
       '主营收入增速预期_二级行业_边际变动', 'ROE预期_二级行业_边际变动', 'PE预期_二级行业_边际变动', 'PEG预期_二级行业_边际变动','ROE_三级行业_边际变动',
       '净利增速_三级行业_边际变动', '主营收入增速_三级行业_边际变动', 'PE_三级行业_边际变动', 'PEG_三级行业_边际变动',
       '净利增速预期_三级行业_边际变动', '主营收入增速预期_三级行业_边际变动', 'ROE预期_三级行业_边际变动',
       'PE预期_三级行业_边际变动', 'PEG预期_三级行业_边际变动', 'ROE_分位数_三级行业_边际变动', '净利增速_分位数_三级行业_边际变动',
       '主营收入增速_分位数_三级行业_边际变动', 'PE_分位数_三级行业_边际变动', 'PEG_分位数_三级行业_边际变动',
       '净利增速预期_分位数_三级行业_边际变动', '主营收入增速预期_分位数_三级行业_边际变动','ROE_分位数_个股_边际变动', '净利增速_分位数_个股_边际变动',
       '主营收入增速_分位数_个股_边际变动', 'PE_分位数_个股_边际变动', 'PEG_分位数_个股_边际变动',
       '净利增速预期_分位数_个股_边际变动', '主营收入增速预期_分位数_个股_边际变动',
       'ROE预期_分位数_个股_边际变动', 'PE预期_分位数_个股_边际变动', 'PEG预期_分位数_个股_边际变动','ROE_分位数_一级行业_边际变动',
       '净利增速_分位数_一级行业_边际变动', '主营收入增速_分位数_一级行业_边际变动',
       'PE_分位数_一级行业_边际变动', 'PEG_分位数_一级行业_边际变动', '净利增速预期_分位数_一级行业_边际变动',
       '主营收入增速预期_分位数_一级行业_边际变动', 'ROE预期_分位数_一级行业_边际变动', 'PE预期_分位数_一级行业_边际变动',
       'PEG预期_分位数_一级行业_边际变动', 'ROE_分位数_二级行业_边际变动', '净利增速_分位数_二级行业_边际变动',
       '主营收入增速_分位数_二级行业_边际变动', 'PE_分位数_二级行业_边际变动', 'PEG_分位数_二级行业_边际变动',
       '净利增速预期_分位数_二级行业_边际变动', '主营收入增速预期_分位数_二级行业_边际变动',
       'ROE预期_分位数_二级行业_边际变动', 'PE预期_分位数_二级行业_边际变动', 'PEG预期_分位数_二级行业_边际变动','ROE_分位数_三级行业_边际变动', '净利增速_分位数_三级行业_边际变动',
       '主营收入增速_分位数_三级行业_边际变动', 'PE_分位数_三级行业_边际变动', 'PEG_分位数_三级行业_边际变动',
       '净利增速预期_分位数_三级行业_边际变动', '主营收入增速预期_分位数_三级行业_边际变动',
       'ROE预期_分位数_三级行业_边际变动', 'PE预期_分位数_三级行业_边际变动', 'PEG预期_分位数_三级行业_边际变动','ROE_个股',
       '净利增速_个股', '主营收入增速_个股', 'PE_个股',
       'PEG_个股', 'PE预期_个股', 'PEG预期_个股', 'ROE预期_个股',
       '净利增速预期_个股', '主营收入增速预期_个股','ROE_二级行业', '净利增速_二级行业',
       '主营收入增速_二级行业', 'PE_二级行业', 'PEG_二级行业', '净利增速预期_二级行业',
       '主营收入增速预期_二级行业', 'ROE预期_二级行业', 'PE预期_二级行业', 'PEG预期_二级行业','ROE_三级行业',
       '净利增速_三级行业', '主营收入增速_三级行业', 'PE_三级行业', 'PEG_三级行业',
       '净利增速预期_三级行业', '主营收入增速预期_三级行业', 'ROE预期_三级行业',
       'PE预期_三级行业', 'PEG预期_三级行业', 'ROE_分位数_三级行业', '净利增速_分位数_三级行业',
       '主营收入增速_分位数_三级行业', 'PE_分位数_三级行业', 'PEG_分位数_三级行业',
       '净利增速预期_分位数_三级行业', '主营收入增速预期_分位数_三级行业','ROE_分位数_个股', '净利增速_分位数_个股',
       '主营收入增速_分位数_个股', 'PE_分位数_个股', 'PEG_分位数_个股',
       '净利增速预期_分位数_个股', '主营收入增速预期_分位数_个股',
       'ROE预期_分位数_个股', 'PE预期_分位数_个股', 'PEG预期_分位数_个股','ROE_分位数_一级行业',
       '净利增速_分位数_一级行业', '主营收入增速_分位数_一级行业',
       'PE_分位数_一级行业', 'PEG_分位数_一级行业', '净利增速预期_分位数_一级行业',
       '主营收入增速预期_分位数_一级行业', 'ROE预期_分位数_一级行业', 'PE预期_分位数_一级行业',
       'PEG预期_分位数_一级行业', 'ROE_分位数_二级行业', '净利增速_分位数_二级行业',
       '主营收入增速_分位数_二级行业', 'PE_分位数_二级行业', 'PEG_分位数_二级行业',
       '净利增速预期_分位数_二级行业', '主营收入增速预期_分位数_二级行业',
       'ROE预期_分位数_二级行业', 'PE预期_分位数_二级行业', 'PEG预期_分位数_二级行业','ROE_分位数_三级行业', '净利增速_分位数_三级行业',
       '主营收入增速_分位数_三级行业', 'PE_分位数_三级行业', 'PEG_分位数_三级行业',
       '净利增速预期_分位数_三级行业', '主营收入增速预期_分位数_三级行业',
       'ROE预期_分位数_三级行业', 'PE预期_分位数_三级行业', 'PEG预期_分位数_三级行业']]


        m = 0
        # get the stock price data
        sql = """
          select b.SecuCode as ZQDM,a.TradingDay as JYRQ,a.BackwardPrice as SPJG from hsjy_gg.SecuMain b left join hsjy_gg.QT_PerformanceData a on a.InnerCode=b.InnerCode where b.SecuCode in ({0})  and a.TradingDay>=to_date('{1}','yyyymmdd') and  a.TradingDay<=to_date('{2}','yyyymmdd')
           """.format(util.list_sql_condition(top10_tickers),
                      str(int(trade_history['trade_date'].min())-100),
                      (datetime.datetime.strptime(trade_history['trade_date'].max(), '%Y%m%d')+datetime.timedelta(days=30)).strftime('%Y%m%d') )
        price_df = hbdb.db2df(sql, db='readonly')

        sql = """
          select b.SecuCode as ZQDM,a.TradingDay as JYRQ,a.BackwardPrice as SPJG from hsjy_gg.SecuMain b left join hsjy_gg.LC_STIBPerformanceData a on a.InnerCode=b.InnerCode where b.SecuCode in ({0})  and a.TradingDay>=to_date('{1}','yyyymmdd') and  a.TradingDay<=to_date('{2}','yyyymmdd')
           """.format(util.list_sql_condition(top10_tickers),
                      str(int(trade_history['trade_date'].min())-100),
                      (datetime.datetime.strptime(trade_history['trade_date'].max(), '%Y%m%d')+datetime.timedelta(days=30)).strftime('%Y%m%d'))
        price_kcb_df = hbdb.db2df(sql, db='readonly')
        price_df = pd.concat([price_df, price_kcb_df], axis=0).drop('ROW_ID', axis=1)
        price_df.sort_values('JYRQ', inplace=True)
        price_df['JYRQ'] = price_df['JYRQ'].str[0:10].str.replace('-', '')

        y_position += 1
        ws["A{}".format(int(y_position))].options(pd.DataFrame,
                                             header=1, index=False, expand='table').value =trade_property
        y_position+=23

        for ticker in top10_tickers:
            df_bar=tempdf[tempdf['zqdm'] == ticker].set_index('trade_date')
            sec_name=df_bar['zqjc'].values[0]
            industry_lv1=df_bar['yjxymc'].values[0]
            industry_lv2 = df_bar['ejxymc'].values[0]
            industry_lv3 = df_bar['sjxymc'].values[0]
            df_bar=df_bar[['adjuested_sl','sl','NETPROFITGROWRATE_sj',
                           'NETPROFITGROWRATE_ticker','PE_sj','PE_ticker','PE_FY1_sj','PE_FY1_ticker']]
            df_line=(price_df[price_df['ZQDM'] == ticker].set_index('JYRQ')['SPJG']).to_frame('股价')
            df_bar=pd.merge(df_line,df_bar,
                            how='left',left_index=True,right_index=True).fillna(0)[['adjuested_sl','sl','NETPROFITGROWRATE_sj',
                           'NETPROFITGROWRATE_ticker','PE_sj','PE_ticker','PE_FY1_sj','PE_FY1_ticker']]
            df_bar['index_count'] = df_bar.reset_index().index
            for position in df_bar[df_bar['sl']!=0]['index_count']:
                df_bar.loc[(df_bar['index_count']<=position)&(df_bar['index_count']>=position-10),'sl']=\
                    df_bar[df_bar['index_count']==position]['sl'].values[0]
                df_bar.loc[(df_bar['index_count']<=position-10)&(df_bar['index_count']>=position-20),'adjuested_sl']=\
                    df_bar[df_bar['index_count']==position]['adjuested_sl'].values[0]

            data,layout=plot.plotly_line_and_bar(df_line,
                                                 df_bar[['sl','adjuested_sl']].rename(columns={'sl':'实际手数',"adjuested_sl":"调整后手数"})
                                                 ,sec_name+"_"+industry_lv1+"_"+industry_lv2+"_"+industry_lv3,
                                                 figsize=(max(len(df_line)*2,700), max(len(df_line),350)))
            annotations=get_annotations(df_bar[['adjuested_sl','sl','NETPROFITGROWRATE_sj',
                           'NETPROFITGROWRATE_ticker','PE_sj','PE_ticker','PE_FY1_sj','PE_FY1_ticker']])
            plot.save_pic2local(data, layout, newpath + r"\{}".format(jjdm+sec_name),annotations=annotations)
            ws.pictures.add(newpath + r"\{}.png".format(jjdm+sec_name),
                            left=ws.range('{0}{1}'.format(x_position_list[m],int(y_position))).left, top=ws.range('{0}{1}'.format(x_position_list[m],int(y_position))).top,
                            width=700, height=350)
            m += 1
            if(m>4):
                m=0
                y_position+=27

    for i in range(len(sheet_list)) :

        ws = wb.sheets[sheet_list[i]]
        ws.clear()
        ws["A1"].options(pd.DataFrame, header=1, index=False, expand='table').value = df_list[i]
        print('{} done'.format(sheet_list[i]))

    wb.save(filename)
    wb.close()
    app.quit()

    # writer=pd.ExcelWriter(r"E:\GitFolder\docs\公募核心池报告.xlsx")
    # industry_p.to_excel(r"E:\GitFolder\docs\公募核心池报告.xlsx", sheet_name="行业画像", index=False)
    # writer.save()


if __name__ == '__main__':


    print('')

    # prv_pic=pd.DataFrame()
    # for table in ['jjpic_prv_industry_p','jjpic_prv_industry_p_monthly',
    #               'jjpic_prv_value_p_hbs','jjpic_prv_monthly_value_p_hbs',
    #               'jjpic_prv_size_p_hbs','jjpic_prv_monthly_size_p_hbs']:
    #     temppic=pd.read_sql("select * from {}".format(table),con=localdb)
    #     if(len(prv_pic)==0):
    #         prv_pic=temppic
    #     else:
    #         prv_pic=pd.merge(prv_pic,temppic,how='left',on='jjdm')
    # prv_pic.to_excel('prv_pic_comparison.xlsx', index=False)

    #plot_picatlocal('166006')

    #save_entire_jjpic2db(asofdate1='20220831',asofdate2='20220630',if_prv=False,fre='Q')

    #jjdm_list=['003232','000117','001179','001476','006111','005583','001490','260110',
               # '001373','001417','233015','070032','000083','000965','000251','163805',
               # '481001','100056','000697','005576']




    #jj ind exp history
    # jjdm_list = ['005775', '001583']
    # ind_exp=pd.read_sql("select * from hbs_industry_class1_exp",con=localdb)
    # ind_exp['zjbl_rank']=ind_exp.groupby(['jsrq','yjxymc']).rank(method='min')['zjbl']
    # ind_exp=pd.merge(ind_exp,
    #                  ind_exp.groupby(['jsrq','yjxymc']).count()['zjbl'].reset_index().rename(columns={'zjbl':'count'}),
    #                  how='left',on=['jsrq','yjxymc'])
    # ind_exp['zjbl_rank']=ind_exp['zjbl_rank']/ind_exp['count']

    # style_exp=pd.read_sql("select * from hbs_style_exp",con=localdb)
    # style_exp['zjbl'] = style_exp['zjbl']/100
    # style_exp['zjbl_rank'] = style_exp.groupby(['jsrq', 'style_type']).rank(method='min')['zjbl']
    # style_exp=pd.merge(style_exp,
    #                  style_exp.groupby(['jsrq','style_type']).count()['zjbl'].reset_index().rename(columns={'zjbl':'count'}),
    #                  how='left',on=['jsrq','style_type'])
    # style_exp['zjbl_rank']=style_exp['zjbl_rank']/style_exp['count']


    #
    # for jjdm in jjdm_list:
    # #     tempdf=ind_exp[ind_exp['jjdm']==jjdm][['jsrq','yjxymc','zjbl','zjbl_rank','know_weight']]
    #     tempdf=style_exp[style_exp['jjdm']==jjdm][['jsrq','style_type','zjbl','zjbl_rank']]
    #     picdf=pd.DataFrame()
    #     picdf['jsrq']=tempdf['jsrq'].unique().tolist()
    #     picdf=pd.merge(picdf,tempdf[['jsrq','know_weight']],how='left',on='jsrq')
    #     top5=tempdf.groupby('yjxymc').mean().sort_values('zjbl')[-5:].index.to_list()
    #     for ind in top5:
    #         picdf=pd.merge(picdf,tempdf[tempdf['yjxymc']==ind][['jsrq','zjbl','zjbl_rank']]
    #                        ,how='left',on='jsrq').rename(columns={'zjbl':ind,'zjbl_rank':ind+"_rank"})
    #     style_list=tempdf['style_type'].unique().tolist()
    #     for ind in style_list:
    #         picdf=pd.merge(picdf,tempdf[tempdf['style_type']==ind][['jsrq','zjbl','zjbl_rank']]
    #                        ,how='left',on='jsrq').rename(columns={'zjbl':ind,'zjbl_rank':ind+"_rank"})
    #     picdf=picdf.set_index('jsrq').fillna(0)
    #     plot=functionality.Plot(1200,600)
    #     plot.plotly_line_style(picdf, jjdm + '占净值比例')
        # plot.plotly_line_style(picdf[style_list],jjdm+'占净值比例')
        # plot.plotly_line_style(picdf[[x+'_rank' for x in style_list]], jjdm + '占净值比例相对排名')



    #
    # mutual_core_jjdm_list=pd.read_sql("select * from core_pool_history where asofdate='202203'",
    #                                   con=localdb)['基金代码'].tolist()
    # value_list=pd.read_sql("SELECT * from jjpic_industry_detail_1 where `行业名称`='银行' and `占持仓比例(时序均值)`>=0.4",
    #                                   con=localdb)['jjdm'].tolist()
    #jjdm_list=['168102','001583','006567','450009','450004','688888','005775']
    #jjdm_list=['168102','001583','006567','450009','450004','688888','005775','005267','161606',]
    #['161606','519133','001975','001856','002340','006624','000739','450004','519126','005241']
    jjdm_list=['161606','519133','001975','001856','002340','006624','000739','450004','519126']
    jjdm_list=['000577','000739','001410','001476','001583','001705','001856','002340','005241','005827','005968','006624','163415','377240','450004','450009','519002','519126','519133','688888']
    jjdm_list=['000739','001476','001856','001975','002340','005241','006624','007449','161606','450004','519126','519133']
    #jjdm_list=['002340','006624','519002','450004','000739','519126','688888','001583','001856','000577','450009','005827','519133','005968','001410','001705','005241','163415','166006','001975']
    #jjdm_list=['377240','000001']
    #jjdm_list=[("000000"+str(x))[-6:] for x in pd.read_excel(r"E:\GitFolder\hbshare\fe\mutual_analysis\similarity_of_005775.xlsx")['jjdm'].tolist()]
    # save_pic_as_excelfromlocaldb(jjdm_list=jjdm_list)
    # #
    # jjdm='000001'
    # plot_picatlocal(jjdm)
    print('Done')

    #
    # jjdm_list=['450004','450009']
    #
    #
    # save_pic_as_excel(jjdm_list)




