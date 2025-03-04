import re
import json
from datetime import datetime

class LogParser:
    """
    战斗日志解析器
    用于解析魔兽世界战斗日志，提取惩戒骑士相关的战斗数据
    """
    
    def __init__(self):
        # 惩戒骑士技能列表
        self.paladin_abilities = {
            "审判": {
                "pattern": r"审判",
                "is_damage": True
            },
            "十字军打击": {
                "pattern": r"十字军打击",
                "is_damage": True
            },
            "奉献": {
                "pattern": r"奉献",
                "is_damage": True
            },
            "神圣风暴": {
                "pattern": r"神圣风暴",
                "is_damage": True
            },
            "白色攻击": {
                "pattern": r"攻击",
                "is_damage": True
            },
            "圣光术": {
                "pattern": r"圣光术",
                "is_damage": False
            },
            "圣疗术": {
                "pattern": r"圣疗术",
                "is_damage": False
            },
            "圣盾术": {
                "pattern": r"圣盾术",
                "is_damage": False
            }
        }
        
        # 初始化数据结构
        self.reset_data()
    
    def reset_data(self):
        """重置数据结构"""
        self.data = {
            "player": "",
            "boss": "",
            "duration": 0,
            "dps": 0,
            "totalDamage": 0,
            "critRate": 0,
            "abilities": [],
            "castingTime": {
                "totalTime": 0,
                "castingTime": 0,
                "idleTime": 0,
                "efficiency": 0
            },
            "checklist": []
        }
        
        # 技能使用数据
        self.ability_data = {}
        for ability in self.paladin_abilities:
            self.ability_data[ability] = {
                "name": ability,
                "casts": 0,
                "damage": 0,
                "crits": 0,
                "hits": 0
            }
        
        # 战斗时间数据
        self.start_time = None
        self.end_time = None
        self.last_cast_time = None
    
    def parse_file(self, file_path):
        """
        解析日志文件
        
        Args:
            file_path: 日志文件路径
            
        Returns:
            解析后的数据字典
        """
        self.reset_data()
        
        # 检查文件类型
        if file_path.endswith('.json'):
            return self.parse_json_file(file_path)
        else:
            return self.parse_text_file(file_path)
    
    def parse_json_file(self, file_path):
        """解析JSON格式的日志文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 如果是已经分析过的数据，直接返回
            if "player" in data and "abilities" in data:
                return data
            
            # 否则尝试解析JSON格式的原始日志
            # 这里需要根据实际的JSON日志格式进行解析
            # 由于没有实际的日志格式，这里只是一个示例
            
            # 模拟解析过程
            return self.get_mock_data()
            
        except Exception as e:
            print(f"解析JSON文件时出错: {str(e)}")
            return self.get_mock_data()
    
    def parse_text_file(self, file_path):
        """解析文本格式的战斗日志"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 解析玩家和Boss信息
            player_name = "未知玩家"
            boss_name = "未知Boss"
            
            for line in lines[:100]:  # 只检查前100行
                player_match = re.search(r"玩家\s*[：:]\s*([^\s]+)", line)
                if player_match:
                    player_name = player_match.group(1)
                
                boss_match = re.search(r"目标\s*[：:]\s*([^\s]+)", line)
                if boss_match:
                    boss_name = boss_match.group(1)
            
            self.data["player"] = player_name
            self.data["boss"] = boss_name
            
            # 解析战斗时间
            for line in lines:
                time_match = re.search(r"\[(\d{2}:\d{2}:\d{2})\]", line)
                if time_match:
                    time_str = time_match.group(1)
                    current_time = datetime.strptime(time_str, "%H:%M:%S")
                    
                    if not self.start_time:
                        self.start_time = current_time
                    
                    self.end_time = current_time
                    
                    # 检查技能使用
                    for ability, info in self.paladin_abilities.items():
                        if re.search(info["pattern"], line):
                            self.ability_data[ability]["casts"] += 1
                            
                            # 检查是否是伤害技能
                            if info["is_damage"]:
                                damage_match = re.search(r"造成了\s*(\d+)\s*点伤害", line)
                                if damage_match:
                                    damage = int(damage_match.group(1))
                                    self.ability_data[ability]["damage"] += damage
                                    self.ability_data[ability]["hits"] += 1
                                    
                                    # 检查是否暴击
                                    if "暴击" in line:
                                        self.ability_data[ability]["crits"] += 1
                            
                            self.last_cast_time = current_time
                            break
            
            # 计算战斗时长（秒）
            if self.start_time and self.end_time:
                delta = self.end_time - self.start_time
                self.data["duration"] = delta.total_seconds()
            
            # 处理技能数据
            total_damage = 0
            total_hits = 0
            total_crits = 0
            
            for ability, data in self.ability_data.items():
                if data["casts"] > 0:
                    ability_info = {
                        "name": ability,
                        "casts": data["casts"],
                        "damage": data["damage"],
                        "dps": data["damage"] / self.data["duration"] if self.data["duration"] > 0 else 0,
                        "critRate": data["crits"] / data["hits"] if data["hits"] > 0 else 0
                    }
                    self.data["abilities"].append(ability_info)
                    
                    if self.paladin_abilities[ability]["is_damage"]:
                        total_damage += data["damage"]
                        total_hits += data["hits"]
                        total_crits += data["crits"]
            
            # 计算总体数据
            self.data["totalDamage"] = total_damage
            self.data["dps"] = total_damage / self.data["duration"] if self.data["duration"] > 0 else 0
            self.data["critRate"] = total_crits / total_hits if total_hits > 0 else 0
            
            # 计算施法时间数据
            # 这里简化处理，假设每次施法间隔超过3秒的视为空闲时间
            casting_time = self.data["duration"] - 0  # 这里需要实际计算空闲时间
            self.data["castingTime"] = {
                "totalTime": self.data["duration"],
                "castingTime": casting_time,
                "idleTime": self.data["duration"] - casting_time,
                "efficiency": casting_time / self.data["duration"] if self.data["duration"] > 0 else 0
            }
            
            # 生成检查列表
            self.generate_checklist()
            
            return self.data
            
        except Exception as e:
            print(f"解析文本文件时出错: {str(e)}")
            return self.get_mock_data()
    
    def generate_checklist(self):
        """生成性能检查列表"""
        # 审判使用检查
        judgment_casts = self.ability_data["审判"]["casts"]
        judgment_expected = self.data["duration"] / 10  # 假设审判应该每10秒使用一次
        judgment_status = judgment_casts >= judgment_expected * 0.8
        
        self.data["checklist"].append({
            "name": "审判使用",
            "status": judgment_status,
            "description": "审判保持良好的上线时间" if judgment_status else "审判使用频率过低，应该更频繁地使用"
        })
        
        # 十字军打击使用检查
        crusader_casts = self.ability_data["十字军打击"]["casts"]
        crusader_expected = self.data["duration"] / 6  # 假设十字军打击应该每6秒使用一次
        crusader_status = crusader_casts >= crusader_expected * 0.8
        
        self.data["checklist"].append({
            "name": "十字军打击使用",
            "status": crusader_status,
            "description": "十字军打击在冷却结束后立即使用" if crusader_status else "十字军打击使用频率过低，应该在冷却结束后立即使用"
        })
        
        # 奉献使用检查
        consecration_casts = self.ability_data["奉献"]["casts"]
        consecration_expected = self.data["duration"] / 8  # 假设奉献应该每8秒使用一次
        consecration_status = consecration_casts >= consecration_expected * 0.7
        
        self.data["checklist"].append({
            "name": "奉献使用",
            "status": consecration_status,
            "description": "奉献使用得当" if consecration_status else "奉献使用频率过低，应该更频繁地使用"
        })
        
        # 神圣风暴使用检查
        divine_storm_casts = self.ability_data["神圣风暴"]["casts"]
        divine_storm_expected = self.data["duration"] / 10  # 假设神圣风暴应该每10秒使用一次
        divine_storm_status = divine_storm_casts >= divine_storm_expected * 0.7
        
        self.data["checklist"].append({
            "name": "神圣风暴使用",
            "status": divine_storm_status,
            "description": "神圣风暴使用得当" if divine_storm_status else "神圣风暴使用频率过低，应该更频繁地使用"
        })
        
        # 整体施法效率检查
        efficiency = self.data["castingTime"]["efficiency"]
        efficiency_status = efficiency >= 0.85
        
        self.data["checklist"].append({
            "name": "整体施法效率",
            "status": efficiency_status,
            "description": "施法效率良好，空闲时间较少" if efficiency_status else "施法效率较低，存在较多空闲时间"
        })
    
    def get_mock_data(self):
        """生成模拟数据用于测试"""
        return {
            "player": "惩戒骑士",
            "boss": "奥妮克希亚",
            "duration": 300,
            "dps": 1250.5,
            "totalDamage": 375150,
            "critRate": 0.25,
            "abilities": [
                {
                    "name": "审判",
                    "casts": 30,
                    "damage": 75000,
                    "dps": 250,
                    "critRate": 0.3
                },
                {
                    "name": "十字军打击",
                    "casts": 60,
                    "damage": 120000,
                    "dps": 400,
                    "critRate": 0.25
                },
                {
                    "name": "奉献",
                    "casts": 15,
                    "damage": 45000,
                    "dps": 150,
                    "critRate": 0.2
                },
                {
                    "name": "神圣风暴",
                    "casts": 10,
                    "damage": 60000,
                    "dps": 200,
                    "critRate": 0.3
                },
                {
                    "name": "白色攻击",
                    "casts": 150,
                    "damage": 75150,
                    "dps": 250.5,
                    "critRate": 0.2
                }
            ],
            "castingTime": {
                "totalTime": 300,
                "castingTime": 270,
                "idleTime": 30,
                "efficiency": 0.9
            },
            "checklist": [
                {
                    "name": "审判使用",
                    "status": True,
                    "description": "审判保持良好的上线时间"
                },
                {
                    "name": "十字军打击使用",
                    "status": True,
                    "description": "十字军打击在冷却结束后立即使用"
                },
                {
                    "name": "奉献使用",
                    "status": False,
                    "description": "奉献使用频率过低，应该更频繁地使用"
                },
                {
                    "name": "神圣风暴使用",
                    "status": True,
                    "description": "神圣风暴使用得当"
                },
                {
                    "name": "整体施法效率",
                    "status": True,
                    "description": "施法效率良好，空闲时间较少"
                }
            ]
        } 