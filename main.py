import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
import re
import urllib.request
import urllib.parse
from datetime import datetime
from log_parser import LogParser
import time

class RetributionPaladinAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("怀旧服惩戒骑士分析工具")
        self.root.geometry("1000x700")
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=("微软雅黑", 10))
        self.style.configure("TLabel", font=("微软雅黑", 10), background="#f0f0f0")
        self.style.configure("Header.TLabel", font=("微软雅黑", 16, "bold"), background="#f0f0f0")
        
        # 当前选择的文件
        self.current_file = None
        self.analysis_data = None
        
        # 创建日志解析器
        self.log_parser = LogParser()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        self.header = ttk.Label(self.main_frame, text="怀旧服惩戒骑士分析工具", style="Header.TLabel")
        self.header.pack(pady=10)
        
        # 创建选项卡控件
        self.tab_control = ttk.Notebook(self.main_frame)
        self.tab_control.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 创建本地文件选项卡
        self.local_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.local_tab, text="本地文件")
        
        # 创建WarcraftLogs选项卡
        self.warcraftlogs_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.warcraftlogs_tab, text="WarcraftLogs")
        
        # 设置本地文件选项卡内容
        self.setup_local_tab()
        
        # 设置WarcraftLogs选项卡内容
        self.setup_warcraftlogs_tab()
        
        # 创建选项卡
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 创建仪表盘选项卡
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="仪表盘")
        
        # 创建技能分析选项卡
        self.abilities_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.abilities_frame, text="技能分析")
        
        # 创建施法时间分析选项卡
        self.casting_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.casting_frame, text="施法时间分析")
        
        # 创建性能检查列表选项卡
        self.checklist_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.checklist_frame, text="性能检查列表")
        
        # 创建底部按钮框架
        self.bottom_frame = ttk.Frame(self.main_frame)
        self.bottom_frame.pack(fill=tk.X, pady=10)
        
        self.save_button = ttk.Button(self.bottom_frame, text="保存分析结果", command=self.save_analysis)
        self.save_button.pack(side=tk.RIGHT, padx=5)
        
        # 初始化各选项卡
        self.init_dashboard()
        self.init_abilities_analysis()
        self.init_casting_time_analysis()
        self.init_checklist()
    
    def setup_local_tab(self):
        """设置本地文件选项卡内容"""
        # 创建文件选择框架
        self.file_frame = ttk.Frame(self.local_tab)
        self.file_frame.pack(fill=tk.X, pady=10)
        
        self.file_label = ttk.Label(self.file_frame, text="选择战斗日志文件:")
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ttk.Entry(self.file_frame, textvariable=self.file_path_var, width=50)
        self.file_path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.browse_button = ttk.Button(self.file_frame, text="浏览...", command=self.browse_file)
        self.browse_button.pack(side=tk.LEFT, padx=5)
        
        self.analyze_button = ttk.Button(self.file_frame, text="分析", command=self.analyze_file)
        self.analyze_button.pack(side=tk.LEFT, padx=5)
        
        # 创建说明文本
        self.local_info = ttk.Label(self.local_tab, text="选择本地战斗日志文件进行分析。支持.txt和.json格式。")
        self.local_info.pack(pady=5)
    
    def setup_warcraftlogs_tab(self):
        """设置WarcraftLogs选项卡内容"""
        # 创建链接输入框架
        self.url_frame = ttk.Frame(self.warcraftlogs_tab)
        self.url_frame.pack(fill=tk.X, pady=10)
        
        self.url_label = ttk.Label(self.url_frame, text="WarcraftLogs链接:")
        self.url_label.pack(side=tk.LEFT, padx=5)
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(self.url_frame, textvariable=self.url_var, width=50)
        self.url_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.fetch_button = ttk.Button(self.url_frame, text="获取数据", command=self.fetch_warcraftlogs)
        self.fetch_button.pack(side=tk.LEFT, padx=5)
        
        # 创建战斗选择框架
        self.fight_frame = ttk.Frame(self.warcraftlogs_tab)
        self.fight_frame.pack(fill=tk.X, pady=10)
        
        self.fight_label = ttk.Label(self.fight_frame, text="选择战斗:")
        self.fight_label.pack(side=tk.LEFT, padx=5)
        
        self.fight_var = tk.StringVar()
        self.fight_combo = ttk.Combobox(self.fight_frame, textvariable=self.fight_var, state="readonly", width=40)
        self.fight_combo.pack(side=tk.LEFT, padx=5)
        
        self.player_label = ttk.Label(self.fight_frame, text="选择玩家:")
        self.player_label.pack(side=tk.LEFT, padx=5)
        
        self.player_var = tk.StringVar()
        self.player_combo = ttk.Combobox(self.fight_frame, textvariable=self.player_var, state="readonly", width=20)
        self.player_combo.pack(side=tk.LEFT, padx=5)
        
        self.analyze_wl_button = ttk.Button(self.fight_frame, text="分析", command=self.analyze_warcraftlogs)
        self.analyze_wl_button.pack(side=tk.LEFT, padx=5)
        
        # 创建日志显示区域
        self.log_frame = ttk.LabelFrame(self.warcraftlogs_tab, text="日志信息")
        self.log_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=5)
        
        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)
        self.log_text.config(state=tk.DISABLED)
        
        # 创建说明文本
        self.wl_info = ttk.Label(self.warcraftlogs_tab, text="输入WarcraftLogs链接，获取战斗数据进行分析。")
        self.wl_info.pack(pady=5)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="选择战斗日志文件",
            filetypes=[("文本文件", "*.txt"), ("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.current_file = file_path
    
    def analyze_file(self):
        if not self.current_file:
            messagebox.showwarning("警告", "请先选择一个文件")
            return
        
        try:
            # 使用日志解析器解析文件
            self.analysis_data = self.log_parser.parse_file(self.current_file)
            
            # 更新各选项卡的数据
            self.update_dashboard()
            self.update_abilities_analysis()
            self.update_casting_time_analysis()
            self.update_checklist()
            
            messagebox.showinfo("成功", "分析完成")
        except Exception as e:
            messagebox.showerror("错误", f"分析文件时出错: {str(e)}")
    
    def fetch_warcraftlogs(self):
        """获取WarcraftLogs数据"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("错误", "请输入WarcraftLogs链接")
            return
        
        # 验证URL格式
        # 支持国际服和国服链接格式
        valid_patterns = [
            r'https?://(www\.)?classic\.warcraftlogs\.com/reports/\w+',
            r'https?://(www\.)?cn\.classic\.warcraftlogs\.com/reports/\w+' 
        ]
        
        is_valid = False
        for pattern in valid_patterns:
            if re.match(pattern, url):
                is_valid = True
                break
                
        if not is_valid:
            messagebox.showerror("错误", "无效的WarcraftLogs链接格式。\n请使用格式: https://classic.warcraftlogs.com/reports/XXXX 或 https://cn.classic.warcraftlogs.com/reports/XXXX")
            return
            
        # 提取报告ID
        report_id = None
        if "cn.classic.warcraftlogs.com" in url:
            # 国服链接
            match = re.search(r'cn\.classic\.warcraftlogs\.com/reports/(\w+)', url)
            if match:
                report_id = match.group(1)
                self.log_message(f"检测到国服WarcraftLogs链接，报告ID: {report_id}")
        else:
            # 国际服链接
            match = re.search(r'classic\.warcraftlogs\.com/reports/(\w+)', url)
            if match:
                report_id = match.group(1)
                self.log_message(f"检测到国际服WarcraftLogs链接，报告ID: {report_id}")
        
        if not report_id:
            messagebox.showerror("错误", "无法从链接中提取报告ID")
            return
            
        self.log_message(f"正在获取报告 {report_id} 的数据...")
        self.log_message("注意: 当前版本使用模拟数据。要使用真实API数据，需要:")
        self.log_message("1. 拥有并关联Battle.net账号（必须条件）")
        self.log_message("2. 在WarcraftLogs开发者门户注册应用")
        self.log_message("3. 获取API密钥和客户端ID")
        self.log_message("4. 实现OAuth2认证流程")
        self.log_message("5. 使用API密钥发送请求到WarcraftLogs API")
        self.log_message("重要提示: 根据WarcraftLogs官方要求，您必须拥有关联的Battle.net账号才能创建密钥或使用API")
        
        # 模拟API请求延迟
        self.log_message("正在连接到WarcraftLogs API...")
        self.root.update()
        time.sleep(1)
        
        # 模拟获取战斗列表
        self.log_message("正在获取战斗列表...")
        self.root.update()
        time.sleep(1)
        
        # 清空现有选项
        self.fight_combo['values'] = []
        self.player_combo['values'] = []
        
        # 添加模拟战斗数据
        fights = [
            "1: 奥妮克希亚 (击杀) - 5:30",
            "2: 黑翼之巢 - 熔岩守卫 (击杀) - 3:45",
            "3: 黑翼之巢 - 勒什雷尔 (击杀) - 4:20",
            "4: 黑翼之巢 - 费尔默 (击杀) - 2:50",
            "5: 黑翼之巢 - 埃博诺克 (击杀) - 3:10",
            "6: 黑翼之巢 - 弗莱格尔 (击杀) - 4:00",
            "7: 黑翼之巢 - 克洛玛古斯 (击杀) - 6:15",
            "8: 黑翼之巢 - 奈法利安 (击杀) - 8:30"
        ]
        self.fight_combo['values'] = fights
        if fights:
            self.fight_combo.current(0)
            
        # 添加模拟玩家数据
        players = [
            "光明使者 (惩戒骑)",
            "暗影之刃 (战士)",
            "自然之力 (德鲁伊)",
            "火焰之心 (法师)",
            "神圣守护 (神圣骑)",
            "暗影愈合 (牧师)",
            "元素掌控 (萨满)",
            "死亡阴影 (术士)",
            "致命毒刃 (盗贼)",
            "野性守护 (猎人)"
        ]
        self.player_combo['values'] = players
        if players:
            # 自动选择惩戒骑士
            for i, player in enumerate(players):
                if "惩戒骑" in player:
                    self.player_combo.current(i)
                    break
            else:
                self.player_combo.current(0)
                
        self.log_message(f"成功获取报告数据！找到 {len(fights)} 场战斗和 {len(players)} 名玩家。")
        self.log_message("请选择要分析的战斗和玩家，然后点击'分析'按钮。")
        
        # 启用分析按钮
        self.analyze_wl_button.config(state=tk.NORMAL)
    
    def analyze_warcraftlogs(self):
        """分析WarcraftLogs数据"""
        if not hasattr(self, 'wl_fights') or not hasattr(self, 'wl_players'):
            messagebox.showwarning("警告", "请先获取WarcraftLogs数据")
            return
        
        # 获取选择的战斗和玩家
        fight_idx = self.fight_combo.current()
        player_idx = self.player_combo.current()
        
        if fight_idx < 0 or player_idx < 0:
            messagebox.showwarning("警告", "请选择战斗和玩家")
            return
        
        fight = self.wl_fights[fight_idx]
        player = self.wl_players[player_idx]
        
        self.log_message(f"正在分析 {player['name']} 在 {fight['name']} 中的表现...")
        
        try:
            # 这里应该是实际从WarcraftLogs API获取详细战斗数据的代码
            # 由于WarcraftLogs API需要认证，这里我们使用模拟数据
            
            # 使用模拟数据
            self.analysis_data = self.log_parser.get_mock_data()
            
            # 更新玩家和Boss名称
            self.analysis_data["player"] = player["name"]
            self.analysis_data["boss"] = fight["name"]
            
            # 更新各选项卡的数据
            self.update_dashboard()
            self.update_abilities_analysis()
            self.update_casting_time_analysis()
            self.update_checklist()
            
            self.log_message("分析完成")
            messagebox.showinfo("成功", "分析完成")
            
        except Exception as e:
            self.log_message(f"分析失败: {str(e)}")
            messagebox.showerror("错误", f"分析WarcraftLogs数据时出错: {str(e)}")
    
    def log_message(self, message):
        """在日志区域显示消息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def save_analysis(self):
        if not self.analysis_data:
            messagebox.showwarning("警告", "没有可保存的分析结果")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="保存分析结果",
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.analysis_data, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("成功", "分析结果已保存")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def init_dashboard(self):
        # 创建仪表盘内容
        self.dashboard_content = ttk.Frame(self.dashboard_frame)
        self.dashboard_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 战斗信息
        self.fight_info_frame = ttk.LabelFrame(self.dashboard_content, text="战斗信息")
        self.fight_info_frame.pack(fill=tk.X, pady=5)
        
        self.player_label = ttk.Label(self.fight_info_frame, text="玩家: ")
        self.player_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.player_value = ttk.Label(self.fight_info_frame, text="未知")
        self.player_value.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        self.boss_label = ttk.Label(self.fight_info_frame, text="Boss: ")
        self.boss_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.boss_value = ttk.Label(self.fight_info_frame, text="未知")
        self.boss_value.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        self.duration_label = ttk.Label(self.fight_info_frame, text="战斗时长: ")
        self.duration_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.duration_value = ttk.Label(self.fight_info_frame, text="未知")
        self.duration_value.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        # DPS信息
        self.dps_frame = ttk.LabelFrame(self.dashboard_content, text="DPS信息")
        self.dps_frame.pack(fill=tk.X, pady=5)
        
        self.dps_label = ttk.Label(self.dps_frame, text="DPS: ")
        self.dps_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.dps_value = ttk.Label(self.dps_frame, text="未知")
        self.dps_value.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        self.total_damage_label = ttk.Label(self.dps_frame, text="总伤害: ")
        self.total_damage_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.total_damage_value = ttk.Label(self.dps_frame, text="未知")
        self.total_damage_value.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        self.crit_rate_label = ttk.Label(self.dps_frame, text="暴击率: ")
        self.crit_rate_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.crit_rate_value = ttk.Label(self.dps_frame, text="未知")
        self.crit_rate_value.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
    
    def init_abilities_analysis(self):
        # 创建技能分析内容
        self.abilities_content = ttk.Frame(self.abilities_frame)
        self.abilities_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建技能列表
        self.abilities_tree = ttk.Treeview(self.abilities_content, columns=("casts", "damage", "dps", "crit_rate"))
        self.abilities_tree.heading("#0", text="技能")
        self.abilities_tree.heading("casts", text="施放次数")
        self.abilities_tree.heading("damage", text="总伤害")
        self.abilities_tree.heading("dps", text="DPS")
        self.abilities_tree.heading("crit_rate", text="暴击率")
        
        self.abilities_tree.column("#0", width=150)
        self.abilities_tree.column("casts", width=100)
        self.abilities_tree.column("damage", width=100)
        self.abilities_tree.column("dps", width=100)
        self.abilities_tree.column("crit_rate", width=100)
        
        self.abilities_tree.pack(fill=tk.BOTH, expand=True)
    
    def init_casting_time_analysis(self):
        # 创建施法时间分析内容
        self.casting_content = ttk.Frame(self.casting_frame)
        self.casting_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建施法时间信息
        self.casting_info_frame = ttk.LabelFrame(self.casting_content, text="施法时间信息")
        self.casting_info_frame.pack(fill=tk.X, pady=5)
        
        self.total_time_label = ttk.Label(self.casting_info_frame, text="总战斗时间: ")
        self.total_time_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.total_time_value = ttk.Label(self.casting_info_frame, text="未知")
        self.total_time_value.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        self.casting_time_label = ttk.Label(self.casting_info_frame, text="施法时间: ")
        self.casting_time_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.casting_time_value = ttk.Label(self.casting_info_frame, text="未知")
        self.casting_time_value.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        self.idle_time_label = ttk.Label(self.casting_info_frame, text="空闲时间: ")
        self.idle_time_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.idle_time_value = ttk.Label(self.casting_info_frame, text="未知")
        self.idle_time_value.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        self.efficiency_label = ttk.Label(self.casting_info_frame, text="施法效率: ")
        self.efficiency_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.efficiency_value = ttk.Label(self.casting_info_frame, text="未知")
        self.efficiency_value.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
    
    def init_checklist(self):
        # 创建性能检查列表内容
        self.checklist_content = ttk.Frame(self.checklist_frame)
        self.checklist_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建检查项列表
        self.checklist_tree = ttk.Treeview(self.checklist_content, columns=("status", "description"))
        self.checklist_tree.heading("#0", text="检查项")
        self.checklist_tree.heading("status", text="状态")
        self.checklist_tree.heading("description", text="描述")
        
        self.checklist_tree.column("#0", width=200)
        self.checklist_tree.column("status", width=100)
        self.checklist_tree.column("description", width=400)
        
        self.checklist_tree.pack(fill=tk.BOTH, expand=True)
    
    def update_dashboard(self):
        if not self.analysis_data:
            return
        
        # 更新战斗信息
        self.player_value.config(text=self.analysis_data["player"])
        self.boss_value.config(text=self.analysis_data["boss"])
        self.duration_value.config(text=f"{self.analysis_data['duration']}秒")
        
        # 更新DPS信息
        self.dps_value.config(text=f"{self.analysis_data['dps']:.2f}")
        self.total_damage_value.config(text=f"{self.analysis_data['totalDamage']}")
        self.crit_rate_value.config(text=f"{self.analysis_data['critRate'] * 100:.2f}%")
    
    def update_abilities_analysis(self):
        if not self.analysis_data:
            return
        
        # 清空现有数据
        for item in self.abilities_tree.get_children():
            self.abilities_tree.delete(item)
        
        # 添加技能数据
        for ability in self.analysis_data["abilities"]:
            self.abilities_tree.insert(
                "", "end", text=ability["name"],
                values=(
                    ability["casts"],
                    ability["damage"],
                    f"{ability['dps']:.2f}",
                    f"{ability['critRate'] * 100:.2f}%"
                )
            )
    
    def update_casting_time_analysis(self):
        if not self.analysis_data:
            return
        
        # 更新施法时间信息
        casting_data = self.analysis_data["castingTime"]
        self.total_time_value.config(text=f"{casting_data['totalTime']}秒")
        self.casting_time_value.config(text=f"{casting_data['castingTime']}秒")
        self.idle_time_value.config(text=f"{casting_data['idleTime']}秒")
        self.efficiency_value.config(text=f"{casting_data['efficiency'] * 100:.2f}%")
    
    def update_checklist(self):
        if not self.analysis_data:
            return
        
        # 清空现有数据
        for item in self.checklist_tree.get_children():
            self.checklist_tree.delete(item)
        
        # 添加检查项数据
        for item in self.analysis_data["checklist"]:
            status = "通过" if item["status"] else "需要改进"
            self.checklist_tree.insert(
                "", "end", text=item["name"],
                values=(status, item["description"])
            )

def main():
    root = tk.Tk()
    app = RetributionPaladinAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main() 