"""
基于私募基金估值表的截面持仓风格归因模块
"""
import pandas as pd
import hbshare as hbs
from hbshare.fe.common.util.config import style_name, industry_name
import datetime
from sqlalchemy import create_engine
from hbshare.quant.Kevin.rm_associated.config import engine_params
from hbshare.fe.common.util.config import factor_map_dict
import plotly
import plotly.graph_objs as go
import plotly.figure_factory as ff


def plot_render(plot_dic, width=1000, height=600, **kwargs):
    kwargs['output_type'] = 'div'
    plot_str = plotly.offline.plot(plot_dic, **kwargs)
    print('%%angular <div style="height: %ipx; width: %spx"> %s </div>' % (height, width, plot_str))


class HoldingAnalysor:
    def __init__(self, fund_name, trade_date, benchmark_id):
        self.fund_name = fund_name
        self.trade_date = trade_date
        self.benchmark_id = benchmark_id
        self._load_data()

    def _load_shift_date(self):
        trade_dt = datetime.datetime.strptime(self.trade_date, '%Y%m%d')
        pre_date = (trade_dt - datetime.timedelta(days=100)).strftime('%Y%m%d')

        sql_script = "SELECT JYRQ, SFJJ, SFZM, SFYM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {}".format(
            pre_date, self.trade_date)
        res = hbs.db_data_query('readonly', sql_script, page_size=5000)
        df = pd.DataFrame(res['data']).rename(
            columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                     "SFZM": "isWeekEnd", "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
        df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
        df['isWeekEnd'] = df['isWeekEnd'].fillna(0).astype(int)
        df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)

        trading_day_list = df[df['isMonthEnd'] == 1]['calendarDate'].tolist()

        return trading_day_list[-1]

    def _load_portfolio_weight_series(self):
        sql_script = "SELECT * FROM private_fund_holding where fund_name = '{}' and trade_date = {}".format(
            self.fund_name, self.trade_date)
        engine = create_engine(engine_params)
        holding_df = pd.read_sql(sql_script, engine)
        holding_df['trade_date'] = holding_df['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))

        # 招商量化精选 special
        # sql_script = "SELECT jsrq as end_date, ggrq as report_date, zqdm as ticker, " \
        #              "zjbl, zgbl, zlbl FROM st_fund.t_st_gm_gpzh where " \
        #              "jjdm = '001917' and jsrq = {}".format(self.trade_date)
        # holding_df = pd.DataFrame(hbs.db_data_query('funduser', sql_script, page_size=5000)['data'])
        # holding_df.rename(columns={"end_date": "trade_date", "zjbl": "weight"}, inplace=True)

        # summary
        # sql_script = "SELECT * FROM private_fund_holding where trade_date = {}".format(self.trade_date)
        # engine = create_engine(engine_params)
        # holding_df = pd.read_sql(sql_script, engine)
        # holding_df['trade_date'] = holding_df['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))
        # holding_df = holding_df[holding_df['fund_name'].str.contains('500')]
        # holding_df['total_weight'] = holding_df.groupby('fund_name')['weight'].transform('sum')
        # holding_df['weight'] = 100 * holding_df['weight'] / holding_df['total_weight']
        # num = len(holding_df['fund_name'].unique())
        # print(num)

        return holding_df.set_index('ticker')['weight'] / 100.
        # return holding_df.groupby('ticker')['weight'].sum() / 100. / num

    def _load_benchmark_weight_series(self, date):
        sql_script = "SELECT * FROM hsjy_gg.SecuMain where SecuCategory = 4 and SecuCode = '{}'".format(
            self.benchmark_id)
        res = hbs.db_data_query('readonly', sql_script)
        index_info = pd.DataFrame(res['data'])
        inner_code = index_info.set_index('SECUCODE').loc[self.benchmark_id, 'INNERCODE']

        sql_script = "SELECT (select a.SecuCode from hsjy_gg.SecuMain a where a.InnerCode = b.InnerCode and " \
                     "rownum = 1) SecuCode, b.EndDate, b.Weight FROM hsjy_gg.LC_IndexComponentsWeight b WHERE " \
                     "b.IndexCode = '{}' and b.EndDate = to_date('{}', 'yyyymmdd')".format(inner_code, date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script)['data'])
        weight_df = data.rename(
            columns={"SECUCODE": "consTickerSymbol", "ENDDATE": "effDate", "WEIGHT": "weight"})

        return weight_df.set_index('consTickerSymbol')['weight'] / 100.

    @staticmethod
    def _load_benchmark_components(date):
        sql_script = "SELECT * FROM hsjy_gg.SecuMain where SecuCategory = 4 and " \
                     "SecuCode in ('000300', '000905', '000852')"
        res = hbs.db_data_query('readonly', sql_script)
        index_info = pd.DataFrame(res['data'])
        inner_code_series = index_info.set_index('SECUCODE')['INNERCODE']

        weight = []
        for benchmark_id in ['000300', '000905', '000852']:
            inner_code = inner_code_series.loc[benchmark_id]
            sql_script = "SELECT (select a.SecuCode from hsjy_gg.SecuMain a where a.InnerCode = b.InnerCode and " \
                         "rownum = 1) SecuCode, b.EndDate, b.Weight FROM hsjy_gg.LC_IndexComponentsWeight b WHERE " \
                         "b.IndexCode = '{}' and b.EndDate = to_date('{}', 'yyyymmdd')".format(inner_code, date)
            data = pd.DataFrame(hbs.db_data_query('readonly', sql_script)['data'])
            weight_df = data.rename(
                columns={"SECUCODE": "ticker", "ENDDATE": "effDate", "WEIGHT": "weight"})
            weight_df['benchmark_id'] = benchmark_id
            weight.append(weight_df[['ticker', 'benchmark_id']])

        return pd.concat(weight)

    @staticmethod
    def _load_style_exposure(date):
        sql_script = "SELECT * FROM st_ashare.r_st_barra_style_factor where TRADE_DATE = '{}'".format(date)
        res = hbs.db_data_query('alluser', sql_script, page_size=5000)
        exposure_df = pd.DataFrame(res['data']).set_index('ticker')
        ind_names = [x.lower() for x in industry_name['sw'].values()]
        exposure_df = exposure_df[style_name + ind_names]

        return exposure_df

    @staticmethod
    def _load_stock_conception(date):
        sql_script = "SELECT * FROM stock_conception where trade_date = {}".format(date)
        engine = create_engine(engine_params)
        concept_df = pd.read_sql(sql_script, engine)
        concept_df['trade_date'] = concept_df['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))
        concept_df = concept_df[['trade_date', 'ticker', 'concept']]

        return concept_df

    def _load_data(self):
        shift_date = self._load_shift_date()
        portfolio_weight_series = self._load_portfolio_weight_series()
        benchmark_weight_series = self._load_benchmark_weight_series(shift_date)
        benchmark_components = self._load_benchmark_components(shift_date)
        style_exposure_df = self._load_style_exposure(shift_date)
        concept_df = self._load_stock_conception(shift_date)

        self.data_param = {
            "portfolio_weight_series": portfolio_weight_series,
            "benchmark_weight_series": benchmark_weight_series,
            "benchmark_components": benchmark_components,
            "style_exposure_df": style_exposure_df,
            "concept_df": concept_df
        }

    @staticmethod
    def plotly_style_bar(df, title_text, figsize=(1000, 600), legend_x=0.30):
        fig_width, fig_height = figsize
        cols = df.columns.tolist()
        color_list = ['rgb(49, 130, 189)', 'rgb(204, 204, 204)', 'rgb(216, 0, 18)']
        data = []
        for i in range(len(cols)):
            col = cols[i]
            trace = go.Bar(
                x=df.index.tolist(),
                y=df[col],
                name=col,
                marker=dict(color=color_list[i])
            )
            data.append(trace)

        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height,
            yaxis=dict(tickfont=dict(size=12), showgrid=True),
            xaxis=dict(showgrid=True),
            legend=dict(orientation="h", x=legend_x),
            template='plotly_white'
        )

        # fig = go.Figure(data=data, layout=layout)

        return data, layout

    @staticmethod
    def plotly_bar(df, title_text, figsize=(1200, 800)):
        fig_width, fig_height = figsize
        cols = df.columns.tolist()
        color_list = ['rgb(49, 130, 189)', 'rgb(204, 204, 204)']
        data = []
        for i in range(len(cols)):
            col = cols[i]
            trace = go.Bar(
                x=df.index.tolist(),
                y=df[col],
                name=col,
                marker=dict(color=color_list[i])
            )
            data.append(trace)

        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height,
            yaxis=dict(tickfont=dict(size=12), showgrid=True),
            xaxis=dict(showgrid=True),
            legend=dict(orientation="h", x=0.38),
            template='plotly_white'
        )

        # fig = go.Figure(data=data, layout=layout)

        return data, layout

    @staticmethod
    def plotly_pie(df, title_text, figsize=(800, 600)):
        fig_width, fig_height = figsize
        labels = df.index.tolist()
        values = df.values.round(3).tolist()
        data = [go.Pie(labels=labels, values=values, hoverinfo="label+percent",
                       texttemplate="%{label}: %{percent}")]
        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height
        )

        # fig = go.Figure(data=data, layout=layout)

        return data, layout

    @staticmethod
    def plotly_displot(df, title_text, figsize=(800, 600)):
        fig_width, fig_height = figsize
        group_labels = ['个股权重', '个股权重偏离']
        fig = ff.create_distplot([df[df['个股权重'] > 1e-8]['个股权重'], df['个股权重偏离']],
                                 group_labels,
                                 show_hist=False,
                                 show_rug=False)
        fig.update_layout(title=title_text,
                          xaxis_title='权重（%）',
                          yaxis_title='density',
                          width=fig_width, height=fig_height,
                          template="plotly_white",
                          showlegend=True,
                          legend=dict(
                              orientation="v",
                              y=1,
                              yanchor="top",
                              x=1.0,
                              xanchor="right")
                          )

        return fig.data, fig.layout

    def get_construct_result(self, isPlot=True):
        portfolio_weight_series = self.data_param.get('portfolio_weight_series')
        benchmark_weight_series = self.data_param.get('benchmark_weight_series') * portfolio_weight_series.sum()
        benchmark_components = self.data_param.get('benchmark_components')
        style_exposure_df = self.data_param.get('style_exposure_df')
        concept_df = self.data_param.get('concept_df')

        # 板块分布
        weight_df = portfolio_weight_series.reset_index().rename(columns={"weight": "port"}).merge(
            benchmark_weight_series.reset_index().rename(columns={"consTickerSymbol": "ticker", "weight": "bm"}),
            on='ticker', how='outer').fillna(0.)
        weight_df.loc[weight_df['ticker'].str.startswith('0'), 'sector'] = '深市'
        weight_df.loc[weight_df['ticker'].str.startswith('60'), 'sector'] = '沪市'
        weight_df.loc[weight_df['ticker'].str.startswith('30'), 'sector'] = '创业板'
        weight_df.loc[weight_df['ticker'].str.startswith('688'), 'sector'] = '科创板'
        sector_distribution = weight_df.groupby('sector')[['port', 'bm']].sum().reset_index().set_index('sector')
        sector_distribution['active'] = sector_distribution['port'] - sector_distribution['bm']

        # 成分股分布
        w_df = pd.merge(portfolio_weight_series.reset_index(), benchmark_components, on='ticker', how='left')
        w_df['benchmark_id'].fillna('other', inplace=True)
        bm_distribution = w_df.groupby('benchmark_id')['weight'].sum().reset_index().replace(
            {"000300": "沪深300", "000905": "中证500", "000852": "中证1000", "other": "1800以外"}).set_index('benchmark_id')
        bm_distribution = bm_distribution['weight']
        bm_distribution.loc['非权益资产'] = 1 - bm_distribution.sum()

        # 风格及行业分布
        idx = portfolio_weight_series.index.union(benchmark_weight_series.index).intersection(
            style_exposure_df.index)

        portfolio_weight_series = portfolio_weight_series.reindex(idx).fillna(0.)
        benchmark_weight_series = benchmark_weight_series.reindex(idx).fillna(0.)
        style_exposure_df = style_exposure_df.reindex(idx).astype(float)
        portfolio_expo = style_exposure_df.T.dot(portfolio_weight_series)
        benchmark_expo = style_exposure_df.T.dot(benchmark_weight_series)
        style_expo = pd.concat([portfolio_expo.to_frame('port'), benchmark_expo.to_frame('bm')], axis=1)
        style_expo['active'] = style_expo['port'] - style_expo['bm']

        reverse_ind = dict([(value.lower(), key) for (key, value) in industry_name['sw'].items()])
        benchmark_id_map = {"000300": "沪深300", "000905": "中证500", "000906": "中证800", "000852": "中证1000"}

        # 概念
        portfolio_weight_series = self.data_param.get('portfolio_weight_series')
        benchmark_weight_series = self.data_param.get('benchmark_weight_series') * portfolio_weight_series.sum()
        concept_df = concept_df.join(pd.get_dummies(concept_df['concept']))
        concept_series = concept_df.groupby('ticker')[concept_df.columns[-8:]].sum()
        idx = portfolio_weight_series.index.union(benchmark_weight_series.index).intersection(
            concept_series.index)
        portfolio_weight_series = portfolio_weight_series.reindex(idx).fillna(0.)
        benchmark_weight_series = benchmark_weight_series.reindex(idx).fillna(0.)
        concept_series = concept_series.reindex(idx).astype(float)
        portfolio_concept = concept_series.T.dot(portfolio_weight_series)
        benchmark_concept = concept_series.T.dot(benchmark_weight_series)
        concept_expo = pd.concat([portfolio_concept.to_frame('port'), benchmark_concept.to_frame('bm')], axis=1)
        concept_expo['active'] = concept_expo['port'] - concept_expo['bm']

        # 个股权重及权重偏离度
        portfolio_weight_series = self.data_param.get('portfolio_weight_series')
        benchmark_weight_series = self.data_param.get('benchmark_weight_series') * portfolio_weight_series.sum()
        weight_df = portfolio_weight_series.to_frame('port').merge(
            benchmark_weight_series.to_frame('bm'), left_index=True, right_index=True, how='outer').fillna(0.)
        weight_df['active'] = (weight_df['port'] - weight_df['bm']).abs()

        # 风格
        style_df = style_expo[['port', 'bm', 'active']].rename(
            columns={"port": self.fund_name, "bm": benchmark_id_map[self.benchmark_id], "active": "主动暴露"}).loc[
            style_name]
        style_df.index = style_df.index.map(factor_map_dict)
        if isPlot:
            data, layout = self.plotly_style_bar(style_df, "横截面持仓风格暴露")
            plot_render({"data": data, "layout": layout})
        # 行业
        ind_df = style_expo[['port', 'bm', 'active']].rename(
            columns={"port": self.fund_name, "bm": benchmark_id_map[self.benchmark_id], "active": "主动暴露"}).iloc[10:]
        ind_df.index = [reverse_ind[x] for x in ind_df.index]
        if isPlot:
            data, layout = self.plotly_style_bar(ind_df, "横截面持仓行业暴露", figsize=(1500, 600), legend_x=0.35)
            plot_render({"data": data, "layout": layout}, width=1500, height=600)
        # 板块分布
        sector_distribution = sector_distribution.rename(
            columns={"port": self.fund_name, "bm": benchmark_id_map[self.benchmark_id], "active": "相对暴露"})
        if isPlot:
            data, layout = self.plotly_style_bar(sector_distribution, "横截面持仓板块暴露")
            plot_render({"data": data, "layout": layout})
        # 成分股分布
        if isPlot:
            data, layout = self.plotly_pie(bm_distribution, "持仓指数成分分布", figsize=(800, 600))
            plot_render({"data": data, "layout": layout}, width=800, height=600)
        # 概念分布
        cp_dis_df = concept_expo[['port', 'bm', 'active']].rename(
            columns={"port": self.fund_name, "bm": benchmark_id_map[self.benchmark_id], "active": "主动暴露"})
        if isPlot:
            data, layout = self.plotly_style_bar(cp_dis_df, "横截面概念持仓暴露")
            plot_render({"data": data, "layout": layout})
        # 个股权重偏离
        weight_df = weight_df.rename(columns={"port": "个股权重", "active": "个股权重偏离"}) * 100
        if isPlot:
            data, layout = self.plotly_displot(weight_df, "个股权重及偏离度分布, 持股数量: {}只".format(
                self.data_param.get('portfolio_weight_series').shape[0]))
            plot_render({"data": data, "layout": layout})

        results = {"style_df": style_df, "ind_df": ind_df,
                   "sector_distribution": sector_distribution, "bm_distribution": bm_distribution,
                   "concept_df": cp_dis_df, "weight_df": weight_df}

        return results


class HoldingDistribution:
    def __init__(self, start_date, end_date, fund_name):
        self.start_date = start_date
        self.end_date = end_date
        self.fund_name = fund_name
        self._load_data()

    def _load_portfolio_weight(self):
        sql_script = "SELECT * FROM private_fund_holding where fund_name = '{}' and " \
                     "trade_date >= {} and trade_date <= {}".format(self.fund_name, self.start_date, self.end_date)
        engine = create_engine(engine_params)
        holding_df = pd.read_sql(sql_script, engine)
        holding_df['trade_date'] = holding_df['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))
        # 归一化
        # holding_df['weight_sum'] = holding_df.groupby('trade_date')['weight'].transform('sum')
        # holding_df['weight'] /= holding_df['weight_sum']

        holding_df['weight'] /= 100.

        return holding_df[['trade_date', 'ticker', 'weight']]

    @staticmethod
    def _load_shift_date(date):
        trade_dt = datetime.datetime.strptime(date, '%Y%m%d')
        pre_date = (trade_dt - datetime.timedelta(days=100)).strftime('%Y%m%d')

        sql_script = "SELECT JYRQ, SFJJ, SFZM, SFYM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {}".format(
            pre_date, date)
        res = hbs.db_data_query('readonly', sql_script, page_size=5000)
        df = pd.DataFrame(res['data']).rename(
            columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                     "SFZM": "isWeekEnd", "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
        df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
        df['isWeekEnd'] = df['isWeekEnd'].fillna(0).astype(int)
        df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)

        trading_day_list = df[df['isMonthEnd'] == 1]['calendarDate'].tolist()

        return trading_day_list[-1]

    @staticmethod
    def _load_benchmark_weight(benchmark_id, shift_date, date):
        sql_script = "SELECT * FROM hsjy_gg.SecuMain where SecuCategory = 4 and SecuCode = '{}'".format(benchmark_id)
        res = hbs.db_data_query('readonly', sql_script)
        index_info = pd.DataFrame(res['data'])
        inner_code = index_info.set_index('SECUCODE').loc[benchmark_id, 'INNERCODE']

        sql_script = "SELECT (select a.SecuCode from hsjy_gg.SecuMain a where a.InnerCode = b.InnerCode and " \
                     "rownum = 1) SecuCode, b.EndDate, b.Weight FROM hsjy_gg.LC_IndexComponentsWeight b WHERE " \
                     "b.IndexCode = '{}' and b.EndDate = to_date('{}', 'yyyymmdd')".format(inner_code, shift_date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script)['data'])
        weight_df = data.rename(
            columns={"SECUCODE": "ticker", "ENDDATE": "effDate", "WEIGHT": "weight"})
        weight_df['benchmark_id'] = benchmark_id
        weight_df['trade_date'] = date

        return weight_df[['trade_date', 'ticker', 'weight', 'benchmark_id']]

    def _load_data(self):
        portfolio_weight_df = self._load_portfolio_weight()
        date_list = sorted(portfolio_weight_df['trade_date'].unique())
        benchmark_weight = []
        for date in date_list:
            shift_date = self._load_shift_date(date)
            weight_300 = self._load_benchmark_weight('000300', shift_date, date)
            weight_500 = self._load_benchmark_weight('000905', shift_date, date)
            weight_1000 = self._load_benchmark_weight('000852', shift_date, date)
            benchmark_weight.append(pd.concat([weight_300, weight_500, weight_1000]))

        benchmark_weight = pd.concat(benchmark_weight)

        self.data_param = {"portfolio_weight": portfolio_weight_df, "benchmark_weight": benchmark_weight}

    def get_construct_result(self):
        data_param = self.data_param
        portfolio_weight = data_param['portfolio_weight']
        benchmark_weight = pd.DataFrame(data_param['benchmark_weight'])

        df = pd.merge(portfolio_weight, benchmark_weight[['trade_date', 'ticker', 'benchmark_id']],
                      on=['trade_date', 'ticker'], how='left').fillna('other')
        distribution_df = df.groupby(['trade_date', 'benchmark_id'])['weight'].sum().reset_index()
        distribution_df = pd.pivot_table(
            distribution_df, index='trade_date', columns='benchmark_id', values='weight').sort_index()
        distribution_df['not_equity'] = 1 - distribution_df.sum(axis=1)

        return distribution_df


class HoldingCompare:
    def __init__(self, trade_date, benchmark_id, include_list):
        self.trade_date = trade_date
        self.benchmark_id = benchmark_id
        self.include_list = include_list
        self._load_data()

    def _load_shift_date(self):
        trade_dt = datetime.datetime.strptime(self.trade_date, '%Y%m%d')
        pre_date = (trade_dt - datetime.timedelta(days=100)).strftime('%Y%m%d')

        sql_script = "SELECT JYRQ, SFJJ, SFZM, SFYM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {}".format(
            pre_date, self.trade_date)
        res = hbs.db_data_query('readonly', sql_script, page_size=5000)
        df = pd.DataFrame(res['data']).rename(
            columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                     "SFZM": "isWeekEnd", "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
        df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
        df['isWeekEnd'] = df['isWeekEnd'].fillna(0).astype(int)
        df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)

        trading_day_list = df[df['isMonthEnd'] == 1]['calendarDate'].tolist()

        return trading_day_list[-1]

    def _load_portfolio_weight_series(self):
        sql_script = "SELECT * FROM private_fund_holding where trade_date = {}".format(self.trade_date)
        engine = create_engine(engine_params)
        holding_df = pd.read_sql(sql_script, engine)
        holding_df['trade_date'] = holding_df['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))
        holding_df = holding_df[holding_df['fund_name'].isin(self.include_list)]
        # holding_df['total_weight'] = holding_df.groupby('fund_name')['weight'].transform('sum')
        # holding_df['weight'] = holding_df['weight'] / holding_df['total_weight']

        return holding_df[['fund_name', 'ticker', 'weight']]

    def _load_benchmark_weight_series(self, date):
        sql_script = "SELECT * FROM hsjy_gg.SecuMain where SecuCategory = 4 and SecuCode = '{}'".format(
            self.benchmark_id)
        res = hbs.db_data_query('readonly', sql_script)
        index_info = pd.DataFrame(res['data'])
        inner_code = index_info.set_index('SECUCODE').loc[self.benchmark_id, 'INNERCODE']

        sql_script = "SELECT (select a.SecuCode from hsjy_gg.SecuMain a where a.InnerCode = b.InnerCode and " \
                     "rownum = 1) SecuCode, b.EndDate, b.Weight FROM hsjy_gg.LC_IndexComponentsWeight b WHERE " \
                     "b.IndexCode = '{}' and b.EndDate = to_date('{}', 'yyyymmdd')".format(inner_code, date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script)['data'])
        weight_df = data.rename(
            columns={"SECUCODE": "consTickerSymbol", "ENDDATE": "effDate", "WEIGHT": "weight"})

        return weight_df.set_index('consTickerSymbol')['weight'] / 100.

    @staticmethod
    def _load_benchmark_components(date):
        sql_script = "SELECT * FROM hsjy_gg.SecuMain where SecuCategory = 4 and " \
                     "SecuCode in ('000300', '000905', '000852')"
        res = hbs.db_data_query('readonly', sql_script)
        index_info = pd.DataFrame(res['data'])
        inner_code_series = index_info.set_index('SECUCODE')['INNERCODE']

        weight = []
        for benchmark_id in ['000300', '000905', '000852']:
            inner_code = inner_code_series.loc[benchmark_id]
            sql_script = "SELECT (select a.SecuCode from hsjy_gg.SecuMain a where a.InnerCode = b.InnerCode and " \
                         "rownum = 1) SecuCode, b.EndDate, b.Weight FROM hsjy_gg.LC_IndexComponentsWeight b WHERE " \
                         "b.IndexCode = '{}' and b.EndDate = to_date('{}', 'yyyymmdd')".format(inner_code, date)
            data = pd.DataFrame(hbs.db_data_query('readonly', sql_script)['data'])
            weight_df = data.rename(
                columns={"SECUCODE": "ticker", "ENDDATE": "effDate", "WEIGHT": "weight"})
            weight_df['benchmark_id'] = benchmark_id
            weight.append(weight_df[['ticker', 'benchmark_id']])

        return pd.concat(weight)

    @staticmethod
    def _load_style_exposure(date):
        sql_script = "SELECT * FROM st_ashare.r_st_barra_style_factor where TRADE_DATE = '{}'".format(date)
        res = hbs.db_data_query('alluser', sql_script, page_size=5000)
        exposure_df = pd.DataFrame(res['data']).set_index('ticker')
        ind_names = [x.lower() for x in industry_name['sw'].values()]
        exposure_df = exposure_df[style_name + ind_names]

        return exposure_df

    @staticmethod
    def _load_stock_conception(date):
        sql_script = "SELECT * FROM stock_conception where trade_date = {}".format(date)
        engine = create_engine(engine_params)
        concept_df = pd.read_sql(sql_script, engine)
        concept_df['trade_date'] = concept_df['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))
        concept_df = concept_df[['trade_date', 'ticker', 'concept']]

        return concept_df

    def _load_data(self):
        shift_date = self._load_shift_date()
        portfolio_weight_series = self._load_portfolio_weight_series()
        benchmark_weight_series = self._load_benchmark_weight_series(shift_date)
        benchmark_components = self._load_benchmark_components(shift_date)
        style_exposure_df = self._load_style_exposure(shift_date)
        concept_df = self._load_stock_conception(shift_date)

        self.data_param = {
            "portfolio_weight_series": portfolio_weight_series,
            "benchmark_weight_series": benchmark_weight_series,
            "benchmark_components": benchmark_components,
            "style_exposure_df": style_exposure_df,
            "concept_df": concept_df
        }

    def run(self):
        portfolio_weight_df = self.data_param.get('portfolio_weight_series')
        portfolio_weight_df = pd.pivot_table(
            portfolio_weight_df, index='ticker', columns='fund_name', values='weight').fillna(0.)
        benchmark_weight_series = self.data_param.get('benchmark_weight_series')
        benchmark_components = self.data_param.get('benchmark_components')
        style_exposure_df = self.data_param.get('style_exposure_df')
        concept_df = self.data_param.get('concept_df')

        # 板块分布
        weight_df = portfolio_weight_df.merge(
            benchmark_weight_series.reset_index().rename(columns={"consTickerSymbol": "ticker", "weight": "bm"}),
            on='ticker', how='outer').fillna(0.)
        weight_df.loc[weight_df['ticker'].str.startswith('0'), 'sector'] = '深市'
        weight_df.loc[weight_df['ticker'].str.startswith('60'), 'sector'] = '沪市'
        weight_df.loc[weight_df['ticker'].str.startswith('30'), 'sector'] = '创业板'
        weight_df.loc[weight_df['ticker'].str.startswith('688'), 'sector'] = '科创板'
        sector_distribution = weight_df.groupby('sector')[self.include_list].sum()
        # 成分股分布
        w_df = pd.merge(portfolio_weight_df.reset_index(), benchmark_components, on='ticker', how='left')
        w_df['benchmark_id'].fillna('other', inplace=True)
        bm_distribution = w_df.groupby('benchmark_id').sum().reset_index().replace(
            {"000300": "沪深300", "000905": "中证500", "000852": "中证1000", "other": "1800以外"}).set_index('benchmark_id')
        # 风格及行业分布
        idx = portfolio_weight_df.index.union(benchmark_weight_series.index).intersection(
            style_exposure_df.index)

        portfolio_weight_series = portfolio_weight_df.reindex(idx).fillna(0.)
        benchmark_weight_series = benchmark_weight_series.reindex(idx).fillna(0.)
        style_exposure_df = style_exposure_df.reindex(idx).astype(float)
        portfolio_expo = style_exposure_df.T.dot(portfolio_weight_series)
        benchmark_expo = style_exposure_df.T.dot(benchmark_weight_series)
        style_expo = pd.concat([portfolio_expo, benchmark_expo.to_frame('bm')], axis=1)
        style_expo = style_expo.sub(style_expo['bm'], axis=0)
        # 概念
        concept_df = concept_df.join(pd.get_dummies(concept_df['concept']))
        concept_series = concept_df.groupby('ticker')[concept_df.columns[-8:]].sum()
        idx = portfolio_weight_df.index.union(benchmark_weight_series.index).intersection(
            concept_series.index)
        portfolio_weight_series = portfolio_weight_df.reindex(idx).fillna(0.)
        benchmark_weight_series = benchmark_weight_series.reindex(idx).fillna(0.)
        concept_series = concept_series.reindex(idx).astype(float)
        portfolio_concept = concept_series.T.dot(portfolio_weight_series)
        benchmark_concept = concept_series.T.dot(benchmark_weight_series)
        concept_expo = pd.concat([portfolio_concept, benchmark_concept.to_frame('bm')], axis=1)
        concept_expo['active'] = concept_expo['port'] - concept_expo['bm']
        # 持仓重合度
        portfolio_weight_df = self.data_param.get('portfolio_weight_series')
        portfolio_weight_df = pd.pivot_table(
            portfolio_weight_df, index='ticker', columns='fund_name', values='weight')
        overlap_df = pd.DataFrame(index=portfolio_weight_df.columns, columns=portfolio_weight_df.columns)
        for i in range(len(portfolio_weight_df.columns)):
            for j in range(len(portfolio_weight_df.columns)):
                if i == j:
                    continue
                else:
                    overlap_df.iloc[i, j] = portfolio_weight_df.T.iloc[[i, j], :].T.dropna().min(axis=1).sum()

        return sector_distribution, bm_distribution, style_expo, concept_expo, overlap_df


if __name__ == '__main__':
    tmp = HoldingAnalysor("顽岩中证500指数增强1号", "20221231", "000905").get_construct_result(isPlot=False)

    # dis_df = HoldingDistribution('20210310', '20220602', '因诺聚配中证500指数增强').get_construct_result()
    # print(dis_df)

    # name_list = ['因诺聚配中证500指数增强', '星阔广厦1号中证500指数增强', '概率500指增2号', '乾象中证500指数增强1号',
    #              '顽岩中证500指数增强1号', '伯兄熙宁', '赫富500指数增强一号']
    # HoldingCompare('20221130', '000905', name_list).run()