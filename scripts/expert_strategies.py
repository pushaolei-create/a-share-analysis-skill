#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
名称：A股终极全量战法扫描器 (v4.0 工业融合版)
架构：面向对象 (OOP) + 强类型注解 + 私有指标模块 + 多维共振打分引擎
适配：Hermes Multi-Agent 架构 & GitHub 开源标准
"""

import sys
import json
from typing import Dict, Any, Optional
import pandas as pd

# 极客容错处理：确保无论环境如何都不会直接崩溃
try:
    import akshare as ak
except ImportError:
    pass

class AShareExpertScanner:
    """
    A股战法扫描核心引擎
    """
    def __init__(self, symbol: str, period: int = 150) -> None:
        # 过滤多余字符，提取纯6位代码
        self.symbol: str = ''.join(filter(str.isdigit, symbol))
        self.period: int = period
        self.df: Optional[pd.DataFrame] = None
        
        # 核心共振打分系统 (0-100制)
        self.score: int = 50
        
        # Agent 专属结构化输出化字典
        self.report: Dict[str, Any] = {
            "symbol": self.symbol,
            "resonance_score": self.score,
            "overall_advice": "",
            "strategy_signals": [],
            "risk_management": {}
        }

    def fetch_data(self) -> bool:
        """拉取历史数据并进行清洗"""
        try:
            df = ak.stock_zh_a_hist(symbol=self.symbol, period="daily", adjust="qfq")
            if df is None or df.empty:
                return False
            
            df = df.tail(self.period).copy()
            df.rename(columns={
                '日期': 'date', '开盘': 'open', '收盘': 'close', 
                '最高': 'high', '最低': 'low', '成交量': 'volume'
            }, inplace=True)
            
            self.df = df
            self.report["date"] = str(self.df.iloc[-1]['date'])
            self.report["current_price"] = float(self.df.iloc[-1]['close'])
            return True
        except Exception:
            return False

    # ---------------------------------------------------------
    # ⚙️ 工业级解耦：私有指标计算模块 (吸取 GPT 模块化优点)
    # ---------------------------------------------------------
    def _calc_moving_averages(self) -> None:
        """计算均线系统与量能均线"""
        for w in [5, 10, 20, 60]:
            self.df[f'MA{w}'] = self.df['close'].rolling(window=w).mean()
        for w in [5, 20]:
            self.df[f'V_MA{w}'] = self.df['volume'].rolling(window=w).mean()

    def _calc_macd(self) -> None:
        """手工推演 MACD 指标 (无第三方重型依赖)"""
        exp1 = self.df['close'].ewm(span=12, adjust=False).mean()
        exp2 = self.df['close'].ewm(span=26, adjust=False).mean()
        self.df['MACD_diff'] = exp1 - exp2
        self.df['MACD_dea'] = self.df['MACD_diff'].ewm(span=9, adjust=False).mean()
        self.df['MACD_hist'] = (self.df['MACD_diff'] - self.df['MACD_dea']) * 2

    def _calc_kdj(self) -> None:
        """手工推演 KDJ 指标 (9, 3, 3)"""
        low_list = self.df['low'].rolling(9, min_periods=9).min()
        high_list = self.df['high'].rolling(9, min_periods=9).max()
        rsv = (self.df['close'] - low_list) / (high_list - low_list) * 100
        self.df['K'] = rsv.ewm(com=2, adjust=False).mean()
        self.df['D'] = self.df['K'].ewm(com=2, adjust=False).mean()
        self.df['J'] = 3 * self.df['K'] - 2 * self.df['D']

    def calculate_indicators(self) -> None:
        """调度所有私有计算模块"""
        self._calc_moving_averages()
        self._calc_macd()
        self._calc_kdj()

    # ---------------------------------------------------------
    # 🧠 共振打分引擎 (保留我们的实战派极客内核)
    # ---------------------------------------------------------
    def _add_signal(self, name: str, status: str, desc: str, score_delta: int = 0) -> None:
        """统一信号装载与计分器"""
        self.score += score_delta
        self.report['strategy_signals'].append({
            "name": name, 
            "status": status, 
            "desc": desc
        })

    def run_strategies(self) -> None:
        """多维战法匹配与得分演算"""
        if self.df is None or len(self.df) < 60:
            return

        latest = self.df.iloc[-1]
        prev = self.df.iloc[-2]
        prev2 = self.df.iloc[-3]
        
        # 1. 60日生命线趋势
        if latest['close'] > latest['MA60']:
            self._add_signal("60日生命线", "✅ 线上多头", "股价稳居60日线上方，大势向好。", 10)
        else:
            self._add_signal("60日生命线", "❌ 线下空头", "股价被压制在60日线下方，弱势特征。", -15)

        # 2. 520战法与短期均线防守
        if latest['MA5'] > latest['MA20']:
            if latest['MA20'] >= prev['MA20']:
                self._add_signal("520我爱你战法", "🔥 强势多头", "5日线上穿20日线且20日线上行，绝佳波段切入点！", 15)
            else:
                self._add_signal("520我爱你战法", "⚠️ 弱势金叉", "5日线上穿20日线，但20日线仍在向下运行。", 5)
        elif latest['close'] < latest['MA20']:
            self._add_signal("短期均线防守", "🚨 破位20日线", "跌破短期防守线，随时准备撤离！", -10)

        # 3. 三金叉觉醒期
        if (latest['MA5'] > latest['MA10']) and (latest['MACD_diff'] > latest['MACD_dea']) and (latest['J'] > latest['K']):
            if latest['close'] > latest['MA60']:
                self._add_signal("三金叉觉醒", "🚀 觉醒期主升浪", "均线、MACD、KDJ三金叉共振！具备主升浪爆发潜力！", 20)
        
        # 4. MACD 做T判定
        if latest['MACD_diff'] > 0 and latest['MACD_hist'] > 0:
            self._add_signal("MACD趋势做T", "💪 水上金叉", "处于0轴上方强势区，支持日内逢低加仓做T。", 10)
        elif latest['MACD_diff'] < 0 and latest['MACD_hist'] > 0:
            self._add_signal("MACD趋势做T", "⚠️ 水下金叉", "仅属于超跌反弹范畴，严禁重仓追高。", 0)

        # 5. K线形态侦测
        max_prev = max(prev['high'], prev2['high'], self.df.iloc[-4]['high'])
        if latest['close'] > latest['open'] and latest['close'] >= max_prev and latest['volume'] > latest['V_MA5']:
            self._add_signal("狮子大张口", "🦁 底部吞没", "放量大阳线强势吞没前三日震荡区间，主力暴力反攻信号！", 15)

        if latest['close'] >= latest['MA60'] and latest['volume'] < latest['V_MA5']:
            self._add_signal("缩量回踩侦测", "🐍 蛇戏水洗盘", "60日线上方出现极其明显的缩量回调，高度疑似洗盘动作。", 5)

        # 确保分数截断在 0-100 之间
        self.score = max(0, min(100, self.score))
        self.report['resonance_score'] = self.score
        
        # 生成 AI 分析师总纲定调
        if self.score >= 80:
            self.report['overall_advice'] = "【极度看涨】多维战法强烈共振，可重仓或坚定持有！"
        elif self.score >= 60:
            self.report['overall_advice'] = "【偏多震荡】趋势向好，建议底仓持有，逢低做T降低成本。"
        elif self.score >= 40:
            self.report['overall_advice'] = "【弱势观望】多空分歧剧烈，暂无明确主升浪特征，控制手痒。"
        else:
            self.report['overall_advice'] = "【破位看跌】技术面已全面恶化，建议清仓规避风险！"

        # 机械化风控纪律输出
        self.report['risk_management'] = {
            "entry_price": float(latest['close']),
            "stop_loss_price": round(float(latest['close']) * 0.95, 2),
            "take_profit_price": round(float(latest['close']) * 1.15, 2),
            "core_rule": "【一根筋纪律】有效跌破5%防守线必须无条件无脑止损，绝不扛单！"
        }

    def get_report_json(self) -> str:
        """返回给 Agent 阅读的纯净 JSON"""
        return json.dumps(self.report, ensure_ascii=False, indent=2)


def main() -> None:
    if len(sys.argv) < 2:
        print(json.dumps({"error": "缺少股票代码参数。用法: python3 expert_strategies.py <代码>"}))
        return
    
    symbol = sys.argv[1]
    scanner = AShareExpertScanner(symbol)
    
    if not scanner.fetch_data():
        print(json.dumps({"error": f"无法获取 {symbol} 数据，请检查网络或确认代码正确。"}))
        return
        
    scanner.calculate_indicators()
    scanner.run_strategies()
    print(scanner.get_report_json())


if __name__ == "__main__":
    main()
